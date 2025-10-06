"""
RAG Engine - Core retrieval-augmented generation logic
"""
import logging
from typing import List, Dict, Optional
import os

from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

import config
from vector_store import VectorStoreManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGEngine:
    """Main RAG engine for question answering"""
    
    def __init__(self, vector_store_manager: VectorStoreManager):
        """
        Initialize the RAG engine
        
        Args:
            vector_store_manager: Initialized VectorStoreManager instance
        """
        self.vector_store_manager = vector_store_manager
        self.llm = None
        self.qa_chain = None
        
        # Check if OpenAI API key is available
        self.use_openai = bool(config.OPENAI_API_KEY)
        
        if self.use_openai:
            self._initialize_openai_llm()
        else:
            logger.warning("No OpenAI API key found. Using fallback mode.")
    
    def _initialize_openai_llm(self):
        """Initialize OpenAI LLM"""
        try:
            self.llm = ChatOpenAI(
                model_name=config.LLM_MODEL,
                temperature=config.LLM_TEMPERATURE,
                max_tokens=config.MAX_TOKENS,
                openai_api_key=config.OPENAI_API_KEY
            )
            logger.info(f"OpenAI LLM initialized: {config.LLM_MODEL}")
        except Exception as e:
            logger.error(f"Error initializing OpenAI LLM: {str(e)}")
            self.llm = None
    
    def setup_qa_chain(self):
        """Setup the QA chain with retriever"""
        if self.vector_store_manager.vectorstore is None:
            logger.error("Vector store not loaded")
            return False
        
        # Create retriever
        retriever = self.vector_store_manager.vectorstore.as_retriever(
            search_kwargs={"k": config.TOP_K_RESULTS}
        )
        
        # Create prompt template
        prompt = PromptTemplate(
            template=config.RAG_PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )
        
        if self.llm:
            # Create QA chain with LLM
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": prompt}
            )
            logger.info("QA chain setup complete with LLM")
        else:
            # Setup for retrieval-only mode
            logger.info("QA chain setup in retrieval-only mode")
        
        return True
    
    def query(self, question: str) -> Dict:
        """
        Process a question and return an answer with sources
        
        Args:
            question: User's question
            
        Returns:
            Dictionary containing answer and source documents
        """
        if not question or not question.strip():
            return {
                "answer": "Please provide a valid question.",
                "source_documents": [],
                "error": "Empty question"
            }
        
        try:
            # Retrieve relevant documents
            relevant_docs = self.vector_store_manager.similarity_search_with_score(
                question, 
                k=config.TOP_K_RESULTS
            )
            
            if not relevant_docs:
                return {
                    "answer": "I couldn't find any relevant information in the knowledge base for your question.",
                    "source_documents": [],
                    "error": "No relevant documents found"
                }
            
            # Extract documents and scores
            documents = [doc for doc, score in relevant_docs]
            scores = [score for doc, score in relevant_docs]
            
            # Generate answer
            if self.qa_chain and self.llm:
                # Use LLM to generate answer
                response = self.qa_chain.invoke({"query": question})
                answer = response["result"]
                source_docs = response.get("source_documents", documents)
            else:
                # Fallback: Return context without LLM generation
                answer = self._generate_fallback_answer(question, documents)
                source_docs = documents
            
            return {
                "answer": answer,
                "source_documents": source_docs,
                "relevance_scores": scores,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "answer": f"An error occurred while processing your question: {str(e)}",
                "source_documents": [],
                "error": str(e)
            }
    
    def _generate_fallback_answer(self, question: str, documents: List[Document]) -> str:
        """
        Generate a simple answer when LLM is not available
        
        Args:
            question: User's question
            documents: Retrieved relevant documents
            
        Returns:
            Formatted answer with context
        """
        answer = "Based on the knowledge base, here are the most relevant excerpts:\n\n"
        
        for i, doc in enumerate(documents, 1):
            content = doc.page_content[:300]  # Limit length
            answer += f"**Excerpt {i}:**\n{content}...\n\n"
        
        answer += "\n*Note: Set up an OpenAI API key in the .env file to get AI-generated answers.*"
        return answer
    
    def get_chat_response(self, question: str, chat_history: Optional[List] = None) -> Dict:
        """
        Get a response with conversation context
        
        Args:
            question: Current question
            chat_history: Previous conversation history
            
        Returns:
            Response dictionary
        """
        # For now, we'll use the basic query method
        # Can be extended to include chat history in the future
        return self.query(question)


class RAGManager:
    """High-level manager for the entire RAG system"""
    
    def __init__(self):
        """Initialize the RAG manager"""
        self.vector_store_manager = VectorStoreManager()
        self.rag_engine = None
        self.is_initialized = False
    
    def initialize(self, force_rebuild: bool = False) -> bool:
        """
        Initialize the RAG system
        
        Args:
            force_rebuild: If True, rebuild the vector store from scratch
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load or create vector store
            if force_rebuild:
                logger.info("Force rebuild requested. Creating new vector store...")
                from document_processor import DocumentProcessor
                processor = DocumentProcessor()
                chunks = processor.process_documents()
                
                if not chunks:
                    logger.error("No documents to process")
                    return False
                
                # Delete old collection if exists
                try:
                    self.vector_store_manager.delete_collection()
                except:
                    pass
                
                self.vector_store_manager.create_vectorstore(chunks)
            else:
                # Try to load existing vector store
                vectorstore = self.vector_store_manager.load_vectorstore()
                
                if vectorstore is None:
                    logger.info("No existing vector store found. Creating new one...")
                    from document_processor import DocumentProcessor
                    processor = DocumentProcessor()
                    chunks = processor.process_documents()
                    
                    if not chunks:
                        logger.error("No documents to process")
                        return False
                    
                    self.vector_store_manager.create_vectorstore(chunks)
            
            # Initialize RAG engine
            self.rag_engine = RAGEngine(self.vector_store_manager)
            self.rag_engine.setup_qa_chain()
            
            self.is_initialized = True
            logger.info("RAG system initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing RAG system: {str(e)}")
            return False
    
    def query(self, question: str) -> Dict:
        """
        Query the RAG system
        
        Args:
            question: User's question
            
        Returns:
            Response dictionary
        """
        if not self.is_initialized or self.rag_engine is None:
            return {
                "answer": "RAG system is not initialized. Please initialize first.",
                "source_documents": [],
                "error": "Not initialized"
            }
        
        return self.rag_engine.query(question)


if __name__ == "__main__":
    # Test the RAG system
    manager = RAGManager()
    
    if manager.initialize():
        response = manager.query("What is this knowledge base about?")
        print(f"Answer: {response['answer']}")
        print(f"Number of sources: {len(response['source_documents'])}")


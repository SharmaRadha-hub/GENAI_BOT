"""
Vector database management using ChromaDB
"""
import logging
from typing import List, Optional
from pathlib import Path

from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Manages vector database operations for RAG"""
    
    def __init__(self, 
                 embedding_model_name: str = config.EMBEDDING_MODEL_NAME,
                 persist_directory: Path = config.VECTOR_DB_DIR,
                 collection_name: str = config.COLLECTION_NAME):
        """
        Initialize the vector store manager
        
        Args:
            embedding_model_name: Name of the sentence transformer model
            persist_directory: Directory to persist the vector database
            collection_name: Name of the collection in ChromaDB
        """
        self.embedding_model_name = embedding_model_name
        self.persist_directory = str(persist_directory)
        self.collection_name = collection_name
        
        logger.info(f"Initializing embedding model: {embedding_model_name}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        self.vectorstore: Optional[Chroma] = None
        
    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """
        Create a new vector store from documents
        
        Args:
            documents: List of Document objects to embed and store
            
        Returns:
            Chroma vector store instance
        """
        if not documents:
            raise ValueError("Cannot create vector store with empty documents list")
        
        logger.info(f"Creating vector store with {len(documents)} documents...")
        
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        
        logger.info("Vector store created successfully")
        return self.vectorstore
    
    def load_vectorstore(self) -> Optional[Chroma]:
        """
        Load an existing vector store from disk
        
        Returns:
            Chroma vector store instance or None if not found
        """
        try:
            logger.info("Loading existing vector store...")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
            
            # Check if the collection has any data
            collection = self.vectorstore._collection
            if collection.count() == 0:
                logger.warning("Vector store is empty")
                return None
            
            logger.info(f"Vector store loaded successfully with {collection.count()} documents")
            return self.vectorstore
            
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            return None
    
    def add_documents(self, documents: List[Document]):
        """
        Add new documents to an existing vector store
        
        Args:
            documents: List of Document objects to add
        """
        if self.vectorstore is None:
            logger.warning("No vector store loaded. Creating new one...")
            self.create_vectorstore(documents)
            return
        
        logger.info(f"Adding {len(documents)} documents to vector store...")
        self.vectorstore.add_documents(documents)
        logger.info("Documents added successfully")
    
    def similarity_search(self, query: str, k: int = config.TOP_K_RESULTS) -> List[Document]:
        """
        Search for similar documents based on a query
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of most similar Document objects
        """
        if self.vectorstore is None:
            logger.error("No vector store loaded")
            return []
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents for query")
            return results
        except Exception as e:
            logger.error(f"Error during similarity search: {str(e)}")
            return []
    
    def similarity_search_with_score(self, query: str, k: int = config.TOP_K_RESULTS):
        """
        Search for similar documents with relevance scores
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of tuples (Document, score)
        """
        if self.vectorstore is None:
            logger.error("No vector store loaded")
            return []
        
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            logger.error(f"Error during similarity search: {str(e)}")
            return []
    
    def delete_collection(self):
        """Delete the entire collection"""
        if self.vectorstore is not None:
            self.vectorstore.delete_collection()
            self.vectorstore = None
            logger.info("Vector store collection deleted")
    
    def get_collection_count(self) -> int:
        """
        Get the number of documents in the vector store
        
        Returns:
            Number of documents
        """
        if self.vectorstore is None:
            return 0
        try:
            return self.vectorstore._collection.count()
        except:
            return 0


if __name__ == "__main__":
    # Test the vector store manager
    manager = VectorStoreManager()
    vectorstore = manager.load_vectorstore()
    
    if vectorstore:
        count = manager.get_collection_count()
        print(f"Vector store contains {count} documents")
        
        # Test search
        results = manager.similarity_search("test query", k=3)
        print(f"Search returned {len(results)} results")


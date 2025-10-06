"""
Configuration file for RAG Chatbot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Paths
PROJECT_ROOT = Path(__file__).parent
DOCUMENTS_DIR = PROJECT_ROOT / "documents"
VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

# Create directories if they don't exist
DOCUMENTS_DIR.mkdir(exist_ok=True)
VECTOR_DB_DIR.mkdir(exist_ok=True)

# Document Processing Settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
SUPPORTED_EXTENSIONS = ['.pdf', '.txt', '.md', '.docx']

# Embedding Model Settings
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # Fast and efficient
# Alternative: "all-mpnet-base-v2" for better quality

# Vector Database Settings
COLLECTION_NAME = "rag_knowledge_base"
TOP_K_RESULTS = 3  # Number of relevant chunks to retrieve

# LLM Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = "gpt-3.5-turbo"  # or "gpt-4" for better quality
LLM_TEMPERATURE = 0.7
MAX_TOKENS = 1000

# Streamlit UI Settings
PAGE_TITLE = "RAG Knowledge Base Chatbot"
PAGE_ICON = "🤖"
LAYOUT = "wide"

# RAG Prompt Template
RAG_PROMPT_TEMPLATE = """You are an intelligent assistant helping to answer questions based on a knowledge base.

Context from knowledge base:
{context}

Question: {question}

Please provide a detailed and accurate answer based on the context provided above. If the context doesn't contain enough information to answer the question fully, acknowledge what you can answer and what information might be missing.

Answer:"""

# System Message
SYSTEM_MESSAGE = """You are a helpful AI assistant that answers questions based on a custom knowledge base. 
Always base your answers primarily on the provided context, and be honest when information is not available in the knowledge base."""


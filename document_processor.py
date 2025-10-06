"""
Document processing module for loading and chunking documents
"""
import os
from pathlib import Path
from typing import List, Dict
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)
from langchain.schema import Document

import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Handles document loading, processing, and chunking"""
    
    def __init__(self, chunk_size: int = config.CHUNK_SIZE, 
                 chunk_overlap: int = config.CHUNK_OVERLAP):
        """
        Initialize the document processor
        
        Args:
            chunk_size: Size of each text chunk
            chunk_overlap: Overlap between chunks for context preservation
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
    def load_document(self, file_path: Path) -> List[Document]:
        """
        Load a document based on its file extension
        
        Args:
            file_path: Path to the document
            
        Returns:
            List of Document objects
        """
        extension = file_path.suffix.lower()
        
        try:
            if extension == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif extension == '.txt':
                loader = TextLoader(str(file_path), encoding='utf-8')
            elif extension == '.md':
                # Load markdown files as text
                loader = TextLoader(str(file_path), encoding='utf-8')
            elif extension == '.docx':
                loader = Docx2txtLoader(str(file_path))
            else:
                logger.warning(f"Unsupported file type: {extension}")
                return []
            
            documents = loader.load()
            logger.info(f"Successfully loaded: {file_path.name}")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading {file_path.name}: {str(e)}")
            return []
    
    def load_documents_from_directory(self, directory: Path) -> List[Document]:
        """
        Load all supported documents from a directory
        
        Args:
            directory: Path to the directory containing documents
            
        Returns:
            List of all loaded Document objects
        """
        all_documents = []
        
        if not directory.exists():
            logger.warning(f"Directory does not exist: {directory}")
            return all_documents
        
        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in config.SUPPORTED_EXTENSIONS:
                docs = self.load_document(file_path)
                all_documents.extend(docs)
        
        logger.info(f"Loaded {len(all_documents)} document(s) from {directory}")
        return all_documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks
        
        Args:
            documents: List of Document objects to chunk
            
        Returns:
            List of chunked Document objects
        """
        if not documents:
            logger.warning("No documents to chunk")
            return []
        
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks from {len(documents)} document(s)")
        return chunks
    
    def process_documents(self, directory: Path = None) -> List[Document]:
        """
        Complete pipeline: load and chunk documents
        
        Args:
            directory: Directory containing documents (defaults to config.DOCUMENTS_DIR)
            
        Returns:
            List of chunked Document objects ready for embedding
        """
        if directory is None:
            directory = config.DOCUMENTS_DIR
        
        logger.info("Starting document processing pipeline...")
        documents = self.load_documents_from_directory(directory)
        
        if not documents:
            logger.warning("No documents loaded. Please add documents to the documents/ folder.")
            return []
        
        chunks = self.chunk_documents(documents)
        return chunks
    
    def get_document_stats(self, directory: Path = None) -> Dict:
        """
        Get statistics about documents in the directory
        
        Args:
            directory: Directory to analyze
            
        Returns:
            Dictionary with document statistics
        """
        if directory is None:
            directory = config.DOCUMENTS_DIR
        
        stats = {
            'total_files': 0,
            'by_type': {},
            'total_size_mb': 0
        }
        
        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in config.SUPPORTED_EXTENSIONS:
                stats['total_files'] += 1
                ext = file_path.suffix.lower()
                stats['by_type'][ext] = stats['by_type'].get(ext, 0) + 1
                stats['total_size_mb'] += file_path.stat().st_size / (1024 * 1024)
        
        return stats


if __name__ == "__main__":
    # Test the document processor
    processor = DocumentProcessor()
    stats = processor.get_document_stats()
    print(f"Document Statistics: {stats}")
    
    chunks = processor.process_documents()
    print(f"Processed {len(chunks)} chunks")


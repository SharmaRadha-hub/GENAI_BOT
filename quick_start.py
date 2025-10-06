"""
Quick Start Script for RAG Chatbot
Initializes the system and tests basic functionality
"""
import sys
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        'langchain',
        'chromadb',
        'sentence_transformers',
        'streamlit',
        'pypdf',
        'openai'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n❌ Missing packages detected!")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("✅ All requirements satisfied!\n")
    return True


def check_documents():
    """Check if documents directory has files"""
    print("📁 Checking documents...")
    
    import config
    doc_dir = config.DOCUMENTS_DIR
    
    if not doc_dir.exists():
        print(f"  ❌ Documents directory not found: {doc_dir}")
        return False
    
    files = list(doc_dir.glob("*"))
    doc_files = [f for f in files if f.suffix.lower() in config.SUPPORTED_EXTENSIONS]
    
    if not doc_files:
        print(f"  ⚠️  No documents found in {doc_dir}")
        print("     Sample documents are included. You can add your own!")
        return True
    
    print(f"  ✅ Found {len(doc_files)} document(s):")
    for f in doc_files[:5]:  # Show first 5
        print(f"     - {f.name}")
    if len(doc_files) > 5:
        print(f"     ... and {len(doc_files) - 5} more")
    
    print()
    return True


def test_document_processing():
    """Test document processing pipeline"""
    print("📄 Testing document processing...")
    
    try:
        from document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        stats = processor.get_document_stats()
        
        print(f"  ✅ Total files: {stats['total_files']}")
        print(f"  ✅ Total size: {stats['total_size_mb']:.2f} MB")
        print(f"  ✅ Document types: {stats['by_type']}")
        
        # Process documents
        chunks = processor.process_documents()
        print(f"  ✅ Generated {len(chunks)} text chunks\n")
        
        return True, chunks
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}\n")
        return False, []


def test_vector_store(chunks):
    """Test vector store creation"""
    print("🗄️  Testing vector store...")
    
    try:
        from vector_store import VectorStoreManager
        
        if not chunks:
            print("  ⚠️  No chunks to process, skipping vector store test\n")
            return True
        
        print("  📊 Creating embeddings (this may take a minute)...")
        manager = VectorStoreManager()
        
        # Delete existing if any
        try:
            manager.delete_collection()
        except:
            pass
        
        vectorstore = manager.create_vectorstore(chunks)
        count = manager.get_collection_count()
        
        print(f"  ✅ Vector store created with {count} embeddings")
        
        # Test search
        print("  🔍 Testing similarity search...")
        results = manager.similarity_search("What is RAG?", k=2)
        print(f"  ✅ Search returned {len(results)} results\n")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}\n")
        return False


def test_rag_engine():
    """Test RAG engine"""
    print("🤖 Testing RAG engine...")
    
    try:
        from rag_engine import RAGManager
        
        manager = RAGManager()
        
        if not manager.initialize():
            print("  ❌ Failed to initialize RAG manager\n")
            return False
        
        print("  ✅ RAG system initialized")
        
        # Test query
        print("  💬 Testing query...")
        response = manager.query("What is Retrieval-Augmented Generation?")
        
        if response['error']:
            print(f"  ⚠️  Query completed with warning: {response['error']}")
        else:
            print("  ✅ Query successful")
        
        print(f"  📝 Answer length: {len(response['answer'])} characters")
        print(f"  📚 Sources found: {len(response.get('source_documents', []))}")
        
        # Show a preview
        print("\n  Preview of answer:")
        preview = response['answer'][:200]
        print(f"  {preview}...\n")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}\n")
        return False


def check_api_key():
    """Check if OpenAI API key is configured"""
    print("🔑 Checking API configuration...")
    
    import config
    
    if config.OPENAI_API_KEY and config.OPENAI_API_KEY != "":
        print("  ✅ OpenAI API key configured")
        print("  💡 Will use GPT for answer generation\n")
        return True
    else:
        print("  ⚠️  No OpenAI API key found")
        print("  💡 System will work in retrieval-only mode")
        print("  💡 To enable AI generation:")
        print("     1. Copy env_template.txt to .env")
        print("     2. Add your OpenAI API key")
        print("     3. Restart the application\n")
        return False


def main():
    """Main quick start function"""
    print("=" * 60)
    print("🚀 RAG Chatbot - Quick Start Check")
    print("=" * 60)
    print()
    
    # Run all checks
    checks_passed = True
    
    if not check_requirements():
        checks_passed = False
        print("\n❌ Please install requirements first!")
        sys.exit(1)
    
    check_api_key()  # Warning only, not critical
    
    if not check_documents():
        checks_passed = False
    
    # Test components
    success, chunks = test_document_processing()
    if not success:
        checks_passed = False
    
    if chunks and success:
        if not test_vector_store(chunks):
            checks_passed = False
        
        if not test_rag_engine():
            checks_passed = False
    
    # Final summary
    print("=" * 60)
    if checks_passed:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("🎉 Your RAG chatbot is ready to use!")
        print()
        print("Next steps:")
        print("  1. Run: streamlit run app.py")
        print("  2. Open your browser to http://localhost:8501")
        print("  3. Click '🚀 Initialize' in the sidebar")
        print("  4. Start asking questions!")
        print()
        print("💡 Tips:")
        print("  - Add your own documents to the documents/ folder")
        print("  - Click '🔄 Rebuild DB' after adding new documents")
        print("  - Configure OpenAI API key for better answers")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print()
        print("Please resolve the issues above and try again.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()


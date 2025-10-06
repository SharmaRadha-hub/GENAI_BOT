"""
Streamlit UI for RAG Chatbot
"""
import streamlit as st
import logging
from pathlib import Path
from datetime import datetime

import config
from rag_engine import RAGManager
from document_processor import DocumentProcessor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #2c3e50;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 5px solid;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border-left-color: #2196F3;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%);
        border-left-color: #9C27B0;
    }
    
    .message-label {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #000000;
    }
    
    .message-content {
        line-height: 1.6;
        font-size: 1rem;
        color: #1a1a1a;
        font-weight: 500;
    }
    
    /* Source box styling */
    .source-box {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 0.8rem;
        border-left: 4px solid #FF9800;
        font-size: 0.95rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    
    .source-header {
        font-weight: 700;
        color: #b71c1c;
        margin-bottom: 0.5rem;
    }
    
    .source-content {
        color: #212121;
        line-height: 1.5;
        font-weight: 500;
    }
    
    /* Stats box styling */
    .stats-box {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border: 2px solid #4CAF50;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .stats-title {
        font-weight: 700;
        color: #1B5E20;
        font-size: 1.1rem;
        margin-bottom: 0.8rem;
    }
    
    .stats-item {
        padding: 0.3rem 0;
        color: #000000;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.7rem 1rem;
        font-weight: 700;
        font-size: 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6);
    }
    
    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, #E1F5FE 0%, #B3E5FC 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #03A9F4;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        color: #1a1a1a;
    }
    
    .info-box h3 {
        color: #000000;
    }
    
    .info-box p, .info-box li {
        color: #212121;
        font-weight: 500;
    }
    
    .info-box strong {
        color: #000000;
    }
    
    /* Welcome box */
    .welcome-box {
        background: linear-gradient(135deg, #FFF9C4 0%, #FFF59D 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #FBC02D;
        margin: 2rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .welcome-box h2 {
        color: #000000;
    }
    
    .welcome-box p {
        color: #1a1a1a;
        font-weight: 500;
    }
    
    .welcome-box strong {
        color: #000000;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #FFF3E0;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Chat input styling */
    .stChatInputContainer {
        border-top: 2px solid #E0E0E0;
        padding-top: 1rem;
        background: white;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #9C27B0, transparent);
    }
    
    /* Global text color overrides */
    .main .block-container {
        color: #1a1a1a;
    }
    
    /* Streamlit markdown text */
    .main p, .main li, .main span {
        color: #212121 !important;
        font-weight: 500;
    }
    
    /* Sidebar text */
    section[data-testid="stSidebar"] .stMarkdown {
        color: #1a1a1a;
    }
    
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] li {
        color: #212121 !important;
        font-weight: 500;
    }
    
    /* Success/Info/Warning text */
    .stSuccess, .stInfo, .stWarning {
        color: #000000 !important;
    }
    
    /* Caption text - make darker */
    .stCaption {
        color: #424242 !important;
        font-weight: 500 !important;
    }
    
    /* Code blocks */
    code {
        color: #000000 !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'rag_manager' not in st.session_state:
        st.session_state.rag_manager = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    if 'processing' not in st.session_state:
        st.session_state.processing = False


def initialize_rag_system(force_rebuild=False):
    """Initialize or reinitialize the RAG system"""
    with st.spinner('🔄 Initializing RAG system... This may take a moment.'):
        try:
            if st.session_state.rag_manager is None:
                st.session_state.rag_manager = RAGManager()
            
            success = st.session_state.rag_manager.initialize(force_rebuild=force_rebuild)
            
            if success:
                st.session_state.initialized = True
                st.success('✅ RAG system initialized successfully!')
                return True
            else:
                st.error('❌ Failed to initialize RAG system. Please check if documents are available.')
                return False
        except Exception as e:
            st.error(f'❌ Error initializing RAG system: {str(e)}')
            logger.error(f"Initialization error: {str(e)}")
            return False


def display_chat_history():
    """Display the chat history with enhanced styling"""
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(
                f'''<div class="chat-message user-message">
                    <div class="message-label">👤 You</div>
                    <div class="message-content">{message["content"]}</div>
                </div>''',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'''<div class="chat-message assistant-message">
                    <div class="message-label">🤖 AI Assistant</div>
                    <div class="message-content">{message["content"]}</div>
                </div>''',
                unsafe_allow_html=True
            )
            
            # Display sources if available
            if 'sources' in message and message['sources']:
                with st.expander("📚 View Source Documents", expanded=False):
                    for i, source in enumerate(message['sources'], 1):
                        content = source.page_content[:250] + "..." if len(source.page_content) > 250 else source.page_content
                        metadata = source.metadata
                        source_file = metadata.get("source", "Unknown")
                        if "\\" in source_file:
                            source_file = source_file.split("\\")[-1]
                        
                        st.markdown(
                            f'''<div class="source-box">
                                <div class="source-header">📄 Source {i}: {source_file}</div>
                                <div class="source-content">{content}</div>
                            </div>''',
                            unsafe_allow_html=True
                        )


def sidebar():
    """Render the sidebar with controls and information"""
    with st.sidebar:
        # Professional Header with Logo Effect
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 10px; margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
            <h2 style='color: white; margin: 0; font-size: 1.5rem; font-weight: 800;'>
                🎛️ Control Panel
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize/Rebuild buttons with enhanced styling
        st.markdown("<div style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 **Initialize**", use_container_width=True, help="Load documents and create vector database", type="primary"):
                initialize_rag_system(force_rebuild=False)
        
        with col2:
            if st.button("🔄 **Rebuild**", use_container_width=True, help="Rebuild database with new documents", type="secondary"):
                if st.session_state.initialized:
                    initialize_rag_system(force_rebuild=True)
                else:
                    st.warning("⚠️ Please initialize first!")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Document statistics with enhanced visibility
        st.markdown("""
        <div style='background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <h3 style='color: #1B5E20; margin: 0 0 0.8rem 0; font-size: 1.2rem; font-weight: 700;'>
                📊 Knowledge Base
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.initialized and st.session_state.rag_manager:
            try:
                doc_count = st.session_state.rag_manager.vector_store_manager.get_collection_count()
                
                # Get document stats
                processor = DocumentProcessor()
                stats = processor.get_document_stats()
                
                st.markdown(f"""
                <div class="stats-box" style='margin-top: -0.5rem;'>
                    <div class="stats-item" style='font-size: 1rem; padding: 0.5rem 0;'>
                        <strong style='color: #000; font-size: 1.05rem;'>📄 Documents:</strong> 
                        <span style='color: #1B5E20; font-weight: 600;'>{stats['total_files']}</span>
                    </div>
                    <div class="stats-item" style='font-size: 1rem; padding: 0.5rem 0;'>
                        <strong style='color: #000; font-size: 1.05rem;'>🧩 Chunks:</strong> 
                        <span style='color: #1B5E20; font-weight: 600;'>{doc_count}</span>
                    </div>
                    <div class="stats-item" style='font-size: 1rem; padding: 0.5rem 0;'>
                        <strong style='color: #000; font-size: 1.05rem;'>💾 Size:</strong> 
                        <span style='color: #1B5E20; font-weight: 600;'>{stats['total_size_mb']:.2f} MB</span>
                    </div>
                    <div class="stats-item" style='font-size: 1rem; padding: 0.5rem 0;'>
                        <strong style='color: #000; font-size: 1.05rem;'>📁 Types:</strong> 
                        <span style='color: #1B5E20; font-weight: 600;'>{', '.join([f"{k.upper()}({v})" for k, v in stats['by_type'].items()]) if stats['by_type'] else 'None'}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error("❌ Error loading stats")
        else:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #E1F5FE 0%, #B3E5FC 100%); 
                        padding: 1.2rem; border-radius: 10px; border-left: 5px solid #03A9F4; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                <p style='margin: 0; color: #000; font-weight: 600; font-size: 1rem;'>
                    <strong>ℹ️ Not Initialized</strong><br>
                    <span style='color: #1565C0;'>Click 🚀 Initialize to start</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Settings - HIDDEN/COMMENTED OUT
        # st.markdown("### ⚙️ Configuration")
        # 
        # # Check API key status
        # if config.OPENAI_API_KEY:
        #     st.success("✅ OpenAI Connected")
        #     st.caption(f"🤖 Model: {config.LLM_MODEL}")
        # else:
        #     st.info("💡 Using retrieval-only mode")
        #     st.caption("Add API key for AI answers")
        # 
        # st.caption(f"🧠 Embeddings: {config.EMBEDDING_MODEL_NAME.split('/')[-1]}")
        # st.caption(f"🔍 Retrieved chunks: {config.TOP_K_RESULTS}")
        # st.caption(f"📏 Chunk size: {config.CHUNK_SIZE} chars")
        
        st.markdown("---")
        
        # Action buttons with professional styling
        st.markdown("""
        <div style='background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%); 
                    padding: 0.5rem; border-radius: 8px; margin: 1rem 0;'>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🗑️ **Clear Chat History**", use_container_width=True, help="Clear conversation history", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()
        
        # Instructions with enhanced visibility
        st.markdown("---")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #FFF9C4 0%, #FFF59D 100%); 
                    padding: 1rem; border-radius: 10px; border: 2px solid #F9A825; 
                    box-shadow: 0 3px 10px rgba(0,0,0,0.1);'>
            <h3 style='color: #000; margin: 0 0 0.8rem 0; font-size: 1.2rem; font-weight: 700;'>
                📖 Quick Guide
            </h3>
            <div style='color: #000; font-size: 0.95rem; line-height: 1.8;'>
                <p style='margin: 0.5rem 0; font-weight: 600;'><strong>🚀 Getting Started:</strong></p>
                <p style='margin: 0.3rem 0; padding-left: 1rem;'>
                    <strong>1.</strong> 📁 Add documents to <code style='background: #FFE082; padding: 2px 6px; border-radius: 3px; color: #000;'>documents/</code> folder<br>
                    <strong>2.</strong> 🚀 Click <strong>Initialize</strong> button<br>
                    <strong>3.</strong> 💬 Ask questions about your docs<br>
                    <strong>4.</strong> 📚 View sources for references
                </p>
                <p style='margin: 0.8rem 0 0.3rem 0; font-weight: 600;'><strong>📄 Supported Files:</strong></p>
                <p style='margin: 0.3rem 0; padding-left: 1rem;'>
                    • <strong>PDF</strong> (.pdf) - Reports, papers<br>
                    • <strong>Text</strong> (.txt) - Notes, data<br>
                    • <strong>Markdown</strong> (.md) - Documentation<br>
                    • <strong>Word</strong> (.docx) - Documents
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 RAG Knowledge Base Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">✨ Ask intelligent questions about your custom knowledge base ✨</p>', unsafe_allow_html=True)
    
    # Sidebar
    sidebar()
    
    # Main chat interface
    st.markdown("---")
    
    # Display initialization status
    if not st.session_state.initialized:
        st.markdown("""
        <div class="welcome-box">
            <h2>👋 Welcome to Your RAG CHATBOT created by RADHA!</h2>
            <p style="font-size: 1.1rem; margin-top: 1rem;">
                Get started by clicking <strong>🚀 Initialize</strong> in the sidebar
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show document directory info
        doc_dir = config.DOCUMENTS_DIR
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h3 style="margin-top:0;">📁 Document Location</h3>
                <p><code>{}</code></p>
                <p><strong>Supported Formats:</strong></p>
                <ul style="margin-bottom:0;">
                    <li>📄 PDF files (.pdf)</li>
                    <li>📝 Text files (.txt)</li>
                    <li>📋 Markdown (.md)</li>
                    <li>📃 Word docs (.docx)</li>
                </ul>
            </div>
            """.format(str(doc_dir)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
                <h3 style="margin-top:0;">🚀 Quick Start</h3>
                <ol style="margin-bottom:0;">
                    <li><strong>Add Documents</strong><br>Place files in the documents folder</li>
                    <li><strong>Initialize System</strong><br>Click 🚀 button in sidebar</li>
                    <li><strong>Start Chatting</strong><br>Ask questions about your docs!</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        
        # Sample documents info
        from document_processor import DocumentProcessor
        processor = DocumentProcessor()
        stats = processor.get_document_stats()
        
        if stats['total_files'] > 0:
            st.success(f"✅ Found {stats['total_files']} document(s) ready to process!")
        else:
            st.warning("⚠️ No documents found. Add some documents first!")
            
    else:
        # Chat interface
        st.markdown("### 💬 Conversation")
        
        # Display chat history
        if not st.session_state.chat_history:
            st.markdown("""
            <div class="info-box">
                <p style="margin:0; font-size: 1.05rem;">
                    <strong>💡 Try asking:</strong><br>
                    • "What is Retrieval-Augmented Generation?"<br>
                    • "How do vector databases work?"<br>
                    • "What are the best practices for RAG?"
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        display_chat_history()
        
        # Chat input
        question = st.chat_input("💬 Type your question here...")
        
        if question:
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': question,
                'timestamp': datetime.now()
            })
            
            # Get response
            with st.spinner('🔍 Searching knowledge base and generating answer...'):
                response = st.session_state.rag_manager.query(question)
            
            # Add assistant response to history
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response['answer'],
                'sources': response.get('source_documents', []),
                'timestamp': datetime.now()
            })
            
            # Rerun to display the new messages
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <p style='color: #999; font-size: 0.95rem; margin: 0;'>
                ⚡ Powered by <strong>LangChain</strong> • <strong>ChromaDB</strong> • <strong>Sentence Transformers</strong>
            </p>
            <p style='color: #999; font-size: 0.9rem; margin-top: 0.5rem;'>
                Contact <strong>@radha/SharmaRadha-hub</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()


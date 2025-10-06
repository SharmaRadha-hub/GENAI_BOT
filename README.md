# 🤖 RAG Knowledge Base Chatbot

Retrieval-Augmented Generation (RAG) chatbot that enables intelligent question-answering over your custom knowledge base. This project addresses the key limitation of Large Language Models: not knowing about specific, private, or recent data.

## 🌟 Features

- **📚 Multi-Format Support**: Process PDF, TXT, Markdown, and DOCX files
- **🔍 Semantic Search**: Find relevant information using vector similarity
- **🧠 AI-Powered Answers**: Generate contextual responses using LLMs
- **💾 Persistent Storage**: ChromaDB for efficient vector storage
- **🎨 Beautiful UI**: Modern Streamlit interface with source attribution
- **⚡ Fast & Efficient**: Optimized embeddings with Sentence Transformers
- **🔒 Privacy-First**: Run completely locally with open-source models
- **📊 Analytics**: Track document statistics and query performance

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  Documents  │────────▶│   Chunking   │────────▶│  Embeddings │
│  (PDF/TXT)  │         │  (LangChain) │         │ (Sentence-T)│
└─────────────┘         └──────────────┘         └─────────────┘
                                                          │
                                                          ▼
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│    User     │────────▶│     RAG      │────────▶│   Vector    │
│   Query     │         │   Engine     │         │  Database   │
└─────────────┘         └──────────────┘         │  (ChromaDB) │
       │                        │                 └─────────────┘
       │                        ▼
       │                ┌──────────────┐
       └───────────────▶│     LLM      │
                        │  (GPT/Local) │
                        └──────────────┘
                                │
                                ▼
                        ┌──────────────┐
                        │   Response   │
                        │ + Sources    │
                        └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) OpenAI API key for best results

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd GENAI
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys (Optional but recommended):**
   
   Create a `.env` file in the project root:
   ```bash
   # Copy the template
   copy env_template.txt .env  # Windows
   cp env_template.txt .env    # macOS/Linux
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
   
   Get your API key from: https://platform.openai.com/api-keys

5. **Add your documents:**
   
   Place your knowledge base files in the `documents/` folder:
   ```
   documents/
   ├── company_handbook.pdf
   ├── product_guide.docx
   ├── faq.txt
   └── technical_docs.md
   ```

### Running the Application

1. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**
   
   The app will automatically open at `http://localhost:8501`

3. **Initialize the system:**
   
   Click the **🚀 Initialize** button in the sidebar

4. **Start asking questions!**
   
   Type your questions in the chat input and get AI-powered answers with source citations.

## 📖 Usage Guide

### Adding Documents

1. Place any PDF, TXT, MD, or DOCX files in the `documents/` folder
2. Click **🔄 Rebuild DB** in the sidebar
3. Wait for processing to complete
4. Start querying your new knowledge base!

### Understanding Results

Each answer includes:
- **AI-Generated Response**: Contextual answer based on your documents
- **Source Attribution**: View the exact document excerpts used
- **Relevance Scores**: See how relevant each source is

### Best Practices

- **Chunk Size**: Default 500 characters works well for most documents
- **Document Quality**: Clean, well-formatted documents yield better results
- **Query Formulation**: Ask specific, clear questions
- **Context**: The system retrieves top 3 most relevant chunks by default

## 🛠️ Configuration

Edit `config.py` to customize:

```python
# Document Processing
CHUNK_SIZE = 500          # Size of text chunks
CHUNK_OVERLAP = 50        # Overlap between chunks

# Embedding Model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # Fast and efficient

# Retrieval
TOP_K_RESULTS = 3         # Number of chunks to retrieve

# LLM Settings
LLM_MODEL = "gpt-3.5-turbo"  # or "gpt-4"
LLM_TEMPERATURE = 0.7     # Creativity level
MAX_TOKENS = 1000         # Response length limit
```

## 📦 Project Structure

```
GENAI/
├── app.py                      # Streamlit UI
├── config.py                   # Configuration settings
├── document_processor.py       # Document loading & chunking
├── vector_store.py            # Vector database management
├── rag_engine.py              # RAG query logic
├── requirements.txt           # Python dependencies
├── env_template.txt          # Environment variables template
├── README.md                  # This file
├── documents/                 # Your knowledge base files
│   ├── sample_document_1.txt
│   ├── sample_document_2.txt
│   └── sample_document_3.md
└── vector_db/                 # Persisted embeddings (auto-generated)
```

## 🔧 Advanced Usage

### Using Local LLMs

If you don't have an OpenAI API key, the system falls back to retrieval-only mode, showing you the most relevant document excerpts without AI generation.

To use local LLMs:
1. Install Ollama or LlamaCPP
2. Modify `rag_engine.py` to use local models
3. Update the LLM initialization code

### Customizing Embeddings

For better domain-specific results, use specialized embedding models:

```python
# In config.py
EMBEDDING_MODEL_NAME = "all-mpnet-base-v2"  # Higher quality
# or
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-mpnet-base-v2"  # Multilingual
```

### Adding More Document Types

To support additional formats:

1. Install the appropriate loader:
   ```bash
   pip install unstructured
   ```

2. Add to `document_processor.py`:
   ```python
   elif extension == '.html':
       loader = UnstructuredHTMLLoader(str(file_path))
   ```

## 🧪 Testing

### Test Document Processing
```bash
python document_processor.py
```

### Test Vector Store
```bash
python vector_store.py
```

### Test RAG Engine
```bash
python rag_engine.py
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: "No documents found"
- **Solution**: Ensure documents are in the `documents/` folder and have supported extensions

**Issue**: "OpenAI API error"
- **Solution**: Check your API key in `.env` file and verify billing is enabled

**Issue**: "ChromaDB error"
- **Solution**: Delete the `vector_db/` folder and reinitialize

**Issue**: "Out of memory"
- **Solution**: Reduce `CHUNK_SIZE` or process fewer documents at once

### Performance Tips

- Use SSD storage for faster vector database operations
- Increase `TOP_K_RESULTS` for more context (but slower)
- Use GPU acceleration for embedding generation (requires GPU-enabled installation)

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add support for more document formats
- [ ] Implement conversational memory
- [ ] Add multi-language support
- [ ] Create Docker container
- [ ] Add authentication system
- [ ] Implement response caching
- [ ] Add evaluation metrics

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Built with these amazing open-source projects:

- [LangChain](https://github.com/hwchase17/langchain) - LLM framework
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Sentence Transformers](https://www.sbert.net/) - Embeddings
- [Streamlit](https://streamlit.io/) - Web interface
- [OpenAI](https://openai.com/) - Language models

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review sample documents for query examples
3. Open an issue on GitHub
4. Review LangChain documentation

## 🔮 Future Roadmap

- **Multi-modal RAG**: Support images and diagrams
- **Hybrid Search**: Combine keyword and semantic search
- **Query Analytics**: Track popular questions and gaps
- **Auto-categorization**: Organize documents by topic
- **API Endpoint**: REST API for integration
- **Mobile Support**: Responsive design for mobile devices

---

**Built with ❤️ for the GenAI Community**

*Star this repo if you find it helpful!* ⭐


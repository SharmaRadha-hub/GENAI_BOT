# 🚀 RAG Chatbot - Complete Setup Guide

This guide will walk you through setting up your RAG (Retrieval-Augmented Generation) chatbot from scratch.

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Using the Chatbot](#using-the-chatbot)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)

---

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4 GB (8 GB recommended)
- **Storage**: 2 GB free space
- **Internet**: Required for downloading dependencies and LLM API calls

### Recommended Requirements
- **RAM**: 8 GB or more
- **Storage**: 5 GB free space (for larger document collections)
- **CPU**: Multi-core processor
- **GPU**: Optional, for faster embedding generation

---

## 📦 Installation Steps

### Step 1: Check Python Installation

Open a terminal/command prompt and verify Python is installed:

```bash
python --version
# Should show Python 3.8 or higher
```

If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: Use Homebrew: `brew install python3`
- **Linux**: `sudo apt install python3 python3-pip`

### Step 2: Navigate to Project Directory

```bash
cd "C:\Users\radhara\OneDrive - AMDOCS\Backup Folders\Desktop\GENAI"
```

### Step 3: Create Virtual Environment

Creating a virtual environment isolates project dependencies:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

Install all required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- LangChain (LLM framework)
- ChromaDB (vector database)
- Sentence Transformers (embeddings)
- Streamlit (web UI)
- OpenAI API client
- Document processing libraries

**Note**: Installation may take 5-10 minutes depending on your internet speed.

### Step 5: Verify Installation

Run the quick start check:

```bash
python quick_start.py
```

This will verify all components are properly installed.

---

## ⚙️ Configuration

### Setting Up API Keys (Optional but Recommended)

1. **Create .env file:**
   
   ```bash
   # Windows
   copy env_template.txt .env
   
   # macOS/Linux
   cp env_template.txt .env
   ```

2. **Get OpenAI API Key:**
   
   - Go to [OpenAI Platform](https://platform.openai.com/)
   - Sign up or log in
   - Navigate to [API Keys](https://platform.openai.com/api-keys)
   - Click "Create new secret key"
   - Copy the key (you won't see it again!)

3. **Edit .env file:**
   
   Open `.env` in a text editor and replace the placeholder:
   
   ```
   OPENAI_API_KEY=sk-your_actual_key_here
   ```

4. **Save the file**

**Important**: Keep your API key secret! Never commit it to version control.

### Without API Key

The system works without an OpenAI API key but provides:
- Document retrieval (shows relevant excerpts)
- No AI-generated answers
- Basic search functionality

### Configuring System Parameters

Edit `config.py` to customize:

```python
# Document chunking
CHUNK_SIZE = 500           # Increase for more context per chunk
CHUNK_OVERLAP = 50         # Overlap between chunks

# Retrieval
TOP_K_RESULTS = 3          # Number of chunks to retrieve (1-10)

# LLM settings
LLM_MODEL = "gpt-3.5-turbo"  # or "gpt-4" for better quality
LLM_TEMPERATURE = 0.7      # 0.0 = factual, 1.0 = creative
MAX_TOKENS = 1000          # Maximum response length
```

---

## 🏃 Running the Application

### Step 1: Add Your Documents

Place your knowledge base files in the `documents/` folder:

```
documents/
├── your_file_1.pdf
├── your_file_2.txt
├── your_file_3.md
└── your_file_4.docx
```

**Supported formats:**
- PDF (`.pdf`)
- Text (`.txt`)
- Markdown (`.md`)
- Word Documents (`.docx`)

**Sample documents** are already included for testing.

### Step 2: Start the Application

```bash
streamlit run app.py
```

The application will:
1. Start a local web server
2. Automatically open your default browser
3. Navigate to `http://localhost:8501`

If the browser doesn't open automatically, manually visit `http://localhost:8501`

### Step 3: Initialize the System

In the web interface:

1. Look at the left sidebar
2. Click the **🚀 Initialize** button
3. Wait for the system to:
   - Load documents
   - Create text chunks
   - Generate embeddings
   - Build vector database

**First-time initialization** may take 1-2 minutes depending on document size.

### Step 4: Start Chatting!

Once initialized:
1. Type your question in the chat input at the bottom
2. Press Enter or click Send
3. View the AI-generated answer
4. Expand "View Sources" to see document references

---

## 💬 Using the Chatbot

### Asking Good Questions

**Do:**
- ✅ "What are the key features of RAG systems?"
- ✅ "How do vector databases work?"
- ✅ "Explain the document chunking process"
- ✅ "What are best practices for embeddings?"

**Don't:**
- ❌ "hi" (too vague)
- ❌ "tell me everything" (too broad)
- ❌ Questions unrelated to your documents

### Understanding Responses

Each answer includes:

1. **AI-Generated Response**: Synthesized answer based on your documents
2. **Sources**: Exact document excerpts used
3. **Metadata**: File names and locations

### Sidebar Features

- **🚀 Initialize**: Initial system setup
- **🔄 Rebuild DB**: Refresh after adding documents
- **📊 Stats**: View document and chunk counts
- **🗑️ Clear Chat**: Start a new conversation
- **⚙️ Settings**: View current configuration

---

## 🔧 Troubleshooting

### Issue: "Failed to initialize RAG system"

**Causes:**
- No documents in `documents/` folder
- Corrupted vector database

**Solutions:**
1. Add documents to `documents/` folder
2. Click **🔄 Rebuild DB**
3. Delete `vector_db/` folder and re-initialize

### Issue: "OpenAI API Error"

**Causes:**
- Invalid or missing API key
- Insufficient API credits
- Rate limiting

**Solutions:**
1. Check `.env` file has correct API key
2. Verify API key at [OpenAI Platform](https://platform.openai.com/)
3. Check billing and usage limits
4. Wait a moment and retry

### Issue: "Module not found" errors

**Cause**: Dependencies not installed correctly

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: Application is slow

**Causes:**
- Large documents
- Many chunks
- Slow embedding generation

**Solutions:**
1. Reduce `CHUNK_SIZE` in `config.py`
2. Reduce `TOP_K_RESULTS`
3. Use faster embedding model:
   ```python
   EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
   ```
4. Process fewer documents

### Issue: Poor answer quality

**Solutions:**
1. Use GPT-4 instead of GPT-3.5:
   ```python
   LLM_MODEL = "gpt-4"
   ```
2. Increase `TOP_K_RESULTS` to provide more context
3. Improve document quality (better formatting, clearer text)
4. Adjust `CHUNK_SIZE` to capture more context

### Issue: "Out of memory" error

**Solutions:**
1. Close other applications
2. Process documents in smaller batches
3. Reduce `CHUNK_SIZE`
4. Upgrade system RAM

---

## 🔐 Advanced Configuration

### Using Different Embedding Models

In `config.py`:

```python
# Fast and lightweight
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Better quality, slower
EMBEDDING_MODEL_NAME = "all-mpnet-base-v2"

# Multilingual support
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-mpnet-base-v2"
```

### Customizing the RAG Prompt

In `config.py`, modify `RAG_PROMPT_TEMPLATE`:

```python
RAG_PROMPT_TEMPLATE = """You are an expert assistant.

Context: {context}

Question: {question}

Provide a detailed answer with examples and citations.

Answer:"""
```

### Adding Document Filters

Modify `document_processor.py` to filter by metadata, date, or content.

### Performance Tuning

**For Speed:**
- Reduce `CHUNK_SIZE` to 300-400
- Reduce `TOP_K_RESULTS` to 2
- Use `all-MiniLM-L6-v2` embeddings

**For Quality:**
- Increase `CHUNK_SIZE` to 700-1000
- Increase `TOP_K_RESULTS` to 5
- Use `all-mpnet-base-v2` embeddings
- Use GPT-4 instead of GPT-3.5

### Running on a Different Port

```bash
streamlit run app.py --server.port 8502
```

### Deploying to Production

For production deployment:
1. Use Docker for containerization
2. Set up proper authentication
3. Use a production vector database (Pinecone, Weaviate)
4. Implement rate limiting
5. Add monitoring and logging
6. Use HTTPS

---

## 📞 Getting Help

If you encounter issues:

1. **Check Logs**: Terminal output shows detailed error messages
2. **Run Quick Start**: `python quick_start.py`
3. **Review README**: `README.md` has additional information
4. **Check Configuration**: Verify `config.py` settings
5. **Reinstall Dependencies**: Delete `venv/` and reinstall

---

## ✅ Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with API key (optional)
- [ ] Documents added to `documents/` folder
- [ ] Quick start check passed (`python quick_start.py`)
- [ ] Application running (`streamlit run app.py`)
- [ ] System initialized in web interface
- [ ] First query tested successfully

---

## 🎓 Next Steps

Once setup is complete:

1. **Add Your Documents**: Replace sample documents with your own
2. **Customize Settings**: Tune `config.py` for your needs
3. **Test Thoroughly**: Try various question types
4. **Monitor Performance**: Track response times and quality
5. **Iterate**: Refine based on results

**Happy Chatting! 🎉**


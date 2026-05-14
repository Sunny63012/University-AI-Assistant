# 🎓 University AI Assistant
### Multi-Database AI Retrieval System using RAG + Vector Search

Python • Streamlit • ChromaDB • Groq API • LangChain • Sentence Transformers

University AI Assistant is an enterprise-style Generative AI application that allows users to query multiple university databases using natural language instead of traditional SQL.

The system combines semantic vector search, metadata filtering, AI routing, and Retrieval-Augmented Generation (RAG) into a single intelligent dashboard.

Built this project to explore how modern AI systems can retrieve structured database information simply by asking questions in plain English.

---

# 🚀 What It Does

### 🧠 Natural Language Database Querying
Ask questions like:

- "Who got placed in Microsoft?"
- "Find students interested in AI"
- "Who teaches machine learning?"
- "Find research papers related to NLP"
- "Which students have CGPA above 9?"

without writing SQL queries.

---

# 📂 Multi-Database AI Routing

Automatically selects the correct databases based on the query.

Supported databases:

- Students
- Faculty
- Courses
- Placements
- Research

---

# 🔍 Vector Search + Metadata Filtering

Uses ChromaDB vector embeddings for semantic retrieval and combines them with structured metadata filters such as:

- CGPA
- Branch
- Gender
- Skills
- Package
- Department

---

# 🤖 Retrieval-Augmented Generation (RAG)

Retrieved documents are passed into an LLM for intelligent reasoning and response generation.

Powered by:

- Groq API
- Llama3
- LangChain

---

# 💬 Conversational AI

Maintains chat history and supports contextual follow-up questions using conversational memory.

---

# 📊 Streamlit Dashboard

Modern browser-based interface with:

- ChatGPT-style chat UI
- Database metrics
- Sidebar filters
- Retrieved document viewer
- Multi-database search flow

---

# 🛠️ Tech Stack

### Frontend
- Streamlit

### Vector Database
- ChromaDB

### Embeddings
- Sentence Transformers
- BAAI/bge-small-en-v1.5

### LLM Framework
- LangChain

### LLM Provider
- Groq API
- Llama3-8b-8192

### Backend
- Python

### Data Sources
- Excel datasets

---

# ⚡ Features

- Multi-database semantic retrieval
- AI-powered database routing
- Natural language querying
- Metadata filtering
- Conversational memory
- Cross-database reasoning
- RAG pipeline
- Vector similarity search
- Streamlit deployment
- Real-time AI responses

---

# 📁 Project Structure

```bash
project/
│
├── App.py
├── requirements.txt
├── chroma_db4/
│
├── Data/
│   ├── Student.xlsx
│   ├── faculty.xlsx
│   ├── courses.xlsx
│   ├── placements.xlsx
│   └── research.xlsx
│
└── .streamlit/
    └── config.toml
```

---

# ⚙️ Setup

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/university-ai-assistant.git
```

Move into the project folder:

```bash
cd university-ai-assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Add Groq API Key

Create:

```bash
.streamlit/secrets.toml
```

Add:

```toml
GROQ_API_KEY="your_api_key"
```

Get your API key from:

https://console.groq.com

---

# ▶️ Running the Application

Start Streamlit:

```bash
streamlit run App.py
```

Open in browser:

```bash
http://localhost:8501
```

---

# 💡 Example Queries

```text
Who got placed in Microsoft?
```

```text
Find students interested in AI
```

```text
Who teaches deep learning?
```

```text
Find AI research papers
```

```text
Which students have highest CGPA?
```

```text
Find placements related to machine learning
```

---

# 🔥 Future Improvements

- Graph RAG integration
- Neo4j relationship mapping
- SQL + Vector hybrid search
- Role-based authentication
- Voice assistant
- PDF upload + RAG
- Multi-user chat system
- Real-time analytics dashboard
- LangGraph agent workflows

---

# ⚠️ Disclaimer

This project is built for educational and research purposes to demonstrate enterprise-style AI retrieval systems using vector databases, RAG pipelines, and natural language querying.

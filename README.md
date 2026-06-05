# 🎓 EduGenie AI

> Transform PDFs into Notes, Flashcards, MCQs, Question Banks, Mock Tests, Revision Sheets, and AI Powered Insights.

EduGenie AI is an intelligent learning assistant designed to help students convert study material into exam ready resources. By leveraging Large Language Models, Retrieval Augmented Generation (RAG), and vector search, EduGenie enables learners to interact with their documents and generate personalized study content instantly.

---

## ✨ Features

## 📄 Document Support

EduGenie AI is currently optimized for academic PDFs and study material ranging from **10–20 pages**, with support for larger documents depending on content complexity and system resources.

The platform uses:

- Recursive text chunking
- Voyage AI embeddings
- FAISS vector search
- Retrieval Augmented Generation (RAG)

This architecture is designed to scale to larger document collections through efficient chunk based retrieval and semantic search.

### 📚 Study Tools

Generate high quality learning material from uploaded PDFs:

* Structured Notes
* Flashcards
* Multiple Choice Questions (MCQs)
* Question Banks

---

### 📊 Content Analysis

Gain insights into your study material:

* Topic Extraction
* Topic Coverage Analysis
* Importance Ranking
* Learning Insights

---

### 📝 Exam Preparation

Prepare effectively with AI generated exam resources:

* Interactive Mock Tests
* Revision Sheets
* Difficulty Based Question Generation
* Exam Readiness Support

---

### 🤖 AI Chat Assistant

Interact directly with your uploaded documents:

* Ask questions about any topic
* Generate explanations
* Summarize content
* Clarify concepts
* Context aware responses using RAG

---

## 🏗️ Architecture

```text
PDF Upload
     │
     ▼
Document Processing
     │
     ▼
Chunk Generation
     │
     ▼
Embeddings Creation
     │
     ▼
Vector Database
     │
     ▼
Retrieval Layer
     │
     ▼
LLM Generation
     │
     ▼
Study Tools / Analysis / Chat
```

---

## ⚙️ Tech Stack

### Frontend

* Streamlit
* HTML
* CSS

### Backend

* Python

### AI & Machine Learning

* LangChain
* Groq LLM
* Voyage AI Embeddings

### Vector Database

* FAISS

### Document Processing

* PyPDF
* Recursive Text Chunking

### Environment Management

* Python Virtual Environment
* Dotenv

---

## 📂 Project Structure

```text
EduGenie/
│
├── src/
│   ├── frontend/
│   │   ├── ui/
│   │   ├── components/
│   │   └── dashboard/
│   │
│   ├── study_tools/
│   │   ├── notes_generator.py
│   │   ├── flashcard_generator.py
│   │   ├── mcq_generator.py
│   │   └── question_bank_generator.py
│   │
│   ├── analysis/
│   │   ├── topic_extractor.py
│   │   ├── topic_coverage.py
│   │   └── importance_ranking.py
│   │
│   ├── exam_prep/
│   │   ├── mock_test_generator.py
│   │   └── revision_sheet_generator.py
│   │
│   ├── chatbot/
│   │   └── rag_chatbot.py
│   │
│   ├── vector_store/
│   ├── prompts/
│   └── app.py
│
├── requirements.txt
├── .env
└── README.md
```

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/Naman21036/EduGenie

cd EduGenie
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Environment

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key

VOYAGE_API_KEY=your_api_key
```

### 6. Run Application

```bash
streamlit run src/app.py
```

---

## 💡 How It Works

### Step 1

Upload one or more PDF documents.

### Step 2

Documents are processed and split into chunks.

### Step 3

Embeddings are generated and stored inside a FAISS vector database.

### Step 4

The retrieval pipeline fetches relevant context for user queries.

### Step 5

The LLM generates intelligent responses, notes, flashcards, questions, and analysis based on retrieved content.

---

## 🎯 Use Cases

* Exam Preparation
* Revision Planning
* Competitive Exam Study
* University Coursework
* Quick Document Understanding
* Knowledge Extraction
* Interactive Learning

---

## 🔮 Future Improvements

* Multi Document Comparison
* PDF Export
* Large Scale Document Processing (100+ Page PDFs)
* Learning Analytics Dashboard
* Personalized Study Plans
* Voice Based Learning Assistant
* Memory Enabled AI Tutor
* Adaptive Difficulty Mock Tests
* Study Progress Tracking

---

## 📸 Screenshots

Add screenshots of:

* Dashboard
* Study Tools
* Analysis Page
* Exam Preparation Module
* AI Chat Assistant

---

## 👨‍💻 Author

**Naman Gupta**

Machine Learning Enthusiast | AI Developer | Quantitative Finance Aspirant

BIT Mesra

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub.

It helps others discover the project and motivates future development.

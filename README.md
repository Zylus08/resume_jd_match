🧠 Resume–JD Semantic Matcher API

A FastAPI-based service that performs bi-directional semantic matching between resumes and job descriptions (JDs) using transformer embeddings and FAISS vector similarity search.

This system allows:

Finding the best matching resumes for a given JD

Finding the best matching JDs for a given resume

Designed as a lightweight, production-aware MVP for hiring and talent-matching use cases.

🚀 Features

📄 Upload resumes and JDs (PDF / DOCX)

🔄 Bi-directional matching (Resume ↔ JD)

🧠 Semantic similarity using transformer embeddings

⚡ Fast similarity search with FAISS

🧹 Handles edge cases (empty docs, top-k overflow, duplicates)

📊 Clean ranked output with similarity scores

🏗️ Tech Stack

Backend: FastAPI

NLP: Sentence Transformers (all-MiniLM-L6-v2)

Vector Search: FAISS (cosine similarity)

Document Parsing: pdfplumber, python-docx

Language: Python

📁 Project Structure
resume-jd-matcher/
│
├── main.py          # FastAPI application
├── parser.py        # PDF/DOCX text extraction
├── embedder.py      # Transformer embeddings
├── matcher.py       # FAISS index & search logic
│
├── data/
│   ├── resumes/
│   └── jds/
│
├── requirements.txt
└── README.md

⚙️ Installation & Setup
1️⃣ Create environment & install dependencies
pip install -r requirements.txt

2️⃣ Run the server
uvicorn main:app --reload


Open Swagger UI:

http://127.0.0.1:8000/docs

🔌 API Endpoints
📤 Upload Resume
POST /upload/resume


Response

{
  "msg": "Resume uploaded",
  "resume_id": 0
}

📤 Upload Job Description
POST /upload/jd


Response

{
  "msg": "JD uploaded",
  "jd_id": 0
}

🔍 Match JDs for a Resume
POST /match/resume


Input

{
  "resume_id": 0,
  "top_k": 3
}

🔍 Match Resumes for a JD
POST /match/jd


Input

{
  "jd_id": 0,
  "top_k": 3
}


Output

[
  {
    "resume": "candidate_resume.pdf",
    "score": 0.55
  }
]

🧠 How It Works

Resumes and JDs are parsed into plain text

Text is converted into semantic embeddings using a transformer model

Embeddings are stored in FAISS vector indexes

Cosine similarity search retrieves the top matching documents

Results are filtered for validity, uniqueness, and relevance

⚠️ Edge Cases Handled

Empty or unreadable documents

top_k larger than index size

FAISS invalid neighbors (-∞ scores)

Duplicate results

🎯 Use Cases

Resume screening automation

Talent matching systems

HR tech platforms

Interview shortlisting tools

🏁 Notes

This project is intentionally kept lightweight and modular

Embeddings are stored in memory for simplicity

Can be extended with persistence, filters, or explainability

👤 Author

Saksham Mishra
AI/ML Engineer | Research-Oriented Builder

# Legal AI Chatbot

This project is a **Legal Assistant Chatbot** built using **FastAPI, Gradio, and FAISS**. It integrates **Retrieval-Augmented Generation (RAG)** to provide legal responses by retrieving relevant case law from stored PDF files.

## Features
- **FastAPI Backend**: Handles document retrieval and AI processing.
- **Gradio Frontend**: Provides an interactive chatbot UI.
- **FAISS Vector Database**: Stores and retrieves legal documents efficiently.
- **OpenAI GPT-4o Integration**: Enhances responses with AI-powered legal assistance.

## 📂 Project Structure
legal-chatbot/ 
# FastAPI backend for RAG-based legal chatbot 
│── backend.py 
# Gradio chatbot frontend 
│── frontend.py 
# Python dependencies 
│── requirements.txt 
│── README.md # Documentation 
│── LICENSE # MIT License 
# Folder for legal PDFs 
│── pdf_files/ # Place here your jurisprudence files in pdf form
# FAISS vector store (created after indexing)
│── legal_jurisprudence_index/ 

## 🔧 Installation
Clone the repository and install dependencies:

git clone https://github.com/yourusername/legal-chatbot.git
cd legal-chatbot
pip install -r requirements.txt

## Running the Chatbot
1️⃣ Start Backend (FastAPI)
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
2️⃣ Start Frontend (Gradio)
python frontend.py

## How It Works
Uploads legal PDFs and converts them into a FAISS vector database.
Retrieves the most relevant documents when a user asks a legal question.
Sends the retrieved context to OpenAI's GPT-4o for a contextualized response.
Displays the AI-generated response via Gradio.

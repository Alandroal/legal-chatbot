import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from typing import List

# Load environment variables (Set OpenAI API Key)
os.environ["OPENAI_API_KEY"] = "INSERT KEY"

app = FastAPI()

PDF_FOLDER = "pdf_files"  # Folder containing legal PDFs
VECTOR_DB_PATH = "legal_jurisprudence_index"

# Initialize vector DB
vector_db = None

# Define the request model
class QueryRequest(BaseModel):
    query: str

# Function to load all PDFs from a folder into FAISS
def load_pdf_folder():
    global vector_db
    print(f"Loading PDFs from: {PDF_FOLDER}")

    # List all PDF files in the folder
    pdf_files = [os.path.join(PDF_FOLDER, file) for file in os.listdir(PDF_FOLDER) if file.endswith(".pdf")]
    
    if not pdf_files:
        print("No PDF files found in the directory!")
        return
    
    all_docs = []
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file}")
        loader = PyMuPDFLoader(pdf_file)
        docs = loader.load()
        all_docs.extend(docs)

    # Create FAISS vector DB
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_documents(all_docs, embeddings)
    vector_db.save_local(VECTOR_DB_PATH)
    print("All PDFs indexed successfully!")

# Load vector database (or recreate if not found)
if os.path.exists(VECTOR_DB_PATH):
    print("Loading existing FAISS index...")
    vector_db = FAISS.load_local(VECTOR_DB_PATH, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
else:
    load_pdf_folder()

@app.post("/query")
def legal_chatbot(request: QueryRequest):
    query = request.query
    if not vector_db:
        return {"response": "Error: Vector database not found. Ensure PDFs are indexed."}

    # Retrieve top 5 most relevant legal texts
    retrieved_docs = vector_db.similarity_search(query, k=5)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    # Call OpenAI GPT-4 with the retrieved legal context
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a legal assistant."},
            {"role": "user", "content": f"Legal Question: {query}\n\nContext:\n{context}"}
        ]
    )

    return {"response": response.choices[0].message.content}


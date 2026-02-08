import os
import hashlib
import tempfile
import requests
from flask import Flask, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

app = Flask(__name__)


GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"

# Models
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # ✅ Correct model name
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",  # ✅ Correct embedding model
    google_api_key=GOOGLE_API_KEY
)

# Vectorstore folder (absolute path)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstores")
os.makedirs(VECTORSTORE_DIR, exist_ok=True)

def get_pdf_hash(url: str) -> str:
    """Generate a unique ID for each PDF based on its URL."""
    return hashlib.md5(url.encode()).hexdigest()

def load_or_create_vectorstore(pdf_url: str):
    """Load FAISS vectorstore if exists, else create it."""
    pdf_hash = get_pdf_hash(pdf_url)
    store_path = os.path.join(VECTORSTORE_DIR, pdf_hash)
    os.makedirs(store_path, exist_ok=True)  # Ensure folder exists

    # Check if store already exists
    if os.path.exists(os.path.join(store_path, "index.faiss")):
        print(f"[INFO] Loading existing vector store: {store_path}")
        return FAISS.load_local(store_path, embeddings, allow_dangerous_deserialization=True)

    print(f"[INFO] Creating vector store for {pdf_url}")

    # Download PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        pdf_data = requests.get(pdf_url, headers={"User-Agent": "Mozilla/5.0"}).content
        tmp_pdf.write(pdf_data)
        pdf_path = tmp_pdf.name

    # Load & embed
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    db = FAISS.from_documents(documents, embeddings)
    db.save_local(store_path)

    print(f"[SAVED] Vector store created at: {store_path}")

    os.remove(pdf_path)
    return db

# Load prompt from file
def load_prompt_normal():
    prompt_path = os.path.join(BASE_DIR, "prompt_normal.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()
PROMPT_TEMPLATE_NORMAL = load_prompt_normal()

def load_prompt_maths():
    prompt_path = os.path.join(BASE_DIR, "prompt_maths.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()
PROMPT_TEMPLATE_MATHS = load_prompt_maths()

def load_prompt_code():
    prompt_path = os.path.join(BASE_DIR, "prompt_code.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()
PROMPT_TEMPLATE_CODE = load_prompt_code()

...

@app.route("/chat_normal", methods=["POST"])
def chat_normal():
    try:
        data = request.json
        question = data.get("question")
        pdf_url = data.get("pdf_url")

        db = load_or_create_vectorstore(pdf_url)
        retriever = db.as_retriever(search_kwargs={"k": 5})

        # Get relevant docs
        relevant_docs = retriever.get_relevant_documents(question)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        # Load prompt and format it
        final_prompt = PROMPT_TEMPLATE_NORMAL.format(context=context, question=question)

        # Ask LLM
        answer = llm.invoke(final_prompt).content

        return jsonify({"answer": answer})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/chat_math", methods=["POST"])
def chat_math():
    try:
        data = request.json
        question = data.get("question")
        pdf_url = data.get("pdf_url")

        db = load_or_create_vectorstore(pdf_url)
        retriever = db.as_retriever(search_kwargs={"k": 5})

        # Get relevant docs
        relevant_docs = retriever.get_relevant_documents(question)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        # Load prompt and format it
        final_prompt = PROMPT_TEMPLATE_MATHS .format(context=context, question=question)

        # Ask LLM
        answer = llm.invoke(final_prompt).content

        return jsonify({"answer": answer})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/chat_code", methods=["POST"])
def chat_code():
    try:
        data = request.json
        question = data.get("question")
        pdf_url = data.get("pdf_url")

        db = load_or_create_vectorstore(pdf_url)
        retriever = db.as_retriever(search_kwargs={"k": 5})

        # Get relevant docs
        relevant_docs = retriever.get_relevant_documents(question)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        # Load prompt and format it
        final_prompt = PROMPT_TEMPLATE_CODE.format(context=context, question=question)

        # Ask LLM
        answer = llm.invoke(final_prompt).content

        return jsonify({"answer": answer})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(f"[STARTED] Vector stores will be saved in: {VECTORSTORE_DIR}")
    app.run(host="127.0.0.1", port=5000, debug=True)

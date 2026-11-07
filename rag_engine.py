
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"
INDEX_DIR = BASE_DIR / "faiss_index"

EMBEDDING_MODEL = "nomic-embed-text"


def build_knowledge_base():

    # Step 1: Read troubleshooting documents
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        if content.strip():
            documents.append(content)

    if not documents:
        raise ValueError("No runbook documents found!")

    print(f"Loaded {len(documents)} runbook(s)")

    # Step 2: Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.create_documents(documents)

    print(f"Created {len(chunks)} chunks")

    # Step 3: Connect to Ollama embedding model
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )

    # Step 4: Generate embeddings and create FAISS index
    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    # Step 5: Save index locally
    vector_store.save_local(str(INDEX_DIR))

    print("FAISS knowledge base created successfully!")


def search_knowledge_base(question):

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )

    vector_store = FAISS.load_local(
        str(INDEX_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    results = vector_store.similarity_search(
        question,
        k=3
    )

    return "\n\n".join(
        document.page_content for document in results
    )


if __name__ == "__main__":

    build_knowledge_base()

    print("\nTesting FAISS search...\n")

    answer = search_knowledge_base(
        "How to troubleshoot HTTP 503 in Kubernetes?"
    )

    print(answer)

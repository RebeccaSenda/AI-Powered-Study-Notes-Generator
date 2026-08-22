import ollama
import chromadb
import uuid


# ---------------------------------------------------------
# RAG CONFIGURATION
# ---------------------------------------------------------

EMBEDDING_MODEL = "nomic-embed-text"

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="course_material"
)


# ---------------------------------------------------------
# CLEAR PREVIOUS COURSE MATERIAL
# ---------------------------------------------------------

def clear_collection():
    """
    Remove previously stored course material.
    This ensures the AI only searches the current material.
    """

    global collection

    try:
        client.delete_collection(name="course_material")
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name="course_material"
    )


# ---------------------------------------------------------
# CREATE EMBEDDINGS
# ---------------------------------------------------------

def create_embedding(text):
    """
    Convert text into an embedding using Ollama.
    """

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response["embeddings"][0]


# ---------------------------------------------------------
# SPLIT TEXT INTO CHUNKS
# ---------------------------------------------------------

def split_text(text, chunk_size=1000, overlap=200):
    """
    Split course material into smaller overlapping chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# ---------------------------------------------------------
# ADD COURSE MATERIAL
# ---------------------------------------------------------

def add_document(text):
    """
    Split the document into chunks, create embeddings,
    and store them in ChromaDB.
    """

    clear_collection()

    chunks = split_text(text)

    if not chunks:
        return 0

    embeddings = []

    for chunk in chunks:

        embedding = create_embedding(chunk)

        embeddings.append(embedding)

    # Generate unique IDs for each chunk
    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    return len(chunks)


# ---------------------------------------------------------
# RETRIEVE RELEVANT COURSE MATERIAL
# ---------------------------------------------------------

def retrieve_relevant_chunks(query, number_of_results=4):
    """
    Retrieve the most relevant chunks from the uploaded
    course material.
    """

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=number_of_results
    )

    return results["documents"][0]


# ---------------------------------------------------------
# GENERATE RAG ANSWER
# ---------------------------------------------------------

def generate_rag_answer(query):
    """
    Retrieve relevant course material and use Llama
    to generate a grounded answer.
    """

    relevant_chunks = retrieve_relevant_chunks(query)

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are an AI teaching assistant helping a university student.

Answer the student's question using ONLY the course material
provided below.

IMPORTANT RULES:

1. Use the provided course material as your primary source.
2. Do not invent facts.
3. If the answer cannot be found in the uploaded material,
   clearly say that the information is not available in the
   uploaded course material.
4. Explain the answer in simple language suitable for a
   university student.

Retrieved course material:

{context}

Student question:

{query}

Provide a clear and helpful answer.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
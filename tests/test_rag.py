import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag import add_document, retrieve_relevant_chunks, generate_rag_answer


# Sample course material
course_material = """
Artificial Intelligence is a branch of computer science concerned
with creating systems that can perform tasks that normally require
human intelligence.

Machine learning is a subset of Artificial Intelligence.
It allows computers to learn patterns from data and make predictions
or decisions without being explicitly programmed for every task.

Supervised learning uses labelled training data.
Unsupervised learning works with data that does not have predefined
labels.

Generative AI refers to artificial intelligence systems that can
generate new content such as text, images, audio, or code.

Retrieval-Augmented Generation, commonly called RAG, combines
information retrieval with generative AI. The system retrieves
relevant information from a knowledge source and provides that
information to a language model as context before generating an answer.
"""

print("📚 Adding course material to the vector database...")

number_of_chunks = add_document(course_material)

print(f"✅ Added {number_of_chunks} chunks.")

print("\n🔎 Testing retrieval...")

question = "What is Retrieval-Augmented Generation?"

chunks = retrieve_relevant_chunks(question)

print("\nRelevant course material:")
print("--------------------------------")

for chunk in chunks:
    print(chunk)
    print("--------------------------------")

print("\n🤖 Asking Llama for an answer...")

answer = generate_rag_answer(question)

print("\nAI Answer:")
print("--------------------------------")
print(answer)
print("--------------------------------")
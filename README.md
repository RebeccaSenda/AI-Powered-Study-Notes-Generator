# AI-Powered Study Notes Generator

## Project Overview

The AI-Powered Study Notes Generator is a Generative AI application designed to help university students study more efficiently.

Students can upload lecture materials in PDF format or paste study material directly into the application. The system processes the material and uses a locally running AI model to generate useful study resources.

The application also implements Retrieval-Augmented Generation (RAG). RAG allows the system to retrieve relevant information from the uploaded course material before generating answers, helping the AI provide responses that are grounded in the student's material.

The project uses Llama 3.2 3B through Ollama, allowing AI processing to take place locally without requiring a paid cloud AI API or API key.

---

## Features

### PDF Upload

Students can upload lecture notes and other educational material in PDF format.

The application automatically extracts readable text from the uploaded document using PyPDF2.

### Text Input

Students can also paste lecture notes, textbook content, or other study material directly into the application.

### Study Notes

Generates organized study notes containing:

- Summary
- Key concepts
- Important definitions
- Important points to remember
- Possible exam questions

### Quick Revision

Creates a concise revision sheet containing:

- Key ideas
- Important terms
- Must-remember information
- Exam tips

### Exam Questions

Generates:

- 5 multiple-choice questions
- 3 short-answer questions
- 2 essay questions

### Flashcards

Generates 8 question-and-answer flashcards based on the uploaded study material.

### AI Tutor

The AI Tutor allows students to ask questions about their uploaded course material.

The system retrieves relevant sections of the uploaded material using RAG and provides them to the AI model as context before generating an answer.

If the requested information cannot be found in the uploaded course material, the AI is instructed to clearly state that the information is not available in the uploaded material.

### Retrieval-Augmented Generation (RAG)

The project uses RAG to improve the reliability of AI-generated answers.

The RAG pipeline:

1. Extracts the uploaded study material.
2. Splits the material into smaller chunks.
3. Creates embeddings for the chunks.
4. Stores the embeddings in ChromaDB.
5. Converts the student's question into an embedding.
6. Retrieves the most relevant course-material chunks.
7. Provides the retrieved material to Llama as context.
8. Generates an answer based on the retrieved material.

### Download

Students can download generated study material as a text file for later revision.

---

## Technologies Used

- Python - Main programming language
- Streamlit - Web application framework
- Ollama - Local AI platform
- Llama 3.2 3B - Generative AI model
- ChromaDB - Vector database used for RAG
- Nomic Embed Text - Embedding model
- PyPDF2 - PDF text extraction
- Git - Version control
- GitHub - Project hosting

---

## AI Topic

### Generative AI, Text Generation, Summarization and Retrieval-Augmented Generation

The project demonstrates how Generative AI can be used to process educational content and create personalized study resources.

The project also demonstrates Retrieval-Augmented Generation (RAG), where relevant information is retrieved from a knowledge base and supplied to a language model before generating an answer.

---

## System Architecture

The main system workflow is:

```text
Student
   |
   v
Upload PDF / Paste Text
   |
   v
Extract Study Material
   |
   v
Split Material into Chunks
   |
   v
Create Embeddings
   |
   v
Store in ChromaDB
   |
   v
Student Selects Study Mode
   |
   +----------------------------+
   |                            |
   v                            v
Study Resources             AI Tutor
   |                            |
   |                     Retrieve Relevant
   |                     Course Material
   |                            |
   |                            v
   |                       Llama 3.2 3B
   |                            |
   +------------+---------------+
                |
                v
         Display Results
                |
                v
        Download Material
AI-Powered Study Notes Generator

Project Overview



The AI-Powered Study Notes Generator is a Generative AI application designed to help university students study more efficiently.



Students can upload lecture materials in PDF format or paste their study material directly into the application. The system extracts the content and uses a locally running AI model to generate different study resources.



The application uses Llama 3.2 3B through Ollama, allowing the AI processing to take place locally without requiring a paid cloud AI API or API key.



Features

📄 PDF Upload



Students can upload lecture notes and other educational material in PDF format. The application automatically extracts readable text from the document.



✍️ Text Input



Students can also paste lecture notes, textbook content, or other study material directly into the application.



📚 Study Notes



Generates organized study notes containing:



Summary

Key concepts

Important definitions

Important points to remember

Possible exam questions

⚡ Quick Revision



Creates a concise revision sheet containing:



Key ideas

Important terms

Must-remember information

Exam tips

❓ Exam Questions



Generates:



5 multiple-choice questions

3 short-answer questions

2 essay questions

🧠 Flashcards



Generates 8 question-and-answer flashcards based on the provided study material.



💾 Download



Students can download the generated study material as a text file for later revision.



Technologies Used

Python — Main programming language

Streamlit — Web application framework

Ollama — Local AI platform

Llama 3.2 3B — Generative AI model

PyPDF2 — PDF text extraction

GitHub — Version control and project hosting

AI Topic



Text Generation and Summarization



The project demonstrates the use of Generative AI to process educational content and create useful study resources for students.



System Workflow

Student

&#x20;  ↓

Upload PDF or Paste Text

&#x20;  ↓

Extract / Read Study Material

&#x20;  ↓

Select Study Mode

&#x20;  ↓

Llama 3.2 3B via Ollama

&#x20;  ↓

Generate Study Resource

&#x20;  ↓

Display Results

&#x20;  ↓

Download Material

How It Works

The student uploads a PDF or enters study material manually.

If a PDF is uploaded, PyPDF2 extracts the readable text.

The student selects a study mode.

The application creates a prompt based on the selected mode.

The study material is sent to the locally running Llama 3.2 3B model through Ollama.

The AI generates the requested study resource.

The generated material is displayed in the Streamlit interface.

The student can download the generated material.

Installation

1\. Clone the repository

git clone <YOUR-GITHUB-REPOSITORY-URL>

2\. Open the project folder

cd AI-Powered-Study-Notes-Generator

3\. Install the required Python packages

pip install -r requirements.txt

4\. Install Ollama



Install Ollama and make sure the required Llama model is available locally.



The application currently uses:



llama3.2:3b

5\. Run the application

python -m streamlit run app.py



The application will open in a web browser.



Project Team



BIT 4543 Artificial Intelligence Group Project


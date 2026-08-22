import streamlit as st
import ollama
from PyPDF2 import PdfReader

# Page configuration
st.set_page_config(
    page_title="AI Study Notes Generator",
    page_icon="📚",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="main-title">📚 AI-Powered Study Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Transform your study material into notes, revision points, '
    'exam questions, or flashcards using AI.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# Study mode
st.subheader("🎯 Choose a Study Mode")

study_mode = st.selectbox(
    "What would you like to generate?",
    [
        "📚 Study Notes",
        "⚡ Quick Revision",
        "❓ Exam Questions",
        "🧠 Flashcards"
    ]
)

# Study material section
st.subheader("📖 Study Material")

input_method = st.radio(
    "How would you like to provide your study material?",
    ["📄 Upload PDF", "✍️ Paste Text"],
    horizontal=True
)

study_material = ""

# PDF Upload
if input_method == "📄 Upload PDF":

    uploaded_file = st.file_uploader(
        "Upload your lecture notes or study material as a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        try:
            pdf_reader = PdfReader(uploaded_file)

            extracted_text = ""

            for page in pdf_reader.pages:
                page_text = page.extract_text()

                if page_text:
                    extracted_text += page_text + "\n"

            if extracted_text.strip():

                study_material = extracted_text

                st.success(
                    f"✅ PDF uploaded successfully! "
                    f"Extracted text from {len(pdf_reader.pages)} page(s)."
                )

                with st.expander("👀 Preview Extracted Text"):
                    st.text_area(
                        "Extracted content",
                        extracted_text,
                        height=250
                    )

            else:

                st.warning(
                    "⚠️ No readable text was found in this PDF. "
                    "Please try another PDF or paste the text manually."
                )

        except Exception as e:

            st.error(
                "❌ There was a problem reading the PDF."
            )

            st.code(str(e))

# Manual text input
else:

    study_material = st.text_area(
        "Paste your lecture notes, textbook content, or study material here:",
        height=300,
        placeholder="Paste your study material here..."
    )


# Generate the AI prompt based on the selected mode

if study_mode == "📚 Study Notes":

    prompt = f"""
You are an AI study assistant helping a university student.

Analyze the study material below and create well-organized study notes.

Use these sections:

## Summary
Give a clear summary of the material.

## Key Concepts
List the most important concepts and explain each briefly.

## Important Definitions
Identify important terms and provide simple definitions.

## Important Points to Remember
List the facts or ideas most important for an exam.

## Possible Exam Questions
Create 3 possible exam questions based only on the material.

Keep the language simple and easy to understand.

Study material:

{study_material}
"""

elif study_mode == "⚡ Quick Revision":

    prompt = f"""
You are an AI study assistant.

Turn the study material below into a quick revision sheet.

Include:

## Key Ideas
Only the most important ideas.

## Important Terms
List important terms with short definitions.

## Must Remember
Give the most important facts a student should memorize.

## Exam Tips
Give useful points for answering exam questions.

Keep everything concise and easy to review quickly.

Study material:

{study_material}
"""

elif study_mode == "❓ Exam Questions":

    prompt = f"""
You are an AI university exam preparation assistant.

Create exam questions based ONLY on the study material below.

Create:

## Multiple Choice Questions
Create 5 multiple-choice questions.
Give 4 options for each question.
Clearly identify the correct answer.

## Short Answer Questions
Create 3 short-answer questions.

## Essay Questions
Create 2 essay-style questions.

Make the questions appropriate for a university student.

Study material:

{study_material}
"""

else:

    prompt = f"""
You are an AI study assistant.

Create study flashcards from the material below.

Create 8 flashcards.

Use this format:

### Flashcard 1
**Question:** ...
**Answer:** ...

### Flashcard 2
**Question:** ...
**Answer:** ...

Continue until you have created 8 flashcards.

Questions should test important concepts, definitions,
and facts from the material.

Study material:

{study_material}
"""


# Generate button

if st.button("✨ Generate", type="primary"):

    if not study_material.strip():

        st.warning(
            "⚠️ Please upload a PDF or enter some study material before generating."
        )

    else:

        with st.spinner("🧠 AI is preparing your study material..."):

            try:

                response = ollama.chat(
                    model="llama3.2:3b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                generated_content = response["message"]["content"]

                st.divider()

                st.subheader("📚 Generated Content")

                st.markdown(generated_content)

                st.download_button(
                    label="💾 Download Study Material",
                    data=generated_content,
                    file_name="study_material.txt",
                    mime="text/plain"
                )

            except Exception as e:

                st.error(
                    "❌ Unable to connect to the AI model. "
                    "Please make sure Ollama is running."
                )

                st.code(str(e))
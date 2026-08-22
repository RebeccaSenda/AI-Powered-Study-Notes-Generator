import streamlit as st
import ollama
from PyPDF2 import PdfReader

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f7f9ff 0%, #f3efff 100%);
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 19px;
        color: #555555;
        margin-bottom: 20px;
    }

    /* Welcome message */
    .welcome-box {
        background: white;
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    }

    /* Section headers */
    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Study mode cards */
    .mode-card {
        background: white;
        padding: 18px;
        border-radius: 16px;
        text-align: center;
        min-height: 125px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }

    .mode-card h3 {
        margin-bottom: 8px;
    }

    .mode-card p {
        color: #666666;
        font-size: 14px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777777;
        font-size: 13px;
        margin-top: 35px;
        padding: 20px;
    }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">📚 AI Study Buddy</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Turn your lecture material into smarter ways to study.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="welcome-box">
    <h3>✨ Ready to study smarter?</h3>
    <p>
        Upload your lecture material, choose how you want to study,
        and let your AI study buddy do the hard work.
    </p>
    <p><strong>You've got this! 💪📖</strong></p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# STUDY MATERIAL
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📖 Bring Your Study Material</div>',
    unsafe_allow_html=True
)

st.write(
    "Upload a lecture PDF or paste your notes below. "
    "We'll turn them into useful study resources."
)

input_method = st.radio(
    "Choose how you want to provide your material:",
    ["📄 Upload PDF", "✍️ Paste Text"],
    horizontal=True
)

study_material = ""

# ---------------------------------------------------------
# PDF UPLOAD
# ---------------------------------------------------------

if input_method == "📄 Upload PDF":

    uploaded_file = st.file_uploader(
        "📄 Drop your lecture PDF here or browse your files",
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
                    f"🎉 Nice! We successfully read "
                    f"{len(pdf_reader.pages)} page(s) from your PDF."
                )

                with st.expander("👀 Preview your study material"):

                    st.text_area(
                        "Extracted text",
                        extracted_text,
                        height=250
                    )

            else:

                st.warning(
                    "⚠️ We couldn't find readable text in this PDF. "
                    "Try another PDF or paste your material instead."
                )

        except Exception as e:

            st.error(
                "❌ Something went wrong while reading the PDF."
            )

            st.code(str(e))

# ---------------------------------------------------------
# TEXT INPUT
# ---------------------------------------------------------

else:

    study_material = st.text_area(
        "✍️ Paste your lecture notes, textbook content, "
        "or study material here:",
        height=300,
        placeholder="Paste your study material here and let's get studying! 📚"
    )

# ---------------------------------------------------------
# STUDY MODES
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">🎯 What Are We Studying Today?</div>',
    unsafe_allow_html=True
)

st.write(
    "Choose the study tool that matches what you need right now."
)

study_mode = st.selectbox(
    "Choose a study mode:",
    [
        "📚 Study Notes",
        "⚡ Quick Revision",
        "❓ Exam Questions",
        "🧠 Flashcards"
    ]
)

# Study mode explanation

mode_descriptions = {
    "📚 Study Notes":
        "Organize your material into clear notes, concepts and definitions.",

    "⚡ Quick Revision":
        "Get the important information you need for a fast review.",

    "❓ Exam Questions":
        "Challenge yourself with MCQs, short answers and essay questions.",

    "🧠 Flashcards":
        "Practice active recall with AI-generated question-and-answer cards."
}

st.info(
    f"💡 **{study_mode}** — {mode_descriptions[study_mode]}"
)

# ---------------------------------------------------------
# AI PROMPTS
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# GENERATE
# ---------------------------------------------------------

st.divider()

if st.button("✨ Generate My Study Material", type="primary"):

    if not study_material.strip():

        st.warning(
            "📖 Please upload a PDF or paste some study material first!"
        )

    else:

        with st.spinner(
            "🧠 Your AI study buddy is working... "
            "Give it a moment!"
        ):

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

                st.markdown(
                    '<div class="section-title">'
                    '🎉 Your Study Material Is Ready!'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(generated_content)

                st.download_button(
                    label="💾 Download My Study Material",
                    data=generated_content,
                    file_name="study_material.txt",
                    mime="text/plain"
                )

                st.success(
                    "🎉 Great job! One step closer to mastering your material. 💪"
                )

            except Exception as e:

                st.error(
                    "❌ Unable to connect to the AI model. "
                    "Please make sure Ollama is running."
                )

                st.code(str(e))

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("""
<div class="footer">
    📚 AI Study Buddy • BIT 4543 Artificial Intelligence Group Project
    <br>
    <em>Study smarter. Revise better. You've got this! 💪✨</em>
</div>
""", unsafe_allow_html=True)
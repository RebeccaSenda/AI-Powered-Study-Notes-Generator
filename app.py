import streamlit as st
import ollama
from PyPDF2 import PdfReader
from src.rag import add_document, retrieve_relevant_chunks, generate_rag_answer

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

    .stApp {
        background: linear-gradient(135deg, #f7f9ff 0%, #f3efff 100%);
    }

    .main-title {
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 19px;
        color: #555555;
        margin-bottom: 20px;
    }

    .welcome-box {
        background: white;
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }

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

            with st.spinner("🔎 Preparing your material for AI search..."):

                chunk_count = add_document(extracted_text)

            st.success(
                f"🧠 RAG knowledge base ready! "
                f"{chunk_count} course material chunks were indexed."
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

else:

    study_material = st.text_area(
        "✍️ Paste your lecture notes, textbook content, "
        "or study material here:",
        height=300,
        placeholder="Paste your study material here and let's get studying! 📚"
    )
  
# ---------------------------------------------------------
# RAG KNOWLEDGE BASE
# ---------------------------------------------------------

if study_material.strip():

    st.divider()

    st.markdown(
        '<div class="section-title">🧠 Course Knowledge Base</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Your material can be indexed so the AI can retrieve "
        "relevant information when answering your questions."
    )

    if st.button("🔎 Prepare Material for AI Tutor"):

        with st.spinner(
            "🧠 Reading and preparing your course material..."
        ):

            try:

                number_of_chunks = add_document(
                    study_material
                )

                st.session_state["rag_ready"] = True

                st.success(
                    f"✅ Your material is ready! "
                    f"{number_of_chunks} knowledge chunks were created."
                )

            except Exception as e:

                st.error(
                    "❌ Unable to prepare the course material."
                )

                st.code(str(e))


# ---------------------------------------------------------
# AI TEACHING ASSISTANT
# ---------------------------------------------------------

if st.session_state.get("rag_ready", False):

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '💬 Ask Your Course Material'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask a question about your uploaded course material. "
        "The AI will retrieve relevant information before answering."
    )

    user_question = st.text_input(
        "💭 What would you like to know?",
        placeholder="Example: What is the difference between supervised and unsupervised learning?"
    )

    if st.button("🤖 Ask My AI Tutor"):

        if not user_question.strip():

            st.warning(
                "💭 Please enter a question first."
            )

        else:

            with st.spinner(
                "🔎 Searching your course material and preparing an answer..."
            ):

                try:

                    answer = generate_rag_answer(
                        user_question
                    )

                    st.markdown(
                        '<div class="section-title">'
                        '💡 AI Tutor Answer'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                    st.download_button(
                        label="💾 Download Answer",
                        data=answer,
                        file_name="ai_tutor_answer.txt",
                        mime="text/plain"
                    )

                except Exception as e:

                    st.error(
                        "❌ Something went wrong while generating "
                        "the AI tutor answer."
                    )

                    st.code(str(e))


# ---------------------------------------------------------
# STUDY MODES
# ---------------------------------------------------------

st.divider()

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

Use ONLY the study material below.

Generate exactly 5 multiple-choice questions.

For each question:
- Give 4 options: A, B, C, D.
- Clearly provide the correct answer.
- Base every question only on the study material.

Do not generate short-answer questions.
Do not generate essay questions.

Study material:

{study_material}
"""
elif study_mode == "🧠 Flashcards":

    prompt = f"""
You are an AI study assistant helping a university student.

Create exactly 8 flashcards based ONLY on the study material below.

Each flashcard must contain:

Card 1
Question: ...
Answer: ...

Card 2
Question: ...
Answer: ...

Continue until Card 8.

IMPORTANT:
- Create exactly 8 flashcards.
- Keep questions clear and useful for exam revision.
- Answers must be based ONLY on the study material.
- Do not invent information.
- Do not create study notes.
- Do not create exam questions.
- Do not create a quick revision sheet.

Study material:

{study_material}
"""
# ---------------------------------------------------------
# GENERATE STUDY MATERIAL USING RAG
# ---------------------------------------------------------

if st.button(
    "✨ Generate My Study Material",
    type="primary"
):

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

                # -------------------------------------------------
                # EXAM QUESTIONS MODE
                # -------------------------------------------------

                if study_mode == "❓ Exam Questions":

                    # Retrieve relevant course material using RAG
                    relevant_chunks = retrieve_relevant_chunks(
                        "important concepts definitions programming modules functions arguments parameters",
                        number_of_results=4
                    )

                    exam_context = "\n\n".join(relevant_chunks)

                    # Generate all exam questions in ONE AI call
                    exam_response = ollama.chat(
                        model="llama3.2:3b",
                        messages=[
                            {
                                "role": "user",
                                "content": f"""
You are a university exam question generator.

Use ONLY the retrieved course material below.

You MUST generate ALL THREE sections.

Your response MUST contain exactly:

## Multiple Choice Questions

Create exactly 5 multiple-choice questions.

For EACH question:
- Give exactly four options: A, B, C, D.
- Clearly state the correct answer.

## Short Answer Questions

Create exactly 3 short-answer questions.
Do not provide answers.

## Essay Questions

Create exactly 2 essay-style questions.
Do not provide answers.

IMPORTANT:
- Generate all 10 questions before finishing.
- Do not generate Study Notes.
- Do not generate Quick Revision.
- Do not generate Flashcards.
- Do not add an introduction or conclusion.
- Base every question ONLY on the retrieved course material.

Retrieved course material:

{exam_context}
"""
                            }
                        ]
                    )

                    generated_content = exam_response[
                        "message"
                    ]["content"]
                # -------------------------------------------------
                # ALL OTHER STUDY MODES
                # -------------------------------------------------

                else:

                    response = ollama.chat(
                        model="llama3.2:3b",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    generated_content = response[
                        "message"
                    ]["content"]


                # -------------------------------------------------
                # DISPLAY RESULT
                # -------------------------------------------------

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
                    "🎉 Great job! One step closer to mastering "
                    "your material. 💪"
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

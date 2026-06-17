import streamlit as st
import random
import io

# PyPDF2 is used to extract raw text from the uploaded PDF.
# Install with: pip install streamlit PyPDF2
import PyPDF2

st.set_page_config(page_title="PDF Quiz Generator", page_icon="📄", layout="centered")


# =====================================================================
# 1) PDF TEXT EXTRACTION
# =====================================================================
def extract_text_from_pdf(uploaded_file) -> str:
    """Reads an uploaded PDF (Streamlit UploadedFile) and returns its raw text."""
    reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text


# =====================================================================
# 2) QUESTION GENERATION — replace this with your own logic
# =====================================================================
def generate_questions_from_text(pdf_text: str, num_questions: int = 5) -> list[dict]:
    """
    Replace the body of this function with your own logic to turn `pdf_text`
    into a list of multiple-choice questions.

    Each question MUST be a dict shaped like this:
        {
            "question": "What is ... ?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option B"   # must exactly match one of the options
        }

    You can call an LLM here (e.g. Claude/OpenAI), run your own NLP pipeline,
    or anything else — as long as you return a list of dicts in this shape.

    Below is a placeholder implementation so the app runs end-to-end before
    you plug in real logic. It just creates dummy fill-in-the-blank style
    questions out of sentences in the PDF, purely so you can test the UI flow.
    """
    sentences = [s.strip() for s in pdf_text.replace("\n", " ").split(".") if len(s.strip()) > 40]
    random.shuffle(sentences)

    questions = []
    for sentence in sentences[:num_questions]:
        words = sentence.split()
        if len(words) < 6:
            continue
        blank_index = random.randint(3, len(words) - 2)
        correct_word = words[blank_index]
        question_text = " ".join(
            words[:blank_index] + ["____"] + words[blank_index + 1:]
        )
        # Dummy distractors — replace with real wrong-answer logic
        distractors = ["example", "placeholder", "unknown"]
        options = [correct_word] + distractors
        random.shuffle(options)

        questions.append(
            {
                "question": f"Fill in the blank: \"{question_text}\"",
                "options": options,
                "answer": correct_word,
            }
        )

    return questions


# =====================================================================
# 3) SESSION STATE SETUP
# =====================================================================
defaults = {
    "stage": "upload",   # "upload" -> "quiz" -> "results"
    "pdf_text": "",
    "questions": [],
    "current_q": 0,
    "score": 0,
    "answers": [],
    "selected_option": None,
    "submitted": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_to_upload():
    for key, value in defaults.items():
        st.session_state[key] = value


def go_to_quiz(questions):
    st.session_state.questions = questions
    st.session_state.stage = "quiz"
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.selected_option = None
    st.session_state.submitted = False


def submit_answer():
    q = st.session_state.questions[st.session_state.current_q]
    selected = st.session_state.selected_option
    is_correct = selected == q["answer"]
    if is_correct:
        st.session_state.score += 1
    st.session_state.answers.append(
        {
            "question": q["question"],
            "selected": selected,
            "correct": q["answer"],
            "is_correct": is_correct,
        }
    )
    st.session_state.submitted = True


def next_question():
    st.session_state.current_q += 1
    st.session_state.selected_option = None
    st.session_state.submitted = False


# =====================================================================
# 4) UI — STAGE: UPLOAD
# =====================================================================
st.title("📄 PDF Quiz Generator")

if st.session_state.stage == "upload":
    st.write("Upload a PDF and a multiple-choice quiz will be generated from its content.")

    uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])
    num_questions = st.slider("Number of questions", min_value=3, max_value=15, value=5)

    if uploaded_file is not None:
        if st.button("Generate Quiz", type="primary"):
            with st.spinner("Reading PDF and generating questions..."):
                pdf_text = extract_text_from_pdf(uploaded_file)
                if not pdf_text.strip():
                    st.error("Couldn't extract any text from this PDF. Try a different file.")
                else:
                    st.session_state.pdf_text = pdf_text
                    questions = generate_questions_from_text(pdf_text, num_questions)
                    if not questions:
                        st.error("Couldn't generate questions from this PDF's content.")
                    else:
                        go_to_quiz(questions)
                        st.rerun()

# =====================================================================
# 5) UI — STAGE: QUIZ
# =====================================================================
elif st.session_state.stage == "quiz":
    total = len(st.session_state.questions)
    current = st.session_state.current_q
    q = st.session_state.questions[current]

    st.progress(current / total, text=f"Question {current + 1} of {total}")
    st.subheader(q["question"])

    if not st.session_state.submitted:
        choice = st.radio(
            "Choose your answer:",
            q["options"],
            index=None,
            key=f"radio_{current}",
        )
        st.session_state.selected_option = choice

        if st.button("Submit", type="primary", disabled=choice is None):
            submit_answer()
            st.rerun()
    else:
        last = st.session_state.answers[-1]
        if last["is_correct"]:
            st.success(f"✅ Correct! The answer is **{last['correct']}**.")
        else:
            st.error(f"❌ Incorrect. You selected **{last['selected']}**. The correct answer is **{last['correct']}**.")

        button_label = "Next Question" if current + 1 < total else "See Results"
        if st.button(button_label, type="primary"):
            if current + 1 < total:
                next_question()
            else:
                st.session_state.stage = "results"
            st.rerun()

    st.caption(f"Score so far: {st.session_state.score} / {len(st.session_state.answers)}")

# =====================================================================
# 6) UI — STAGE: RESULTS
# =====================================================================
elif st.session_state.stage == "results":
    total = len(st.session_state.questions)
    score = st.session_state.score
    pct = round((score / total) * 100) if total else 0

    st.header("🎉 Quiz Complete!")
    st.subheader(f"Your score: {score} / {total} ({pct}%)")

    if pct == 100:
        st.balloons()
    elif pct >= 70:
        st.write("Great job!")
    elif pct >= 40:
        st.write("Decent effort — review the PDF and try again.")
    else:
        st.write("Worth another read-through of the PDF.")

    st.divider()
    st.subheader("Review your answers")
    for i, a in enumerate(st.session_state.answers, start=1):
        icon = "✅" if a["is_correct"] else "❌"
        with st.expander(f"{icon} Q{i}: {a['question']}"):
            st.write(f"Your answer: **{a['selected']}**")
            st.write(f"Correct answer: **{a['correct']}**")

    st.divider()
    if st.button("Upload a New PDF", type="primary"):
        reset_to_upload()
        st.rerun()

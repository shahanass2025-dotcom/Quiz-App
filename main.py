import streamlit as st
import random

st.set_page_config(page_title="Quiz Generator", page_icon="🧠", layout="centered")

# =====================================================================
# STYLES
# =====================================================================
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .block-container {
            padding-top: 3.5rem;
            max-width: 720px;
        }

        .page-title {
            text-align: center;
            font-size: 2.6rem;
            font-weight: 800;
            color: #111111;
            margin-bottom: 0.4rem;
        }

        .page-subtitle {
            text-align: center;
            font-size: 1.05rem;
            color: #6b7280;
            margin-bottom: 2.2rem;
        }

        .upload-box {
            border: 2px dashed #d1d5db;
            border-radius: 14px;
            background-color: #fafafa;
            padding: 2.5rem 2rem 1.5rem 2rem;
            text-align: center;
            margin-bottom: 1.4rem;
        }

        .upload-icon {
            font-size: 2rem;
            margin-bottom: 0.6rem;
        }

        .upload-text {
            color: #6b7280;
            font-size: 1rem;
            margin-bottom: 0.2rem;
        }

        .upload-subtext {
            color: #9ca3af;
            font-size: 0.85rem;
        }

        div[data-testid="stFileUploaderDropzone"] {
            background-color: transparent;
            border: none;
        }

        div.stButton > button[kind="primary"] {
            background-color: #e11d2e;
            border: none;
            color: white;
            font-weight: 600;
            padding: 0.7rem 1.6rem;
            border-radius: 8px;
            width: 100%;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #c11626;
            color: white;
        }

        div.stButton > button[kind="secondary"] {
            border: 1.5px solid #d1d5db;
            color: #111111;
            font-weight: 600;
            border-radius: 8px;
            width: 100%;
        }

        /* Score summary cards */
        .score-hero {
            text-align: center;
            margin-bottom: 1.8rem;
        }

        .score-hero-value {
            font-size: 3.4rem;
            font-weight: 800;
            color: #111111;
            line-height: 1;
        }

        .score-hero-label {
            color: #6b7280;
            font-size: 1rem;
            margin-top: 0.2rem;
        }

        .stat-card {
            border-radius: 12px;
            padding: 1.1rem 0.5rem;
            text-align: center;
        }

        .stat-card-correct {
            background-color: #ecfdf3;
        }

        .stat-card-wrong {
            background-color: #fef2f2;
        }

        .stat-card-percentage {
            background-color: #f3f4f6;
        }

        .stat-value {
            font-size: 1.9rem;
            font-weight: 800;
        }

        .stat-value-correct { color: #15803d; }
        .stat-value-wrong { color: #dc2626; }
        .stat-value-percentage { color: #111111; }

        .stat-label {
            font-size: 0.85rem;
            color: #6b7280;
            margin-top: 0.2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# PLACEHOLDER QUESTION GENERATION — replace with your real logic/backend
# =====================================================================
def generate_questions_from_file(uploaded_file) -> list[dict]:
    """
    Replace this with a real call to your backend / generation logic.
    Must return a list of dicts shaped like:
        {"question": str, "options": [str, str, str, str], "answer": str}
    """
    return [
        {
            "question": "What is the capital of France?",
            "options": ["Berlin", "Madrid", "Paris", "Rome"],
            "answer": "Paris",
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Earth", "Mars", "Jupiter", "Venus"],
            "answer": "Mars",
        },
        {
            "question": "Which language is primarily used for Streamlit apps?",
            "options": ["JavaScript", "Python", "Java", "C++"],
            "answer": "Python",
        },
        {
            "question": "How many continents are there on Earth?",
            "options": ["5", "6", "7", "8"],
            "answer": "7",
        },
        {
            "question": "What is the chemical symbol for gold?",
            "options": ["Go", "Gd", "Au", "Ag"],
            "answer": "Au",
        },
    ]


# =====================================================================
# SESSION STATE
# =====================================================================
defaults = {
    "stage": "upload",     # "upload" -> "quiz" -> "score" -> "review"
    "questions": [],
    "current_q": 0,
    "answers": [],
    "selected_option": None,
    "submitted": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_all():
    for key, value in defaults.items():
        st.session_state[key] = value


def start_quiz(questions):
    st.session_state.questions = questions
    st.session_state.stage = "quiz"
    st.session_state.current_q = 0
    st.session_state.answers = []
    st.session_state.selected_option = None
    st.session_state.submitted = False


def submit_answer():
    q = st.session_state.questions[st.session_state.current_q]
    selected = st.session_state.selected_option
    is_correct = selected == q["answer"]
    st.session_state.answers.append(
        {
            "question": q["question"],
            "options": q["options"],
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
# STAGE 1 — UPLOAD
# =====================================================================
if st.session_state.stage == "upload":
    st.markdown('<div class="page-title">Quiz Generator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Upload a document and get an instant multiple-choice quiz to test your knowledge.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="upload-box">
            <div class="upload-icon">📄</div>
            <div class="upload-text">Click to upload or drag and drop</div>
            <div class="upload-subtext">PDF, DOCX (MAX. 10MB)</div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload file",
        type=["pdf", "docx"],
        label_visibility="collapsed",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Upload PDF", type="primary", use_container_width=True):
        if uploaded_file is None:
            st.warning("Please choose a file first.")
        else:
            with st.spinner("Generating your quiz..."):
                questions = generate_questions_from_file(uploaded_file)
            if not questions:
                st.error("Couldn't generate questions from this file.")
            else:
                start_quiz(questions)
                st.rerun()

# =====================================================================
# STAGE 2 — QUIZ
# =====================================================================
elif st.session_state.stage == "quiz":
    total = len(st.session_state.questions)
    current = st.session_state.current_q
    q = st.session_state.questions[current]

    st.markdown('<div class="page-title">Quiz Generator</div>', unsafe_allow_html=True)
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

        if st.button("Submit", type="primary", disabled=choice is None, use_container_width=True):
            submit_answer()
            st.rerun()
    else:
        last = st.session_state.answers[-1]
        if last["is_correct"]:
            st.success(f"✅ Correct! The answer is **{last['correct']}**.")
        else:
            st.error(f"❌ Incorrect. You selected **{last['selected']}**. The correct answer is **{last['correct']}**.")

        label = "Next Question" if current + 1 < total else "See Score"
        if st.button(label, type="primary", use_container_width=True):
            if current + 1 < total:
                next_question()
            else:
                st.session_state.stage = "score"
            st.rerun()

# =====================================================================
# STAGE 3 — SCORE SUMMARY
# =====================================================================
elif st.session_state.stage == "score":
    answers = st.session_state.answers
    total = len(answers)
    correct = sum(1 for a in answers if a["is_correct"])
    wrong = total - correct
    pct = round((correct / total) * 100) if total else 0

    st.markdown('<div class="page-title">Quiz Generator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Here\'s how you did on this quiz.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="score-hero">
            <div class="score-hero-value">{correct} / {total}</div>
            <div class="score-hero-label">Score</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="stat-card stat-card-correct">
                <div class="stat-value stat-value-correct">{correct}</div>
                <div class="stat-label">Correct answers</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="stat-card stat-card-wrong">
                <div class="stat-value stat-value-wrong">{wrong}</div>
                <div class="stat-label">Wrong answers</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="stat-card stat-card-percentage">
                <div class="stat-value stat-value-percentage">{pct}%</div>
                <div class="stat-label">Percentage</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.write("")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Review Answers", type="primary", use_container_width=True):
            st.session_state.stage = "review"
            st.rerun()
    with col_b:
        if st.button("Start New Quiz", type="secondary", use_container_width=True):
            reset_all()
            st.rerun()

# =====================================================================
# STAGE 4 — REVIEW ANSWERS
# =====================================================================
elif st.session_state.stage == "review":
    st.markdown('<div class="page-title">Review Answers</div>', unsafe_allow_html=True)

    for i, a in enumerate(st.session_state.answers, start=1):
        icon = "✅" if a["is_correct"] else "❌"
        with st.expander(f"{icon} Q{i}: {a['question']}"):
            st.write(f"Your answer: **{a['selected']}**")
            st.write(f"Correct answer: **{a['correct']}**")

    st.write("")
    if st.button("Back to Score", type="primary", use_container_width=True):
        st.session_state.stage = "score"
        st.rerun()

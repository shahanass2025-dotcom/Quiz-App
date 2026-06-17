
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"  # change if backend runs elsewhere

st.set_page_config(page_title="PDF/Word Quiz Generator", page_icon="📄", layout="centered")


# =====================================================================
# SESSION STATE SETUP
# =====================================================================
defaults = {
    "stage": "upload",   # "upload" -> "quiz" -> "results"
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
# CALL BACKEND
# =====================================================================
def call_backend_generate_quiz(uploaded_file, num_questions: int) -> list[dict]:
    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
    }
    params = {"num_questions": num_questions}

    response = requests.post(
        f"{BACKEND_URL}/generate-quiz",
        files=files,
        params=params,
        timeout=60,
    )

    if response.status_code != 200:
        try:
            detail = response.json().get("detail", response.text)
        except Exception:
            detail = response.text
        raise RuntimeError(detail)

    return response.json()["questions"]


# =====================================================================
# UI — STAGE: UPLOAD
# =====================================================================
st.title("📄 PDF/Word Quiz Generator")

if st.session_state.stage == "upload":
    st.write("Upload a PDF or Word document. The backend will generate a multiple-choice quiz from its content.")

    uploaded_file = st.file_uploader("Upload your file", type=["pdf", "docx"])
    num_questions = st.slider("Number of questions", min_value=3, max_value=15, value=5)

    if uploaded_file is not None:
        if st.button("Generate Quiz", type="primary"):
            with st.spinner("Sending file to backend and generating questions..."):
                try:
                    questions = call_backend_generate_quiz(uploaded_file, num_questions)
                except requests.exceptions.ConnectionError:
                    st.error("Could not reach the backend. Make sure it's running at " + BACKEND_URL)
                except RuntimeError as e:
                    st.error(f"Backend error: {e}")
                else:
                    if not questions:
                        st.error("No questions were generated from this file.")
                    else:
                        go_to_quiz(questions)
                        st.rerun()

# =====================================================================
# UI — STAGE: QUIZ
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
# UI — STAGE: RESULTS
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
        st.write("Decent effort — review the document and try again.")
    else:
        st.write("Worth another read-through of the document.")

    st.divider()
    st.subheader("Review your answers")
    for i, a in enumerate(st.session_state.answers, start=1):
        icon = "✅" if a["is_correct"] else "❌"
        with st.expander(f"{icon} Q{i}: {a['question']}"):
            st.write(f"Your answer: **{a['selected']}**")
            st.write(f"Correct answer: **{a['correct']}**")

    st.divider()
    if st.button("Upload a New File", type="primary"):
        reset_to_upload()
        st.rerun()

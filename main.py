import streamlit as st
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Online Quiz App", page_icon="🧠", layout="centered")

# ── Question Bank ─────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "question": "What does HTML stand for?",
        "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Logic", "Home Tool Markup Language"],
        "answer": "Hyper Text Markup Language",
        "category": "Web Development"
    },
    {
        "question": "Which language is primarily used for styling web pages?",
        "options": ["JavaScript", "Python", "CSS", "SQL"],
        "answer": "CSS",
        "category": "Web Development"
    },
    {
        "question": "What is the time complexity of binary search?",
        "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
        "answer": "O(log n)",
        "category": "Data Structures"
    },
    {
        "question": "Which data structure uses LIFO order?",
        "options": ["Queue", "Stack", "Linked List", "Tree"],
        "answer": "Stack",
        "category": "Data Structures"
    },
    {
        "question": "What keyword is used to define a function in Python?",
        "options": ["func", "define", "def", "function"],
        "answer": "def",
        "category": "Python"
    },
    {
        "question": "Which Python library is used for data manipulation?",
        "options": ["NumPy", "Pandas", "Matplotlib", "Scikit-learn"],
        "answer": "Pandas",
        "category": "Python"
    },
    {
        "question": "What does SQL stand for?",
        "options": ["Structured Query Language", "Simple Query Logic", "Sequential Query List", "Standard Query Language"],
        "answer": "Structured Query Language",
        "category": "Database"
    },
    {
        "question": "Which command retrieves data from a SQL table?",
        "options": ["FETCH", "GET", "SELECT", "RETRIEVE"],
        "answer": "SELECT",
        "category": "Database"
    },
    {
        "question": "What is the output of: print(type([]))?",
        "options": ["<class 'tuple'>", "<class 'dict'>", "<class 'list'>", "<class 'array'>"],
        "answer": "<class 'list'>",
        "category": "Python"
    },
    {
        "question": "Which HTTP method is used to send data to a server?",
        "options": ["GET", "DELETE", "PUT", "POST"],
        "answer": "POST",
        "category": "Web Development"
    },
]

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Background */
    .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); }

    /* Main card */
    .main-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
    }

    /* Title */
    .app-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #e94560, #0f3460, #533483);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .app-subtitle {
        text-align: center;
        color: #aaa;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* Question box */
    .question-box {
        background: linear-gradient(135deg, #e94560, #533483);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(233,69,96,0.3);
    }

    /* Category badge */
    .category-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 3px 14px;
        font-size: 0.78rem;
        margin-bottom: 0.7rem;
        color: #fff;
        letter-spacing: 0.5px;
    }

    /* Progress bar label */
    .progress-label {
        color: #ccc;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }

    /* Score card */
    .score-card {
        background: linear-gradient(135deg, #1a1a2e, #0f3460);
        border: 2px solid #e94560;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        color: white;
    }
    .score-number {
        font-size: 4rem;
        font-weight: 900;
        color: #e94560;
    }
    .score-label {
        font-size: 1.1rem;
        color: #aaa;
    }

    /* Result item */
    .result-correct {
        background: rgba(39,174,96,0.15);
        border-left: 4px solid #27ae60;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        color: #eee;
        font-size: 0.9rem;
    }
    .result-wrong {
        background: rgba(231,76,60,0.15);
        border-left: 4px solid #e74c3c;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        color: #eee;
        font-size: 0.9rem;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #e94560, #533483);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(233,69,96,0.5);
    }

    /* Radio buttons */
    .stRadio > label { color: #ddd !important; font-size: 1rem; }
    div[data-testid="stRadio"] > div { gap: 0.5rem; }

    /* General text */
    .stMarkdown, p, label { color: #ddd; }
    h1,h2,h3 { color: white; }
</style>
""", unsafe_allow_html=True)


# ── Session State Init ────────────────────────────────────────────────────────
def init_state():
    if "started" not in st.session_state:
        st.session_state.started = False
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "selected" not in st.session_state:
        st.session_state.selected = None
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "finished" not in st.session_state:
        st.session_state.finished = False
    if "player_name" not in st.session_state:
        st.session_state.player_name = ""
    if "num_questions" not in st.session_state:
        st.session_state.num_questions = 5

init_state()


# ── Helper ────────────────────────────────────────────────────────────────────
def reset_quiz():
    for key in ["started","q_index","score","answers","questions","selected","answered","finished"]:
        if key in st.session_state:
            del st.session_state[key]
    init_state()

def get_grade(pct):
    if pct == 100: return "🏆 Perfect Score!", "#f1c40f"
    elif pct >= 80: return "🎉 Excellent!", "#27ae60"
    elif pct >= 60: return "👍 Good Job!", "#2980b9"
    elif pct >= 40: return "📚 Keep Practicing!", "#e67e22"
    else:           return "💪 Don't Give Up!", "#e74c3c"


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 1 — Welcome / Setup
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.started and not st.session_state.finished:
    st.markdown('<div class="app-title">🧠 QuizMaster</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Test your knowledge across multiple topics</div>', unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    name = st.text_input("👤 Enter your name", placeholder="e.g. Alex", max_chars=30)
    num_q = st.slider("📋 Number of questions", min_value=3, max_value=len(QUESTIONS), value=5, step=1)

    categories = list(set(q["category"] for q in QUESTIONS))
    chosen_cats = st.multiselect("🏷️ Filter by category (optional — leave blank for all)",
                                  options=categories, default=[])

    shuffle = st.checkbox("🔀 Shuffle questions", value=True)

    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Quiz"):
            if not name.strip():
                st.warning("Please enter your name to continue.")
            else:
                pool = [q for q in QUESTIONS if not chosen_cats or q["category"] in chosen_cats]
                if len(pool) == 0:
                    st.error("No questions available for selected categories.")
                else:
                    if shuffle:
                        random.shuffle(pool)
                    st.session_state.questions = pool[:num_q]
                    st.session_state.player_name = name.strip()
                    st.session_state.num_questions = num_q
                    st.session_state.started = True
                    st.rerun()

    # Stats preview
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("📚 Total Questions", len(QUESTIONS))
    c2.metric("🏷️ Categories", len(categories))
    c3.metric("⏱️ Avg Time", "~5 min")


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 2 — Quiz
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.started and not st.session_state.finished:
    questions = st.session_state.questions
    idx = st.session_state.q_index
    total = len(questions)

    # Guard: all answered
    if idx >= total:
        st.session_state.finished = True
        st.rerun()

    q = questions[idx]

    # Header row
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f'<div class="progress-label">Question {idx+1} of {total}</div>', unsafe_allow_html=True)
        st.progress((idx) / total)
    with col_b:
        st.metric("Score", f"{st.session_state.score}/{idx}")

    st.markdown("---")

    # Question card
    st.markdown(f"""
    <div class="question-box">
        <div class="category-badge">🏷️ {q['category']}</div><br>
        Q{idx+1}. {q['question']}
    </div>
    """, unsafe_allow_html=True)

    # Options
    selected = st.radio(
        "Choose your answer:",
        options=q["options"],
        key=f"radio_{idx}",
        index=None
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit Answer", disabled=(selected is None)):
            is_correct = selected == q["answer"]
            if is_correct:
                st.session_state.score += 1

            st.session_state.answers.append({
                "question": q["question"],
                "your_answer": selected,
                "correct_answer": q["answer"],
                "correct": is_correct,
                "category": q["category"]
            })
            st.session_state.q_index += 1

            if st.session_state.q_index >= total:
                st.session_state.finished = True

            st.rerun()

    # Quit button
    st.markdown("---")
    if st.button("🚪 Quit Quiz"):
        reset_quiz()
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 3 — Results
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.finished:
    score = st.session_state.score
    total = len(st.session_state.answers)
    pct = int((score / total) * 100) if total > 0 else 0
    grade_text, grade_color = get_grade(pct)
    name = st.session_state.player_name

    st.markdown('<div class="app-title">📊 Results</div>', unsafe_allow_html=True)

    # Score card
    st.markdown(f"""
    <div class="score-card">
        <div style="font-size:1.2rem; color:#aaa; margin-bottom:0.5rem;">Great effort, {name}!</div>
        <div class="score-number">{pct}%</div>
        <div style="font-size:1.5rem; font-weight:700; color:{grade_color}; margin:0.5rem 0;">{grade_text}</div>
        <div class="score-label">You got <b style="color:#e94560">{score}</b> out of <b style="color:#e94560">{total}</b> questions correct</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats columns
    c1, c2, c3 = st.columns(3)
    c1.metric("✅ Correct", score)
    c2.metric("❌ Wrong", total - score)
    c3.metric("🎯 Accuracy", f"{pct}%")

    st.markdown("---")

    # Answer review
    st.markdown("### 📝 Answer Review")
    for i, ans in enumerate(st.session_state.answers, 1):
        if ans["correct"]:
            st.markdown(f"""
            <div class="result-correct">
                <b>Q{i}.</b> {ans['question']}<br>
                ✅ Your answer: <b>{ans['your_answer']}</b>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-wrong">
                <b>Q{i}.</b> {ans['question']}<br>
                ❌ Your answer: <b>{ans['your_answer']}</b><br>
                ✅ Correct: <b>{ans['correct_answer']}</b>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Category breakdown
    st.markdown("### 📊 Performance by Category")
    cat_stats = {}
    for ans in st.session_state.answers:
        cat = ans["category"]
        if cat not in cat_stats:
            cat_stats[cat] = {"correct": 0, "total": 0}
        cat_stats[cat]["total"] += 1
        if ans["correct"]:
            cat_stats[cat]["correct"] += 1

    for cat, stats in cat_stats.items():
        cat_pct = int((stats["correct"] / stats["total"]) * 100)
        st.markdown(f"**{cat}** — {stats['correct']}/{stats['total']} ({cat_pct}%)")
        st.progress(cat_pct / 100)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Play Again"):
            reset_quiz()
            st.rerun()
    with col2:
        if st.button("🏠 Change Settings"):
            reset_quiz()
            st.rerun()

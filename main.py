"""
Streamlit landing page UI — "Quiz Maker from PDF"
Matches the reference design (upload box, red CTA, trust line, social proof)
but without the top navigation bar.

Run with:
    pip install streamlit
    streamlit run landing.py
"""

import streamlit as st

st.set_page_config(page_title="PDFQuiz — Quiz Maker from PDF", page_icon="📄", layout="centered")

# =====================================================================
# STYLES
# =====================================================================
st.markdown(
    """
    <style>
        /* Hide default Streamlit chrome */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .block-container {
            padding-top: 4rem;
            max-width: 760px;
        }

        .wordmark {
            font-size: 1.4rem;
            font-weight: 800;
            color: #111111;
            margin-bottom: 2.5rem;
            text-align: left;
        }

        .hero-title {
            text-align: center;
            font-size: 3.2rem;
            font-weight: 700;
            color: #111111;
            line-height: 1.1;
            margin-bottom: 0.6rem;
        }

        .hero-subtitle {
            text-align: center;
            font-size: 1.15rem;
            color: #6b7280;
            margin-bottom: 2.5rem;
        }

        /* Upload dropzone look */
        .upload-box {
            border: 2px dashed #d1d5db;
            border-radius: 14px;
            background-color: #fafafa;
            padding: 3rem 2rem;
            text-align: center;
            margin-bottom: 1.5rem;
        }

        .upload-icons {
            font-size: 2rem;
            margin-bottom: 0.8rem;
        }

        .upload-text {
            color: #6b7280;
            font-size: 1rem;
            margin-bottom: 0.2rem;
        }

        .upload-subtext {
            color: #9ca3af;
            font-size: 0.85rem;
            margin-bottom: 1.2rem;
        }

        div[data-testid="stFileUploaderDropzone"] {
            background-color: transparent;
            border: none;
        }

        /* Red primary buttons */
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

        .trust-line {
            text-align: center;
            color: #6b7280;
            font-size: 0.85rem;
            margin-top: 1.2rem;
            margin-bottom: 3.5rem;
        }

        .social-proof-heading {
            text-align: center;
            font-size: 2.4rem;
            font-weight: 800;
            color: #111111;
            margin-bottom: 1rem;
        }

        .social-proof-line {
            text-align: center;
            color: #6b7280;
            font-size: 0.95rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# SESSION STATE
# =====================================================================
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# =====================================================================
# WORDMARK (no nav links, per request)
# =====================================================================
st.markdown('<div class="wordmark">PDFQuiz</div>', unsafe_allow_html=True)

# =====================================================================
# HERO
# =====================================================================
st.markdown('<div class="hero-title">Quiz Maker from PDF</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Upload a PDF and generate a quiz using AI</div>', unsafe_allow_html=True)

# =====================================================================
# UPLOAD BOX
# =====================================================================
st.markdown(
    """
    <div class="upload-box">
        <div class="upload-icons">📄 → 📋</div>
        <div class="upload-text">Click to upload or drag and drop</div>
        <div class="upload-subtext">PDF (MAX. 10MB)</div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"],
    label_visibility="collapsed",
)
st.session_state.uploaded_file = uploaded_file

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# CTA BUTTON
# =====================================================================
clicked = st.button("Convert PDF to Quiz →", type="primary", use_container_width=True)

if clicked:
    if st.session_state.uploaded_file is None:
        st.warning("Please upload a PDF first.")
    else:
        st.success(f"Got it! '{st.session_state.uploaded_file.name}' is ready to be converted.")
        # Hook up your quiz-generation flow / backend call here.

# =====================================================================
# TRUST LINE
# =====================================================================
st.markdown(
    '<div class="trust-line">🛡️ Your files will be securely handled by PDF2Quiz servers and deleted after the quiz creation.</div>',
    unsafe_allow_html=True,
)

# =====================================================================
# SOCIAL PROOF
# =====================================================================
st.markdown('<div class="social-proof-heading">Students ❤️ it</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="social-proof-line">Join 100,000+ students and professionals using AI to verify their knowledge!</div>',
    unsafe_allow_html=True,
)

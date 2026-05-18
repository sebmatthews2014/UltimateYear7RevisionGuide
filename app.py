import json
import os
import random
import re
from fractions import Fraction

import streamlit as st

st.set_page_config(page_title="Ultimate Year 7 Revision Guide", page_icon="🧠", layout="centered")

QUESTION_FILES = [
    "questions.json",
    "maths_questions.json",
    os.path.join("data", "questions.json"),
    os.path.join("data", "maths_questions.json"),
]

BBC_BITESIZE_LINKS = {
    "Maths": "https://www.bbc.co.uk/bitesize/subjects/zqhs34j",
    "Religious Education": "https://www.bbc.co.uk/bitesize/subjects/z7hs34j",
}

st.markdown(
    """
    <style>
    .stApp { background: #f7f8fb; }
    .block-container { max-width: 920px; padding-top: 1.4rem; }
    h1, h2, h3 { color: #172033; }
    div[data-testid="stRadio"] label, div[data-testid="stCheckbox"] label {
        color: #172033 !important;
        font-size: 1rem !important;
        line-height: 1.35 !important;
        white-space: normal !important;
        overflow: visible !important;
    }
    div[role="radiogroup"] > label, div[data-testid="stCheckbox"] > label {
        background: #ffffff;
        border: 1px solid #d9dee8;
        border-radius: 14px;
        padding: 0.65rem 0.8rem;
        margin: 0.35rem 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .stButton button {
        background: #1f4fd8 !important;
        color: #ffffff !important;
        border-radius: 999px !important;
        border: 0 !important;
        padding: 0.55rem 1rem !important;
        font-weight: 700 !important;
    }
    .secondary button { background: #ffffff !important; color: #1f2937 !important; border: 1px solid #d9dee8 !important; }
    .question-card {
        background: #ffffff;
        border: 1px solid #d9dee8;
        border-radius: 22px;
        padding: 1.15rem;
        box-shadow: 0 8px 22px rgba(23,32,51,0.08);
        margin-bottom: 1rem;
    }
    .meta-pill {
        display: inline-block;
        background: #eef3ff;
        color: #1f4fd8;
        border-radius: 999px;
        padding: 0.2rem 0.55rem;
        margin: 0.1rem 0.2rem 0.1rem 0;
        font-size: 0.78rem;
        font-weight: 700;
    }
    .goblin-box {
        background: #fff7dc;
        border: 1px solid #f5d36b;
        border-radius: 18px;
        padding: 1rem;
        color: #3b2f00;
        font-weight: 650;
    }
    @media (max-width: 640px) {
        .block-container { padding-left: 0.85rem; padding-right: 0.85rem; }
        .question-card { padding: 0.9rem; border-radius: 18px; }
        div[data-testid="stRadio"] label { font-size: 0.98rem !important; }
        .stButton button { width: 100%; margin-top: 0.25rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_questions():
    loaded = []
    seen_ids = set()
    for path in QUESTION_FILES:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    data = data.get("questions", [])
                for q in data:
                    qid = q.get("id") or f"generated_{len(loaded)+1}"
                    if qid in seen_ids:
                        qid = f"{qid}_{len(seen_ids)+1}"
                    q["id"] = qid
                    loaded.append(q)
                    seen_ids.add(qid)
            except Exception as exc:
                st.warning(f"Could not load {path}: {exc}")
    return loaded


def clean_answer(value):
    value = str(value).strip().lower()
    value = value.replace("£", "").replace("cm²", "").replace("cm2", "").replace("degrees", "").replace("°", "")
    value = value.replace(" ", "")
    value = value.replace("−", "-")
    return value


def as_number(value):
    value = clean_answer(value).replace("%", "")
    try:
        if "/" in value:
            return float(Fraction(value))
        return float(value)
    except Exception:
        return None


def is_correct(user_answer, question):
    if user_answer is None:
        return False
    possible = question.get("acceptable_answers") or [question.get("answer", "")]
    user_clean = clean_answer(user_answer)

    for ans in possible:
        ans_clean = clean_answer(ans)
        if user_clean == ans_clean:
            return True
        user_num = as_number(user_answer)
        ans_num = as_number(ans)
        if user_num is not None and ans_num is not None and abs(user_num - ans_num) < 1e-9:
            return True

    return False


def reset_quiz():
    for key in ["quiz_questions", "current", "score", "answered", "last_correct", "user_answer"]:
        st.session_state.pop(key, None)


all_questions = load_questions()

st.title("🧠 Ultimate Year 7 Revision Guide")
st.caption("Small chunks. Big progress. Mildly terrified goblins optional.")

subjects = sorted(set(q.get("subject", "General") for q in all_questions))
subject = st.sidebar.selectbox("Subject", subjects if subjects else ["Maths"])

subject_questions = [q for q in all_questions if q.get("subject", "General") == subject]
units = ["All"] + sorted(set(q.get("unit", "General") for q in subject_questions))
unit = st.sidebar.selectbox("Unit", units)

available_questions = subject_questions if unit == "All" else [q for q in subject_questions if q.get("unit") == unit]

if subject in BBC_BITESIZE_LINKS:
    st.sidebar.link_button("BBC Bitesize revision", BBC_BITESIZE_LINKS[subject])

st.sidebar.markdown(f"**Available questions:** {len(available_questions)}")

if not available_questions:
    st.markdown(
        """
        <div class="goblin-box">
        The revision goblins are still building questions for this section. They are tiny, dramatic, and unionised.
        Try another subject or topic for now.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

max_q = len(available_questions)
default_q = min(10, max_q)
number_of_questions = st.sidebar.slider("How many questions?", min_value=1, max_value=max_q, value=default_q)

if st.sidebar.button("Start / restart quiz"):
    reset_quiz()
    st.session_state.quiz_questions = random.sample(available_questions, number_of_questions)
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.answered = False

if "quiz_questions" not in st.session_state:
    st.info("Choose your subject and press **Start / restart quiz**. Future-you will be annoyingly grateful.")
    st.stop()

quiz_questions = st.session_state.quiz_questions
current_index = st.session_state.current

if current_index >= len(quiz_questions):
    st.success(f"Quiz complete! You scored {st.session_state.score} out of {len(quiz_questions)}.")
    if st.button("Restart quiz"):
        reset_quiz()
        st.rerun()
    st.stop()

q = quiz_questions[current_index]
progress = (current_index + 1) / len(quiz_questions)
st.progress(progress)
st.write(f"Question {current_index + 1} of {len(quiz_questions)}")

st.markdown(
    f"""
    <div class="question-card">
        <span class="meta-pill">{q.get('unit', 'General')}</span>
        <span class="meta-pill">{q.get('topic', 'Topic')}</span>
        <span class="meta-pill">{q.get('sparx_code', '')}</span>
        <h3>{q.get('question', '')}</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

qtype = q.get("question_type", "short_answer")
answer_key = f"answer_{q.get('id')}"

if qtype == "multiple_choice":
    choices = q.get("choices", [])
    user_answer = st.radio("Choose one answer:", choices, key=answer_key, index=None)
elif qtype == "true_false":
    user_answer = st.radio("Choose one answer:", ["True", "False"], key=answer_key, index=None)
else:
    user_answer = st.text_input("Type your answer:", key=answer_key, placeholder="Example: 12, 3/4, £4.50, 7x")

col1, col2 = st.columns(2)
with col1:
    submit = st.button("Check answer")
with col2:
    skip = st.button("Skip")

if submit and not st.session_state.get("answered", False):
    correct = is_correct(user_answer, q)
    st.session_state.answered = True
    st.session_state.last_correct = correct
    if correct:
        st.session_state.score += 1

if skip:
    st.session_state.answered = True
    st.session_state.last_correct = False

if st.session_state.get("answered", False):
    if st.session_state.get("last_correct"):
        st.success("Correct. Lovely stuff.")
    else:
        st.error(f"Not quite. Correct answer: {q.get('answer')}")

    if q.get("working"):
        st.markdown(f"**Working:** {q.get('working')}")

    if st.button("Next question"):
        st.session_state.current += 1
        st.session_state.answered = False
        st.rerun()

st.sidebar.markdown(f"**Score:** {st.session_state.get('score', 0)}")

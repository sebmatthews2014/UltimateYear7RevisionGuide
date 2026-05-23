import streamlit as st
import random
import json
import os
import re
import html
from fractions import Fraction

st.set_page_config(
    page_title="Ultimate Year 7 Revision Guide",
    page_icon="✏️",
    layout="centered"
)

QUESTIONS_FOLDER = "questions"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Nunito:wght@500;700;900&display=swap');

    .stApp {
        background:
            linear-gradient(rgba(255,255,255,0.78), rgba(255,255,255,0.78)),
            repeating-linear-gradient(0deg, #fffdf5, #fffdf5 28px, #dbeafe 29px);
        color: #1f2937;
        font-family: 'Nunito', sans-serif;
        overflow-x: hidden;
    }

    .main .block-container {
        max-width: 920px;
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        overflow-x: hidden;
    }

    .hero-card {
        background: #fffaf0;
        padding: 2rem 2.2rem;
        border-radius: 26px;
        border: 3px solid #111827;
        box-shadow: 8px 8px 0px #111827;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-family: 'Patrick Hand', cursive;
        font-size: clamp(2.1rem, 7vw, 3.2rem);
        font-weight: 900;
        color: #1e3a8a;
        margin-bottom: 0.8rem;
        line-height: 1.05;
        overflow-wrap: anywhere;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        color: #374151;
        line-height: 1.5;
        max-width: 720px;
    }

    .easter-egg-card, .empty-card {
        background: #fef3c7;
        padding: 1.4rem;
        border-radius: 22px;
        border: 3px dashed #111827;
        box-shadow: 6px 6px 0px #111827;
        margin-bottom: 1.5rem;
        font-size: 1.1rem;
    }

    .easter-title, .empty-title {
        font-family: 'Patrick Hand', cursive;
        font-size: 2rem;
        color: #7c2d12;
        font-weight: 900;
        margin-bottom: 0.4rem;
    }

    .question-card {
        background: #ffffff;
        padding: 1rem;
        border-radius: 22px;
        border: 3px solid #111827;
        box-shadow: 5px 5px 0px #111827;
        margin-top: 0.5rem;
        margin-bottom: 0.7rem;
        overflow-wrap: anywhere;
    }

    .question-text {
        font-family: 'Patrick Hand', cursive;
        font-size: 1.85rem;
        color: #111827;
        margin-top: 0.25rem;
        margin-bottom: 0.45rem;
        line-height: 1.12;
        overflow-wrap: anywhere;
    }

    .subject-pill {
        display: inline-block;
        background: #bfdbfe;
        color: #1e3a8a;
        padding: 0.4rem 0.8rem;
        border-radius: 999px;
        font-weight: 900;
        border: 2px solid #111827;
        box-shadow: 3px 3px 0px #111827;
        font-size: 0.9rem;
        max-width: 100%;
        white-space: normal;
    }

    .subject-art-card {
        background: #ffffff;
        padding: 0.65rem 0.9rem;
        border-radius: 18px;
        border: 3px solid #111827;
        box-shadow: 4px 4px 0px #111827;
        margin-bottom: 0.45rem;
        font-size: 1.1rem;
        font-weight: 900;
    }

    .score-box {
        background: #fef3c7;
        padding: 0.55rem;
        border-radius: 14px;
        border: 2px dashed #92400e;
        font-weight: 900;
        color: #78350f;
        text-align: center;
        margin-top: 0.45rem;
    }

    .result-good {
        background: #dcfce7;
        color: #14532d;
        padding: 0.6rem 0.7rem;
        margin-top: 0.35rem;
        margin-bottom: 0.35rem;
        border-radius: 14px;
        border: 2px solid #14532d;
        box-shadow: 3px 3px 0px #14532d;
        font-weight: 900;
        line-height: 1.2;
    }

    .result-bad {
        background: #ffe4e6;
        color: #9f1239;
        padding: 0.6rem 0.7rem;
        margin-top: 0.35rem;
        margin-bottom: 0.35rem;
        border-radius: 14px;
        border: 2px solid #9f1239;
        box-shadow: 3px 3px 0px #9f1239;
        font-weight: 900;
        line-height: 1.2;
    }

    .review-card-bad {
        background: #ffe4e6;
        border: 2px solid #9f1239;
        box-shadow: 3px 3px 0px #9f1239;
        border-radius: 14px;
        padding: 0.7rem 0.85rem;
        margin-bottom: 0.7rem;
    }

    .review-question {
        font-weight: 900;
        font-size: 0.98rem;
        margin-bottom: 0.35rem;
        line-height: 1.2;
    }

    .review-card-bad p {
        margin: 0.2rem 0;
        font-size: 0.92rem;
        line-height: 1.25;
    }

    .review-meta {
        color: #6b7280;
        font-size: 0.78rem;
        margin-top: 0.4rem;
        margin-bottom: 0;
    }

    div.stButton {
        margin-top: 0.15rem;
        margin-bottom: 0.15rem;
    }

    div.stButton > button {
        border-radius: 16px !important;
        border: 3px solid #111827 !important;
        box-shadow: 3px 3px 0px #111827 !important;
        font-weight: 900 !important;
        font-size: 0.98rem !important;
        transition: all 0.1s ease-in-out !important;
        background: #facc15 !important;
        color: #111827 !important;
        min-height: 40px;
        padding-top: 0.45rem !important;
        padding-bottom: 0.45rem !important;
    }

    div.stButton > button:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #111827 !important;
    }

    div.stButton > button:not([kind="primary"]) {
        background: #ffffff !important;
        color: #111827 !important;
    }

    /* Keeps the quiz mode radio buttons visible and readable */
    .stRadio > div {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        background: transparent;
        padding: 0;
        border: none;
    }

    .stRadio label {
        background: #ffffff !important;
        border: 3px solid #111827 !important;
        border-radius: 14px !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 3px 3px 0px #111827 !important;
        cursor: pointer;
        transition: all 0.1s ease-in-out;
        color: #111827 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    .stRadio label:hover {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0px #111827 !important;
        background: #fef3c7 !important;
    }

    .stRadio label p,
    .stRadio label span,
    .stRadio label div,
    .stRadio [data-testid="stMarkdownContainer"] p {
        color: #111827 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        opacity: 1 !important;
        visibility: visible !important;
        line-height: 1.35 !important;
    }

    .answer-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 0.35rem;
        margin-top: 0.35rem;
        margin-bottom: 0.4rem;
    }

    .answer-card button {
        width: 100%;
        min-height: 42px;
        text-align: left !important;
        white-space: normal !important;
        line-height: 1.18 !important;
        background: #ffffff !important;
        padding: 0.5rem 0.7rem !important;
    }

    .footer-note {
        font-family: 'Patrick Hand', cursive;
        color: #4b5563;
        font-size: 1.15rem;
        text-align: center;
        margin-top: 1.5rem;
    }

    @media (max-width: 700px) {
        .main .block-container {
            padding-left: 0.75rem;
            padding-right: 0.75rem;
            padding-top: 0.75rem;
        }

        .hero-card {
            padding: 1.2rem;
            border-radius: 20px;
            box-shadow: 5px 5px 0px #111827;
            margin-bottom: 1rem;
        }

        .hero-title {
            font-size: 2rem;
            line-height: 1.05;
        }

        .hero-subtitle {
            font-size: 0.95rem;
        }

        .question-card {
            padding: 0.75rem;
            border-radius: 16px;
            box-shadow: 3px 3px 0px #111827;
            margin-top: 0.35rem;
            margin-bottom: 0.45rem;
        }

        .question-text {
            font-size: 1.42rem;
            line-height: 1.08;
            margin-top: 0.15rem;
            margin-bottom: 0.3rem;
        }

        .subject-art-card {
            padding: 0.5rem 0.75rem;
            font-size: 0.98rem;
            border-radius: 15px;
            box-shadow: 3px 3px 0px #111827;
            margin-bottom: 0.3rem;
        }

        .answer-grid {
            gap: 0.25rem;
            margin-top: 0.25rem;
            margin-bottom: 0.25rem;
        }

        .answer-card button,
        div.stButton > button {
            width: 100%;
            min-height: 38px;
            padding-top: 0.38rem !important;
            padding-bottom: 0.38rem !important;
        }

        .result-good,
        .result-bad {
            padding: 0.5rem 0.6rem;
            margin-top: 0.25rem;
            margin-bottom: 0.25rem;
            border-radius: 12px;
            box-shadow: 2px 2px 0px currentColor;
        }

        .score-box {
            padding: 0.45rem;
            margin-top: 0.3rem;
        }

        .easter-egg-card, .empty-card {
            padding: 1rem;
            font-size: 0.95rem;
            box-shadow: 4px 4px 0px #111827;
        }

        .review-card-bad {
            padding: 0.9rem;
            box-shadow: 3px 3px 0px #111827;
        }
    }
</style>
""", unsafe_allow_html=True)

SUBJECT_EMOJIS = {
    "Religious Education": "🕊️",
    "Maths": "➗",
    "Science": "🔬",
    "History": "🏰",
    "Geography": "🌍",
    "IT": "💻",
    "Computer Science": "💻",
    "Spanish": "🇪🇸",
    "General": "📘",
    "All Subjects": "🎯",
    "Custom": "🧩"
}

SUBJECT_ART = {
    "Religious Education": "🕊️✨",
    "Maths": "➗📐",
    "Science": "🔬🧪",
    "History": "🏰📜",
    "Geography": "🌍🧭",
    "IT": "💻🤖",
    "Computer Science": "💻🤖",
    "Spanish": "🇪🇸💃",
    "General": "📘✨",
    "All Subjects": "🎯📚",
    "Custom": "🧩📚"
}


def safe_text(value):
    return html.escape(str(value))


def normalise_subject(subject):
    if subject == "Computer Science":
        return "IT"
    return subject or "General"


def add_question_to_bank(question_bank, question):
    subject = normalise_subject(question.get("subject", "General"))
    topic = question.get("topic") or question.get("unit") or "General"

    cleaned_question = question.copy()
    cleaned_question.pop("subject", None)
    cleaned_question.pop("topic", None)

    if subject not in question_bank:
        question_bank[subject] = {}

    if topic not in question_bank[subject]:
        question_bank[subject][topic] = []

    question_bank[subject][topic].append(cleaned_question)


def load_question_bank():
    question_bank = {}

    if not os.path.exists(QUESTIONS_FOLDER):
        st.error("I cannot find the 'questions' folder.")
        return {}

    for filename in os.listdir(QUESTIONS_FOLDER):
        if filename.endswith(".json"):
            file_path = os.path.join(QUESTIONS_FOLDER, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                if isinstance(data, dict):
                    subject = normalise_subject(data.get("subject"))
                    topics = data.get("topics", {})

                    if subject and isinstance(topics, dict):
                        if subject not in question_bank:
                            question_bank[subject] = {}

                        for topic_name, topic_questions in topics.items():
                            if topic_name not in question_bank[subject]:
                                question_bank[subject][topic_name] = []

                            question_bank[subject][topic_name].extend(topic_questions)

                elif isinstance(data, list):
                    for question in data:
                        if isinstance(question, dict):
                            add_question_to_bank(question_bank, question)

            except Exception as error:
                st.error(f"Problem loading {filename}: {error}")

    return question_bank


QUESTION_BANK = load_question_bank()

defaults = {
    "quiz_started": False,
    "questions": [],
    "current_question": 0,
    "score": 0,
    "answered": False,
    "selected_answer": "",
    "results": [],
    "show_easter_egg": False,
    "review_wrong_answers": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def get_questions(subject):
    questions = []

    if subject == "All Subjects":
        for subject_name, topics in QUESTION_BANK.items():
            for topic_name, topic_questions in topics.items():
                for question in topic_questions:
                    new_question = question.copy()
                    new_question["subject"] = subject_name
                    new_question["topic"] = topic_name
                    questions.append(new_question)
    else:
        if subject not in QUESTION_BANK:
            return []

        for topic_name, topic_questions in QUESTION_BANK[subject].items():
            for question in topic_questions:
                new_question = question.copy()
                new_question["subject"] = subject
                new_question["topic"] = topic_name
                questions.append(new_question)

    return questions


def get_custom_questions(subjects):
    questions = []

    for subject in subjects:
        questions.extend(get_questions(subject))

    return questions


def prepare_question(question):
    prepared = question.copy()
    options = prepared.get("options", []).copy()
    random.shuffle(options)
    prepared["shuffled_options"] = options

    if options:
        prepared["question_type"] = prepared.get("question_type", "multiple_choice")
    else:
        prepared["question_type"] = prepared.get("question_type", "short_answer")

    return prepared


def start_quiz(available_questions, number_of_questions):
    random.shuffle(available_questions)

    selected_questions = available_questions[:number_of_questions]
    prepared_questions = [prepare_question(q) for q in selected_questions]

    st.session_state.questions = prepared_questions
    st.session_state.quiz_started = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_answer = ""
    st.session_state.results = []
    st.session_state.review_wrong_answers = False


def reset_quiz():
    keep_easter_egg = st.session_state.show_easter_egg

    for key, value in defaults.items():
        st.session_state[key] = value

    st.session_state.show_easter_egg = keep_easter_egg


def normalise_text(value):
    value = str(value).strip().lower()
    value = value.replace("−", "-")
    value = value.replace("£", "")
    value = value.replace(",", "")
    value = re.sub(r"\s+", "", value)
    return value


def as_number(value):
    value = normalise_text(value)

    try:
        if "/" in value:
            return float(Fraction(value))
        return float(value)
    except Exception:
        return None


def answer_is_correct(question, selected_answer):
    possible_answers = [question.get("answer", "")]
    possible_answers.extend(question.get("acceptable_answers", []))

    selected_normalised = normalise_text(selected_answer)

    for possible_answer in possible_answers:
        if selected_normalised == normalise_text(possible_answer):
            return True

        selected_number = as_number(selected_answer)
        possible_number = as_number(possible_answer)

        if selected_number is not None and possible_number is not None:
            if abs(selected_number - possible_number) < 0.000001:
                return True

    return False


def check_answer(question, selected_answer):
    correct = answer_is_correct(question, selected_answer)

    if correct:
        st.session_state.score += 1

    st.session_state.results.append({
        "subject": question["subject"],
        "topic": question["topic"],
        "question": question["question"],
        "selected": selected_answer,
        "correct_answer": question["answer"],
        "working": question.get("working", ""),
        "was_correct": correct
    })

    st.session_state.answered = True
    st.session_state.selected_answer = selected_answer


def next_question():
    st.session_state.current_question += 1
    st.session_state.answered = False
    st.session_state.selected_answer = ""


def toggle_easter_egg():
    st.session_state.show_easter_egg = not st.session_state.show_easter_egg


st.button("✏️", key="secret_pencil", on_click=toggle_easter_egg)

st.markdown("""
<div class="hero-card">
    <div class="hero-title">
        Ultimate Year 7 Revision Guide
    </div>
    <div class="hero-subtitle">
        Pick a subject, answer quick questions, and slowly defeat the revision goblin.
        Hand-drawn vibes. Serious learning. Minimal panic.
    </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.show_easter_egg:
    st.markdown("""
<div class="easter-egg-card">
    <div class="easter-title">✨ Secret unlocked ✨</div>
    <p>This app was built by <strong>Seb Matthews</strong>.</p>
    <p>Peak coder energy.</p>
    <p>The revision goblin got cooked.</p>
</div>
""", unsafe_allow_html=True)

if not QUESTION_BANK:
    st.warning("No questions loaded.")
    st.stop()

if not st.session_state.quiz_started:

    st.subheader("Start a new quiz")

    subject_names = list(QUESTION_BANK.keys())

    quiz_mode = st.radio(
        "Choose quiz mode",
        ["All Subjects", "Single Subject", "Custom"],
        horizontal=True
    )

    selected_subject = None
    selected_subjects = []

    if quiz_mode == "All Subjects":
        selected_subject = "All Subjects"
        selected_subjects = subject_names
        available_questions = get_questions("All Subjects")
        display_name = "All Subjects"

    elif quiz_mode == "Single Subject":
        selected_subject = st.selectbox("Choose a subject", subject_names)
        selected_subjects = [selected_subject]
        available_questions = get_questions(selected_subject)
        display_name = selected_subject

    else:
        selected_subjects = st.multiselect(
            "Choose the subjects you want in your custom quiz",
            subject_names,
            default=subject_names[:2] if len(subject_names) >= 2 else subject_names
        )

        available_questions = get_custom_questions(selected_subjects)
        display_name = "Custom"

    subject_art = SUBJECT_ART.get(display_name, "📘✨")

    if quiz_mode == "Custom":
        chosen_text = ", ".join(selected_subjects) if selected_subjects else "No subjects selected yet"

        st.markdown(f"""
<div class="subject-art-card">
    {subject_art} Custom revision: {safe_text(chosen_text)}
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div class="subject-art-card">
    {subject_art} {safe_text(display_name)} revision
</div>
""", unsafe_allow_html=True)

    st.write(f"Available questions: **{len(available_questions)}**")

    if quiz_mode == "Custom" and len(selected_subjects) == 0:
        st.markdown("""
<div class="empty-card">
    <div class="empty-title">🧩 Pick your subjects...</div>
    <p>
        Choose at least one subject for your custom quiz.
        The goblin cannot revise thin air, despite several confident attempts.
    </p>
</div>
""", unsafe_allow_html=True)

    elif len(available_questions) == 0:
        st.markdown("""
<div class="empty-card">
    <div class="empty-title">🛠️ Questions coming soon...</div>
    <p>
        The revision goblins are still building this subject’s question bank.
        They are very small, mildly chaotic, and currently arguing over snacks.
    </p>
    <p>
        Try another subject for now. This one is still under construction.
    </p>
</div>
""", unsafe_allow_html=True)

    elif len(available_questions) == 1:
        number_of_questions = 1
        st.info("Only 1 question available. The goblins have made a start. Barely.")

        if st.button("Start Quiz", type="primary"):
            start_quiz(available_questions, number_of_questions)
            st.rerun()

    else:
        number_of_questions = st.slider(
            "How many questions?",
            min_value=1,
            max_value=len(available_questions),
            value=min(10, len(available_questions))
        )

        st.info("Choose as many questions as you want. If you want anything added, let me know!")

        if st.button("Start Quiz", type="primary"):
            start_quiz(available_questions, number_of_questions)
            st.rerun()

else:

    total_questions = len(st.session_state.questions)
    current_index = st.session_state.current_question

    if current_index < total_questions:

        question = st.session_state.questions[current_index]

        st.progress(current_index / total_questions)
        st.caption(f"Question {current_index + 1} of {total_questions}")

        subject_art = SUBJECT_ART.get(question["subject"], "📘✨")

        st.markdown(f"""
<div class="subject-art-card">
    {subject_art} {safe_text(question['subject'])} revision
</div>
""", unsafe_allow_html=True)

        st.markdown(
            f'<div class="question-text">{safe_text(question["question"])}</div>',
            unsafe_allow_html=True
        )

        if question.get("question_type") == "multiple_choice" and question.get("shuffled_options"):
            st.markdown('<div class="answer-grid">', unsafe_allow_html=True)
            for option_index, option in enumerate(question["shuffled_options"]):
                st.markdown('<div class="answer-card">', unsafe_allow_html=True)
                if st.button(
                    option,
                    key=f"answer_{current_index}_{option_index}",
                    disabled=st.session_state.answered,
                    use_container_width=True
                ):
                    check_answer(question, option)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            selected_answer = st.text_input(
                "Type your answer:",
                key=f"typed_question_{current_index}",
                disabled=st.session_state.answered,
                placeholder="Type your answer here"
            )

            if not st.session_state.answered:
                if st.button("Check Answer", type="primary"):
                    if str(selected_answer).strip() == "":
                        st.warning("Type an answer first. The goblin refuses to mark invisible maths.")
                    else:
                        check_answer(question, selected_answer)
                        st.rerun()

        if st.session_state.answered:

            latest_result = st.session_state.results[-1]

            if latest_result["was_correct"]:
                st.markdown(
                    '<div class="result-good">✅ Correct! That one has entered the brain vault.</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="result-bad">❌ Not quite. Correct answer: {safe_text(question["answer"])}</div>',
                    unsafe_allow_html=True
                )

            if question.get("working"):
                st.info(f"Working: {question['working']}")

            if st.button("Next Question"):
                next_question()
                st.rerun()

        answered_count = current_index + (1 if st.session_state.answered else 0)

        st.markdown(
            f'<div class="score-box">Current score: {st.session_state.score} / {answered_count}</div>',
            unsafe_allow_html=True
        )

        if st.button("Restart Quiz"):
            reset_quiz()
            st.rerun()

    else:

        score = st.session_state.score
        percentage = round((score / total_questions) * 100)

        st.markdown('<div class="question-card">', unsafe_allow_html=True)

        st.progress(1.0)

        st.header("Quiz complete!")
        st.subheader(f"Final score: {score} / {total_questions}")
        st.subheader(f"Percentage: {percentage}%")

        if percentage >= 80:
            st.success("Excellent work. The exam goblin has backed away slowly.")
        elif percentage >= 60:
            st.info("Good effort. A few more rounds and you’ll be dangerous.")
        else:
            st.warning("Keep going. The knowledge is loading... like school Wi-Fi.")

        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("New Quiz", type="primary", use_container_width=True):
                reset_quiz()
                st.rerun()

        with col2:
            if st.button("Review Only Wrong Answers", use_container_width=True):
                st.session_state.review_wrong_answers = True
                st.rerun()

        if st.session_state.review_wrong_answers:
            wrong_answers = [
                result for result in st.session_state.results
                if not result["was_correct"]
            ]

            if len(wrong_answers) == 0:
                st.success("You got everything correct. The goblin is furious.")
            else:
                st.subheader("Questions to revise")

                for i, result in enumerate(wrong_answers, start=1):
                    subject_art = SUBJECT_ART.get(result["subject"], "📘✨")

                    working_line = ""
                    if result.get("working"):
                        working_line = f"<p><strong>Working:</strong> {safe_text(result['working'])}</p>"

                    card_html = f"""
<div class="review-card-bad">
<div class="review-question">❌ {i}. {safe_text(result['question'])}</div>
<p><strong>Your answer:</strong> {safe_text(result['selected'])}</p>
<p><strong>Correct answer:</strong> {safe_text(result['correct_answer'])}</p>
{working_line}
<p class="review-meta">{subject_art} {safe_text(result['subject'])} | {safe_text(result['topic'])}</p>
</div>
"""

                    st.markdown(card_html, unsafe_allow_html=True)

st.markdown(
    '<div class="footer-note">Built for revision.</div>',
    unsafe_allow_html=True
)

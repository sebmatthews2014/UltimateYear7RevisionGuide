import streamlit as st
import random
import json
import os

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
            repeating-linear-gradient(
                0deg,
                #fffdf5,
                #fffdf5 28px,
                #dbeafe 29px
            );
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

    .easter-egg-card {
        background: #fef3c7;
        padding: 1.4rem;
        border-radius: 22px;
        border: 3px dashed #111827;
        box-shadow: 6px 6px 0px #111827;
        margin-bottom: 1.5rem;
        font-size: 1.1rem;
    }

    .easter-title {
        font-family: 'Patrick Hand', cursive;
        font-size: 2rem;
        color: #7c2d12;
        font-weight: 900;
        margin-bottom: 0.4rem;
    }

    .question-card {
        background: #ffffff;
        padding: 1.8rem;
        border-radius: 24px;
        border: 3px solid #111827;
        box-shadow: 7px 7px 0px #111827;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        overflow-wrap: anywhere;
    }

    .question-text {
        font-family: 'Patrick Hand', cursive;
        font-size: 2rem;
        color: #111827;
        margin-top: 1rem;
        margin-bottom: 1rem;
        line-height: 1.2;
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

    .score-box {
        background: #fef3c7;
        padding: 1rem;
        border-radius: 18px;
        border: 2px dashed #92400e;
        font-weight: 900;
        color: #78350f;
        text-align: center;
        margin-top: 1rem;
    }

    .result-good {
        background: #dcfce7;
        color: #14532d;
        padding: 1rem;
        border-radius: 18px;
        border: 2px solid #14532d;
        box-shadow: 4px 4px 0px #14532d;
        font-weight: 900;
    }

    .result-bad {
        background: #ffe4e6;
        color: #9f1239;
        padding: 1rem;
        border-radius: 18px;
        border: 2px solid #9f1239;
        box-shadow: 4px 4px 0px #9f1239;
        font-weight: 900;
    }

    div.stButton > button {
        border-radius: 18px;
        border: 3px solid #111827;
        box-shadow: 4px 4px 0px #111827;
        font-weight: 900;
        font-size: 1rem;
        transition: all 0.1s ease-in-out;
    }

    div.stButton > button:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #111827;
    }

    div.stButton > button[kind="primary"] {
        background: #facc15;
        color: #111827;
    }

    .stRadio > div {
        background: #f9fafb;
        padding: 1rem;
        border-radius: 18px;
        border: 2px dashed #94a3b8;
        width: 100%;
    }

    label[data-baseweb="radio"] {
        white-space: normal !important;
        align-items: flex-start !important;
    }

    label[data-baseweb="radio"] div {
        white-space: normal !important;
        overflow-wrap: anywhere !important;
        word-break: normal !important;
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
            font-size: 2.15rem;
            line-height: 1.05;
        }

        .hero-subtitle {
            font-size: 0.95rem;
        }

        .question-card {
            padding: 1rem;
            border-radius: 18px;
            box-shadow: 4px 4px 0px #111827;
        }

        .question-text {
            font-size: 1.55rem;
            line-height: 1.15;
        }

        .stRadio > div {
            padding: 0.75rem;
        }

        div.stButton > button {
            width: 100%;
            min-height: 48px;
        }

        .easter-egg-card {
            padding: 1rem;
            font-size: 0.95rem;
            box-shadow: 4px 4px 0px #111827;
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
    "Spanish": "🇪🇸",
    "All Subjects": "🎯"
}


def load_question_bank():
    question_bank = {}

    if not os.path.exists(QUESTIONS_FOLDER):
        st.error("I cannot find the 'questions' folder. Make sure it is in the same folder as app.py.")
        return {}

    for filename in os.listdir(QUESTIONS_FOLDER):
        if filename.endswith(".json"):
            file_path = os.path.join(QUESTIONS_FOLDER, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                subject = data.get("subject")
                topics = data.get("topics", {})

                if subject:
                    question_bank[subject] = topics

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
    "results": [],
    "show_easter_egg": False
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
        for topic_name, topic_questions in QUESTION_BANK[subject].items():
            for question in topic_questions:
                new_question = question.copy()
                new_question["subject"] = subject
                new_question["topic"] = topic_name
                questions.append(new_question)

    return questions


def prepare_question(question):
    prepared = question.copy()
    options = prepared.get("options", []).copy()
    random.shuffle(options)
    prepared["shuffled_options"] = options
    return prepared


def start_quiz(subject, number_of_questions):
    available_questions = get_questions(subject)
    random.shuffle(available_questions)

    selected_questions = available_questions[:number_of_questions]
    prepared_questions = [prepare_question(question) for question in selected_questions]

    st.session_state.questions = prepared_questions
    st.session_state.quiz_started = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.results = []


def reset_quiz():
    keep_easter_egg = st.session_state.show_easter_egg

    for key, value in defaults.items():
        st.session_state[key] = value

    st.session_state.show_easter_egg = keep_easter_egg


def check_answer(question, selected_answer):
    correct = selected_answer == question["answer"]

    if correct:
        st.session_state.score += 1

    st.session_state.results.append({
        "subject": question["subject"],
        "topic": question["topic"],
        "question": question["question"],
        "selected": selected_answer,
        "correct_answer": question["answer"],
        "was_correct": correct
    })

    st.session_state.answered = True


def next_question():
    st.session_state.current_question += 1
    st.session_state.answered = False


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
    st.markdown(
        """
        <div class="easter-egg-card">
            <div class="easter-title">✨ Secret unlocked ✨</div>
            <p>This app was built by <strong>Seb Matthews</strong>.</p>
            <p>
                Certified absolute legend behaviour.<br>
                Peak coder energy.<br>
                Zero cringe detected.
            </p>
            <p>The revision goblin got absolutely cooked. 💀</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if not QUESTION_BANK:
    st.warning("No questions have loaded yet. Check your questions folder and JSON files.")
    st.stop()


if not st.session_state.quiz_started:

    st.subheader("Start a new quiz")

    subject_options = ["All Subjects"] + list(QUESTION_BANK.keys())
    selected_subject = st.selectbox("Choose a subject", subject_options)

    available_questions = get_questions(selected_subject)

    emoji = SUBJECT_EMOJIS.get(selected_subject, "📘")

    st.markdown(
        f"""
        <p>
            <span class="subject-pill">{emoji} {selected_subject}</span>
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write(f"Available questions: **{len(available_questions)}**")

    if len(available_questions) == 0:
        st.warning("This subject has no questions yet. Tiny quiz cupboard is empty.")

    elif len(available_questions) == 1:
        st.write("Only 1 question available.")
        number_of_questions = 1

        if st.button("Start Quiz", type="primary"):
            start_quiz(selected_subject, number_of_questions)
            st.rerun()

    else:
        number_of_questions = st.slider(
            "How many questions?",
            min_value=1,
            max_value=len(available_questions),
            value=min(10, len(available_questions))
        )

        st.info("Best move: short quiz, quick review, repeat later. Basically gym reps, but for your brain.")

        if st.button("Start Quiz", type="primary"):
            start_quiz(selected_subject, number_of_questions)
            st.rerun()

else:

    total_questions = len(st.session_state.questions)
    current_index = st.session_state.current_question

    if current_index < total_questions:

        question = st.session_state.questions[current_index]

        st.markdown('<div class="question-card">', unsafe_allow_html=True)

        st.progress(current_index / total_questions)

        st.caption(f"Question {current_index + 1} of {total_questions}")

        subject_emoji = SUBJECT_EMOJIS.get(question["subject"], "📘")

        st.markdown(
            f"""
            <p>
                <span class="subject-pill">{subject_emoji} {question['subject']}</span>
            </p>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="question-text">{question["question"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

        selected_answer = st.radio(
            "Choose your answer:",
            question["shuffled_options"],
            key=f"question_{current_index}",
            disabled=st.session_state.answered
        )

        if not st.session_state.answered:
            if st.button("Check Answer", type="primary"):
                check_answer(question, selected_answer)
                st.rerun()
        else:
            latest_result = st.session_state.results[-1]

            if latest_result["was_correct"]:
                st.markdown(
                    '<div class="result-good">✅ Correct! That one has entered the brain vault.</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="result-bad">
                        ❌ Not quite. Correct answer: {question['answer']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

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

        st.subheader("Review your answers")

        for i, result in enumerate(st.session_state.results, start=1):
            if result["was_correct"]:
                st.write(f"✅ **{i}. {result['question']}**")
                st.write(f"Your answer: {result['selected']}")
            else:
                st.write(f"❌ **{i}. {result['question']}**")
                st.write(f"Your answer: {result['selected']}")
                st.write(f"Correct answer: **{result['correct_answer']}**")

            st.caption(f"{result['subject']} | {result['topic']}")
            st.divider()

        if st.button("Take another quiz", type="primary"):
            reset_quiz()
            st.rerun()

st.markdown(
    '<div class="footer-note">Built for short, focused revision. No panic-cramming goblins were harmed.</div>',
    unsafe_allow_html=True
)

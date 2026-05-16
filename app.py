import streamlit as st
import base64
from pathlib import Path
import random

st.set_page_config(
    page_title="Revision Quiz",
    page_icon="✏️",
    layout="centered"
)

# ---------------------------------------------------
# Styling
# ---------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: #f7f9fc;
    }

    h1, h2, h3 {
        color: #1f2937;
    }

    .main-card {
        background: white;
        padding: 1.2rem;
        border-radius: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }

    .question-box {
        background: #ffffff;
        border: 2px solid #dbeafe;
        padding: 1rem;
        border-radius: 16px;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    div[role="radiogroup"] label {
        color: #111827 !important;
        font-size: 1rem !important;
        background: #ffffff;
        padding: 0.55rem;
        border-radius: 10px;
        margin-bottom: 0.35rem;
    }

    .stButton button {
        background-color: #2563eb;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.6rem 1rem;
        font-weight: 600;
    }

    .stButton button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    .restart button {
        background-color: #f97316 !important;
        color: white !important;
    }

    iframe {
        border-radius: 14px;
        border: 1px solid #d1d5db;
        margin-top: 1rem;
    }

    @media only screen and (max-width: 600px) {

        .main-card {
            padding: 1rem;
        }

        div[role="radiogroup"] label {
            font-size: 1.05rem !important;
            line-height: 1.4 !important;
            white-space: normal !important;
        }

        .stButton button {
            width: 100%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# Quiz Data
# ---------------------------------------------------
QUIZ_DATA = {
    "Religious Education": [
        {
            "question": "What does atheist mean?",
            "options": [
                "Someone who believes in many gods",
                "Someone who does not believe in God",
                "Someone who is not sure whether God exists",
                "Someone who believes in one God"
            ],
            "answer": "Someone who does not believe in God"
        },
        {
            "question": "What does agnostic mean?",
            "options": [
                "Someone who is not sure whether God exists",
                "Someone who believes God exists",
                "Someone who believes in many gods",
                "Someone who worships in a church"
            ],
            "answer": "Someone who is not sure whether God exists"
        },
        {
            "question": "What does monotheism mean?",
            "options": [
                "Belief in no gods",
                "Belief in many gods",
                "Belief in one God",
                "Belief that God is all-loving"
            ],
            "answer": "Belief in one God"
        },
        {
            "question": "Who founded Sikhi?",
            "options": [
                "Jesus",
                "Muhammad",
                "Guru Nanak",
                "Abraham"
            ],
            "answer": "Guru Nanak"
        },
        {
            "question": "What is the Sikh holy book called?",
            "options": [
                "The Bible",
                "The Qur’an",
                "The Torah",
                "The Guru Granth Sahib"
            ],
            "answer": "The Guru Granth Sahib"
        }
    ],

    "Science": [
        {
            "question": "What planet do we live on?",
            "options": [
                "Mars",
                "Earth",
                "Venus",
                "Jupiter"
            ],
            "answer": "Earth"
        }
    ]
}

# ---------------------------------------------------
# Learning Materials
# ---------------------------------------------------
LEARNING_MATERIALS = {
    "Religious Education": [
        {
            "title": "Full RE KAT Learning",
            "path": "materials/religious_education/1_re_full_kat_learning.pdf"
        },
        {
            "title": "RE Summer KAT Learning",
            "path": "materials/religious_education/2_re_summer_kat_learning.pdf"
        }
    ],

    "Science": []
}

# ---------------------------------------------------
# Session State
# ---------------------------------------------------
def initialise_state():

    if "subject" not in st.session_state:
        st.session_state.subject = None

    if "questions" not in st.session_state:
        st.session_state.questions = []

    if "question_index" not in st.session_state:
        st.session_state.question_index = 0

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "answered" not in st.session_state:
        st.session_state.answered = False

    if "show_material" not in st.session_state:
        st.session_state.show_material = False


# ---------------------------------------------------
# Quiz Functions
# ---------------------------------------------------
def start_quiz(subject):

    questions = QUIZ_DATA.get(subject, []).copy()
    random.shuffle(questions)

    st.session_state.subject = subject
    st.session_state.questions = questions
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.show_material = False


def restart_quiz():

    if st.session_state.subject:
        start_quiz(st.session_state.subject)


# ---------------------------------------------------
# PDF Viewer
# ---------------------------------------------------
def show_pdf(file_path):

    path = Path(file_path)

    if not path.exists():
        st.error(f"File not found: {file_path}")
        return

    with open(path, "rb") as pdf_file:
        base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")

    pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="700px"
            type="application/pdf">
        </iframe>
    """

    st.markdown(pdf_display, unsafe_allow_html=True)

    with open(path, "rb") as file:
        st.download_button(
            label="⬇ Download PDF",
            data=file,
            file_name=path.name,
            mime="application/pdf"
        )


# ---------------------------------------------------
# Learning Material Section
# ---------------------------------------------------
def show_learning_material(subject):

    materials = LEARNING_MATERIALS.get(subject, [])

    if not materials:
        return

    if st.button("📘 View learning material"):
        st.session_state.show_material = not st.session_state.show_material

    if st.session_state.show_material:

        st.markdown("### Learning Material")

        selected_material = st.selectbox(
            "Choose a document",
            materials,
            format_func=lambda x: x["title"]
        )

        show_pdf(selected_material["path"])


# ---------------------------------------------------
# Main App
# ---------------------------------------------------
initialise_state()

st.title("✏️ Revision Quiz")
st.write("Choose a subject, revise the material, then test yourself.")

subjects = list(QUIZ_DATA.keys())

selected_subject = st.selectbox(
    "Choose your subject",
    subjects
)

# Reset if subject changes
if selected_subject != st.session_state.subject:
    start_quiz(selected_subject)

# Show learning material
show_learning_material(selected_subject)

questions = st.session_state.questions

if not questions:
    st.warning("No questions available yet.")
    st.stop()

current_index = st.session_state.question_index
total_questions = len(questions)

# ---------------------------------------------------
# Quiz Complete
# ---------------------------------------------------
if current_index >= total_questions:

    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    st.subheader("Quiz complete 🎉")

    st.write(
        f"You scored **{st.session_state.score} out of {total_questions}**."
    )

    percentage = round(
        (st.session_state.score / total_questions) * 100
    )

    if percentage == 100:
        st.success("Perfect score. Slightly suspicious.")
    elif percentage >= 70:
        st.success("Great job. Revision wizard detected.")
    elif percentage >= 40:
        st.info("Good effort. A little more revision and you’re flying.")
    else:
        st.warning("Keep going. Even Einstein probably failed a quiz once. Maybe.")

    st.markdown('<div class="restart">', unsafe_allow_html=True)

    if st.button("Restart quiz"):
        restart_quiz()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# ---------------------------------------------------
# Current Question
# ---------------------------------------------------
current_question = questions[current_index]

st.markdown('<div class="question-box">', unsafe_allow_html=True)

st.write(f"**Question {current_index + 1} of {total_questions}**")

st.subheader(current_question["question"])

selected_answer = st.radio(
    "Choose your answer",
    current_question["options"],
    index=None,
    key=f"question_{current_index}"
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# Submit Answer
# ---------------------------------------------------
if selected_answer and not st.session_state.answered:

    if st.button("Submit answer"):

        st.session_state.answered = True

        if selected_answer == current_question["answer"]:

            st.session_state.score += 1

            st.success("Correct ✅")

        else:

            st.error(
                f"Incorrect ❌\n\nCorrect answer: **{current_question['answer']}**"
            )

# ---------------------------------------------------
# Next Question
# ---------------------------------------------------
if st.session_state.answered:

    if st.button("Next question"):

        st.session_state.question_index += 1
        st.session_state.answered = False

        st.rerun()

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")

st.write(f"Current Score: **{st.session_state.score}**")

st.markdown('<div class="restart">', unsafe_allow_html=True)

if st.button("Restart quiz"):

    restart_quiz()
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

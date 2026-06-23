import streamlit as st


def initialize_test(test_data):

    st.session_state.mock_test = {

        "questions": test_data.get(
            "mcqs",
            []
        ),

        "answers": {},

        "submitted": False,

        "score": 0
    }

def render_mock_test():

    test = st.session_state.mock_test

    questions = test["questions"]

    st.write(
    f"Questions Found: {len(questions)}"
    )

    st.subheader(
        "Interactive Mock Test"
    )

    for idx, question in enumerate(
        questions
    ):

        st.markdown(
            f"""
### Question {idx + 1}

{question['question']}
"""
        )

        options = question["options"]

        choice = st.radio(
            "Choose an answer",
            options=[
                f"A. {options['A']}",
                f"B. {options['B']}",
                f"C. {options['C']}",
                f"D. {options['D']}"
            ],
            key=f"q_{idx}"
        )

        if choice:

            test["answers"][idx] = choice[0]

        st.divider()

    if st.button(
        "Submit Test",
        use_container_width=True
    ):

        score = calculate_score()

        test["submitted"] = True

        test["score"] = score

        st.rerun()

    if test["submitted"]:

        show_results()


def calculate_score():

    test = st.session_state.mock_test

    score = 0

    for idx, question in enumerate(
        test["questions"]
    ):

        correct = question[
            "answer"
        ]

        selected = test[
            "answers"
        ].get(
            idx,
            ""
        )

        if selected == correct:

            score += 1

    return score


def show_results():

    test = st.session_state.mock_test

    total = len(
        test["questions"]
    )

    score = test["score"]

    percentage = round(
        score / total * 100,
        2
    )

    st.success(
        f"Score: {score}/{total}"
    )

    st.progress(
        percentage / 100
    )

    st.metric(
        "Percentage",
        f"{percentage}%"
    )

    st.subheader(
        "Answer Review"
    )

    for idx, question in enumerate(
        test["questions"]
    ):

        correct = question[
            "answer"
        ]

        selected = test[
            "answers"
        ].get(
            idx,
            "Not Answered"
        )

        with st.expander(
            f"Question {idx + 1}"
        ):

            st.write(
                question[
                    "question"
                ]
            )

            st.write(
                f"Your Answer: {selected}"
            )

            st.write(
                f"Correct Answer: {correct}"
            )

            if selected == correct:

                st.success(
                    "Correct"
                )

            else:

                st.error(
                    "Incorrect"
                )


def reset_test():

    if st.button(
        "New Test"
    ):

        if "mock_test" in st.session_state:

            del st.session_state[
                "mock_test"
            ]

        st.rerun()
def calculate_marks(quiz, answers):
    # Get all questions for the quiz
    questions = quiz.questions.all()

    # Initialize the total marks and the list of answer data
    total_marks = 0
    answer_data = []

    # Loop through each question and compare the user's answer to the correct answer
    for question in questions:
        # Get the correct answer for the question
        correct_answer = question.correct_answer

        # Get the user's answer from the answers dictionary
        user_answer = answers.get(str(question.id))

        # Check if the user's answer is correct
        if user_answer == correct_answer:
            # Assign full marks for correct answers
            marks = question.marks
        else:
            # Assign zero marks for incorrect answers
            marks = 0

        # Add the marks to the total marks for the quiz
        total_marks += marks

        # Add the answer data to the list
        answer_data.append({
            'question': question.id,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'marks': marks,
        })

    # Return the total marks and the answer data
    return total_marks, answer_data
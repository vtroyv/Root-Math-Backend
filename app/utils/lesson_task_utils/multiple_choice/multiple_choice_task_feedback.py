
def multiple_choice_response(response) -> dict:
    """Determine correctness a multiple choice question selection and generate feedback

    Args:
        feedbackData (dict): _description

    Returns:
        dict: {correct, feedback}
        - correct (bool): indciates whether the choice selected by the student is true or false 
        - feedback (str): string returning feedback for a students selected choice 
    """
    
    choice = response.selectedChoice
    correct = choice.isCorrect
    feedback = choice.explanation
    
    print(f"The answer is {correct} and the feedback is {feedback}")
    
    return {"correct":correct, "feedback":feedback}
    
    

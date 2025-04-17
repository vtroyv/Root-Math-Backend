from ....utils.others.preprocess_sympy import preprocess_sympy
from ....utils.others.grade_sympy_response import evaluate_correctness


def feedback_question_image(response: dict) -> dict:
    """determine if a question with a image is correct or incorrect aswell as provide feedback

    Args:
        response (dict): dictionary containing information regarding the task, gpt guideline prompt data and the students latexInput 

    Returns:
        dict: A dictionary with two keys {"correct": (bool), "feedback": (str) }
    """
    
    studentsResponse = response.compiledStrings
    
    sympyResponse = preprocess_sympy(studentsResponse)
    
    print(f"The sympy response is {sympyResponse}")
    
    responseEvaluation= evaluate_correctness(sympyResponse)
    print('The evaluated response is ', responseEvaluation)
    
  
    
    
    return 'test'
    
       
#You need to create a function that goes through each line of the students work checking the correctness or it, e.g. does this x imply y, does a=b, etc, return a list essentially, with true or false,
#if false identify where in the students response a mistake is made, however this list must not be conclusive in other words it is just a pointed to gpt, but you'll also need to finetune gpt and improve it.


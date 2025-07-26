from ...others.preprocess_sympy import preprocess_sympy

def feedback_curve_and_mfe(response: dict) -> dict:
    #Note its probably not best practice to state the type of response as a dict when its actually a pydantic class, because 
    #you can't actually use dot notation on python dictionaries 
    
    studentResponse = response.compiledStrings
    print(f"The students Response is {studentResponse}")
    
    sympyResponse = preprocess_sympy(studentResponse)
    print(f"The students sympy response is {sympyResponse}")
    
    #I think the first most valuable thing to do would examine how the evaulate_correctness and evaluate_context functions work 
    #IN detail, then perpahs we can simply extend them to handle these simpler cases! However for this type of question, would i only need to work on the 
    #evaluate_
    
    
    pass
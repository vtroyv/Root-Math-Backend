from typing import List, Union, Dict, Any, Tuple
from sympy import symbols, sympify
def evaluate_context(evaluatedResponse: List[Union[str,Tuple[str,bool]]], markScheme: Dict[str, Any]) -> Dict[str,Union[str,bool]]:
    """
    LISTEN UP
    
    ESSENTIALLY MARKING ON THE SITE WILL BE ACHIEVED VIA 2 METHODS CONCATENATED
    THE FIRST METHOD IS CHECKING THE MATHEMATICAL CORRECTNESS  OF WHAT THE STUDENT HAS WRITTEN WHICH IS DONE IN THE PREVIOUS FILE grade_sympy_response.py
    
    NEXT WE CHECK FOR THE PRESENCE OR ABSENCE OF VARIOUS CRITERIA FROM THE MARKING SCHEME. 
    
    IF THE STUDENTS WORK IS FULLY MATHEMATICALLY CORRECT AND ALL CRITERIA IN MARKSCHEME IS HIT RETURN WELL DONE AND CORRECT
    
    IF IT"S FULLY MATHEMATICALLY CORRECT BUT IF MARKSCHEME ONLY PARTIALLY HIT USE THE MISSING PARTS OF THE MARKSCHEME TO RETURN FEEDBACK
    
    POTENTIALLY USE SEMANTIC SIMILARITY BUT WITH MATHS TO COVER STUDENTS HITTING MARKSCHEME CRITERIA BUT BEING DISCOUNTED
    
    USE LLM TO CREATE A MAJORITY VOTING SYSTEM TO CHECK THAT STUDENTS WORK INCLUDES CRITERIA IN MARKSCHEME 
    YOU SHOULDN"T NEED TO USE LLM TO PROVIDE FEEDBACK FOR MISSNG PARTS IN THE MARKSCHEME IF YOUR CODE CAN IDENTIFY WHAT PARTS ARE MISSNG 
    USE THE MISSNG PARTS IDENTIFIED TO HELP PROVIDE TAILORED FEEDBACK!
  """
    
    all_statements_true =[]
    
    
    for i in evaluatedResponse:
        if type(i) == 'tuple':
            all_statements_true.append(i[1])
        else:
            continue
    
    
    all_true = all(all_statements_true)
    print(f"Are the statements all true? {all_true}")
    print(f"The markScheme is {markScheme}")

    marks = markScheme['marks']
    
    sym_keys = markScheme['symbols']
    syms = symbols(sym_keys)
    local_dict = dict(zip(sym_keys, syms))
    
    print('The local dict is ', local_dict)
    
    criteria = []
    explanations = []
    
    #obtain a list with sympy criteria 
    for i in marks:
        mark = sympify(i['mark'])
        criteria.append({'mark': mark, 'order':i['order']})
        explanations.append(i['explanation'])
        
    #Now we need to check for the presence of each of the criteria in the students work.
    criteria_satisfied = []
    for i in criteria: 
        for j in evaluatedResponse:
            if type(j) == tuple: 
                expr,_ = j
                print(f"The expr is {expr} and the type is {type(expr)}")
                if i['mark'].equals(expr):
                    criteria_satisfied.append(True)
                    continue
                
    print(f"The criteria satisfied is {criteria_satisfied}")
    



        
    
    return 'test'
    
    
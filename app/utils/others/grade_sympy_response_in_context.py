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
    
    POTENTIALLY USE SEMANTIC SIMILARITY BUT WITH MATHS TO PROTECT AGAINST STUDENTS HITTING MARKSCHEME CRITERIA BUT BEING DISCOUNTED
    
    USE LLM TO CREATE A MAJORITY VOTING SYSTEM TO CHECK THAT STUDENTS WORK INCLUDES CRITERIA IN MARKSCHEME 
    YOU SHOULDN"T NEED TO USE LLM TO PROVIDE FEEDBACK FOR MISSNG PARTS IN THE MARKSCHEME IF YOUR CODE CAN IDENTIFY WHAT PARTS ARE MISSNG 
    USE THE MISSNG PARTS IDENTIFIED TO HELP PROVIDE TAILORED FEEDBACK!
    
    
    
    CURRENT PROGRESS OF THIS FUNCTION:
    ----------------------------------
    Currently all this does is take in the results from the evaluate correctness function and makes sure all statements made are mathematically correct
    Next we look at the criteria specified in the markscheme and check that all conditions are present in the students response. 
    If everything the student has written is mathematically correct and satisfies all criteria specified within the markscheme we return correct alongside some hardcoded feedback
    
    I think the easiest way to improve this system is generate lots of test input responses with known output caes and then modify the code incrementally to ensure that each of the test cases 
    is being correctly marked - ovbiously write code in a way that abstracts common patterns within questions until the system is robust 
    
    Also have a last resort robust llm exception handler case in situations where my code can't correctly mark!
    
    //So what i should essentially do is upgrade the response so that it, checks according to the markscheme that may look like: 
    
    markScheme  ={
        marks: [
            {
                mark: '0 <=(x-3)**2', 
                explanation:'Student must include the fact that (x-3)**2 is >= 0', 
                order:1
                },
            {
                mark: 'Ne((x - 3)**2, -1)', 
                explanation: 'Student must use the fact that (x-3)**2 is >= 0 to deduce (Ne((x - 3)**2, -1)', 
                order:2
            }  
                ]
        symbols:'x'
                
    }
    ########################################################
    #i think the explanations can be used to prompt GPT, 
    #but what i need to do is have a feedback for each explanation where if it's present we return well done for 'xyz' 1 mark
    #or if it's missing mention it unfortunately 'your response was missing 'xyz'
    #next if everything is mathematically correct from the first function 
    ########################################################
    
    so maybe first check that everything is correct from the first function, 
    then check for the presence of things in the second function. 
    if everything is correct in the first function, 
    
  """
    
    all_statements_true =[]
    
    isCorrect = None
    feedback = None
    
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
                if i['mark'].equals(expr):
                    criteria_satisfied.append(True)
                    continue
                
    is_criteria_satisfied = all(criteria_satisfied)
    
    if (all_true and is_criteria_satisfied):
        isCorrect = True
        feedback = 'Well done! Your answer is correct'
        
    else: 
        isCorrect=False
        feedback = 'Your answer is incorrect, please try again!'
        
        
    return {"correct": isCorrect, "feedback": feedback}
    
    
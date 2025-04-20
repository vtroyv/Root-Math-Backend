from typing import List, Union, Dict, Any, Tuple
def evaluate_context(evaluatedResponse: List[Union[str,Tuple[str,bool]]], markScheme: Dict[str, Any]) -> Dict[str,Union[str,bool]]:
    """
    The purpose of this is to take a students response evaluatedResponse,
    and use it to return a dictionary indicating whether or not their work is correct as well as provide feedback
    To achieve this we will be using a  hybrid approach trying to leave the majority checking correctness logic to sympy 
    and llm logic for high quality feedback
    
    However also have a voting system initially to check sympy conclusion and llm agree and also some form of logic for sympy to learn from llm
    
    """
    pass
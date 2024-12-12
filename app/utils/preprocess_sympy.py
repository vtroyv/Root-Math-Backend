#The purpose of this file is to have functions etc, that take in an array response and convert it into sympy 
from sympy import sympify
from typing import List

def process_sympy(sympy_strings: List[str]):
    
    
    print("Received SymPy functions/expressions:", sympy_strings)

    # Process each string into a SymPy expression
    sympy_expressions = []
    for func_str in sympy_strings:
        try:
            expr = sympify(func_str)  # Convert string to SymPy expression
            sympy_expressions.append(expr)
        except Exception as e:
            print(f"Error processing function '{func_str}':", e)
            sympy_expressions.append(f"Error: {str(e)}")

    return {
        "expressions": [expr for expr in sympy_expressions],
        "success": all(isinstance(expr, str) and "Error" not in expr for expr in sympy_expressions),
    }
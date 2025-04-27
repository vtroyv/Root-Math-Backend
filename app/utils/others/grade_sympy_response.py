from typing import Any, Dict, List, Union
from sympy import symbols, sympify, S, Implies, Equality, simplify
from sympy.core.sympify import SympifyError
from sympy.core.relational import Relational
from sympy.solvers.inequalities import reduce_inequalities
from sympy.logic.boolalg import BooleanFunction
from sympy.logic import simplify_logic
from sympy.parsing.sympy_parser import parse_expr

def eq_algebraically_same(eq1: Equality, eq2: Equality) -> bool:
    # form lhs - rhs for each, then simplify()
    diff1 = simplify(eq1.lhs - eq1.rhs)
    diff2 = simplify(eq2.lhs - eq2.rhs)
    # now test if they represent the same symbolic value
    return diff1.equals(diff2)




def evaluate_correctness(
    sympy_response: Dict[str, Any]
) -> List[Union[str, bool]]:
    """
    Grade a mixed list of text and Sympy expressions:
    - Text stays as-is
    - Boolean/inequality tautologies collapse to True/False
    
    NOTES TO REMEMBER:
    -Implies(A,B) if A is false this will always return True, so be mindful,
    you may need to create  a work around for this or instead see if something can be rearrange into something else
    """
  
    names = sympy_response['meta_data']['symbols']

    syms = symbols(names)
    local_dict = dict(zip(names, syms))

    
    
    
    
    out: List[Union[str, bool]] = []
    eq_ineq = []
    for piece in sympy_response['meta_data']['response']:
        expr=None
        
        if isinstance(piece, str):
            try:
                if 'Implies' in piece:
                    expr = parse_expr(piece, local_dict=local_dict, evaluate=False)
                    # print(f"The expr is {expr}")
                else:
                     expr = sympify(piece, locals=local_dict)
                    #  print(f"The expr is {expr} and the type of  expr is {type(expr)}")
            except (SympifyError, TypeError):
                out.append(piece)
                continue
        else:
            expr = piece  # already a Sympy object
            # print(f"The type of expr is {type(expr)}")
            
        #2) Now we check if its a Implies instance and if so check for false antecedenat
        if isinstance(expr, Implies):
            A,B = expr.args
            # print(f"The args are {A} and {B}")
            if bool(expr) and expr.args[0] == True:
                # print("The implication is coming as True")
                out.append(True)
            elif isinstance(A, Equality) and isinstance(B,Equality):
                
                eq_ineq.append(A)
                eq_ineq.append(B)
                antecdent = simplify_logic(A)
                # print(f"The antecdent is {antecdent}")
                if antecdent != True:
                    #check if algebraically equalivalent
                    if eq_algebraically_same(A,B): 
                        # print(f"The two args are algebraically equivalent")
                        out.append(True)
                        continue
                    else:
                        out.append(False)
                        continue 
           
                           

        # 3) Constant booleans
        if expr is S.true:
            out.append(True)
            continue
        if expr is S.false:
            out.append(False)
            continue

        # 4) Univariate inequalities
        if isinstance(expr, Relational) and expr.free_symbols:
            try:
                taut = reduce_inequalities([expr], *expr.free_symbols)
        
                
                if taut is True or taut is S.true:
                    out.append(True)
                elif taut is False or taut is S.false:
                    out.append(False)
                
                elif isinstance(expr, Equality) and simplify(expr.lhs - expr.rhs)== 0:
                    print(f"This elif ran")
                    out.append(True)
           
                else: 
                    print('This else statement ran here')
                    out.append(piece)
                
            except Exception:
                print('This expception occured')
                out.append(piece)
            continue

        # 5) Propositional logic (And, Or, Implies, etc.)
        if isinstance(expr, BooleanFunction):
            simp = simplify_logic(expr, force=True)
            if getattr(simp, 'is_true', False):
                out.append(True)
                continue
            if getattr(simp, 'is_false', False):
                out.append(False)
                continue

        # 6) Fallback
        out.append(piece)

    # print('The output is ', out)
    # print('The eq_ineq is ', eq_ineq)
    
    grouped = zip(sympy_response['meta_data']['response'], out)
    evaluated_response = [(x,y) if x != y else x for x,y in grouped ]
    

    return evaluated_response
   




#First of all 

#TASK LIST 
#Firstly you need to deeply understand this code like inside out, 

#In addition to this you need to beable to store an array of equalities throughout the the script, so when you get to something later down the line in the code,
#e.g. an expr which we have already given a value then we can do a quick comparison with our list which stores equalities stated within the question to see if it still holds
#Here is an interesting example: 
#The final sympified response is ['Type your response below: ', 'Implies((x + -3) ** 2 + 1 == 0, (x + -3) ** 2 == -1)', 'however we know that ', 0 <= (x - 3)**2, 'therefore ', Ne((x - 3)**2, -1), 'so ', (x - 3)**2 + 1, 'has no roots']
# The output is  ['Type your response below: ', True, 'however we know that ', 0 <= (x - 3)**2, 'therefore ', True, 'so ', (x - 3)**2 + 1, 'has no roots']
#Note you need to keep a track of different statments you make which contain equalities or inequalities, for instance, you wrote: 
#in the implies two equalities (x + -3) ** 2 + 1 == 0 , (x + -3) ** 2 == -1)  we also have  0 <= (x - 3)**2 and  Ne((x - 3)**2, -1), we should have a function that keeps track of all of these
#and tests the relation from one to another e.g from equality 1 we know that equality 2 is true, also from equality 3 we know that equality 4 is true. 
#e.g. a litte reinforcement of correctness. 
#

#Next once you've got this correctly marking and returning the output we then need to feed this in to a robust llm to interpret the output, 
#i.e. in particular look at which statements caused the students work to be marked as false and provide adequate feedback. 

#Marking 
#In regards to marking we've now evaluated the correctness of what the student has written in the context of what the student has written
#But not necessarily in the context of the question, in otherwords we are now able to determine if what a student has written is mathematically correct
#However we still need to determine if this answers the question. E.g. for full marks it must be mathematically correct and answer the question. 

#Maybe to mark in the context of the question we can check for the presence of certain truth elements e.g. in this example a student would need to include 
#((x-3)**2 >= 0), True ) in part of their reasoning to obtain full marks. Therefore if their work includes this we can conlude that they've satisfied a given mark in the markscheme ? 

#But how robust is this approach^


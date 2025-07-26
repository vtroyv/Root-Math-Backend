from typing import Any, Dict, List, Union
from sympy import symbols, sympify, S, Implies, Equality, simplify, And
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
    """
    # ─── Helpers ────────────────────────────────────────────────

    def is_nonneg(expr):
        """Returns True if expr is guaranteed >= 0 (even powers, .is_nonnegative==True)."""
        nn = expr.is_nonnegative
        if nn is True:
            return True
        if expr.is_Pow and expr.exp.is_integer and expr.exp % 2 == 0:
            # e.g. (p-q)**2, x**4, etc.
            return True
        return False

    def sq_test(lhs, rhs):
        """Check lhs ≤ rhs by squaring: (rhs**2 - lhs**2) >= 0."""
        sq_diff = simplify(rhs**2 - lhs**2)
        return is_nonneg(sq_diff)

    def eval_rel(r):
        """
        Evaluate a Relational r to True/False/None:
        - univariate: uses reduce_inequalities
        - multivariate ≤/≥: uses is_nonneg & sq_test
        """
        syms_r = list(r.free_symbols)
        # 1) univariate
        if len(syms_r) == 1:
            taut = reduce_inequalities([r], syms_r[0])
            if taut in (True, S.true):
                return True
            if taut in (False, S.false):
                return False
            return None

        # 2) multivariate
        op = r.rel_op
        if op == '<=':
            # sqrt on lhs?
            if r.lhs.is_Pow and r.lhs.exp == S.Half:
                return sq_test(r.lhs, r.rhs)
            # sqrt on rhs?
            if r.rhs.is_Pow and r.rhs.exp == S.Half:
                return sq_test(r.lhs, r.rhs)
            # plain diff
            return is_nonneg(simplify(r.rhs - r.lhs))

        if op == '>=':
            if r.lhs.is_Pow and r.lhs.exp == S.Half:
                return sq_test(r.rhs, r.lhs)
            if r.rhs.is_Pow and r.rhs.exp == S.Half:
                return sq_test(r.rhs, r.lhs)
            return is_nonneg(simplify(r.lhs - r.rhs))

        # strict '<' or '>' we leave as unknown
        return None

    # ─── Setup ─────────────────────────────────────────────────

    names = sympy_response['meta_data']['symbols']
    syms = symbols(names)
    local_dict = dict(zip(names, syms))

    out: List[Union[str, bool]] = []

    # ─── Main loop ─────────────────────────────────────────────

    for piece in sympy_response['meta_data']['response']:
        # parse into expr
        if isinstance(piece, str):
            try:
                if 'Implies' in piece:
                    expr = parse_expr(piece, local_dict=local_dict, evaluate=False)
                else:
                    expr = sympify(piece, locals=local_dict)
            except (SympifyError, TypeError):
                out.append(piece)
                continue
        else:
            expr = piece

        # 1) And of Equalities
        if isinstance(expr, And):
            ok = all(
                isinstance(cl, Equality) and simplify(cl.lhs - cl.rhs) == 0
                for cl in expr.args
            )
            out.append(ok)
            continue

        # 2) Implies
        if isinstance(expr, Implies):
            A, B = expr.args
            # 2a) any vacuously- or trivially-true implication
            if bool(expr):
                out.append(True)
                continue
            # 2b) Eq→Eq
            if isinstance(A, Equality) and isinstance(B, Equality):
                out.append(eq_algebraically_same(A, B))
                continue
            # 2c) Relational→Relational
            if isinstance(A, Relational) and isinstance(B, Relational):
                A_val = eval_rel(A)
                B_val = eval_rel(B)
                if A_val is False:
                    out.append(True)
                    continue
                if A_val is True:
                    out.append(B_val is True)
                    continue
            # fallback
            out.append(piece)
            continue

        # 3) True/False constants
        if expr is S.true:
            out.append(True)
            continue
        if expr is S.false:
            out.append(False)
            continue

        # 4) Stand‑alone Relational
        if isinstance(expr, Relational) and expr.free_symbols:
            res = eval_rel(expr)
            if res is True or res is False:
                out.append(res)
            else:
                out.append(piece)
            continue

        # 5) Propositional BooleanFunction
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

    # collapse identicals for nicer output
    grouped = zip(sympy_response['meta_data']['response'], out)
    evaluated = [(x, y) if x != y else x for x, y in grouped]
    return evaluated




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


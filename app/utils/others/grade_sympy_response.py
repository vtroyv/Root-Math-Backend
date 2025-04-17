from typing import Any, Dict, List, Union
from sympy import symbols, sympify
from sympy.core.sympify import SympifyError
from sympy.core.relational import Relational
from sympy.solvers.inequalities import reduce_inequalities
from sympy.logic.boolalg import BooleanFunction, BooleanAtom
from sympy.logic import simplify_logic

def evaluate_correctness(
    sympy_response: Dict[str, Any]
) -> List[Union[str, bool]]:
    """
    Grade a mixed list of text and Sympy expressions:
    - Text stays as-is
    - Boolean/inequality tautologies collapse to True/False
    """
    # 1) Set up your symbols
    names = sympy_response['meta_data']['symbols']
    syms = symbols(names)
    local_dict = dict(zip(names, syms))

    out: List[Union[str,bool]] = []
    for piece in sympy_response['meta_data']['response']:
        # 2) Parse strings, pass through non-strings
        if isinstance(piece, str):
            try:
                expr = sympify(piece, locals=local_dict)
            except (SympifyError, TypeError):
                out.append(piece)
                continue
        else:
            expr = piece  # already a Sympy object

        # 3) Constant booleans
        if expr is True or isinstance(expr, BooleanAtom):
            out.append(True)
            continue
        if expr is False:
            out.append(False)
            continue

        # 4) Univariate inequalities
        if isinstance(expr, Relational) and expr.free_symbols:
            try:
                taut = reduce_inequalities([expr], *expr.free_symbols)
                out.append(taut is True)
            except Exception:
                out.append(piece)
            continue

        # 5) Propositional logic (And, Or, Implies, etc.)
        if isinstance(expr, BooleanFunction):
            simp = simplify_logic(expr, force=True)
            if simp is True:
                out.append(True)
                continue
            if simp is False:
                out.append(False)
                continue

        # 6) Fallback
        out.append(piece)

    return out


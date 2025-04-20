import re
from typing import List
from sympy.parsing.sympy_parser import parse_expr, standard_transformations
from sympy import Eq, And

# Configure parser to avoid automatic evaluation
transformations = standard_transformations


def remove_outer_parens(s: str) -> str:
    """
    Removes one matching pair of parentheses if they wrap the entire string.
    Example: "((p + q))" -> "(p + q)" -> "p + q".
    If there's no *single* outer pair, it returns s unchanged.
    """
    s = s.strip()
    if s.startswith("(") and s.endswith(")"):
        inner = s[1:-1].strip()
        return inner
    return s


def convert_condition(cond: str) -> str:
    """
    1) Remove one outer layer of parentheses from the entire cond.
    2) If '==' is present, split into LHS/RHS -> Eq(LHS, RHS).
    3) Otherwise, leave the inequality (or !=) as-is.
    """
    cond = remove_outer_parens(cond.strip())

    if "==" in cond:
        parts = cond.split("==")
        if len(parts) == 2:
            lhs = remove_outer_parens(parts[0].strip())
            rhs = remove_outer_parens(parts[1].strip())
            return f"Eq({lhs}, {rhs})"
        return cond
    # leave all other relations (<, >, <=, >=, !=) intact
    return cond


def convert_equals_and_ands(line: str) -> str:
    """
    1) Split the line by '&&' to get sub-conditions.
    2) Convert each sub-condition with convert_condition.
    3) If >1 sub-condition, wrap them in And(...).
    """
    sub_conditions = line.split("&&")
    converted = [convert_condition(sc.strip()) for sc in sub_conditions]

    if len(converted) == 1:
        return converted[0]
    return f"And({', '.join(converted)})"


def preprocess_sympy(response: List[str]) -> dict:
    """
    Main entry point:
    1) Strip '_.' prefixes
    2) Convert '==' -> Eq(), keep <, >, <=, >=, != untouched
    3) Combine '&&' -> And(...)
    4) Parse with evaluate=False to avoid auto-evaluation
    """
    meta_data = {
        "symbols": [],
        "response": []
    }

    # 1) Collect and dedupe symbols (_.x -> x)
    for line in response:
        syms = re.findall(r"_\.(.)", line)
        meta_data["symbols"].extend(syms)
    meta_data["symbols"] = list(dict.fromkeys(meta_data["symbols"]))

    # 2) Remove '_.' prefixes
    cleaned = [re.sub(r"_\.", "", line) for line in response]
    meta_data["response"] = cleaned

    # 3) Convert eqs and ands
    eq_converted = [convert_equals_and_ands(line) for line in cleaned]

    # 4) Parse each into a SymPy expression without evaluating
    processed = []
    for text in eq_converted:
        try:
            expr = parse_expr(
                text,
                transformations=transformations,
                evaluate=False
            )
            processed.append(expr)
        except Exception:
            # On parse error, keep raw string
            processed.append(text)

    meta_data["response"] = processed
    print(f"The final parsed response is {processed}")
    return {"meta_data": meta_data}

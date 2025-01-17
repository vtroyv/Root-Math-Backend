from sympy import sympify, Eq, And
from typing import List
import re

def remove_outer_parens(s: str) -> str:
    """
    Removes one matching pair of parentheses if they wrap the entire string.
    Example: "((p + q))" -> "(p + q)" -> "p + q".
    If there's no *single* outer pair, it returns s unchanged.
    """
    s = s.strip()
    if s.startswith("(") and s.endswith(")"):
        # Check if by removing the first and last char
        # we still have a valid "balance" or typical expression.
        # For simple cases, we can do the naive approach:
        inner = s[1:-1].strip()
        # You can do deeper checks if needed, but typically one pass is enough.
        return inner
    return s

def convert_condition(cond: str) -> str:
    """
    1) Remove one outer layer of parentheses from the entire cond.
    2) If '==' is present, split into LHS/RHS -> Eq(LHS, RHS).
    3) Otherwise, leave the inequality as-is.
       (Sympy can parse strings like '4*p*q < (p + q)**2'.)
    """
    # Remove any outer parentheses first
    cond = remove_outer_parens(cond.strip())

    if "==" in cond:
        parts = cond.split("==")
        # Handle only the common case of a single '==' 
        # (if there's chaining like a == b == c, you'll need more logic)
        if len(parts) == 2:
            lhs = remove_outer_parens(parts[0].strip())
            rhs = remove_outer_parens(parts[1].strip())
            return f"Eq({lhs}, {rhs})"
        else:
            # If there's something unusual like multiple ==, handle accordingly.
            # We'll just return cond unchanged or raise an error.
            return cond
    else:
        # It's an inequality or something else. Just leave it as-is so sympy can parse it.
        return cond

def convert_equals_and_ands(line: str) -> str:
    """
    1) Split the line by '&&' to get sub-conditions.
    2) Convert each sub-condition with convert_condition (which 
       replaces '==' with Eq(...) or leaves inequalities alone).
    3) If >1 sub-condition, wrap them in And(...).
    """
    sub_conditions = line.split("&&")
    converted = [convert_condition(sc.strip()) for sc in sub_conditions]

    if len(converted) == 1:
        # Just a single condition
        return converted[0]
    else:
        # Multiple conditions -> combine with And(...)
        # e.g. ["Eq(x, y)", "x < 5"] -> "And(Eq(x, y), x < 5)"
        return f"And({', '.join(converted)})"

def preprocess_sympy(response: List[str]):
    """
    Main entry point. 
    1) Removes '_.', 
    2) Converts '==' to Eq(...) but leaves <, >, etc. alone,
    3) Splits by '&&' to produce And(...),
    4) Attempts sympify
    """
    lines = response

    print(f"successfully got the response it is {lines}")

    meta_data = {
        "symbols": [],
        "response": []
    }

    # 1) Collect symbols
    for line in lines:
        symbols = re.findall(r"_\.(.)", line)  # e.g. "_.p" -> "p"
        meta_data["symbols"].append(symbols)

    # Flatten & remove duplicates
    meta_data["symbols"] = sum(meta_data["symbols"], [])
    meta_data["symbols"] = list(dict.fromkeys(meta_data["symbols"]))
    print(f"The meta_data symbols without duplicates are {meta_data['symbols']}")

    # 2) Remove '_.' from each line
    cleaned_lines = []
    for line in lines:
        no_prefix = re.sub(r"_\.", "", line)
        cleaned_lines.append(no_prefix)

    meta_data["response"] = cleaned_lines
    print(f"Now the lines no longer have '_.' trailing: {meta_data['response']}")

    # 3) Convert '==' to Eq(...), '&&' to And(...). 
    #    We keep <, >, etc. unaltered so they become normal Sympy inequalities.
    eq_converted_lines = [convert_equals_and_ands(line) for line in meta_data["response"]]
    print(f"Lines after converting '==' -> Eq() and '&&' -> And(): {eq_converted_lines}")

    # 4) Sympify
    processed_resp = []
    for line in eq_converted_lines:
        try:
            expression = sympify(line)
            processed_resp.append(expression)
        except Exception as e:
            print("Error in sympify:", e)
            # If sympify fails, just store the raw string
            processed_resp.append(line)

    meta_data["response"] = processed_resp
    print(f"The final sympified response is {meta_data['response']}")
    
    return {
        "meta_data": meta_data
    }

from ..sketch.lagrange_interpolation import lagrange_implementation
from sympy import symbols

def graph(coords: list, guide: dict) -> dict:
    """Tests if a Students sketch is correct or not by comparing input and outputs of the lagrange interpolation
        of the students sketch, with the inputs and outputs of the specific polynomial.

    Args:
        coords ([{'x': int, 'y': int, 'threshold': int}]) : ...
        guide (_type_): _description_
    
    Returns:
        A dictionary with keys: 
        - "correct" : bool indicating if the inputs or outputs are 
        - "comparison" : ...

    """
    
    graph_values = guide['graph-values']
    lagrange_func = lagrange_implementation(coords)
    
    x_values =[]
    target_values= []
    thresholds = []
    output_values = []
    
    for i in graph_values:
        x_values.append(i['x'])
        target_values.append(i['y'])
        thresholds.append(i['threshold'])
        
    
    
    x = symbols('x')
    for x_val in x_values:
        output_values.append(lagrange_func.subs(x, x_val).evalf())
        
    print(f"The output values are {output_values}")
    
    truth_list= []
    for output_val, target_val, thresh in zip(output_values, target_values, thresholds):
        
        if (abs(output_val - target_val) < thresh):
            truth_list.append(True)
        else:
            truth_list.append(False)
            
    comparison_list = list(zip(output_values, target_values))
    correct = all(truth_list)
    
    print(f"The final comparison is {comparison_list}")
    print(f"The final Truth list is {truth_list}")
    

    
    return {"correct": correct, "comparison": comparison_list}

    
    
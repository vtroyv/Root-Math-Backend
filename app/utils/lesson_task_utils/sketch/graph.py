from ..sketch.lagrange_interpolation import lagrange_implementation
from sympy import symbols

def graph(coords: list, guide: dict) -> dict:
    """_summary_

    Args:
        coords (list): _description_
        guide (dict): _description_

    Returns:
        dict: _description_
        
        write this docstring properly later at some point but for the time being lets rewrite this, now we've given each coord a label, so lets run comparisons by labels, essentially. 
    """
    
    graph_values = guide['graph-values']
    lagrange_func = lagrange_implementation(coords)
    # print('the coords are ', coords)
    
    x_values = []
    target_values = []
    
    thresholds = []
    output_values = []
    new_output_values = []
    new_target_values = []
   
    for i in graph_values:
        x_values.append(i['x'])
        target_values.append( {'y':i['y'], 'label':i['label']})
        # I should create some new target values because theres no point comparing y coordinates on the roots because it will just be 0
        
        if (i['label'] == 'y-intercept'):
            new_target_values.append({'y':i['y'], 'label':i['label']})
            
        elif (i['label'] == 'first root'):
            new_target_values.append({'x':i['x'], 'label':i['label']})
            
        elif (i['label'] == 'second root'):
            new_target_values.append({'x':i['x'], 'label':i['label']})
            
        
        thresholds.append(i['threshold'])
        
    
    # print('the x values are ', x_values )
    # print('the target values are ', target_values)
    # print('the new target values are ', new_target_values)
    
    x = symbols('x')
    for x_val in x_values:
        output_values.append(lagrange_func.subs(x, x_val).evalf())
    
    
    # for i in coords:
    #     if i['label'] == 'y-intercept': 
    #         new_output_values.append({'y':i['y'], 'label':i['label']})
    #     elif i['label'] == 'first root':
    #         new_output_values.append({'x':i['x'], 'label':i['label']})
            
    #     elif i['label'] == 'second root':
    #         new_output_values.append({'x':i['x'], 'label':i['label']})
            
    # print('the new output values are ', new_output_values)
            
    # new_truth_list = []
    # for output_val, target_val
            
    
    # print(f"The output values are {output_values}")
    
    truth_list= []
    for output_val, target_val, thresh in zip(output_values, target_values, thresholds):
        
        if (abs(output_val - target_val['y']) < thresh):
            truth_list.append(True)
        else:
            truth_list.append(False)
            
    comparison_list = list(zip(output_values, target_values))
    correct = all(truth_list)
    
    # print(f"The final comparison is {comparison_list}")
    # print(f"The final Truth list is {truth_list}")
    
    new_truth_list = []
    new_comparison_list = []
    for user_pt, targ_pt in zip(coords, graph_values ):
        if user_pt['label'] == targ_pt['label']:
            if (abs(user_pt['x'] - targ_pt['x']) < targ_pt['threshold'] and abs(user_pt['y'] - targ_pt['y']) < targ_pt['threshold']):
                new_truth_list.append(True)
                new_comparison_list.append({'label':user_pt['label'], 'user_point':{'x':user_pt['x'], 'y':user_pt['y']}, 'target_point':{'x':targ_pt['x'], 'y':targ_pt['y']}, "is_correct":True})
            else:
                new_truth_list.append(False)
                new_comparison_list.append({'label':user_pt['label'], 'user_point':{'x':user_pt['x'], 'y':user_pt['y']}, 'target_point':{'x':targ_pt['x'], 'y':targ_pt['y']}, "is_correct":False})
            
            

    new_correct= all(new_truth_list)
    # print('the new comparsion list is ', new_comparison_list)
    
    
    # return {"correct": correct, "comparison": comparison_list, "metric":"graph values"}

    
    return {'correct':new_correct, "comparison": new_comparison_list, 'metric':'graph values'}
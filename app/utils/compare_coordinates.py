from typing import List, Dict, Any
import math 

def compare_coordinates(correct_intercepts: Dict[str,Any], student_coords: List[Dict[str,float]], threshold: float=0.2)-> bool:
    """Compare student's coordinates with the correct intercepts

    Args:
        correct_intercepts (Dict[str,Any]): The intercepts from the correct answer from the questionData
        student_coords (List[Dict[str,float]]): The students coordinates.
        threshold (float, optional): The maximum allowable distance between corresponding points. Defaults to 0.2

    Returns:
        bool: True if all the points are within the threshold, False otherwise. 
    """
    
    #Extract correct coordinates
    correct_coords = []
    
    #Add y-axis intercepts as (0,y)
    for y in correct_intercepts.get('y-axis', []):
        correct_coords.append({'x':0.0, 'y':y})
        
    #Add x-axis intercepts as (x,0)
    for intercept in correct_intercepts.get('x-axis',[]):
        if isinstance(intercept, list) and len(intercept) ==2:
            x,y = intercept
            correct_coords.append({'x': x, 'y':y})
        else:
            raise ValueError("Each x-axis intercept must be a list of two floats. ")
        
    
    # Validate that both lists have the same length
    if len(correct_coords) != len(student_coords):
        raise ValueError('The number of student coordinates does not match the correct answer.')
    
    #Sort both lists by 'x' in ascending order
    sorted_correct = sorted(correct_coords, key=lambda c :c['x'])
    sorted_student = sorted(student_coords, key=lambda c: c['x'])
    
    #Compare each pair of coordinates
        
    
    
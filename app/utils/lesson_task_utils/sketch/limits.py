from ..sketch.lagrange_interpolation import lagrange_implementation
from sympy import symbols

def limit(func, guide: dict) -> dict:
    """Return True or False if a function is approaching its desired limit.
    
    Cases: 
      - When a list of points is provided, use lagrange_interpolation to determine 
        an approximate polynomial and then evaluate its behavior at the indicated limits.
    
    The 'guide' dict is expected to have a key 'limit-values' with a list of dictionaries:
       {"x": <x-coordinate>, "y": <target limit value>, "threshold": <acceptable deviation>}
    
    For a negative target value, the function is considered as approaching the limit 
    if its output is less than or equal to the target. If it's greater, then it must 
    be within the threshold (i.e. the difference is less than the threshold) to return True.
    
    For a positive target value, the logic is symmetric: the function output must be 
    greater than or equal to the target, or if lower, within the threshold.
    
    Returns:
       A dictionary with keys:
         - "correct": bool indicating if all comparisons were acceptable.
         - "comparison": list of tuples (output_value, target_value) for each limit point.
    """
    
    # lets take some information in essentially on the curve
    if isinstance(func, list):
        print('the func is ', func)
        lagrange_func = lagrange_implementation(func)
        # print('The limits guide is:', guide)
        
        # Extract limit values from the guide
        limit_values = guide['limit-values']
        x_values = []
        target_values = []
        thresholds = []
        output_values = []
        
        for i in limit_values:
            x_values.append(i['x'])
            target_values.append(i['y'])
            thresholds.append(i['threshold'])
             
        x = symbols('x')
        for x_val in x_values:
            output_values.append(lagrange_func.subs(x, x_val).evalf())
            
        # print(f"The output values are: {output_values}")
        
        # Compare each output value with its corresponding target value and threshold.
        truth_list = []
        for out_val, target_val, thresh in zip(output_values, target_values, thresholds):
            # For negative target values: expecting outputs to be less than or equal.
            if target_val < 0:
                if out_val <= target_val:
                    truth_list.append(True)
                elif out_val > target_val and (out_val - target_val) < thresh:
                    truth_list.append(True)
                else:
                    truth_list.append(False)
            # For positive target values: expecting outputs to be greater than or equal.
            else:
                if out_val >= target_val:
                    truth_list.append(True)
                elif out_val < target_val and (target_val - out_val) < thresh:
                    truth_list.append(True)
                else:
                    truth_list.append(False)
        
        # Create a combined comparison list for debugging or output
        comparison_list = list(zip(output_values, target_values))
        # print(f"Comparison list: {comparison_list}")
        # print(f"Truth list: {truth_list}")
            
        correct = all(truth_list)
        # print('Final comparison:', comparison_list)
        
        return {"correct": correct, "comparison": comparison_list, "meteric":"limits"}
    
    else: 
        # Put implementation logic here for the case where func is not a list
        pass


# if the polynomial is of degree n, you need (n+1) points to specify it uniquely e.g. all the roots and the y-intercept, 
# so for questions where you specify the polynomial specifically that you want them to draw you can do it 
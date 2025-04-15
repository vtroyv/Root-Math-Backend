from ..sketch.lagrange_interpolation import lagrange_implementation
from sympy import symbols

def limit(func, guide):
    """Return the True or False if a function approaches it's desired limit
    ---------------------------------------------
    Cases: 
    -> If simply a set of n coordinates are given first apply lagrange_interpolation to determine a approximate polynomial of (n-1)th degree, then 
    extract the limits and determine the output [Probably need to rewrite this clearer at some point]
    
    
    Returns -> {correct, limits}
    -----------------------------
    
    -> correct: True or False
                If a function displays desired behaviour when 
    
    
    
    
    """

    if isinstance(func, list):
        lagrange_func = lagrange_implementation(func)
        print('The limits guide is ', guide)
        #Now you need to add logic here to evaluate the limit of a function using the guide and the lagrange_func
        limit_values = guide['limit-values']
        x_values = []
        target_values =[]
        thresholds =[]
        output_values=[]
        
        for i in limit_values:
            x_values.append(i['x'])
            target_values.append(i['y'])
            thresholds.append(i['threshold'])
             
        x = symbols('x')
        for i in x_values:
            output_values.append(lagrange_func.subs(x,i).evalf())
            
        print(f"The output values are {output_values}")
        #Now we simply need to compare our output values with our target values and see if each output exceeds it's corresponding output 
        truth_list=[]
        comparison = zip(output_values, target_values)
        for i in comparison:
            if (i[0] >= i[1]):
                truth_list.append(True)
            elif (i[1] - i[0] < thresholds[i]):
                truth_list.append(True)
            else:
                truth_list.append(False)
        print(f"The truth_list is  {truth_list}")
        print(f"the comparison is {comparison}")
            
        correct = all(truth_list)
        print('the comparison is ', list(comparison))
        
        return {correct, list(comparison)}
    
    
    
        
    else: 
        #Put implementation logic here in the case where a function is given to evaluate the limt of it using the guide 
        pass
        
    
    
    
    
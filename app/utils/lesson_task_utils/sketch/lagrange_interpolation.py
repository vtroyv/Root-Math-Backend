from sympy import symbols
from sympy.polys.specialpolys import interpolating_poly

def lagrange_implementation(coords):
    """
Lagrange_interpolation implementation
--------------------------------------

Description: This function should accept a list of (x,y) coordinates and return 
             a lagrange_interpolation of the polynomial estimated using the list
             of coordinates provided
             
Params: List[{x,y}]
        A list of {x,y} coordinates 
"""    
    x = symbols('x')
    X_values=[]
    Y_values=[]
    for i in coords:
        X_values.append(i['x'])
        Y_values.append(i['y'])
    
    n = len(X_values)
    
  
    poly = interpolating_poly(n,x, X_values, Y_values)
    
    return poly
    

#The purpose of this file is to have functions etc, that take in an array response and convert it into sympy 
from sympy import sympify
from typing import List
import re

# in this file your tasks are the following;
#beable to take out text aswellas clean up the sympyish response from nextjs (i say ish as it can't be sympyfied yet into a form where )
#you should get it essentially to a point where it can be ran straight away, you should also replace all instances of '_.something' and add it to a dictionary called symbols, 
# to enable sympy to use it to successfully sympify the code.  

def preprocess_sympy(response: List[str]): 
    
    lines = response.sympy
    print(f'successfully got the response it is {lines}' )
    meta_data ={
        "symbols": [],
        "response": []
    }
    for line in lines:
            #Store all symbols in entire response in dictionary
            symbols = re.findall(r"_\.(.)", line)
            meta_data['symbols'].append(symbols)
    
    #remove duplicates symbols
    meta_data['symbols']= sum(meta_data["symbols"],[])
    
    meta_data["symbols"]= list(dict.fromkeys(meta_data["symbols"]))
    print(f"The meta_data symbols without duplicates are {meta_data['symbols']}")
    
    #next we wish to replace all _. with it's corresponding symbol representation
    cleaned=[] 
    for line in lines:
        cleaned.append(re.sub('_\.', "", line))
        meta_data["response"] = cleaned
        
    print(f'Now the lines no longer have _. trailing the symbols are {meta_data["response"]}')
    #next sympy can be strange about how it treats equal signs e.g. '(x+1)**2 = x**2 + 2*x + 1' evaluates to false, this is becaues == only
    #tests for structural equivalence, therefore lets change this so that whenever there is a == we convert it into Eq(expr1, expr2), 
    # then we will have a predefined function in validation_functions to handle testing for equality. 
        
    
    processed_resp =[]
    for line in meta_data['response']:
        try:
            processed_resp.append(sympify(line))
        except Exception as e:
            print('the error is ', e)
            
    meta_data["response"]= processed_resp
    
    print(f"The final sympified response is {meta_data['response']} ")
    # testing testing again 
    return {
        "meta_data": meta_data,
    }
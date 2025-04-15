from ..sketch.limits import limit
def feedback_sketch_task(response):
    tool = response.task.task.marking['tool']
    
  
  
    
    
    
    if tool == 'limit':
        #You need to call the limits function here, however, at this point everything is a task, 
        #You need to have logic that extracts the reduced Coordinates, or function. 
        #So search through the task/response object looking for reduced coordinates or a function, and if you find it then call the limit funciton
        #with either the reduced coordinates or the function that you have along with te guide/limit marking instruction object.
        
        guide = response.task.task.marking['guide']
        
        
        if 'reducedCoordinates' in response.dict():
            coords = response.reducedCoordinates
            print(f"the coords are {coords}")
            
            
            result = limit(coords,guide)
            #Note after getting this result although we have a correct value, we still need to add adequate logic for providing feedback,
            # so perhaps we should also return the funciton e.g. given function or lagrange function from the limit file, as well as the correct outcome and comparsion list from 
            #the limit file and thus use this to to provide feedback 
            #Additionally you may want to add a alot of detail to the gpt field in the task to provide adequate instructions regarding providing feedback e.g. and for the sake of structuring these instructions 
            #you may want to change the gpt field from str-> dict in the lesson_response_model.py file
            
            print(f"The output from the limit function is ", result)
    
        pass
        
        
    
    
    return {"correct":False, "feedback":'This is simply hardcoded for now' }
    
    
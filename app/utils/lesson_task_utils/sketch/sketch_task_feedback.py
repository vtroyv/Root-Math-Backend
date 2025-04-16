from ..sketch.limits import limit
from ..sketch.graph import graph
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
            if (result['correct'] == True):
                return {"correct": True, "feedback": "Hardcoded - this is correct"}
            
            else:
                return {"correct": False, "feedback":"Hardcoded - this is incorrect"}
    
        pass
        
    if (isinstance(tool, list)):
        print(f'This question requires multiple functions to mark it requires {tool}')
        guide= response.task.task.marking['guide']
        
        tools_output = []
        for i in tool:
            if i == 'limit':
                if 'reducedCoordinates' in response.dict():
                    coords = response.reducedCoordinates
                    tools_output.append(limit(coords,guide))
                #You may need to add somelogic here for correctly passing in a funciton, 
                #If you need to compute  a limit, but have the function instead of coords 
            elif i == 'graph':
                coords = response.reducedCoordinates
                tools_output.append(graph(coords, guide))
                
            else:
                pass
            
        #Now in the case where you've got a output of different responses, you simply need to create some logic to correct the correctness of each part and return an overall True or False as well as feedback. 
        
            
        #In this case you must call two functions the limit function and also create and build a graph function, which should work by using the reduced coords to create a estimation of the curve
        #Then simply evaluate it using the graph-values (which correspond to the correct input and output of an actual graph, and then  have logic to check if each tool is correct
        truth_list = []
        for i in tools_output:
            truth_list.append(i['correct'])
        
        correct = all(truth_list)
        return {'correct': correct, 'feedback':'Currently -hardcoded feedback'}
            

    
    
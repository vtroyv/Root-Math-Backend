from ..sketch.limits import limit
from ..sketch.graph import graph
from ....utils.others.llm import llm_sketch_feedback

# Now i should simply just adapt this to handle requests coming from both questionsByTopics and 

# ALSO handle the case where no reduced Coordinates are given and in this case, provide generic
#  feedback like draw a sketch to get feedbak

# 
def feedback_sketch_task(response):
    
    try:
         tool = response.task.task.marking['tool'] 
    except(AttributeError):
        tool = response.questionData['marking']['tool']
        
    print('The tool in this case is ', tool)
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
    if tool == 'graph':
        print('we are in the graphyy')
        try:
            guide = response.task.task.marking['guide'] #in the case of lesson task
        except(AttributeError):
            guide = response.questionData['marking']['guide'] #in the case of question
            
            
        tools_output = []
        coords = response.reducedCoordinates
        tools_output.append(graph(coords, guide))
        # print('the tools output from the guide is ', tools_output)
        correct = tools_output[0]['correct']
        if (correct != True):
            in_correct_features = []
            comparison_list = tools_output[0]['comparison']
            print('the comparison list is ', comparison_list)
            
            for i in comparison_list:
                if (i['is_correct'] != True):
                    in_correct_features.append(i['label'])

            feedback_blocks = guide['feedback']['response']
            
            labels = []
            for i in coords:
                labels.append(i['label'])
                
            print('the incorrect features are ', in_correct_features)
            
            if (response.questionData['degree'] == 2):
                # print('the length is given by ', len(in_correct_features))
                
                if (len(in_correct_features) == len(labels) ):
                    feedback = feedback_blocks['all']
                    
                elif len(in_correct_features) == 2:
                    feature_set = set(in_correct_features)
                    
                    if feature_set == {"first root", "second root"}:
                        
                        feedback = feedback_blocks["roots"]
                        
                    elif "y-intercept" in feature_set:
                        feedback = feedback_blocks["y-intercept"][:]
                        feedback.append({"type": "paragraph", "content": "Now additionally ..."})
                        if "first root" in feature_set:
                            feedback.extend(feedback_blocks["first root"])
                        elif "second root" in feature_set:
                            feedback.extend(feedback_blocks["second root"])

                else:
                    feedback = [{"type": "paragraph", "content": "Congrats you've only got one error:"}]
                    label = in_correct_features[0]
                    if label in feedback_blocks:
                        feedback.extend(feedback_blocks[label][:])
                    else:
                        feedback.append({"type": "paragraph", "content": "But we at RootMaths believe you can figure it out yourself goodluck lol "})
                    
                    
            
                
                
                        
            # print('The feedback being returned is ', feedback)    
            return {'correct': correct, 'feedback': feedback}
        else:
            return {'correct': correct, 'feedback':guide['feedback']['all-correct']}
            
            
        
    if (isinstance(tool, list)):
        # print(f'This question requires multiple functions to mark it requires {tool}')
        try:
            guide= response.task.task.marking['guide']
        except(AttributeError):
            guide = response.questionData['marking']['guide']
        
        
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
        print('The tools output is ', tools_output)
        for i in tools_output:
            truth_list.append(i['correct'])
        
        correct = all(truth_list)
        if correct: 
            return {'correct': correct, 'feedback': response.questionData['marking']['guide']['feedback']['all-correct']}
        
        else:
          print('The coorsd that we send are ', coords)  
          feedback = llm_sketch_feedback(coords,tools_output,guide )
          
          return {'correct': correct, 'feedback': feedback}
        
            

    
    
    
    
    
#--------------------
#The code below is generated, read through it and understand it later and see if it's a good template
#otherwise ignore it/delete
#------------------- 
    
#     from copy import deepcopy

# def _get_guide(response):
#     """Supports both lesson-task and question payload shapes."""
#     try:
#         return response.task.task.marking['guide']          # lesson task
#     except AttributeError:
#         return response.questionData['marking']['guide']    # question

# def _norm_bool(cmp_item):
#     """Handle either 'ok' or 'is_correct' keys from graph()."""
#     if 'ok' in cmp_item: 
#         return bool(cmp_item['ok'])
#     if 'is_correct' in cmp_item:
#         return bool(cmp_item['is_correct'])
#     # default safe fallback
#     return False

# def _feedback_blocks_node(guide):
#     """
#     Fetch the feedback->response node and be resilient to small typos
#     (e.g., 'repsonse'). Also return 'all-correct' if present.
#     """
#     fb = guide.get('feedback', {})
#     resp = fb.get('response') or fb.get('repsonse') or {}
#     all_correct = fb.get('all-correct', [])
#     return resp, all_correct

# def _clone(blocks):
#     """Deep copy lists of blocks so we never mutate templates stored in guide."""
#     return deepcopy(blocks)

# def _combine(*parts):
#     """Concatenate multiple block lists safely."""
#     out = []
#     for p in parts:
#         if not p:
#             continue
#         out.extend(deepcopy(p))
#     return out

# # ------------------ main branch ------------------

# if tool == 'graph':
#     print('we are in the graphyy')

#     guide = _get_guide(response)

#     # Run tool
#     coords = response.reducedCoordinates
#     result = graph(coords, guide)            # -> {"correct": bool, "comparison": [...], "metric": "graph values"}
#     correct = bool(result.get('correct', False))

#     # If everything passed, return the prewritten “all correct” block if available
#     resp_node, all_correct_block = _feedback_blocks_node(guide)
#     if correct:
#         return {'correct': True, 'feedback': _clone(all_correct_block) or [
#             {"type": "heading", "level": 3, "content": "Great work!"},
#             {"type": "paragraph", "content": "Your sketch matches the target behavior at all checked features."}
#         ]}

#     # Build list of incorrect feature labels from the comparison list
#     comparison_list = result.get('comparison', [])
#     incorrect_labels = []
#     for item in comparison_list:
#         # item might be: {"label": "...", "ok": bool, ...} or {"label": "...", "is_correct": bool, ...}
#         is_ok = _norm_bool(item)
#         if not is_ok:
#             lbl = item.get('label')
#             if lbl:
#                 incorrect_labels.append(lbl)

#     # Normalize to a set (order-agnostic)
#     inc = set(incorrect_labels)

#     # Degree-based paths (you can add more per-degree later)
#     degree = response.questionData.get('degree') if hasattr(response, 'questionData') else guide.get('degree', None)

#     # Safety: small helper to fetch a named block list (may be missing)
#     def B(name):
#         val = resp_node.get(name, [])
#         # Ensure it's a list; if a single dict slipped in, wrap it
#         if isinstance(val, dict):
#             return [val]
#         return val

#     # Helpful shared note you append when mixing y-intercept with a root
#     bridge_note = [{"type": "paragraph", "content": "Now additionally …"}]

#     # ---------- decision table for common quadratic (degree 2) cases ----------
#     if degree == 2:
#         # 0 already handled above (all correct)
#         if len(inc) == 1:
#             # just one feature off -> return that feature’s block directly if present
#             lbl = next(iter(inc))
#             return {'correct': False, 'feedback': _clone(B(lbl)) or [
#                 {"type": "paragraph", "content": f"There is an issue with your {lbl}. Revisit your calculation and adjust the point accordingly."}
#             ]}

#         if len(inc) == 2:
#             # {first root, second root} -> the “both roots” template
#             if inc == {"first root", "second root"}:
#                 return {'correct': False, 'feedback': _clone(B("roots"))}

#             # y-intercept + one root -> combine y-intercept then the specific root
#             if "y-intercept" in inc and ("first root" in inc or "second root" in inc):
#                 parts = [B("y-intercept"), bridge_note]
#                 if "first root" in inc:
#                     parts.append(B("first root"))
#                 if "second root" in inc:
#                     parts.append(B("second root"))
#                 return {'correct': False, 'feedback': _combine(*parts)}

#             # Fallback: combine whatever we have in alphabetical order
#             parts = []
#             for lbl in sorted(inc):
#                 parts.append(B(lbl))
#             return {'correct': False, 'feedback': _combine(*parts)}

#         if len(inc) >= 3:
#             # all three incorrect -> provide a comprehensive mix or a dedicated template if you add one
#             parts = [B("y-intercept"), bridge_note, B("roots")]
#             # If you ever add a dedicated template like B("all"), prefer that:
#             all_block = B("all") or B("all incorrect")  # optional names you might add later
#             fb = _clone(all_block) or _combine(*parts)
#             return {'correct': False, 'feedback': fb}

#         # Just in case: unknown shape -> minimal fallback
#         return {'correct': False, 'feedback': [
#             {"type": "paragraph", "content": "Some features do not match; revisit your intercepts and turning behavior."}
#         ]}

#     # ---------- generic (non-degree-specific) fallback ----------
#     if len(inc) == 1:
#         lbl = next(iter(inc))
#         return {'correct': False, 'feedback': _clone(B(lbl)) or [
#             {"type": "paragraph", "content": f"There is an issue with your {lbl}. Please review that calculation."}
#         ]}

#     if len(inc) > 1:
#         # Combine all relevant blocks in a stable order
#         parts = []
#         for lbl in sorted(inc):
#             parts.append(B(lbl))
#         return {'correct': False, 'feedback': _combine(*parts)}

#     # No labels found (unexpected) – return a safe fallback
#     return {'correct': False, 'feedback': [
#         {"type": "paragraph", "content": "We detected a mismatch, but could not identify which features. Please re-check roots and intercepts."}
#     ]}

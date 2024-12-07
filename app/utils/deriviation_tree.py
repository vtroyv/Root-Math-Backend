implication_operators ={
    
}


class TreeNode:
    def __init__(self, data):
        self.data= data
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
        
    #Create a function for depth-first traversal (pre-order)
    def pre_order_traversal(node):
        if node is None:
            return
        
        
        
        
        




# Use this file to create a tree based on the compliled sympy reponse. 
#It should be basically equivalent to a derivation tree on page 13 of the book


##### GENERAL PLAN/IDEA #########
#Convert the students response into a derivation tree, where each logic gate denotes a node. 
#e.g. cosx = 2sinx + 3, = would be the parent node and cosx would be the lfe child node, and + would be the right child node
#2sinx and 3 would be the children of the right child node

#Think i maybe don't need + or multiply to denote separating nodes, I should instead focus on 
#Logical gates like equal, implies, and, not, new lines of working etc, to denote logical gates. 

#Then once we have our tree we can convert the tree into conjunctive normal form, and thus make checks according to the mark scheme
#Alternatively, once our work is in the tree, we can make checks on the logical operators of the nodes. 

#As a very start perhaps focus on building this tree based on logical gates, 
#Then focus on performing checks to determine whether logical gates (i.e sympys assumptions library) are true or not

#later on  we will focus on creating theories that can integrate the markscheme in
#and also inherently do checking of logical gate/CNF form for us, e.g. SMT solvers.

#e.g. perhaps focus on having a predefined markscheme/theory, that states the valid assumptions and predicates/atoms of the question, 
#Then have a solver that checks if the students formulas (node (logical gate)+ children are satisfiable or not satisfiable). 

#Then perhaps at the end when accuracy of students work is checked, we can compare finally to a markscheme to get the returned output. 


#IMPORTANT NOTES TO BARE IN MIND

# - When defining a theory, interpretation will only be necessary for anonymous symbols, things like cos(x) or + which already have meanings won't require an interpretatio
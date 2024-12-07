#Store all derivation_trees ((potential) response trees), then build a decision tree
#That helps make decisions if it's seen the identical/ very similar tree before, based on the dataset

#Also check https://www.datacamp.com/tutorial/decision-tree-classification-python
#and https://www.datacamp.com/tutorial/decision-tree-classification-python, 
#The aim should be to look at previous trees, label them based on accuracy, and where the system made errors, 
#e.g. did i have to rely on some external tools e.g. gpt, or processing utils, to help answer the questions.
#Then if i see a similar tree once again, aim to cut out external api calls like gpt, via learning through experience 
#That is the purpose of the decision_Tree.py file. 

#Note that we don't have to stick with decision trees, but definitely some type of algorithm 
#That can learn from mistakes made when marking previous derivation_trees, aswell as remembering identical/similar derivation_trees, and speeding up the marking process. 
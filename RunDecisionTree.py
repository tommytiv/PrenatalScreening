import scr.DecisionTree as dt
import numpy as np


def age_adj_risk():
    return ((1/(1+np.exp(7.330-(4.211/(1+np.exp(-0.282*(MATERNAL_AGE-37.23))))))))
MATERNAL_AGE = 19

PRM = .0022
SFL= .43
TOP = .8

ULB_cost = 0    #   cost of Unaffected Live Birth
TLB_cost = 427577  # 	cost of Trisomy Live Birth
SFL_cost = 5    # 	cost of Spontaneous Fetal Loss
PRM_cost = 50   # 	cost of Procedure Related Miscarriage
TOP_cost = 581  # 	cost of Termination of Pregnancy
CVS_cost = 1010 # 	cost of chorionic villus sampling

# dictionary for decision nodes
#               // key: cost, utility, [future nodes]
dictDecisions = {'d1': [0,     0,       ['c1', 'c2']]};

# dictionary for chance nodes
#           // key: cost,   utility,  [future nodes],  [probabilities]
dictChances = {'c1': [CVS_cost,   0,       ['c3', 'c4'],    [age_adj_risk(), 1-age_adj_risk()]],
               'c2': [0,          0,       ['c5', 't9'],    [age_adj_risk(), 1-age_adj_risk()]],
               'c3': [0,          0,       ['c6', 't4'],    [1-PRM, PRM]],
               'c4': [0,          0,       ['t5', 't6'],    [1-PRM, PRM]],
               'c5': [0,          0,       ['t7', 't8'],    [SFL, 1-SFL]],
               'c6': [0,          0,       ['t1', 'c7'],    [TOP, 1-TOP]],
               'c7': [0,          0,       ['t2', 't3'],    [SFL, 1-SFL]]};


# dictionary for terminal nodes
#               //key: cost, utility
dictTerminals = {'t1': [TOP_cost,       0],
                 't2': [SFL_cost,       0],
                 't3': [TLB_cost,       0],
                 't4': [PRM_cost,       0],
                 't5': [ULB_cost,       0],
                 't6': [PRM_cost,       0],
                 't7': [SFL_cost,       0],
                 't8': [TLB_cost,       0],
                 't9': [ULB_cost,       0]};

#build the decision tree

myDT = dt.DecisionNode('d1', 1, dictDecisions, dictChances, dictTerminals)
print(myDT.get_cost_utility())

#myDT = dt.DecisionNode('d1', 1, dictDecisions, dictChances, dictTerminals)
#print(myDT.get_cost_utility())

# print the expected cost and utility of each alternative
#print('\nExpected cost and utility:')
#print(myDT.get_cost_utility())

# print the probability of terminal nodes under each alternative
#print('\nProbabilities of terminal nodes:')
#print(myDT.get_terminal_prob())

#plot the expected cost and utility of each alternative
#dt.graph_outcomes(myDT)

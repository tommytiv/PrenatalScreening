import COPYDecisionTreeModel as inp
import numpy as np


class Node:
    """ base class """
    def __init__(self, name, cost):
        """
        :param name: name of this node
        :param cost: cost of this node
        """
        self.name = name
        self.cost = cost

    def get_expected_cost(self):
        """ abstract method to be overridden in derived classes
        :returns expected cost of this node """
        raise NotImplementedError("This is an abstract method and needs to be implemented in derived classes.")


class ChanceNode(Node):

    def __init__(self, name, cost, future_nodes, probs):
        """
        :param future_nodes: future nodes connected to this node
        :param probs: probability of the future nodes
        """
        Node.__init__(self, name, cost)
        self.futureNodes = future_nodes
        self.probs = probs

    def get_expected_cost(self):
        """
        :return: expected cost of this chance node
        """
        exp_cost = self.cost  # expected cost initialized with the cost of visiting the current node
        i = 0
        for node in self.futureNodes:
            exp_cost += self.probs[i]*node.get_expected_cost()
            i += 1
        return exp_cost


class TerminalNode(Node):

    def __init__(self, name, cost):
        Node.__init__(self, name, cost)

    def get_expected_cost(self):
        """
        :return: cost of this chance node
        """
        return self.cost


class DecisionNode(Node):

    def __init__(self, name, cost, future_nodes):
        Node.__init__(self, name, cost)
        self.futureNode = future_nodes

    def get_expected_costs(self):
        """ returns the expected costs of future nodes"""
        outcomes = dict() # dictionary to store the expected cost of future nodes along with their names as keys
        for node in self.futureNode:
            outcomes[node.name] = node.get_expected_cost()

        return outcomes


#######################
# See figure DT3.png (from the project menu) for the structure of this decision tree
########################

def age_adj_risk():
    return ((1/(1+np.exp(7.330-(4.211/(1+np.exp(-0.282*(inp.AGE-37.23))))))))

PRM = .0022
SFL= .43
TOP = .8

ULB_cost = 0 #  Unaffected Live Birth
TLB_cost = 100 # 	Trisomy Live Birth
SFL_cost = 5 # 	Spontaneous Fetal Loss
PRM_cost = 50 # 	Procedure Related Miscarriage
TOP_cost = 581 # 	Termination of Pregnancy
CVS_cost = 1,010

# create the terminal nodes
T1 = TerminalNode('T1', TOP_cost)
T2 = TerminalNode('T2', SFL_cost)
T3 = TerminalNode('T3', TLB_cost)
T4 = TerminalNode('T4', PRM_cost)
T5 = TerminalNode('T5', ULB_cost)
T6 = TerminalNode('T6', PRM_cost)
T7 = TerminalNode('T7', SFL_cost)
T8 = TerminalNode('T8', TLB_cost)
T9 = TerminalNode('T9', ULB_cost)

# create C7
C7 = ChanceNode('C7', 0, [T2, T3], [SFL, 1-SFL])
# create C5
C5 = ChanceNode('C5', 0, [T7, T8], [SFL, 1-SFL])
# create C5
C6 = ChanceNode('C6', 0, [T1, C7], [TOP, 1-TOP])
# create C3
C3 = ChanceNode('C3', 0, [C6, T4], [1-PRM, PRM])
# create C4
C4 = ChanceNode('C4', 0, [T5, T6], [1-PRM, PRM])
# create C1
C1 = ChanceNode('C1', CVS_cost, [C3, C4], [age_adj_risk(), 1-age_adj_risk()])
# create C2
C2 = ChanceNode('C2', 0, [C5, T9], [age_adj_risk(), 1-age_adj_risk()])

# create D1
D1 = DecisionNode('D1', 0, [C1, C2])

# print the expect cost of C1
print(D1.get_expected_costs())



def simulate(self, ages):
    maternal_age = 15  # age, set to 15 to begin
    return myDT

        # age 40 years
        for i in range(ages):
            if maternal_age() < 56:
                myDT
            self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

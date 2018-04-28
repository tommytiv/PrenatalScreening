from enum import Enum
import matplotlib.pyplot as plt


class Properties(Enum):
    """ Index of parameters in decision and chance node dictionaries. """
    COST = 0
    UTILITY = 1
    NODES = 2
    PROB = 3


class Node:
    def __init__(self, name, cum_prob):
        """
        :param name:(string) key of the node in node dictionaries
        :param cum_prob: probability of visiting this node
        """
        self.name = name        # name of this node (also the key in the node dictionaries)
        self.cumProb = cum_prob  # probability of visiting this node
        self.cost = 0           # immediate cost of visiting this node
        self.utility = 0        # immediate utility of visiting this node
        self.eCost = 0          # expected cost of visiting this node (includes the immediate cost)
        self.eUtility = 0       # expected utility of visiting this node (includes the immediate utility)

    def get_terminal_prob(self):
        """ abstract method to be overridden in derived classes
        :returns probability of terminal nodes (if any) """
        raise NotImplementedError("This is an abstract method and needs to be implemented in derived classes.")


class DecisionNode(Node):
    def __init__(self, name, cum_prob, dict_decisions, dict_chances, dict_terminals):
        """
        :param name: (string) key of this decision node in the dictionary of decision nodes
        :param cum_prob: probability of visiting this node
        :param dict_decisions: dictionary of decision nodes
        :param dict_chances: dictionary of chance nodes
        :param dict_terminals: dictionary of terminal nodes
        """
        self.futureNodes = []  # list of future node objects

        # find if this node is in the decision dictionary
        if name in dict_decisions:
            # if found, initialize this node
            Node.__init__(self, name, cum_prob)
            # find the names of future nodes for this decision node
            names = dict_decisions[name][Properties.NODES.value]
            # add the future nodes
            self.futureNodes = create_future_nodes(names, dict_chances, dict_terminals)

        else:
            print('{} is not in the decision node dictionary'.format(self.name))

    def get_cost_utility(self):
        """ returns the expected cost and health utility of each decisions
        :return: dictionary of outcomes where key = node name and value =[expected cost, expected utility]
        """
        outcomes = dict()
        for node in self.futureNodes:
            outcomes[node.name] = [node.eCost, node.eUtility]

        return outcomes

    def get_terminal_prob(self):
        """ :returns a dictionary where key = the name of terminal nodes (if any) and values = probabilities """

        terminal_prob = dict()
        for node in self.futureNodes:
            # assign the terminal probabilities to a new key (the name of this future node)
            terminal_prob[node.name] = node.get_terminal_prob()

        return terminal_prob


class ChanceNode(Node):
    def __init__(self, name, cum_prob, dict_chances, dict_terminals):
        """
        :param name: (string) key of this chance node in the dictionary of chance nodes
        :param cum_prob: probability of visiting this node
        :param dict_chances: dictionary of chance nodes
        :param dict_terminals: dictionary of terminal nodes
        """
        self.futureNodes = []  # list of future node objects
        self.pFutureNodes = [] # probabilities of future nodes

        # find if this node is in the chance dictionary
        if name in dict_chances:
            # if found, initialize this node
            Node.__init__(self, name, cum_prob)

            self.cost = dict_chances[name][Properties.COST.value]            # find cost
            self.utility = dict_chances[name][Properties.UTILITY.value]      # find utility
            self.pFutureNodes = dict_chances[name][Properties.PROB.value]    # find probability of each future nodes

            # find the names of future nodes for this chance node
            names = dict_chances[name][Properties.NODES.value]
            # add the future nodes
            self.futureNodes = create_future_nodes\
                (names, dict_chances, dict_terminals, cum_prob, self.pFutureNodes)

        else:
            print('{} is not in the chance node dictionary'.format(self.name))

        # calculate expected cost and utility of this node
        self.eCost = self.cost          # adding the immediate cost
        self.eUtility = self.utility    # adding the immediate utility
        i = 0  # iterator in future nodes
        for node in self.futureNodes:
            # add the expected cost of this future node
            self.eCost += node.eCost * self.pFutureNodes[i]
            # add the expected utility of this future node
            self.eUtility += node.eUtility * self.pFutureNodes[i]
            # increment i
            i += 1

    def get_terminal_prob(self):
        """ :returns a dictionary where key = the name of terminal nodes (if any) and values = probabilities """

        terminal_prob = dict()
        for node in self.futureNodes:
            # add the terminal probabilities to this dictionary
            terminal_prob.update(node.get_terminal_prob())

        return terminal_prob


class TerminalNode(Node):
    def __init__(self, name, cum_prob, dict_terminals):
        """ Instantiating a terminal node
        :param name: key of this node
        :param cum_prob: probability of visiting this node
        :param dict_terminals: dictionary of terminal nodes
        """

        # find if this node is in the dictionary of terminal nodes
        if name in dict_terminals:
            # create the node
            Node.__init__(self, name, cum_prob)
            # find the cost of this node (for terminal nodes eCost = immediate cost)
            self.eCost = dict_terminals[name][Properties.COST.value]
            # find the utility of this node (for terminal nodes eUtility = immediate utility)
            self.eUtility = dict_terminals[name][Properties.UTILITY.value]

        else:
            print('{} is not in the terminal node dictionary'.format(self.name))

    def get_terminal_prob(self):
        """ :returns a dictionary where key = the name of this terminal node, and value = probability """

        terminal_prob = dict()
        # add a new entity (key = name of this terminal node, value = cumulative probability)
        terminal_prob[self.name] = self.cumProb

        return terminal_prob

def create_future_nodes(names, dict_chances, dict_terminals, cum_prob=1, p_future_nodes=[]):
    """ gets the names of future nodes and return the future node objects
    :param names: names of future nodes
    :param dict_chances: dictionary of chance nodes
    :param dict_terminals: dictionary of terminal nodes
    :param cum_prob: probability of visiting the current node (default 1 represents a decision node)
    :param p_future_nodes: probabilities of future nodes (default [] represents a decision node)
    :return: list of future nodes
    """

    future_nodes = []     # list of future nodes to return
    i = 0           # iterator in future nodes
    for name in names:
        cp = 0       # cumulative probability of this future node

        # check if probabilities of future nodes are provided
        if len(p_future_nodes) == 0:
            # if node, this is a decision node and hence the cp = 1
            cp = 1
        else:
            cp = cum_prob * p_future_nodes[i]

        # if this name is associated to a chance node
        if name in dict_chances:
            # create a chance node
            cn = ChanceNode(name, cp, dict_chances, dict_terminals)
            # append this node to the collection of future nodes
            future_nodes.append(cn)

        # if this name is associated to a terminal node
        elif name in dict_terminals:
            # create a terminal node
            cn = TerminalNode(name, cp, dict_terminals)
            # append this node to the collection of future nodes
            future_nodes.append(cn)

        i += 1

    return future_nodes


def graph_outcomes(decision_tree):
    """ plots the expected cost and expected utility of choices """

    # specify title and labels
    fig = plt.figure('cost vs. utility')
    plt.xlabel('health utility')
    plt.ylabel('cost')

    # build the legend and add the series
    names = []  # names of choices
    for key, cost_utility in decision_tree.get_cost_utility().items():
        plt.plot(cost_utility[1], cost_utility[0], 'o')
        names.append(key)

    # plot the legend
    plt.legend(names, loc='lower right')

    # specify the range of x and y-axes
    plt.xlim([0,1])
    plt.ylim(ymin=0)

    # save the figure
    plt.show()

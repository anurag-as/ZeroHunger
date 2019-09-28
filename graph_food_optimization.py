import networkx as nx
import matplotlib.pyplot as plt
from numpy import array


def get_graph():
    G = nx.Graph()
    return G


def add_node(G, name):
    G.add_node(name)
    return G


def calculate_weight(distance, type):
    distance = float(distance)
    if 'R' in type:
        distance = distance * 1.2
    return distance


def add_edge(G, e1, e2, distance, type):
    if 'R' in type:
        G.add_edge(e1, e2, color='g')
    else:
        G.add_edge(e1, e2, color='b')
    G[e1][e2]['weight'] = calculate_weight(distance, type)
    return G


G = get_graph()
nodes_list = open("countries.txt")
for node in nodes_list.readlines():
    add_node(G, node.strip())

routes_list = open("routes.csv")
for route in routes_list.readlines():
    e1, e2, distance, type = route.split(",")
    add_edge(G, e1, e2, distance, type)


def design_graph():
    #pos = nx.spring_layout(G)
    pos = {'Afghanistan': array([0.6547137 , 0.23380045]), 'Australia': array([ 0.03158262, -0.63200374]),
           'Brazil': array([-0.14201865, -0.10996432]), 'China': array([-0.11559148, -0.41866266]),
           'France': array([-0.46618438,  0.38498369]), 'Greece': array([-0.2331486 ,  0.70411025]),
           'India': array([ 0.28314053, -0.30444072]), 'Iraq': array([0.89231701, 0.61340584]),
           'Japan': array([-0.27181286, -0.41112809]), 'Kenya': array([0.32571651, 0.08222442]),
           'Republic of Korea': array([-0.04147944, -1.]), 'Russian Federation': array([-0.50210967, -0.26875588]),
           'South Africa': array([ 0.14463958, -0.13950966]), 'Spain': array([-0.50250254,  0.91165256]),
           'Syrian Arab Republic': array([0.33975101, 0.39591749]),
           'United States of America': array([-0.39701335, -0.04162964])}

    colors = [G[u][v]['color'] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, node_size=60, font_size=8, edge_color=colors, node_color='r')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
    plt.savefig("graph.png", dpi=1000)
    plt.show()
    return G

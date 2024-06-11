import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from torch_geometric.utils.convert import from_networkx

n = 10  # nombre de noeuds

max = 100
points = [[np.random.rand() * max, np.random.rand() * max] for i in range(n)]

nx_G = nx.complete_graph(n)
nx.set_node_attributes(nx_G, {i: {'pos': points[i]} for i in range(n)})



## Convertir en un graphe de PyTorch Geometric
# G = from_networkx(nx_G)

nx.draw(nx_G)
plt.show()

import os, json, random, argparse
from datetime import datetime
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



def gen(nb_nodes: int, density: float, attr_min: float, attr_max: float) -> nx.DiGraph:
    """
        nb_nodes: Nombre de noeuds du graphe.
        density: Proportion de liens présents par rapport à un graphe complet.
        attr_min: Valeur minimale de la position (axe X & axe Y).
        attr_max: Même chose pour la valeur maximale.
        
        Retourne une graphe orienté dont les noeuds sont les entiers de 0 à n.
        Les noeuds ont une liste de taille 2 comme attributs de position.
        Les arcs ont une chaîne de caractères comme attribut.
    """
    first_n_letters = list(range(nb_nodes))
    G = nx.complete_graph(first_n_letters, nx.DiGraph())

    # Dégradation: réduction de densité
    tbr = random.sample(
        tuple(G.edges()), 
        int(nx.number_of_edges(G) * (1 - p.density))
    )
    G.remove_edges_from(tbr)

    # Attributs
    for node in G.nodes():
        G.nodes[node]['pos'] = np.random.uniform(p.min, p.max, 2).tolist()

    for edge in G.edges():
        dir = ''
        src, dest = edge
        p1, p2 = G.nodes[src]['pos'], G.nodes[dest]['pos']
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]

        if abs(dx) > abs(dy):
            if dx > 0:
                dir = 'E'
            else:
                dir = 'W'
        elif abs(dy) > abs(dx):
            if dy > 0:
                dir = 'N'
            else:
                dir = 'S'
        else:
            if dy > 0:
                dir = 'N'
            elif dy < 0:
                dir = 'S'
            elif dx > 0:
                dir = 'E'
            elif dx < 0:
                dir = 'W'

        G.edges[edge]['dir'] = dir
    
    return G



def save(G: nx.Graph, filename: str) -> None:
    """
        Sauvegarder le graphe G sous format json. Permet de préserver les
        attributs des noeuds et des liens.
    """
    out_dir = f'./../in/' if os.path.basename(os.getcwd()) == 'src' else f'./in/'

    data = nx.node_link_data(G)

    with open(out_dir + filename, 'w') as f:
        json.dump(data, f)



def display(G: nx.Graph) -> None:
    """
        Afficher le graphe avec pyplot.
    """
    def get_color(dir: str) -> str:
        if dir == 'N':
            return 'green'
        elif dir == 'S':
            return 'purple'
        elif dir == 'W':
            return 'blue'
        else:
            return 'red'


    layout = {node: tuple(G.nodes[node]['pos']) for node in G.nodes}

    edge_colors = [get_color(v) for k, v in nx.get_edge_attributes(G, 'dir').items()]

    nx.draw(G, layout, node_size=50, edge_color=edge_colors, arrowsize=10)

    plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser('graph_generator')

    parser.add_argument('-n', '--nodes', help='number of nodes (default=10)', type=int, default=10)
    parser.add_argument('-d', '--density', help='density of the graph (default=0.15)', type=float, default=0.15)
    parser.add_argument('-m', '--min', help='node attribute minimum value (default=0.0)', type=float, default=0.0)
    parser.add_argument('-M', '--max', help='node attribute maximum value (default=1.0)', type=float, default=1.0)
    parser.add_argument('-i', '--image', help='show graph', action='store_true')
    parser.add_argument('-s', '--save', help='save graph to disk', action='store_true')

    p = parser.parse_args()

    G = gen(p.nodes, p.density, p.min, p.max)
    
    if p.save:
        save(G, f'G_n{p.nodes}_d{p.density}_{datetime.now().strftime("%d%f")}.json')
    
    if p.image:
        display(G)

import os, json, random, argparse
from datetime import datetime
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



def gen(nb_nodes: int, density: float, unknown: float) -> nx.DiGraph:
    """
        nb_nodes: Nombre de noeuds du graphe.
        density: Proportion de liens présents par rapport à un graphe complet.
        unknown: Proportion de noeuds sans position.
        
        Retourne une graphe orienté dont les noeuds sont les entiers de 0 à n.
        Les noeuds ont une liste de taille 2 comme attributs de position.
        Les arcs ont une chaîne de caractères comme attribut.
    """
    G = nx.complete_graph(range(nb_nodes), nx.DiGraph())

    # Réduction de densité: supprimer certains liens.
    tbr = random.sample(
        tuple(G.edges()), 
        int(nx.number_of_edges(G) * (1 - density))
    )
    G.remove_edges_from(tbr)

    # Attributs des noeuds.
    m = np.random.choice([0, 1], size=nb_nodes, p=[unknown, 1-unknown])
    for i, node in enumerate(G.nodes()):
        G.nodes[node]['pos'] = np.random.uniform(0.0, 1.0, 2).tolist() if m[i] else list()

    # Attributs des liens.
    for edge in G.edges():
        dir = 'N/A'
        src, dest = edge
        p1, p2 = G.nodes[src]['pos'], G.nodes[dest]['pos']

        if not p1 or not p2:
            G.edges[edge]['dir'] = dir
            continue

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
        Les noeuds apparaissent bleus s'ils ont leur attribut, ruoge sinon.
        Les arcs sont colorés selon leurs attributs:
            - Nord : vert
            - Sud : violet
            - Ouest: bleu
            - Est: rouge
            - sans direction: orange
    """
    def get_color(dir: str) -> str:
        if dir == 'N':
            return 'green'
        elif dir == 'S':
            return 'purple'
        elif dir == 'W':
            return 'blue'
        elif dir == 'E':
            return 'red'
        else:
            return 'orange'

    edge_colors = [get_color(v) for k, v in nx.get_edge_attributes(G, 'dir').items()]
    node_colors = ['red' if not v else 'blue' for k, v in nx.get_node_attributes(G, 'pos').items()]

    # Disposition des noeuds sur l'image
    layout = nx.kamada_kawai_layout(G)

    nx.draw(G, layout, node_size=50, arrowsize=10, node_color=node_colors, edge_color=edge_colors)

    plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser('graph_generator')

    parser.add_argument('-n', '--nodes', help='number of nodes (default=10)', type=int, default=10)
    parser.add_argument('-d', '--density', help='density of the graph (default=0.5)', type=float, default=0.5)
    parser.add_argument('-u', '--unknown', help='proportion of nodes without position (default=0.5)', type=float, default=0.5)
    parser.add_argument('-i', '--image', help='show graph', action='store_true')
    parser.add_argument('-s', '--save', help='save graph object to disk', action='store_true')

    p = parser.parse_args()

    G = gen(p.nodes, p.density, p.unknown)
    
    if p.save:
        save(G, f'G_n{p.nodes}_d{p.density}_{datetime.now().strftime("%d%f")}.json')
    
    if p.image:
        display(G)

import os, json, random, argparse
from datetime import datetime
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

"""
    gen
        nb_nodes: Nombre de noeuds du graphe.
        density: Proportion de liens présents par rapport à un graphe complet.
        unknown: Proportion de noeuds sans position.
        
        Retourne une graphe orienté dont les noeuds sont les entiers de 0 à n.
        Les noeuds ont une liste de taille 2 comme attributs de position.
        Les arcs ont une chaîne de caractères comme attribut.
    
    degrade

    gen_bulk

    save
        Sauvegarder le graphe G sous format json. Permet de préserver les
        attributs des noeuds et des liens.

    load

    display
        Afficher le graphe avec pyplot.
        Les noeuds apparaissent bleus s'ils ont leur attribut, ruoge sinon.
        Les arcs sont colorés selon leurs attributs:
            - Nord : vert
            - Sud : violet
            - Ouest: bleu
            - Est: rouge
            - sans direction: orange
"""


def gen(nb_nodes: int) -> nx.DiGraph:
    G = nx.complete_graph(range(nb_nodes), nx.DiGraph())

    for node in G.nodes:
        G.nodes[node]['pos'] = np.random.uniform(0.0, 1.0, 2).tolist()

    for edge in G.edges():
        dir = 'N/A'
        src, dest = edge
        p1 = G.nodes[src]['pos']
        p2 = G.nodes[dest]['pos']

        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        if abs(dx) > abs(dy):
            dir = "West" if dx > 0 else "East"
        else:
            dir = "South" if dy > 0 else "North"

        G.edges[edge]['dir'] = dir
    
    return G



def degrade(G: nx.Graph, density: float, relpos: float, unknown: float) -> nx.DiGraph:
    # Delete edges.
    remove = random.sample(
        tuple(G.edges()),
        int(nx.number_of_edges(G) * (1 - density))
    )
    G.remove_edges_from(remove)

    # Remove edge attribute.
    edges_tbr = random.sample(
        tuple(G.edges()),
        int(nx.number_of_edges(G) * relpos)
    )
    for edge in edges_tbr:
        G.edges[edge]['dir'] = 'N/A'

    # Remove node position attribute.
    nodes_tbr = random.sample(
        tuple(G.nodes()),
        int(nx.number_of_nodes(G) * unknown)
    )
    for node in nodes_tbr:
        G.nodes[node]['pos'] = list()
    
    return G



def gen_bulk(nb: int, nodes: int, density: float, relpos: float, unknown: float) -> None:
    id = datetime.now().strftime('%d%f')
    base = gen(nodes)

    filename = f'complete/{id}_n{nodes}d{density}r{relpos}u{unknown}.json'
    save(base, filename)

    for num in range(nb):
        G = degrade(base, density, relpos, unknown)
        
        filename = f'degraded/{id}_{num+1}.json'
        save(G, filename)



def save(G: nx.Graph, filename: str) -> None:
    out_dir = './../in/' if os.path.basename(os.getcwd()) == 'src' else './in/'

    data = nx.node_link_data(G)

    with open(out_dir + filename, 'w') as f:
        json.dump(data, f)



def load(id: int) -> list[nx.Graph]:
    path = './../in/degraded/' if os.path.basename(os.getcwd()) == 'src' else './in/degraded/'
    files = os.listdir(path)
    files.sort()
    graph_list = [i for i in files if i.startswith(str(id))]

    graphs = list()
    for g in graph_list:
        with open(path + g) as file:
            content = json.load(file)
            G = nx.node_link_graph(content)
            graphs.append(G)

    return graphs


def display(G: nx.Graph) -> None:
    def get_color(dir: str) -> str:
        if dir == 'North':
            return 'green'
        elif dir == 'South':
            return 'purple'
        elif dir == 'West':
            return 'blue'
        elif dir == 'East':
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
    parser.add_argument('-r', '--relpos', help='proportion of unlabelled edges (default=0.5)', type=float, default=0.5)
    parser.add_argument('-u', '--unknown', help='proportion of nodes without position (default=0.5)', type=float, default=0.5)
    parser.add_argument('-i', '--image', help='show graph', action='store_true')
    parser.add_argument('-s', '--save', help='save graph object to disk', action='store_true')

    p = parser.parse_args()

    # C = gen(p.nodes)
    # if p.save:
    #     save(C, f'complete/C_n{p.nodes}_d{p.density}_{datetime.now().strftime("%d%f")}.json')

    # G = degrade(C, p.density, p.relpos, p.unknown)
    # if p.save:
    #     save(G, f'degraded/G_n{p.nodes}_d{p.density}_{datetime.now().strftime("%d%f")}.json')
    
    # if p.image:
    #     display(G)

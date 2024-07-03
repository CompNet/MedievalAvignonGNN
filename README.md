# MedievalAvignonGNN
Vertex position estimation in spatial graphs


## Create a graph
The ```graph_generator``` script can be run by itself. It is also used by the other scripts as an import.

```
usage: graph_generator [-h] [-n NODES] [-d DENSITY] [-u UNKNOWN] [-i] [-s]

options:
  -h, --help            show this help message and exit
  -n NODES, --nodes NODES
                        number of nodes (default=10)
  -d DENSITY, --density DENSITY
                        density of the graph (default=0.5)
  -u UNKNOWN, --unknown UNKNOWN
                        proportion of nodes without position (default=0.5)
  -i, --image           show graph
  -s, --save            save graph object to disk
```

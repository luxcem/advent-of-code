import logging

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from sklearn.cluster import KMeans

test_input = """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

logger = logging.getLogger(__name__)


def part1(text_input: str) -> int | str:
    G = nx.Graph()
    for line in text_input.strip().split("\n"):
        component, connected = line.split(": ")
        connected = connected.split(" ")
        G.add_node(component)
        for c in connected:
            G.add_edge(component, c)

    pos = nx.spring_layout(G)
    node_positions = [pos[node] for node in G.nodes()]
    node_positions_array = np.array(node_positions)

    kmeans = KMeans(n_clusters=2, random_state=42)
    clusters = kmeans.fit_predict(node_positions_array)

    cluster_mapping = {node: cluster for node, cluster in zip(G.nodes(), clusters)}

    # Print the nodes in each cluster
    cluster_0 = [node for node, cluster in cluster_mapping.items() if cluster == 0]
    cluster_1 = [node for node, cluster in cluster_mapping.items() if cluster == 1]

    node_colors = [cluster_mapping[node] for node in G.nodes()]

    nx.draw(G, pos=pos, node_color=node_colors, cmap=plt.cm.tab10, with_labels=True)
    plt.show()
    return len(cluster_0) * len(cluster_1)


def part2(text_input: str) -> int | str:
    for line in text_input.strip().split("\n"):
        pass

    return 0

# Network-algorithms
A short script to create a network and run various algorithms on it.

The script supports two algorithms at the current time.
A function to find Euler cycles/paths and Dijkstra's algorithm.

The network is stored as a dictionary of nodes each with a dictionary of connections.
Most code I have seen for network algorithms especially eulers seems to store the network as it's edges
so I attempted a node based network as it seemed more logical a data structure especially with a large network.

The result of this was that the code was a little more complicated compared to an edge based data storeage
but not so much that I believe it to be an incorrect decision as I think the node based storage is nicer to visualize.

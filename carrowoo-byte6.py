import copy
import csv

# open the file you have downloaded
# these files are organized
file = open("amazon.txt")
# this returns an array with one entry for each line ni the file
# lines = csv.reader(file, delimiter=',', quotechar='|')
lines = file.readlines()
# print len(lines)
# 132308

# construct the graph

# a set is an unordered collection of unique elements
edges = set()

# this will store our nodes
nodes = {}

# divide the line into the node and all of its edges

# for each line in the file that was loaded in
for line in lines:
    # divide the line into the node and all of its edges
    line = line.split()
    a = int(line[1])
    b = int(line[0])
    # add the edge
    edges.add((a, b))
    # update the count for the number of times we've seen each node
    nodes[a] = nodes.get(a, -1) + 1
    nodes[b] = nodes.get(b, -1) + 1

# print "number of unique edges"
# print len(edges)
# print "number of unique nodes"
# print len(nodes)
#
# number of unique edges
# 114778
# number of unique nodes
# 63339

# get the degrees of each node in a set of edges
def get_degrees(edges):
    degree_counts={}

    # for each pair of nodes (edge)
    for i,j in edges:
        # increment the count for the number of edges connected
        # to each node by one
        degree_counts[i] = degree_counts.get(i, 0) + 1
        degree_counts[j] = degree_counts.get(j, 0) + 1
    return degree_counts

# Delete all nodes in delete_nodes from edges
def delete_node(edges, delete_nodes):
    # construct a new set of edges
    new_edges = []

    print "# of nodes to be deleted", len(delete_nodes)

    # loop through all the current edges
    for i, j in edges:
        # if an edges two nodes are not in the
        # set of nodes to be deleted
        if i not in delete_nodes and j not in delete_nodes:
            # append that edge to our new edges
            new_edges.append((i,j))
    return new_edges

# kcore algorithm
# We run the kcore algorithm to delete all
# the nodes whose cores are less than k
# returns a new set of edges and nodes
# including only those in the k core.
def kcore(edges, k):
    # make a complete copy of the edges so we can delete or change
    # things without messing up our original
    edges = copy.deepcopy(edges)
    # now for each pair of nodes, count the number of
    degree_counts = get_degrees(edges)
    # sort the nodes by degree and return
    # only the node numbers (not their degree)
    sorted_nodes = sorted(degree_counts, key = degree_counts.get)
    print "largest degree: ", degree_counts[sorted_nodes[0]]
    # repeatedly delete all nodes with degrees < k to find the k core
    # if we run out of nodes, or the largest count is < k we should stop
    while ((len(sorted_nodes) > 0) and (degree_counts[sorted_nodes[0]]<k)):
        # collect nodes with degrees < k in to_delete
        to_delete = set()
        for node in sorted_nodes:
            if degree_counts[node]<k:
                to_delete.add(node)
            else:
                break
        # delete all edges that include those nodes
        edges = delete_node(edges, to_delete)
        print "# of edges left:",len(edges)
        # recount the degrees for this (smaller) graph
        degree_counts = get_degrees(edges)
        # resort the nodes
        sorted_nodes = sorted(degree_counts, key = degree_counts.get)
    return edges, sorted_nodes

core_edges, core_nodes=kcore(edges, 4)
#
# # largest degree:  1
# # of nodes to be deleted 43663
# # of edges left: 65680
# # of nodes to be deleted 2059
# # of edges left: 61974
# # of nodes to be deleted 244
# # of edges left: 61494
# # of nodes to be deleted 49
# # of edges left: 61396
# # of nodes to be deleted 9
# # of edges left: 61378
# # of nodes to be deleted 1
# # of edges left: 61376

# We can use this method to create
# an adjacency matrix to represent the graph
def build_neighborhood(edges, nodes):
    neighborhood = {}
    for node in nodes:
        # create a place to store the neighbors
        neighborhood[node]=set()
        for edge in edges:
            # if either side of the edge contains node
            # add the other side as a neighbor
            if node == edge[0]:
                neighborhood[node].add(edge[1])
            if node == edge[1]:
                neighborhood[node].add(edge[0])
    return neighborhood

# This method is used to discover the connected components
# The basic idea is Breadth First Search
# We start from a node and find all the nodes it can reach
# In this way we can get a cluster of nodes which is called
# a connected component
# to start, we pass in the edges,
def get_connected_components(edges, neighborhood, nodes):
    result = []
    nodes = set(nodes)
    # keep track of what we've seen
    visited = set()
    # loop until there are no more nodes
    while nodes:
        # grab the first one
        node = nodes.pop()
        # create a new set for it
        component = set()
        # start searching from node
        queue = [node]
        while queue:
            # pick a node and mark as visited
            node = queue.pop(0)
            visited.add(node)
            # add it to our connected component
            component.add(node)
            # find all its neighbors
            neighbors = neighborhood[node]
            # add them to the queue (if we haven't seen them before)
            for neighbor in neighbors:
                if neighbor not in visited:
                    nodes.discard(neighbor)
                    queue.append(neighbor)
        result.append(component)
    return result

neighborhood = build_neighborhood(core_edges, core_nodes)
ret = get_connected_components(core_edges, neighborhood, core_nodes)
print "# of connected components",len(ret)

import networkx as nx
from networkx.readwrite import json_graph
import json

# create a graph and add al the edges
G=nx.Graph()
for edge in edges:
    G.add_edge(edge[0],edge[1])

nld = json_graph.node_link_data(G)
# We store the data in a json file
# So the javascript code can read it
json.dump(nld, open('force.json','w'))


# code to analyze undirected graphs
from pylab import *
import matplotlib.pyplot as plt

# get the degrees for each node (again)
nodes = get_degrees(edges)

v = nodes.values()
# this ensures that we don't have any values more than once
noRep = list(set(v))
noRep.sort()

x = []
y = []
for count in noRep:
    # f is the number of times this value occurs
    f = v.count(count)
    x.append(count)
    y.append(f)
figure()
loglog(x, y, '*')
xlabel('x')
ylabel('y')
title('power law plot')
show()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Python program to read
# json file
 
 
import json
import bbst
 
# Opening JSON file
f = open('p1.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
 
# Iterating through the json
# list
for d in data:
	print(data[d])
nodes_x = data["x"]
nodes_y = data["y"]
edge_source = data["edge_i"]
edge_dest = data["edge_j"]
'''
List of edges 
an edge will be in the form of
((start_x,start_y),(end_x,end_y))
'''
edges = []
 
# Closing file
f.close()
#  

def printList(givenList):
	for i in givenList:
		print(i)

def insert_event():
	return 0
	
def extract_event():
	return 0
	
def handle_event():
	return 0

def swap_edges():
	'''
	iterate over list and swap source and destination to get the highest values as sources
	|_Runtime O(n)
	'''
	for i in range(len(edge_source)):
		if nodes_y[edge_dest[i]] >  nodes_y[edge_source[i]]:
			tmp = edge_dest[i]
			edge_dest[i] = edge_source[i]
			edge_source[i] = tmp;

def get_coords(node):
	return ( nodes_x[node], nodes_y[node])

def create_edgelist():
	'''
	Add all edges to the edgelist by iterating over all edges
	|_O(n)
	Python sort uses Tim sort:
	|_time complexity O(nlog n) in average/worst case, best case O(n)
	'''
	
	for i in range(len(edge_source)):
		edges.append((get_coords(edge_source[i]),get_coords(edge_dest[i])));
	
	edges.sort(reverse = True, key=lambda x : x[0][1])

def create_eventlist():
	e_list = bbst.BSTNode()
	'''
	We can fill the e-list in a special way since we know that
	|_edge list is sorted in descending order
	|_we need to sort nodes_y in descending order
	'''
	edge_pointer = 0;
	for y in sorted(nodes_y, reverse=True):
		local_edge_list = []
		#print(y)#debug print
		if edge_pointer == len(edges):
			break
		while y == edges[edge_pointer][0][1] and edge_pointer < len(edges):
			local_edge_list.append(edges[edge_pointer])
			#print("\t",edges[edge_pointer]) #debug print
			edge_pointer += 1
			if edge_pointer == len(edges):
				break
		if len(local_edge_list) != 0:
			e_list.insert(val = y, data = (get_coords(nodes_y.index(y)),local_edge_list))
	return e_list
	
	
event_list = None
def main(args):
	'''
	1. preprocess the edges for a horizontal sweep
	if the destination is higher than the source, swap the elements.
	Allowed since it doesnt matter if they're undirected or directed
	'''
	swap_edges();
	create_edgelist();
	'''
	2. create the eventlist as a BBST
	!!for now its a BST find out how to do the conversion to BBST without rebuilding entire tree every time
	In the event tree, the nodes are stored, sorted by their y-value.
	Whenever a start point for an edge is inserted, the corresponding edge must be inserted as well for handling when updating the status queue.
	|_find a proper way to attach edges
	'''
	event_list = create_eventlist()
	'''
	handeling events will be:
	get event with event_list.get_max();
	add all possible new sections to status queue
	delete endpoint sections from status queue
	add new intersection events
	delete event from event list
	rinse and repeat untill event list is clear
	'''
	

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

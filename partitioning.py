#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Python program to read
# json file
 
 
import json
import bbst
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
import numpy as np
 
 


control = []
s_control = []
e_control = []
event_history = []
'''
List of edges 
an edge will be in the form of
((start_x,start_y),(end_x,end_y))
'''
edges = []
event_list = None
status_queue = None
# Closing file

nodes_x     = None
nodes_y     = None
edge_source = None
edge_dest   = None

#  
partitions = []		

'''
This function shows all partitions in one figure, different colors for different partitions for visibility
'''	
def show_partitions(name):
	fig, ax = plt.subplots()
	
	for p in partitions:
		ls = []
		for line in p:
			ls.append([line[0],line[1]])
		lc = mc.LineCollection(ls, linewidths=2, color=(np.random.random_sample(),np.random.random_sample(),np.random.random_sample()))
		ax.add_collection(lc)	
	plt.ylim([min(nodes_y),max(nodes_y)])
	plt.xlim([min(nodes_x),max(nodes_x)])
	ax.autoscale()
	ax.margins(0.1)
	plt.savefig(f"output/{name}.png")
	plt.show()	
'''
show just one partition, or list of lines
'''	
def show_partition(partition):
	fig, ax = plt.subplots()
	ls = []
	for line in partition:
		ls.append([line[0],line[1]])
	lc = mc.LineCollection(ls, linewidths=2, color=(np.random.random_sample(),np.random.random_sample(),np.random.random_sample()))
	ax.add_collection(lc)	
	plt.ylim([min(nodes_y),max(nodes_y)])
	plt.xlim([min(nodes_x),max(nodes_x)])
	ax.autoscale()
	ax.margins(0.1)
	plt.show()	
'''
Shows the status queue as it is initialized
(boolean) 	v		: 	show the picture
(int)		h_line	:	height of the sweepline
'''		
def show_statusqueue(sq,v = False, h_line = None):
	if sq == None:
		return
	queue = []
	sq.inorder(queue);
	ls = []
	order = []
	for segment in queue:
		for l in segment[1][3]:
			ls.append([l[0],l[1]])
	lc = mc.LineCollection(ls, linewidths=2)
	fig, ax = plt.subplots()
	if h_line != None:
		plt.hlines(h_line, min(nodes_x),max(nodes_x),colors="red")
	ax.add_collection(lc)
	plt.ylim([min(nodes_y),max(nodes_y)])
	plt.xlim([min(nodes_x),max(nodes_x)])
	ax.autoscale()
	ax.margins(0.1)
	if v == True:
		plt.show()

'''
just a function to nicely print a list
'''
def printList(givenList):
	for i in givenList:
		print(i)
		

'''
function to calculate the x position or a line segment for a given y
'''		
def calc_line(line,y):
	x1 = line[0][0];
	y1 = line[0][1];
	x2 = line[1][0];
	y2 = line[1][1];
	
	rc = (y2-y1)/(x2-x1)
	
	b = -(rc*x1 - y1)
	
	v = (y-b)/rc
	return round(v)
'''
function to swap an edge around so the highest point of the edge is the first coordinate
'''
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

'''
Function to return the coordinates of a node for a given node index
'''
def get_coords(node):
	return ( nodes_x[node], nodes_y[node])


'''
creates a list of edges 
'''
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

'''
(SLOW)
this implementation of a balance function for a BBST extracts ALL items from a bst in an ordered fashion and 
recreates it as a bbst
O(n*logn)

ToDo:
- switch from current structure to AVL tree
'''
def balance_bbst(bst):
	arr = []
	while bst != None:
		tmp_seg = bst.get_min()
		arr.append(tmp_seg)
		bst = bst.delete(tmp_seg[0])
	bst = bbst.sortedArrayToBST(arr)
	return bst


'''
This is the initial event list, so only start events are present in this list
'''
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
		if edge_pointer == len(edges):
			break
		while y == edges[edge_pointer][0][1] and edge_pointer < len(edges):
			local_edge_list.append(edges[edge_pointer])
			edge_pointer += 1
			if edge_pointer == len(edges):
				break
		if len(local_edge_list) != 0:
			e_list.insert(val = y, data = (0,get_coords(nodes_y.index(y)),local_edge_list,[]))
			e_list = balance_bbst(e_list);
	return e_list

'''
checks if bbst exists and inserts or updates the current node
'''	
def insert_in_bbst(queue, val, data):
	if queue == None:
		queue = bbst.BSTNode();
		queue.insert(val = val, data = data)
	else:
		if queue.exists(val) == True:
			queue.update(val = val, data = data)
		else:
			queue.insert(val = val, data = data)
	return queue

'''
updates the bbst with new height values
'''	
def update_sq(y,status_queue):
	tmp_sq = None
	inQ = 0;
	while status_queue != None:
		line_segment = status_queue.get_min()
		for line in line_segment[1][3]:
			tmp_sq = insert_in_bbst(tmp_sq, calc_line(line,y), (0,0,[],[line]))
			inQ += 1
			if inQ > 100:
				tmp_sq = balance_bbst(tmp_sq)
				inQ = 0
			
		status_queue = status_queue.delete(line_segment[0]) 
	
	return balance_bbst(tmp_sq)

'''
checks all lines in the partition with each other to see if they cross
'''
def check_partitions():
	
	for p in partitions:
		for x in p:
			for y in p:
				if x != y:
					if bbst.intersects(x,y) == True:
						print("\nStill intersections found")
						return
	print("\nNo intersections found")

'''
Function to determine the intersection coordinates of a line
'''
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return round(x), round(y)


'''
Function to check if there are intersections between any of the lines
'''	
def check_intersections(status_queue,y):
	order = status_queue.inorder([])
	intersections = []
	for i in range(1,len(order)):
		offset = 1
		while len(order[i-offset][1][3]) == 0:
			offset += 1
			if i-offset == 0:
				continue;
		for line_l in order[i-offset][1][3]:
			deletable = []
			for line_c in order[i][1][3]:
				if bbst.intersects(line_l, line_c) == True:
					intersections.append((line_l, line_c))
					deletable.append(line_c)
					if status_queue.can_delete(calc_line(line_c, y), line_c) == True:
						status_queue = status_queue.delete(calc_line(line_c, y))
			for d in deletable:
				order[i][1][3].remove(d)
						
						
	
	return status_queue, intersections
'''
Open the input file
'''
def load_set(filename):
	print(f"we use file: {filename}")
	# Opening JSON file
	f = open(filename)
	# returns JSON object as
	# a dictionary
	global nodes_x    
	global nodes_y    
	global edge_source
	global edge_dest  
	
	data = json.load(f)
	 
	# Iterating through the json
	# list
	for d in data:
		print(data[d])
	nodes_x     = data["x"]
	nodes_y     = data["y"]
	edge_source = data["edge_i"]
	edge_dest   = data["edge_j"]
	
	f.close


'''
Hnadles all types of events
events with a leading 0 are start or end events, others are intersection events
'''					
def handle_event(e_list, next_event, s_queue, next_partition, current_partition):
	event_list = e_list
	status_queue = s_queue
	if next_event[1][0] == 0:
		for line in next_event[1][2]:
			status_queue = insert_in_bbst(status_queue,val = line[0][0], data = (0,0,[],[line]))
			event_list = insert_in_bbst(event_list,val = line[1][1], data = (0,get_coords(nodes_y.index(line[1][1])),[],[line]))
		if status_queue != None:	
			status_queue = update_sq(next_event[1][1][1],status_queue)
			
			for line in next_event[1][3]:
				if status_queue == None:
					break;
				if status_queue.exists(val=calc_line(line, next_event[1][1][1])):
					if line in status_queue.get_data(val=calc_line(line, next_event[1][1][1]))[3]:
						partitions[current_partition].append(line)
						if status_queue.can_delete(calc_line(line, next_event[1][1][1]), line) == True:
							status_queue = status_queue.delete(calc_line(line, next_event[1][1][1]))
				
	
	
	#ends with rebalancing the status queue
	if status_queue != None:
		#status_queue = update_sq(next_event[1][1][1],status_queue) #maybe not needed now
		status_queue, intersections = check_intersections(status_queue,next_event[1][1][1])
		for i in intersections:
			next_partition = insert_in_bbst(next_partition, val = i[1][0][1], data=(0,i[1][0],[i[1]],[]))
			intersection_point = line_intersection(i[0],i[1])
			event_list = insert_in_bbst(event_list, val = intersection_point[1], data = (1,intersection_point,[],[]))
			if event_list.exists(i[1][1][1]) == True:
				if event_list.can_delete(i[1][1][1], i[1]) == True:
					event_list = event_list.delete(i[1][1][1])
	event_list = balance_bbst(event_list)
	return status_queue, event_list, next_partition
	
	
	
	
def main(args):
	f_name = "p1.json"
	if len(sys.argv) == 1:
		load_set("p1.json")
	else:
		f_name = sys.argv[1]
		load_set(sys.argv[1])
		
	visualize = True if "-v" in sys.argv else False
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
	print("start")
	status_queue = None
	current_partition = 0;
	event_counter = 0
	next_partition = None
	partitions.append([])
	while event_list != None:
		print(f"working on partition {current_partition} event {event_counter}",end='\r')
		event_counter += 1
		next_event = event_list.get_max();
		status_queue, event_list, next_partition = handle_event(event_list,next_event,status_queue,next_partition, current_partition)
		event_list = event_list.delete(next_event[0])
		
		if status_queue != None and visualize == True:
			show_statusqueue(status_queue, visualize, next_event[1][1][1])
		if event_list == None and next_partition != None:
			current_partition += 1
			event_counter = 0
			partitions.append([])
			event_list = balance_bbst(next_partition);
			next_partition = None
	show_partitions(f_name)
	check_partitions();
	
	
	

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

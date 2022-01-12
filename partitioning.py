#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Python program to read
# json file
 
 
import json
import bbst
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
 
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
f.close()
#  

def add_control_line(line):
	s = None
	e = None;
	for i in range(len(nodes_x)):
		if line[0][0] == nodes_x[i] and line[0][1] == nodes_y[i]:
			s = i
		if line[1][0] == nodes_x[i] and line[1][1] == nodes_y[i]:
			e = i;
	for i in range(len(edge_source)):
		if (edge_source[i] == s and edge_dest[i] == e) or (edge_dest[i] == s and edge_source[i] == e):
			return i
				
		
		
def show_statusqueue(sq,v = False, h_line = None):
	if sq == None:
		return
	queue = []
	sq.inorder(queue);
	ls = []
	order = []
	for segment in queue:
		order.append(segment[0])
		for l in segment[1][2]:
			ls.append([l[1][0],l[1][1]])
	print("sq order",order)
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
		

def printList(givenList):
	'''
	just a function to nicely print a list
	'''
	for i in givenList:
		print(i)
		
def calc_line(line,y):
	x1 = line[0][0];
	y1 = line[0][1];
	x2 = line[1][0];
	y2 = line[1][1];
	
	rc = (y2-y1)/(x2-x1)
	
	b = -(rc*x1 - y1)
	
	v = (y-b)/rc
	return v
		
def insert_line_sq(line,y,status_queue):
	'''
	check if the status queue is empty
	|_ if so, create a new bbst instance
	else
	|_ add the line segment to the status queue in the shape
	   val = horizontal position, data = ((x1,y1),(x2,y2))
	'''
	if status_queue == None:
		print("status queue was empty");
		status_queue = bbst.BSTNode()
		status_queue.insert(val = calc_line(line[1],y), data=(0,0,[line],[]))
	else:
		print("insert line in status queue")
		if status_queue.exists(val = calc_line(line[1],y)) == True:
			status_queue.update(val=calc_line(line[1],y), data = (0,0,[line],[])); 
		else:
			status_queue.insert(val = calc_line(line[1],y), data=(0,0,[line],[]))
	#status_queue = update_sq(y,status_queue)
	return status_queue
	
def delete_line_sq(line,y,status_queue):
	
	if status_queue == None:
		return status_queue
	status_queue = update_sq(y,status_queue);
	status_queue = status_queue.delete(calc_line(line,y));
	sq = []
	if status_queue != None:
		status_queue.preorder(sq)
	#printList(sq)
	return status_queue

'''
probleem nu:
- lijnen staan obv niet in general positie, niet over nagedacht
- in de status queue worden ze bijgehouden op hun x positie maar er kan er maar een per positie staan in de status queue

oplossing:
- update functie voor als hij al bestaat
- segmenten splitten in de update functie

- ik raak lijnen kwijt in de update functie :l
'''

def update_sq(y,status_queue):
	tmp_sq = None
	#print("update status queue" );#debug print
	pre = len(status_queue.preorder([]))
	#print(f"current event height: {y} ")
	while status_queue != None:
		line_segment = status_queue.get_min() #gets the data
		#print(f"ive got {len(line_segment[1][2])} segments")
		for line in line_segment[1][2]:
			#print(f"\t line: {line} goes from {line_segment[0]} to {calc_line(line[1],y)}")
			if add_control_line(line[1]) not in control:
				control.append(add_control_line(line[1]))
			tmp_sq = insert_line_sq(line,y,tmp_sq)
			
		status_queue = status_queue.delete(line_segment[0]) # hij delete meteen alle lijnen die op de current y eindigen, dus delete zelf is niet helemaal nodig tbh, maar voor de show
	status_queue = bbst.BSTNode()
	arr = []
	tussen = len(tmp_sq.preorder([]))
	#print("swap queues" );#debug print
	while tmp_sq != None:
		tmp_seg = tmp_sq.get_min()
		arr.append(tmp_seg)
		tmp_sq = tmp_sq.delete(tmp_seg[0])
	status_queue = bbst.sortedArrayToBST(arr)
	#print("\t\t\t done" );#debug print
	
	post = len(status_queue.preorder([]))
	print(f"array len difference {pre} -> {tussen} ->{post}")
	return status_queue
		
	

def insert_endpoint_event(bbst, y,edge):
	'''
	Check if the node exists then we have to update the data
	if the node does not exist then it will only be used for an endpoint event and we have to create it
	'''
	if bbst.exists(y) == True:
		bbst.update(val=y, data=(0,0,[],[edge]))
	else:
		bbst.insert(val=y,data=(0,get_coords(nodes_y.index(y)),[],[edge]))
	el = []
	bbst.preorder(el)
	#printList(el)
	
	
def check_intersections(status_queue):
	status_queue.check_intersections([])
	
def insert_intersection_event(bbst,y):
	'''
	This happens when two lines that are next to each other cross so we need to check if they intersect and then add the event to the event list.
	'''
	bbst.insert(val=y,data=(1,get_coords(nodes_y.index(y)),[],[]))
	
def extract_event():
	return 0
	
def handle_event(e_list,event_data,s_queue):
	'''
	we hebben 3 events
	|_het is een beginpoint voor een edge
	| |_voeg alle nieuwe edges toe in de juiste volgorde in de status queue
	| |_kijk voor mogelijke intersection points tussen edges
	| |_een beginpunt van een edge kan ook een endpoint zijn voor een andere edge
	|_het is een endpoint voor een edge
	| |_verwijder de edges uit de status queue
	|_het is een intersection tussen twee edges
	| |_wissel de edges om in de status queue en check voor nieuwe intersection points
	| |_kijk verdelen over partitions
	
	Gezien dat alle soorten events uiteindelijk kijken naar de intersection points tussen de lijnen kan je net zo goed dit na ieder event doen dan los
	'''
	status_queue = s_queue
	print("next event");
	if event_data[0] == 0:
		if len(event_data[2]) != 0:
			for e in event_data[2]:
				print("\t new line event");
				insert_endpoint_event(e_list,e[1][1],e)
				status_queue = insert_line_sq((0,e),e[0][1],status_queue)
				status_queue = update_sq(e[0][1],status_queue)
				if add_control_line(e) not in s_control:
					s_control.append(add_control_line(e))
				#show_statusqueue(status_queue)
		if len(event_data[3]) != 0:
			print("end point event");
			for e in event_data[3]:
				status_queue = delete_line_sq(e,e[1][1],status_queue)
				if add_control_line(e) not in e_control:
					e_control.append(add_control_line(e))
	
	if event_data[0] == 1:
		print("this is an intersection event");
		'''
		What should happen now;
		|_we have the current height, which doesn't really matter here, we should flip two edges
		'''
	if status_queue != None:
		check_intersections(status_queue);
	return status_queue

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
	'''
	This is the initial event list, so only start events are present in this list
	'''
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
			# The 0 in data willl indicate that this is an start/end-point to differentiate between intersection events
			#print(y, " -> list ->", local_edge_list)	#debug print
			e_list.insert(val = y, data = (0,get_coords(nodes_y.index(y)),local_edge_list,[]))
	return e_list
	
	
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
	status_queue = None
	while event_list != None:
		next_event = event_list.get_max();
		#shows the next event:
		#print("next event is:\t" ,next_event[0], next_event[1]); #debug print to check the next event
		status_queue = handle_event(event_list,next_event[1],status_queue)
		event_list = event_list.delete(next_event[0])
		if status_queue != None:
			event_history.append(next_event[0])
			show_statusqueue(status_queue, v=True, h_line = next_event[0])
	s_control.sort()		
	control.sort()	
	e_control.sort()		
			
	print("start event controle: ", s_control)
	print("statusqueue controle: ", control)
	print("end event   controle: ", e_control)
	printList(event_history)
	
	
	

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

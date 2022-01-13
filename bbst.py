class BSTNode:
	def __init__(self, val=None,data=None):
		self.left = None
		self.right = None
		self.val = val
		self.data = data

	def insert(self, val,data):
		if not self.val:
			self.val = val
			self.data = data
			return

		if self.val == val:
			return

		if val < self.val:
			if self.left:
				self.left.insert(val,data)
				return
			self.left = BSTNode(val,data)
			return

		if self.right:
			self.right.insert(val,data)
			return
		self.right = BSTNode(val,data)

	def get_min(self):
		current = self
		while current.left is not None:
			current = current.left
		return (current.val,current.data)

	def get_max(self):
		current = self
		while current.right is not None:
			current = current.right
		return (current.val,current.data)

	def delete(self, val):
		if self == None:
			return self
		if val < self.val:
			if self.left:
				self.left = self.left.delete(val)
			return self
		if val > self.val:
			if self.right:
				self.right = self.right.delete(val)
			return self
		if self.right == None:
			return self.left
		if self.left == None:
			return self.right
		min_larger_node = self.right
		while min_larger_node.left:
			min_larger_node = min_larger_node.left
		self.val = min_larger_node.val
		self.data = min_larger_node.data
		self.right = self.right.delete(min_larger_node.val)
		return self
	
	def can_delete(self,val,d_line):
		if val == self.val:
			newLines = []
			for line in self.data[2]:
				if line[1] != d_line:
					newLines.append(line);
					#print(d_line,"!=" ,line[1])
			#print(newLines)
			self.data = (self.data[0], self.data[1], newLines, self.data[3])
			#print(self.data)
			if len(newLines) != 0:
				return False
			else:
				return True

		if val < self.val:
			if self.left == None:
				return True
			return self.left.can_delete(val,d_line)

		if self.right == None:
			return True
		return self.right.can_delete(val,d_line)
		

	def exists(self, val):
		if val == self.val:
			return True

		if val < self.val:
			if self.left == None:
				return False
			return self.left.exists(val)

		if self.right == None:
			return False
		return self.right.exists(val)
		
		
	def get_data(self, val):
		if val == self.val:
			return self.data

		if val < self.val:
			if self.left == None:
				return False
			return self.left.get_data(val)

		if self.right == None:
			return False
		return self.right.get_data(val)

	def update(self, val, data):
		if val == self.val:
			#print(self.data)
			for d in data[2]:
				self.data[2].append(d)
			for d in data[3]:
				self.data[3].append(d)
			#print(self.data)
			return True

		if val < self.val:
			if self.left == None:
				return False
			return self.left.update(val,data)

		if self.right == None:
			return False
		return self.right.update(val,data)

	def preorder(self, vals):
		if self.val is not None:
			vals.append((self.val,self.data))
		if self.left is not None:
			self.left.preorder(vals)
		if self.right is not None:
			self.right.preorder(vals)
		return vals

	def inorder(self, vals):
		if self.left is not None:
			self.left.inorder(vals)
		if self.val is not None:
			vals.append((self.val,self.data))
		if self.right is not None:
			self.right.inorder(vals)
		return vals
		
	
	def check_intersections(self,intersections):
		if self.left is not None:
			self.left.check_intersections(intersections)
		if self.val is not None:
			if self.left is not None:
				#print("sorting data!");
				#print(self.left.data[2])
				self.left.data[2].sort(key=lambda x : x[1][0])
				#print(self.left.data[2][-1][1])
				if intersects(self.data[2][-1][1], self.left.data[2][-1][1]) == True:
					#print(f"lines {self.data[2][-1][1]} and {self.left.data[2][-1][1]} intersect")
					#print(f"\t increase {self.data[2][-1][0]} to {self.data[2][-1][0]+1} intersect")
					self.data[2][-1][0] =self.data[2][-1][0]+1;
				#check crossing functie
				'''
				Todo, check meest linkse van self met meest rechtse van self.left.data[2]
				|_ als deze kruisen dan passen we de partition aan van de lijn zodat de partion van de lijn partition(self.left.data[2](right))+1 wordt
				Todo, check meest rechtse van self met meest linkse van self.right.data[2]
				|_ als deze kruisen dan passen we de partition aan van de lijn zodat self.right.data[2](left) = +1 van de partition van self
				'''
		if self.right is not None:
			self.right.check_intersections(intersections)
		return intersections

	def postorder(self, vals):
		if self.left is not None:
			self.left.postorder(vals)
		if self.right is not None:
			self.right.postorder(vals)
		if self.val is not None:
			vals.append((self.val,self.data))
		return vals
		
	def check_depth(self,depth):
		res = depth + 1;
		right = self.right.check_depth(res) if self.right != None else res;
		left = self.left.check_depth(res) if self.left != None else res;
		
		return max(left,right)
		
		

def check_crossing_line(left,right):
	return False

def sortedArrayToBST(arr):
	 
	if not arr:
		return None
 
	# find middle
	mid = int((len(arr)) / 2)
	 
	# make the middle element the root
	root = BSTNode(val = arr[mid][0], data = arr[mid][1])
	 
	# left subtree of root has all
	# values <arr[mid]
	root.left = sortedArrayToBST(arr[:mid])
	 
	# right subtree of root has all
	# values >arr[mid]
	root.right = sortedArrayToBST(arr[mid+1:])
	return root


def on_segment(p, q, r):
	if r[0] <= max(p[0], q[0]) and r[0] >= min(p[0], q[0]) and r[1] <= max(p[1], q[1]) and r[1] >= min(p[1], q[1]):
		return True
	return False

def orientation(p, q, r):
	val = ((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1]))
	if val == 0 : return 0
	return 1 if val > 0 else -1

def intersects(seg1, seg2):
	p1 = seg1[0]
	q1 = seg1[1]
	p2 = seg2[0]
	q2 = seg2[1]
	if p1 == p2 or p1 == q2 or q1 == p2 or q1 == q2:
		return False

	o1 = orientation(p1, q1, p2)

	o2 = orientation(p1, q1, q2)
	o3 = orientation(p2, q2, p1)
	o4 = orientation(p2, q2, q1)

	if o1 != o2 and o3 != o4:#check general case

		return True

	if o1 == 0 and on_segment(p1, q1, p2) : return True#check special cases

	if o2 == 0 and on_segment(p1, q1, q2) : return True
	if o3 == 0 and on_segment(p2, q2, p1) : return True
	if o4 == 0 and on_segment(p2, q2, q1) : return True

	return False

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

	def update(self, val, data):
		if val == self.val:
			for d in data[2]:
				self.data[2].append(d)
			for d in data[3]:
				self.data[3].append(d)
			return True

		if val < self.val:
			if self.left == None:
				return False
			return self.left.exists(val)

		if self.right == None:
			return False
		return self.right.exists(val)

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

	def postorder(self, vals):
		if self.left is not None:
			self.left.postorder(vals)
		if self.right is not None:
			self.right.postorder(vals)
		if self.val is not None:
			vals.append((self.val,self.data))
		return vals

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

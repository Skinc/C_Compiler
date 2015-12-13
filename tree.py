"""

Tree(root) class will create a tree object 
with given root value.

tree.findLeave(leave) returns a boolean 
representing whether a certain value exsits
on the branchs of a given root of a tree.

tree.grow(left, right) will create a left 
branch and a right branch given the root of
a exsiting tree.

"""

class Tree(object):
    def __init__(self, value):
        # for a given node on the tree, there are only two branches: left and right
        self.left = None
        self.right = None
        self.data = value

    def findLeave(self, leave):
    	if (self.data == leave):
    		return True
    	if (self.left == None and self.right == None): # means that's the end of a tree
    		return False
    	return self.left.findLeave(leave) or self.right.findLeave(leave)

    def grow(self, left, right):
    	self.left = Tree(left)
    	self.right = Tree(right)


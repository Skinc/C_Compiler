class Tree(object):
    def __init__(self, value):
        self.left = None
        self.right = None
        self.data = value

    def findLeave(self, leave):
    	if (self.data == leave):
    		return True
    	if (self.left == None and self.right == None):
    		return False
    	return self.left.findLeave(leave) or self.right.findLeave(leave)

    def grow(self, left, right):
    	self.left = Tree(left)
    	self.right = Tree(right)


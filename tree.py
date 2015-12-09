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


def main():
	root = Tree("a")
	root.left = Tree("b")
	root.right = Tree("c")

	root.left.left = Tree("d")
	root.left.right = Tree("e")

	root.right.left = Tree("f")
	root.right.right = Tree("g")

	print root.findLeave("e")
	print root.findLeave("h")

if __name__ == "__main__":
    main()

import re
import string
import tree

class compiler:
	def __init__ (self, c_file):

		self.file_name = c_file
		rfile = open(self.file_name, "r")
		self.code_orig = rfile.read()
		rfile.close()
		self.code_array = self.code_orig.split("\n")

		self.single_assignment()
		self.create_lib()
		self.findRoot()
		self.populate(self.root)

	def write(self):
		wfile = open(  "%s_optimized.c" % ( self.file_name.split(".")[0]), "w")
		for l in self.code_array:
			wfile.write(l)
			wfile.write("\n")
		wfile.close()

	def findRoot(self):
		self.root = tree.Tree(self.code_array[-1][0])

	def populate(self, root):
		if root.data in self.lib:
			root.grow(*self.variable_seperator(self.lib[root.data]))
			self.populate(root.left)
			self.populate(root.right)
		else: return

	def create_lib(self):
		self.lib = {}
		for statement in self.code_array:
			self.lib[statement[0]] = statement

	def single_assignment(self):
		hashtable = {}
		variable = list(string.ascii_lowercase)
		variable_index = 25

		for statement in self.code_array:
			if statement[0] not in hashtable:
				hashtable[statement[0]] = 1
			else:
				j=0
				hashtable[statement[0]] += 1
				temp = statement[0]
				l=[]

				index = self.code_array.index(statement)
				while j <= index:
				 	self.code_array[j] = self.code_array[j].replace(statement[0], variable[variable_index])
				 	j += 1

				variable_index = variable_index-1
				self.code_array[index] = temp + self.code_array[index][1:]

	def common_subexpression_elimination(self):
		rhsList = []
		for statement in self.code_array:
			rhs = statement[statement.index('=') + 1:]
			if rhs in rhsList:
				self.replace_rhs(rhsList.index(rhs), self.code_array.index(statement), self.code_array[rhsList.index(rhs)].index("="), statement.index("="), self.code_array)
			rhsList.append(rhs)


	def copy_propagation(self):
		for statement in self.code_array:
			lhs = statement[:statement.index('=')]
			rhs = statement[statement.index('=') + 1:]
			if len(rhs) == 2:
				temp = lhs[0]
				self.code_array[self.code_array.index(statement) + 1:] = self.search_and_replace(self.code_array[self.code_array.index(statement) + 1:], temp, rhs[1])

	def dead_code_elimination(self):
		for statement in self.code_array:
			if not self.root.findLeave(statement[0]): self.code_array.remove(statement)


	def search_and_replace(self, myList, old, new):
		for statement in myList:
			myList[myList.index(statement)] = statement.replace(old, new)
		return myList

	def replace_rhs(self, indexList1, indexList2, indexString1, indexString2, myList):
		myList[indexList2] = myList[indexList2][:indexString2 + 2] + myList[indexString1][:indexString1 - 1]

	def variable_seperator(self, input):
		operator = ["+","-", "*", "/", "%", "<<"]
		myList = input.split(" ")
		opration = False

		for char in myList:
			if char in operator:
				var1 = myList[myList.index(char) - 1]
				var2 = myList[myList.index(char) + 1]
				opration = True
		
		if opration:
			return var1, var2
		else:
			return myList[myList.index("=") + 1], None

def main():
	c = compiler("test.txt")
	print c.code_array
	c.common_subexpression_elimination()
	print c.code_array
	c.copy_propagation()
	print c.code_array
	c.dead_code_elimination()
	print c.code_array

if __name__ == "__main__":
    main()

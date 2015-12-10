import re
import string
import tree

class compiler:
	
	def __init__ (self, c_file):

		# used for constant folding, feel free to move
		self.ops = {"+": (lambda x,y: x+y), "-": (lambda x,y: x-y), "*": (lambda x,y: x*y), "/": (lambda x,y: x/y), "%": (lambda x,y: x%y) }

		self.file_name = c_file
		rfile = open(self.file_name, "r")
		self.code_orig = rfile.read()
		rfile.close()
		self.code_array = self.code_orig.split("\n")
		self.constant_fold()
		
		self.single_assignment()
		self.findRoot()

		self.optimize()
		self.write()

	def optimize(self):
		preList = self.code_array[:]
		self.common_subexpression_elimination()
		self.copy_propagation()
		self.constant_fold()
		self.dead_code_elimination()
		if preList != self.code_array:
			self.optimize()
		else: return

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
			self.lib.pop(root.data)
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
			if statement is not "":
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
			myList = statement.split(" ")
			lhs = statement[:statement.index('=')]
			rhs = statement[statement.index('=') + 1:]
			if len(myList) == 3:
				temp = lhs[0]
				self.code_array[self.code_array.index(statement) + 1:] = self.search_and_replace(self.code_array[self.code_array.index(statement) + 1:], temp, rhs[1])

	def dead_code_elimination(self):
		self.create_lib()
		self.populate(self.root)
		for statement in self.code_array:
			if not self.root.findLeave(statement[0]): self.code_array.remove(statement)

	def constant_fold(self):
		outputs = []
		for l in self.code_array:
			out = l
			if ( ("="  in l) and not ("=="  in l)):
				line = l.split("=")
				LHS = line[0] + "= "
				RHS = line[1]
				inputs = re.split("[/+*\-%]+", RHS)
				if (len(inputs) is 2):
					input1 = inputs[0].replace(" ", "")
					input2 =inputs[1].replace(" ", "")
					if (input1.isdigit() and  input2.isdigit()):
					 	newValue = self.ops[RHS[len(inputs[0])]] (float(input1), float(input2))
						out = LHS + str(int(newValue) if newValue.is_integer() else newValue)

			outputs.append(out)
		self.code_array = outputs

	def search_and_replace(self, myList, old, new):
		for statement in myList:
			myList[myList.index(statement)] = statement.replace(old, new)
		return myList

	def replace_rhs(self, indexList1, indexList2, indexString1, indexString2, myList):
		myList[indexList2] = myList[indexList2][:indexString2 + 2] + myList[indexList1][:indexString1 - 1]

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

if __name__ == "__main__":
    main()

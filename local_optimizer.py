import re
import string
import math
import tree

class compiler:
	
	def __init__ (self, c_file):

		# used for constant folding, feel free to move
		self.ops = {"+": (lambda x,y: x+y), "-": (lambda x,y: x-y), "*": (lambda x,y: x*y), "/": (lambda x,y: x/y), "%": (lambda x,y: x%y) }

		self.file_name = c_file
		rfile = open(self.file_name, "r")
		self.code_orig = rfile.read()
		rfile.close()

		self.code_array = self.filter(self.code_orig.split("\n"))
		self.constant_fold()
		
		self.single_assignment()
		self.findRoot()

		self.optimize()
		self.write()

	def filter(self, array):
		offset = 0
		for i in range(len(array)):
			if (len(array[i+offset]) is 0) or array[i+offset].isspace():
				del array[i+offset]
				offset-= 1
		return array

	def optimize(self):
		preList = self.code_array[:]
		self.common_subexpression_elimination()
		print "CSE"
		print self.code_array

		self.copy_propagation()
		print "CP"
		print self.code_array

		self.constant_fold()
		print "CF"
		print self.code_array

		self.algebraic_simplification()
		print "AS"
		print self.code_array

		self.dead_code_elimination()
		print "DCE"
		print self.code_array

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
			root.grow(*self.variable_seperator_tuple(self.lib[root.data]))
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
					hashtable[statement[0]] = statement
				elif not statement == hashtable[statement[0]]:
					j=0
					temp = statement[0]
					l=[]

					index = self.code_array.index(statement)
					while j <= index:
					 	self.code_array[j] = self.code_array[j].replace(statement[0], variable[variable_index])
					 	j += 1

					variable_index = variable_index-1
					self.code_array[index] = temp + self.code_array[index][1:]
				else:
					self.removeSecond(statement)

	def removeSecond(self, statement):
		delete = False
		for i in range(len(self.code_array)):
			if self.code_array[i] == statement:
				if delete:
					self.code_array.pop(i)
					break
				else:
					delete = True

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
				self.code_array[self.code_array.index(statement) + 1:] = self.search_and_replace(self.code_array[self.code_array.index(statement) + 1:], temp, rhs[1:])

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

	def algebraic_simplification(self):
		for statement in self.code_array:
			var = self.variable_seperator_list(statement)
			if (len(var) == 3): 
				self.code_array[self.code_array.index(statement)] = statement[:3] + self.operation_simplification(var)

	def operation_simplification(self, var):
		rhs = ""
		other = True

		if var[1].isdigit() and var[2].isdigit():
			return " " + var[1] + " " + var[0] + " " + var[2]

		if var[1] == "0" or var[2] == "0":
			if var[1] == "0":
				rhs = " " + var[2]
				other = False
			if var[2] == '0':
				rhs = " " + var[1]
				other = False

		elif var[0] == "*":
			if var[1].isdigit():
				if self.check_two_exp(var[1]):
					num1 = int(var[1])
					if num1 == 1:
						rhs = " " + var[2]
					else:
						rhs = " " + var[2] + " << " + str(int(math.log(num1,2)))
					other = False
			if var[2].isdigit():
				if self.check_two_exp(var[2]):
					num2 = int(var[2])
					if num2 == 1:
						rhs = " " + var[1]
					else:
						rhs = " " + var[1] + " << " + str(int(math.log(num2,2)))
					other = False
		if other:
			rhs = " " + var[1] + " " + var[0] + " " + var[2]
		return rhs

	def dead_code_elimination(self):
		self.create_lib()
		self.populate(self.root)
		for statement in self.code_array:
			if not self.root.findLeave(statement[0]): self.code_array.remove(statement)

	def search_and_replace(self, myList, old, new):
		for statement in myList:
			myList[myList.index(statement)] = statement.replace(old, new)
		return myList

	def replace_rhs(self, indexList1, indexList2, indexString1, indexString2, myList):
		myList[indexList2] = myList[indexList2][:indexString2 + 2] + myList[indexList1][:indexString1 - 1]

	def variable_seperator_tuple(self, input):
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

	def variable_seperator_list(self, input):
		operators = ["+","-", "*", "/", "%", "<<"]
		myList = input.split(" ")
		opration = False

		for char in myList:
			if char in operators:
				var1 = myList[myList.index(char) - 1]
				var2 = myList[myList.index(char) + 1]
				opration = True
				return [char, var1, var2]
		return []

	def check_two_exp(self, num):
		num = int(num)
		return ((num & (num - 1)) == 0) and num != 0

def main():
	c = compiler("test.txt")

if __name__ == "__main__":
    main()

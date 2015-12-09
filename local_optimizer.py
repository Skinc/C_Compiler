import re
import string
import tree.py

class compiler:
	def __init__ (self, c_file):
		self.file_name = c_file
		rfile = open(self.file_name, "r")
		self.code_orig = rfile.read()
		rfile.close()
		self.code_array = self.code_orig.split("\n")
		self.write()

	def write(self):
		wfile = open(  "%s_optimized.c" % ( self.file_name.split(".")[0]), "w")
		for l in self.code_array:
			wfile.write(l)
			wfile.write("\n")
		wfile.close()

	def Single_Assignment(self):
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

	def commonSubexpressionElimination(self):
		rhsList = []
		for statement in self.code_array:
			rhs = statement[statement.index('=') + 1:]
			if rhs in rhsList:
				self.replaceRhs(rhsList.index(rhs), self.code_array.index(statement), self.code_array[rhsList.index(rhs)].index("="), statement.index("="), self.code_array)
			rhsList.append(rhs)


	def copyPropagation(self):
		for statement in self.code_array:
			lhs = statement[:statement.index('=')]
			rhs = statement[statement.index('=') + 1:]
			if len(rhs) == 2:
				temp = lhs[0]
				self.code_array[self.code_array.index(statement) + 1:] = self.searchAndReplace(self.code_array[self.code_array.index(statement) + 1:], temp, rhs[1])

	def searchAndReplace(self, myList, old, new):
		for statement in myList:
			myList[myList.index(statement)] = statement.replace(old, new)
		return myList

	def replaceRhs(self, indexList1, indexList2, indexString1, indexString2, myList):
		myList[indexList2] = myList[indexList2][:indexString2 + 2] + myList[indexString1][:indexString1 - 1]

def main():
	c = compiler("test.txt")
	c.Single_Assignment()
	c.commonSubexpressionElimination()
	c.copyPropagation()

if __name__ == "__main__":
    main()

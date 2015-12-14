import re
import string
import math
import tree

"""

optimizer(filename) class will create a 
local optimizer given the name of a file 
lives under directory "./test/". The file 
will first be transformed into single 
assignment form, and perform a series of
optimizations until the file cannot be 
further optimized. The series of 
optimization techniques, namely, are 
common subexpression elimination, copy 
propagation, constant folding, algebraic 
simplification and dead code elimination,
in order.

"""

class optimizer:

	"""

	The initialing phase of the optimizer reads 
	the input file, get rid of semicolons and blank
	lines, and perform single-assignment-
	transformation. Meanwhile, the optimizer finds
	the root of the syntax tree for optimization 
	uses. Then, the optimizer go through optimization 
	phase and write to a file in the directory 
	"./optimize/".

	"""
	
	def __init__ (self, c_file, debug = False): # in debug mode, optimizer will print() for debugging uses

		# used for constant folding
		#dictionary used to turn a string operator into actually performing the operation
		self.ops = {"+": (lambda x,y: x+y), "-": (lambda x,y: x-y), "*": (lambda x,y: x*y), "/": (lambda x,y: x/y), "%": (lambda x,y: x%y), "<": (lambda x,y: x*(2**y)), ">": (lambda x,y: x*(2**(y*-1))) }
		self.verbose = debug # indication of debug mode

		# starts reading from raw file
		self.file_name = c_file
		rfile = open("./rawcode/" + self.file_name, "r")
		self.code_orig = rfile.read()
		rfile.close()
		# end reading and get the raw file

		# transfroms the string buffer to a list by spliting on new line charactor
		self.code_array = self.filter(self.code_orig.split("\n"))
		self.semicolonProcessing() # takes away semicolons
		
		self.single_assignment() # performs single-assignment transformation
		self.findRoot() # finds the syntax root and build a tree upon that

		self.optimize() # performs recursive optimization until the file cannot be further optimized 
		self.write() # write back to the according file in "./test/optimize/"

	"""

	self.semicolonProcessing() get rid of semicolons 
	by poping the last charactor in code array

	"""

	def semicolonProcessing(self):
		for statement in self.code_array:
			self.code_array[self.code_array.index(statement)] = statement[:-1]
	
	"""

	self.filter() gets rid of any lines in the code_array 
	that are that are empty or completely whitespace

	"""

	def filter(self, array):
		offset = 0 #used to keep track of where we are in the array
		for i in range(len(array)):
			#check if element of the array 0 length (is blank) or is made of whitespace
			if (len(array[i+offset]) is 0) or array[i+offset].isspace():
				del array[i+offset]
				offset-= 1
		return array

	"""

	self.optimize() performs common subexpression 
	elimination, copy propagation, constant folding, 
	algebraic simplification and dead code 
	elimination, in order.

	At the beginning of each iteration of optimize(),
	preList will make a copy of the current code
	array for later compare uses. 

	At the end of the optimize(), if preList is the 
	same as the code array after optimization, 
	optimization is considered done. Otherwise, 
	it will call self.optimize again.	

	"""

	def optimize(self):
		preList = self.code_array[:]
		self.common_subexpression_elimination()
		if self.verbose:
			print "CSE"
			print self.code_array

		self.copy_propagation()
		if self.verbose:
			print "CP"
			print self.code_array

		self.constant_fold()
		if self.verbose:
			print "CF"
			print self.code_array

		self.algebraic_simplification()
		if self.verbose:
			print "AS"
			print self.code_array

		self.dead_code_elimination()
		if self.verbose:
			print "DCE"
			print self.code_array

		if preList != self.code_array:
			self.optimize()
		else: return

	"""

	self.write() takes the generated code and writes into a
	c file in the optimize folder. 

	"""

	def write(self):
		wfile = open(  "./optimize/%s_optimized.c" % ( self.file_name.split(".")[0]), "w")
		wrapper_before = open("wrapper_open.txt", 'r')
		wfile.write(wrapper_before.read())
		wrapper_before.close()

		for l in self.code_array:
			wfile.write("	" + l + ";") #write each line of the code_array and and a ;
			wfile.write("\n ") #write a new line
		wfile.write( "	return " + self.root.data + ";\n")
		wrapper_after = open("wrapper_close.txt", 'r')
		wfile.write(wrapper_after.read())
		wrapper_after.close()
		wfile.close() #close the file

	"""

	self.findRoot() get the root of syntax tree.
	We assumed that the code block return the variable 
	in the left hand side of the final statement.

	"""

	def findRoot(self):
		self.root = tree.Tree(self.code_array[-1][0])

	"""

	self.populate(root) get a root of tree and build 
	the tree based on its dependency. The dependency
	between nodes can be referred from self.lib, which
	includes pairs of keys and values, with variable 
	name as key and right hand side of the statment 
	as value. Since we are populate on a single 
	assignment form, each key has only one value.

	For example, code block shown as following:

	a = b + c
	d = e
	f = a * d

	will generate a tree like this:

				f
			//  	\\
			d 		 a
		  // \\	   // \\
	   None   e	   b   c

	"""

	def populate(self, root):
		if root.data in self.lib:
			root.grow(*self.variable_seperator_tuple(self.lib[root.data]))
			self.lib.pop(root.data)
			self.populate(root.left)
			self.populate(root.right)
		else: return

	"""

	self.create_lib() create a library in the
	form that has pairs of keys and values that
	takes variable as keys and its right hand
	side as values.

	"""

	def create_lib(self):
		self.lib = {}
		for statement in self.code_array:
			self.lib[statement[0]] = statement

	"""
	self.single_assignment() change a raw code array
	to the form of single assignment, which means 
	any variable in the code should only be assigned 
	once. 

	If double assingment were found in the code, 
	all the previous place which holds the double 
	assigned variable will be replace with a new
	variable name, including the right hand side of 
	the second assignment.

	"""

	def single_assignment(self):
		hashtable = {} # a hashtable is created to record already appeared variables

		# a list of all the possible variabels
		variable = list(string.ascii_lowercase)
		variable_index = 25

		# loops through the code array
		for statement in self.code_array:
			if statement is not "":
				# records newly appeared variable names
				if statement[0] not in hashtable:
					hashtable[statement[0]] = statement
				# performs replacing if double assignment were spotted
				elif not statement == hashtable[statement[0]]:
					j=0
					temp = statement[0]
					l=[]

					# replaces the variable name with the end of possible variable names, starting from 'z',
					# before and including the current statement	
					index = self.code_array.index(statement)
					while j <= index:
					 	self.code_array[j] = self.code_array[j].replace(statement[0], variable[variable_index])
					 	j += 1

					# move the index forward
					variable_index = variable_index-1
					# change the variable name back on the current assignment
					self.code_array[index] = temp + self.code_array[index][1:]
				# handle the dubious assignment cases
				else:
					self.removeSecond(statement)

	"""

	self.removeSecond(statement) handle the case that
	dubious statment is appeared in the code. In this
	case, we cannot handle it as a simple double 
	assignment. We need to delete all dubious after
	the first statement.

	"""


	def removeSecond(self, statement):
		delete = False
		for i in range(len(self.code_array)):
			if self.code_array[i] == statement:
				# delete flag ignores the first and delete all the follower
				if delete:
					self.code_array.pop(i)
					break
				else:
					delete = True

	"""

	self.common_subexpression_elimination() optimizes
	by handling the statements with same right hand sides.

	For example:

	a = b + c
	d = b + c 

	will be changed to:

	a = b + c 
	d = a

	"""


	def common_subexpression_elimination(self):
		rhsList = [] # records all the right hand side as looping throughout the code array
		for statement in self.code_array:
			rhs = statement[statement.index('=') + 1:] # get right hand side of a statement
			# perform replacement if dubious right hand side were found
			if rhs in rhsList:
				self.replace_rhs(rhsList.index(rhs), self.code_array.index(statement), self.code_array[rhsList.index(rhs)].index("="), statement.index("="), self.code_array)
			# rhsList will still record the dubious right hand side to make index correct
			rhsList.append(rhs)


	"""

	self.copy_propagation() optimizes by handling 
	the case of single variable right hand side 
	statment, and propagate right hand side of 
	the statement to the following of code where
	left hand side variable is used.

	For example:

	a = 3
	c = a + b 

	will be changed to:

	a = 3
	c = 3 + b

	"""

	def copy_propagation(self):
		for statement in self.code_array:
			myList = statement.split(" ") # split the statement into components
			lhs = statement[:statement.index('=')] # get left hand side
			rhs = statement[statement.index('=') + 1:] # get right hand side
			# if the statememnt is of the form "a = b", perform copy propagation 
			# on all the statements after the current one
			if len(myList) == 3:
				temp = lhs[0]
				self.code_array[self.code_array.index(statement) + 1:] = self.search_and_replace(
					self.code_array[self.code_array.index(statement) + 1:],
					temp, rhs[1:])

	"""

		self.constant_fold() optimizes by folding 
	constants, which means if there are ever two
	constants and an operator on the RHS, we can replace
	them with the outcome. It handles +, -, /, *, <<, and >>.

	For example:

	a = 1 + 2
	b = 9 / 3 
	c = d * 4 

	will be changed to:

	a = 3
	b = 3
	c = d * 4

	"""


	def constant_fold(self):
		outputs = [] #temporary array to save changes. 

		for l in self.code_array:
			out = l #saving the line 
			if ( ("="  in l) and not ("=="  in l)):
				line = l.split("=")
				LHS = line[0] + "= "
				RHS = line[1]

				#used Python regex to split on any of the symbols
				inputs = re.split("<<|>>|[/+\*\-%]+", RHS) 
				# len() will be 2 if the python regex matched.		
				if (len(inputs) is 2):
					input1 = inputs[0].replace(" ", "")
					input2 =inputs[1].replace(" ", "")

					#check if both sides are nums (floats or ints)
					if (self.isnum(input1) and  self.isnum(input2)):
						#use dict self.ops to run the operation desrcribed in the string. 
						newValue = self.ops[RHS[len(inputs[0])]] (float(input1), float(input2))
						#replace the RHS with the newvalue
						out = LHS + str(int(newValue) if newValue.is_integer() else newValue)

			outputs.append(out) #add the output to the temporary array
		#replace the code_array with the new code_array
		self.code_array = outputs

	"""

	self.isnum(n) checks whether the input string is a valid number
	It is different to String.isdigit(), which only determines if 
	a string is an integer.

	"""

	def isnum(self, n):
		# check if string is an int
		if n.isdigit():
			return True
		try:
			float(n) #tries to cast a string to a float. 
			return True #if cast works, string is float, return True
		except ValueError:
			return False #if cast throws exception, then string is not float, return False

	"""

	self.algebraic_simplification() optimizes by replacing 
	expansive opration with simpler ones, or even removing.

	For example:

	a = b + 0 -> a = b
	a = b * 1 -> a = b
	a = b * 64 -> a = b << 6

	"""


	def algebraic_simplification(self):
		for statement in self.code_array:
			var = self.variable_seperator_list(statement) # get the right hand side components in list 'var'
			# if the right hand side contains algebraic operation, performs operation
			if (len(var) == 3): 
				self.code_array[self.code_array.index(statement)] = statement[:3] + self.operation_simplification(var)


	"""

	self.operation_simplification(var) replaces
	expensive algebraic operation with cheaper ones
	according to certain roles.

	roles are given below:

	1. a = b *(or /) 1 		->	 a = b
	2. a = b * 0 			->	 a = 0
	3. a = b +(or -) 0 		->	 a = 0
	4. a = b * 32(exp of 2) ->	 a = b << 5

	all the roles above are also applied to
	cases when variables switch places.

	All other cases will be returned as they
	are before to be handled by other optimizations

	"""

	def operation_simplification(self, var):
		rhs = ""
		other = True # indicates whether the statement falls to 
		# any of the given cases

		# return the original if it is job of constant folding
		if var[1].isdigit() and var[2].isdigit():
			return " " + var[1] + " " + var[0] + " " + var[2]

		# if one of the oprands are '0', return the other variable
		# if it is multiplication, return ' 0'
		if var[1] == "0" or var[2] == "0":
			if var[1] == "0":
				rhs = " " + var[2]
				other = False
			if var[2] == '0':
				rhs = " " + var[1]
				other = False
			if var[0] == "*":
				rhs = " 0"
				other = False

		# if the operation is multiplication, perform 2's exp checking
		elif var[0] == "*":
			# performs shift based on the position of constant variable
			if var[1].isdigit():
				if self.check_two_exp(var[1]):
					num1 = int(var[1])
					# if the number is 1, return the other variable
					if num1 == 1:
						rhs = " " + var[2]
					# if not, do shift
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

		# if the left hand side does not belong to 
		# any of the special cases, return the original statement
		if other:
			rhs = " " + var[1] + " " + var[0] + " " + var[2]
		return rhs

	"""

	self.dead_code_elimination() removes
	statements that is not depended by 
	the final return statement. In other 
	word, dead code will be removed to achieve
	better cache efficiency

	"""

	def dead_code_elimination(self):
		self.create_lib() # create a library for the code array
		self.populate(self.root) # build the syntax tree based on the root
		for statement in self.code_array:
			# remove the statement if it is not a leave of the tree
			if not self.root.findLeave(statement[0]): self.code_array.remove(statement)

	"""

	self.search_and_replace(myList, old, new)
	replace all "old" with "new" in the given
	list

	"""

	def search_and_replace(self, myList, old, new):
		for statement in myList:
			myList[myList.index(statement)] = statement.replace(old, new)
		return myList

	"""

	self.replace_rhs(indexList1, indexList2, 
	indexString1, indexString2, myList) replace 
	the right hand side of a given statement
	with that of another given statement in the 
	given list. 

	"""

	def replace_rhs(self, indexList1, indexList2, indexString1, indexString2, myList):
		myList[indexList2] = myList[indexList2][:indexString2 + 2] + myList[indexList1][:indexString1 - 1]

	"""

	self.variable_seperator_tuple(input) takes a
	statement and separates into components.

	This method will return a two-element tuple
	if the right hand side is an algebraic operation.

	It will return a tuple with variable 1 and None otherwise.
	"""

	def variable_seperator_tuple(self, input):
		operator = ["+","-", "*", "/", "%", "<<"] # includes all the valid operations
		myList = input.split(" ") # separates into components
		opration = False # boolean to decide the form of return tuple

		for char in myList:
			if char in operator:
				var1 = myList[myList.index(char) - 1]
				var2 = myList[myList.index(char) + 1]
				opration = True
		
		if opration: 
			return var1, var2 # returns the two oprands if algebraic operation is found
		else:
			return myList[myList.index("=") + 1], None # returns variable 1 and None otherwise

	"""

	self.variable_seperator_list(input) takes a 
	statement and separates into components.

	This method will return a three element list
	if the right hand side is an algebraic operation.

	It will return an emtpy list otherwise.

	"""

	def variable_seperator_list(self, input):
		operators = ["+","-", "*", "/", "%", "<<"] # includes all the valid operations
		# separates into components
		myList = input.split(" ")

		# if it is an algebraic operation, return a list with 
		# operation symbol, variable 1, variable 2 in order
		for char in myList:
			if char in operators:
				var1 = myList[myList.index(char) - 1]
				var2 = myList[myList.index(char) + 1]
				return [char, var1, var2]
		# otherwise, empty list will be returned
		return []

	"""

	self.check_two_exp(num) checks whether a number
	is a exponitial of 2

	"""

	def check_two_exp(self, num):
		num = int(num)
		return ((num & (num - 1)) == 0) and num != 0

	"""

	self.test() checks whether the optimized code created by the compiler
	is correct. It compares it to the code kept in the expected files.
	This system allows the code to consistently be checked so we know
	as soon as something is broken.
	If test is called for a compiled file that doesn't have an expected output, 
	we return False and print that there is no expected output.

	"""

	def test(self):

		#open the code generated by the compiler
		genfile = open("./optimize/" + self.file_name.split(".")[0] + "_optimized.c", "r")
		generated_code = genfile.read().replace(" ", "").replace("\n", "") #take out all space and lines
		genfile.close()

		#open the expected code
		
		try: 
			expfile = open("./expected/" + self.file_name.split(".")[0] + "_expected.c", "r")
			expected_code = expfile.read().replace(" ", "").replace("\n", "") #take out all space and lines
			expfile.close()

			#compare code for equality
			#return true if optimized code is the same as expected code
			if generated_code == expected_code:
				return True
			return False
		except IOError:
			print "Expected code not found for " + self.file_name.split(".")[0]
			return False

"""

testCompilers() runs the compiler test function for a variety of 
files we've designed to test important aspects of the compiler.

"""

def testCompilers():

	failed = 0
	passed = 0
	#get the files to be optimized:
	tests =  ["AStest.txt", "CPtest.txt", "CSEtest.txt", "DCEtest.txt", "DiffOfFourth.txt", "Heron.txt", "LawOfCosines.txt", "MultiplyAndDivide.txt", "SAFtest.txt", "ThreeSquares.txt" ]#["test_single_assignment.txt" , "test_constant_folding.txt", "test_algebraic_simplification.txt", "test_single_assignment.txt" ]
	for test in tests:
		c = optimizer(test)
		testName = test.split(".")[0]
		
		if c.test():
			# print testName + " Passed"
			passed += 1
		else: 
			print testName  + " Failed"
			failed += 1

	print str(passed) + " tests passed."
	print str(failed) + " tests failed."

	

def main():
	c = optimizer("MultiplyAndDivide.txt")
	testCompilers()


if __name__ == "__main__":
    
    main()

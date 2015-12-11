import math

def algebraic_simplification(myList):
	for statement in myList:
		var = variable_seperator_list(statement)
		if (len(var) == 3): 
			myList[myList.index(statement)] = statement[:3] + operation_simplification(var)

def operation_simplification(var):
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
			if check_two_exp(var[1]):
				num1 = int(var[1])
				if num1 == 1:
					rhs = " " + var[2]
				else:
					rhs = " " + var[2] + " << " + str(int(math.log(num1,2)))
				other = False
		if var[2].isdigit():
			if check_two_exp(var[2]):
				num2 = int(var[2])
				if num2 == 1:
					rhs = " " + var[1]
				else:
					rhs = " " + var[1] + " << " + str(int(math.log(num2,2)))
				other = False

	if other:
		rhs = " " + var[1] + " " + var[0] + " " + var[2]

	return rhs



	# if var[2] == '0' and var[1] == "+":
	# 	statement = statement[0:5]+ var[2]
	# elif var[2] == '0' and var[1] == "+":
	# 	statement = statement[0:5]+ var[0]
	# elif var[2] == '0' and var[1] == "*" or var[0] == '0' and var[1] == "*":
	# 	statement = statement[0:5]+ '0 '
	# elif (var[0].isdigit() == True and var[2].isdigit() == False):
	# 	if (check_two_exp(var[0]) == True and var[1] == "*" and type(var[2]) == str):
	# 		statement = statement[0:5]+ var[2] + " << " + str(int(math.log(float(var[0]),2)))
	# elif (var[2].isdigit() == True and var[0].isdigit() == False):
	# 	if check_two_exp(var[2]) == True and var[1] == "*" and type(var[0]) == str:
	# 		statement = statement[0:5]+ var[0] + " << " + str(int(math.log(float(var[2]),2)))	
	# return statement

def variable_seperator_list(input):
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

def check_two_exp(num):
	num = int(num)
	return ((num & (num - 1)) == 0) and num != 0

l= ["a = i * h", "b = 48 - 0", "c = 0 - 8", "k = "]
algebraic_simplification(l)


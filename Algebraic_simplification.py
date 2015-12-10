import math

def algebraic_simplification(input):
	l = variable_seperator(input)
	if l[0] == '0' and l[1] == "+":
		input = input[0:5]+ l[2]
	elif l[2] == '0' and l[1] == "+":
		input = input[0:5]+ l[0]
	elif l[2] == '0' and l[1] == "*" or l[0] == '0' and l[1] == "*":
		input = input[0:5]+ '0 '
	elif (l[0].isdigit() == True and l[2].isdigit() == False):
		if (check_two_exp(l[0]) == True and l[1] == "*" and type(l[2]) == str):
			input = input[0:5]+ l[2] + " << " + str(int(math.log(float(l[0]),2)))
	elif (l[2].isdigit() == True and l[0].isdigit() == False):
		if check_two_exp(l[2]) == True and l[1] == "*" and type(l[0]) == str:
			input = input[0:5]+ l[0] + " << " + str(int(math.log(float(l[2]),2)))
	print input

def variable_seperator(input):
	operator = ["+","-", "*", "/", "%"]
	for i in range(0, len(input)-1):
		if input[i] == "=":
			temp = i
		if input[i] in operator:
			var1 = input[temp+2:i-1]
			var2 = input[i+2:len(input)-1]
			l= [var1, input[i], var2]
	return l

def check_two_exp(num):
	num = int(num)
	return ((num & (num - 1)) == 0) and num != 0

l= " a = a * 32 "
algebraic_simplification(l)


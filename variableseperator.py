def variable_seperator(input):
	operator = ["+","-", "*", "/", "%"]
	for i in range(0, len(input)-1):
		if input[i] in operator:
			var1 = input[5:i-1]
			var2 = input[i+2:len(input)-1]
	return var1, var2


l=" a = b + c "
variable_seperator(l)
def variable_seperator(input):
	operator = ["+","-", "*", "/", "%", "<<"]
	myList = input.split(" ")
	opration = False

	for char in myList:
		if char in operator:
			var1 = myList[myList.index(char) - 1]
			var2 = myList[myList.index(char) + 1]
			opration = True
	
	if opration:
		print var1, var2
		return var1, var2
	else:
		print myList[myList.index("=") + 1]
		return myList[myList.index("=") + 1]
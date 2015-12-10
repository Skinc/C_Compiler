import re
ops = {"+": (lambda x,y: x+y), "-": (lambda x,y: x-y), "*": (lambda x,y: x*y), "/": (lambda x,y: x/y), "%": (lambda x,y: x%y) }

def constantFold(myList):
	outputs = []
	for l in myList:
		out = l
		if ( ("="  in l) and not ("=="  in l)):
			line = l.split("=")
			LHS = line[0] + "="
			RHS = line[1]
			inputs = re.split("[/+*\-%]+", RHS)
			if (len(inputs) is 2):
				input1 = inputs[0].replace(" ", "")
				input2 =inputs[1].replace(" ", "")
				if (input1.isdigit() and  input2.isdigit()):
				 	newValue = ops[RHS[len(inputs[0])]] (float(input1), float(input2))
					out = LHS + str(int(newValue) if newValue.is_integer() else newValue)

		outputs.append(out)
	return outputs



def main():
	myList = ["x = 1", "y = 2", "w = 1 + y", "z = x + 2", "m = x + y", "a = 1+2", "a = 2*2", "a = 9%2","a = 1/2", "a = 1-2"]
	myList = constantFold(myList)
	print myList

if __name__ == "__main__":
    main()
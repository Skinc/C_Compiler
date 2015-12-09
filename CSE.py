def commonSubexpressionElimination(myList):
	rhsList = []
	for statement in myList:
		rhs = statement[statement.index('=') + 1:]
		if rhs in rhsList:
			replaceRhs(rhsList.index(rhs), myList.index(statement), myList[rhsList.index(rhs)].index("="), statement.index("="), myList);
		rhsList.append(rhs)
	print myList

def replaceRhs(indexList1, indexList2, indexString1, indexString2, myList):
	myList[indexList2] = myList[indexList2][:indexString2 + 2] + myList[indexString1][:indexString1 - 1]

def main():
	myList = ["x = 1", "y = 2", "w = x + y", "z = x + y", "m = x + y"]
	commonSubexpressionElimination(myList)

if __name__ == "__main__":
    main()
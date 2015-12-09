def copyPropagation(myList):
	for statement in myList:
		lhs = statement[:statement.index('=')]
		rhs = statement[statement.index('=') + 1:]
		if len(rhs) == 2:
			temp = lhs[0]
			myList[myList.index(statement) + 1:] = searchAndReplace(myList[myList.index(statement) + 1:], temp, rhs[1])

def searchAndReplace(myList, old, new):
	for statement in myList:
		myList[myList.index(statement)] = statement.replace(old, new)
	return myList


def main():
	myList = ["x = 1", "y = 2", "w = x + y", "z = x + y", "m = x + y"]
	copyPropagation(myList)
	print myList

if __name__ == "__main__":
    main()
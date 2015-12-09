def Single_Assignment(input):
	hashtable = {}
	variable=list(string.ascii_lowercase)
	variable_index=25

	for i in range(0,len(input)-1):
		if  input[i][0] not in hashtable:
			hashtable[input[i][0]]=1
		else:
			j=0
			hashtable[input[i][0]]+=1
			l=[]
			for k in range(0,i-1):
				l=l+input[k]
				k=k+1
			# ''.join(map(str, l))
			# tempstring=''.join(map(str, c))
			# tempstring = tempstring.replace(input[i][0], variable[variable_index])
			while j < i:
			 	input[j]= [word.replace(input[i][0],variable[variable_index]) for word in input[j]]
			 	return
			variable_index=variable_index-1
			return input



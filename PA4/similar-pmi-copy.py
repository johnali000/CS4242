import sys
import os
import re
import math 
import numpy as np

def main(argv):
	windowSize = sys.argv[1]
	path = sys.argv[2]
	wordPairs = sys.argv[3]
	tokenLimit = sys.argv[4]
	allTokens =""
	with os.scandir(path) as entries:
		for entry in entries:
			f = open(entry, "r", encoding = "ascii", errors='ignore')
			text = f.read()
			allTokens += text
			f.close
	allTokens = allTokens.lower()
	allTokens = re.sub(r'([^a-z0-9])', '\n', allTokens)
	tokens = allTokens.split()
	f = open(wordPairs, "r")
	pairs = f.read()
	pairs = pairs.split("\n")
	del pairs[-1]
	if(tokenLimit == 'f'):
		tokenLimit = len(tokens)
#Time to make the matrix
	keyIndex = dict()
	count = []
	i = 0
	t = 0 
	for x in tokens:
		if((x not in keyIndex) and (i<int(tokenLimit))):
			keyIndex[x] = i
			count.append(0)
			i+=1
	matrix = np.empty((0,i), int)
	for t in range(i):
		emptyCount= [0]* i
		matrix=np.append(matrix, np.array([[0]*i]), axis=0)
	t = 0
	for t in range(len(tokens)):
		if(tokens[t] in keyIndex):
			w=0
			indexone = keyIndex[tokens[t]]
			num = count[indexone]
			num +=1
			count[indexone] = num
			for w in range(int(windowSize)):
				if(((t+w+1) < (len(tokens)-1)) and(tokens[t+(w+1)] in keyIndex)):
					indextwo = keyIndex[tokens[t+(w+1)]]
					value = matrix[indexone, indextwo] 
					value +=1
					matrix[indexone,indextwo] = value
	
	for x in pairs:
		vectorwords = x.split()
		pmi = 0
		cosine = -9999
		if((vectorwords[0] in keyIndex) and (vectorwords[1] in keyIndex)):
			indexone = keyIndex[vectorwords[0]]
			indextwo = keyIndex[vectorwords[1]]
			px = count[indexone]/len(tokens)
			py = count[indextwo]/len(tokens)
			pxy = matrix[indexone,indextwo]/len(tokens)
			if(pxy == 0): 
				pmi =  0
			else:
				pmi = math.log((pxy/(px*py)), 2)
				t=0
			vwsum = 0
			v2sum = 0
			w2sum = 0
			for t in range(i):
				v = matrix[indexone, t]
				w = matrix[indextwo, t]
				vwsum += (v*w)
				v2sum += (v*v)
				w2sum += (w*w)
			cosine = (vwsum/(math.sqrt(v2sum)*math.sqrt(w2sum)))
			print("%s %s %s %s %s %s %s \n"% (cosine, vectorwords[0], vectorwords[1], count[indexone], count[indextwo], matrix[indexone,indextwo], pmi ))
		else: 
			count1 = 0 
			count2 = 0
			if(vectorwords[0] in keyIndex):
				count1 = count[keyIndex[vectorwords[0]]]
			if(vectorwords[1] in keyIndex):
				count2 = count[keyIndex[vectorwords[1]]]
			print("%s %s %s %s %s %s %s \n"% (cosine, vectorwords[0], vectorwords[1], count1, count2, 0, pmi ))	

main(sys.argv)

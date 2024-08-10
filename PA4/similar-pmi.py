'''
Written by: Alicia John
Date:11/7/20

Overall - This computes word similarity from a word by word PMI co-occurance matrix

Example -

0.07343319470668533 new advancement 2009 1 1 14.52144743504305 

0.5236640692371516 election results 183 373 2 10.434977625237062 

0.7575478994396204 union workers 174 167 1 10.66706149545356 

0.1990335161249143 fire wildfire 195 1 0 0 

0.44228202041261877 ocean sea 48 75 0 0 

0.0 spiderman batman 1 5 0 0 


Algorithm - This program tokenizes an input and creates a matrix of the co-occurance of every unique word. The command line input takes in the window size, the text file to parse through and the 
amount of tokens in the corpus to count. The window size is used to count how many can be co-occurances 
when they occur with up to and including 3 intervening words between them. 
With the matrix the PMI is cacluted with the probability of word 1, word 2 and the probabilty of 
the co-occurance of word one and two. The cosine of the word vectors are used to determine the 
similarity of word one and two. The output is the cosine, word 1, word 2, count of word 1, count of 
word 2, co-occurance of word one and two and the PMI of word one and word two. 

'''

import sys
import os
import re
import math 
import numpy as np

def main(argv):
# Get the command line inputs
	windowSize = sys.argv[1]
	path = sys.argv[2]
	wordPairs = sys.argv[3]
	tokenLimit = sys.argv[4]
	allTokens =""
#Get and proccess all of the files in the directory that was passed in
	with os.scandir(path) as entries:
		for entry in entries:
			f = open(entry, "r", encoding = "ascii", errors='ignore')
			text = f.read()
			allTokens += text
			f.close
	allTokens = allTokens.lower() # make all letters lowercase
	allTokens = re.sub(r'([^a-z0-9])', '\n', allTokens)# only alphanumeric characters
	tokens = allTokens.split() #tokenization
	f = open(wordPairs, "r") # Get all of the word pairs to calculate PMI and cosine
	pairs = f.read()
	pairs = pairs.split("\n")
	del pairs[-1]
	if(tokenLimit == 'f'): #if the full corpus is being processed change it to the amount of words in the corpus
		tokenLimit = len(tokens)
#Time to make the matrix
	keyIndex = dict()
	count = []
	i = 0
	t = 0 
	for x in tokens: # for every token if the word is not in the dictionary add it
		if(x not in keyIndex):
			keyIndex[x] = i
			count.append(0)
			i+=1 # i is equal to the index the key word is associated with
	print("PA 4 computing similarity from a word by word PMI co-occurrence matrix, programmed by Alicia John. Tokens Size = %s , Window Size = %s, Corpus Size = %s \n" % (i, windowSize, tokenLimit))
	matrix = np.zeros((i,i), int) # make an matrix of zeros i is equal to the number of unique words
	t = 0
	for t in range(int(tokenLimit)): # for every word up to the limit count the co-occurances of the word pair.
		if(tokens[t] in keyIndex):
			w=0 # is used to get the following word(s) to calcuate the co-occurance
			indexone = keyIndex[tokens[t]] # this is used to find the row word 1 is located
			num = count[indexone]
			num +=1
			count[indexone] = num
			for w in range(int(windowSize)):
				if(((t+w+1) < (len(tokens)-1)) and(tokens[t+(w+1)] in keyIndex)):
					indextwo = keyIndex[tokens[t+(w+1)]] # this is used to find the column word two is located at
					# Get and increment the location of the matrix of the co-occurance
					value = matrix[indexone, indextwo] 
					value +=1
					matrix[indexone,indextwo] = value 
	
	for x in pairs: # for every word pair
		vectorwords = x.split() # split into two words
		pmi = 0
		cosine = -9999
		if((vectorwords[0] in keyIndex) and (vectorwords[1] in keyIndex)): # if the words are in the matrix
		# Calculate the PMI and cosine
			indexone = keyIndex[vectorwords[0]] #Gets the indexes the key are in the matrix and total counts
			indextwo = keyIndex[vectorwords[1]]
			#probability of word 1, word 2 and the co-occurance
			px = count[indexone]/len(tokens)
			py = count[indextwo]/len(tokens)
			pxy = matrix[indexone,indextwo]/len(tokens)
			if(pxy == 0): #if there are no co-occurances set pmi to 0
				pmi =  0
			else:
				pmi = math.log((pxy/(px*py)), 2) # calulated the pmi
				t=0
			#Calcuting the cosine
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
			if(math.isnan(cosine)): # if it divides by zero set cosine to -9999
				cosine = -9999
			print("%s %s %s %s %s %s %s \n"% (cosine, vectorwords[0], vectorwords[1], count[indexone], count[indextwo], matrix[indexone,indextwo], pmi )) # output
		else: # if the word is not in the key list set cosine to -9999 and find counts for other word if it occurs
			count1 = 0 
			count2 = 0
			cosine = -9999
			if(vectorwords[0] in keyIndex):
				count1 = count[keyIndex[vectorwords[0]]]
			if(vectorwords[1] in keyIndex):
				count2 = count[keyIndex[vectorwords[1]]]
			print("%s %s %s %s %s %s %s \n"% (cosine, vectorwords[0], vectorwords[1], count1, count2, 0, pmi ))	

main(sys.argv)

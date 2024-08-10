'''
Written by:Alicia John
Date: 10/24/20

Overall - A program that creates a decision list based on the unigrams and bigrams found in 
positive and negive reviews.

Example - python3 decisionlisttrainer.py sentiment-train.txt

seagal 0 5.950758041735145
bateman 1 4.926526091788051
"_chicken 1 4.926526091788051
chicken_run 1 4.926526091788051
gladiator 1 4.8821319724295975
maximus 1 4.836328282816473
leila 1 4.789022568038116
lifeless 0 4.761724217345127
lebowski 1 4.74011296755717
run_" 1 4.74011296755717
imamura 0 4.702830528291559

Algorithm - This parses positive and and negative reviews. Before creating the 
decision list, it tokenizes, does some not handling and add all bigrams to all reviews.
Then all occurances of each word are counted as well as total positive, negitive and unique words. 
The log2 prbability of each word is calculated, is its postive the word is classified as positive and if its negative
then its classified as negative. All tokens are then sorted by log2 probability and each token, classification and the absolute value 
log2 probability are outputed in a text file (decisionlist.txt)
'''
import sys 
import re 
from collections import defaultdict
import math
def main(argv):

	trainList = sys.argv[1] # Opens the training data 
	f = open(trainList, "r")
	allReviews = f.read() # all reviews
	f.close() 
	reviewList = allReviews.split("\n")
	del reviewList[-1]
	masterKeyList = [] # all unique tokens
	masterPosNegCount = defaultdict(list) #all tokens with positive and negative counts
	reviewToken = []
	total  = 0 
	pTotal = 0 # total positive word count
	nTotal = 0	 # total negative word count
	for i in reviewList:# Tokenizing, not handeling and adding bigrams to all reviews
		review = i.split()
		reviewToken = []
		del review[0]
		classer = reivew[0]
		del review[0]
		reviewToken = notHandle(review)
		reviewToken=extend(reviewToken)
		total += len(review)
		if(classer == "0"): # proccessing negative reviews
			j = 0 
			for j in range(len(reviewToken)): # For every token
				nTotal +=1
				if reviewToken[j] not in masterKeyList: # Adds new token to keylist and key pos neg counts
					value = reviewToken[j]
					masterKeyList.append(value)
					masterPosNegCount[reviewToken[j]].append(0)
					masterPosNegCount[reviewToken[j]].append(1)
					
				else: # Increases the negative counter
					temp = []
					temp = masterPosNegCount[reviewToken[j]]
					temp[1] = temp[1]+ 1
					masterPosNegCount[reviewToken[j]] = temp
					
		elif(classer == "1"):# proccessing positive reviews 
			j = 0 
			for j in range(len(reviewToken)):# For every token
				pTotal +=1
				if reviewToken[j] not in masterKeyList:# Adds new token to keylist and key pos neg counts
					value = reviewToken[j]
					masterKeyList.append(value)
					masterPosNegCount[reviewToken[j]].append(1)
					masterPosNegCount[reviewToken[j]].append(0)
					
				else: # Increases the positive counter
					temp = []
					temp = masterPosNegCount[reviewToken[j]]
					temp[0] = temp[0] + 1
					masterPosNegCount[reviewToken[j]] = temp	
	j=0 
	outf = open("decisionlist.txt", "w")
	decisionList = defaultdict(list)
	for j in range(len(masterKeyList)-1): # finds the log2 probability of each word
		temp = masterPosNegCount[masterKeyList[j]]
		posCount = temp[0] # total count of word in a positive context
		negCount = temp[1] # total count of word in a negative context
		pProbability = (posCount + 1)/(pTotal+ len(masterKeyList)) # probability of a word given that its positive
		nProbability = (negCount+1)/(nTotal + len(masterKeyList))# probability of a word given that its negative
		logp = math.log2(pProbability/nProbability) # log2 (positive probability/negative probability)
		if(logp < 0): # if the log2 probabiltity is negative then the classfication is negative else its positive
			classer = 0
		else: 
			classer = 1
		logp = abs(logp) # absolute value of log2 to make it easier to sort
		decisionList[masterKeyList[j]].append(classer)# create a dictionary to sort with to keep the data together
		decisionList[masterKeyList[j]].append(logp)
	sortedDecisionList = sorted(decisionList.items(), key=lambda x:x[1][1], reverse=True)# sort by largest log2	
	for key, (classed, log) in sortedDecisionList: 
		outf.write("%s %s %s\n" % (key, classed, log)) # creates decision list file
			
				 


def notHandle(review): # When a not is encountered append not to the rest of the words in the sentance
	i = 0	
	for i in range(len(review)-1):
		if(review[i] == "not"):
			notFound = True
			i+=1
			while(notFound == True):
				review[i] = "not_"+review[i]
				i+=1
				if((i == len(review)) or ((review[i] == ".") or (review[i] == "?") or (review[i] == "!"))):
					notFound = False
	return review 
		

def extend(review): # Create bigrams then append every bigram to the end of the review
	i = 0 
	j = 1
	length = len(review)-1
	for i in range(length):
		review.append(review[i]+"_"+review[j])
		j+=1
	return review


main(sys.argv)

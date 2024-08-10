'''
Written by: Alicia John
Date: 10/24/20

Overall - This is a program that determines the sentiment of test data based on a descion list

Example -  python3 decisionlisttest.py sentiment-test.txt decisionlist.txt
cv666_tok-13320.txt 0
cv535_tok-19937.txt 0
cv245_tok-19462.txt 1
cv561_tok-26915.txt 0
cv329_tok-17076.txt 1
cv235_tok-11172.txt 1
cv634_tok-28807.txt 1
cv236_tok-23452.txt 1
cv415_tok-28738.txt 0

Algorithm - This takes in the test data and the decision list. The test data is tokenized, 
not handled and all bigrams are added. Each word in the decision list is compared to each word in a review
until one is found. The word that matched is associated with with a positive or negative classification
so the review is assigned that classification. The title of the test review and the classification is 
outputed to a text file (sentimentanalysis.txt) 
'''
import sys 
import re 
from collections import defaultdict
import math

def main(argv):

	testList = sys.argv[1]  # opens and read test data
	f = open(testList, "r")
	allReviews = f.read() # all reviews
	f.close() 
	reviewList = allReviews.split("\n")
	del reviewList[-1] #removes the \n at the end of the file
	decisionList = sys.argv[2] # opens and reads decision list
	f = open(decisionList, "r")
	trainData = f.read()
	f.close()
	trainList = trainData.split("\n") # splits training data into induvidual words and classification
	trainDict = defaultdict(list) # will contain each word with the appropriate classification
	i =0
	keyList = []
	for i in range(len(trainList)-1): # setting up trainingDict
		temp = trainList[i].split()
		keyList.append(temp[0])
		trainDict[temp[0]].append(temp[1])
		outf = open("sentimentanalysis.txt", "w")
	for i in reviewList: # Tokenizing, not handeling and adding bigrams to all reviews
		review = i.split()
		title = review[0] #Get the title of review
		del review[0] #removes title
		del review[0] #removes __
		review = notHandle(review)
		review = extend(review)
		i=0
		j=0
		rating = getRating(review, keyList, trainDict) # Assigning the rating based on decision list
		outf.write("%s %s\n" % (title, rating))
	outf.close()
						
		
def notHandle(review):# When a not is encountered append not to the rest of the words in the sentance
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

def extend(review): # adds all bigrams into the review
	i = 0 
	j = 1
	lis =[]
	length = len(review)-1
	for i in range(length):
		lis.append(review[i]+"_"+review[j])
		j+=1
	return review

def getRating(review, keyList, trainDict): # Finds the first word in the decsion list that matches with the review
	for i in keyList:
		for j in review:
			if(j == i):
				rating = trainDict[i]
				return rating[0]

main(sys.argv)

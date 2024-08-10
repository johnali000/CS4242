'''
Written by: Alicia John
Date: 10/24/20

Overall - A program that test the accuracy, precision and recall of the sentiment analysis programs

Example -
66.83417085427136
61.0
69.31818181818183

Algorithm -  This compares the output of the test data to the true values of the 
each review. For each correct positive or negative the correct count, true postive and true negative counts increase.
For each incorrect positive or negative the correct count, false postive and false negative counts increase.
'''
import sys
import math 
from collections import defaultdict

def main(argv):
	testList = sys.argv[1] # Opens file associated with the testing results
	f = open(testList, "r")
	testData = f.read()
	f.close()
	testList = testData.split("\n")
	del testList[-1]
	testDict = defaultdict(list)
	i =0
	keyList = list()
	for i in range(len(testList)-1):# gets the title and classification an puts it into a dictionary
		temp = testList[i].split()
		value = temp[0]
		keyList.append(value) # makes a list of key values
		testDict[temp[0]].append(temp[1])
	goldList = sys.argv[2]# Opens file associated with the actual results
	f = open(goldList, "r")
	goldData = f.read()
	f.close()
	goldList = goldData.split("\n") 
	del goldList[-1]
	goldDict = defaultdict(list)
	i =0
	for i in range(len(goldList)-1):# gets the title and classification an puts it into a dictionary
		temp = goldList[i].split()
		goldDict[temp[0]].append(temp[1])
	correctCount=0
	incorrectCount=0
	trueneg = 0 # is a negative correct value
	truepos = 0 # is a positive correct value
	falsepos= 0 # is a positive uncorrect value
	falseneg =0 # is a negative incorrect value
	count = 0
	key = 0
	positive = 1
	negative = 0
	for key in range(len(keyList)):
		test = testDict[keyList[key]]
		gold = goldDict[keyList[key]]
		value = gold[0]
		#print(value)
		if(test[0] == gold[0]):
			if (int(value) == int(negative)): #correct negative review
				correctCount +=1
				trueneg += 1
				count +=1
			elif(int(value) == int(positive)): # correct positive review
				correctCount +=1
				truepos += 1
				count +=1
		else:
			if(int(value) == int(negative)): # incorrect negative review
				incorrectCount +=1
				falseneg += 1
				count +=1
			elif(int(value)==int(positive)): # incorrect positive review
				incorrectCount +=1
				falsepos += 1
				count +=1
	accurracy = ((correctCount/count)*100) # number of correct classifications over all reviews
	precision = ((truepos/(truepos+falsepos))*100)# precision based on positive reviews
	recall = ((truepos/(truepos+falseneg))*100)# recall based on positive reviews
	#print(accurracy)
	#print(precision) 
	#print(recall)
	f=open("sentimentresults.txt", "w")
	f.write("Accurracy: %s \n Presicion: %s \n Recall: %s" % (accurracy, precision, recall))
	f.close()



main(sys.argv)

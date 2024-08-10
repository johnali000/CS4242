'''
Written by: Alicia John
Date: 11/21/20

Overall - This is a Part of Speech evaluator that compares the test results with the true values

Example -
no DT DT :806

major JJ JJ :777

Eurobond NN NNP :1

Algorithm -  This program takes in inputs of the predicted results, the gold 
and the traing data(only for the counts). The program compares the predicted 
values to the key values. The accuracy is calculated from the correct values over
the total values. The output for this are the word, predicted tag, gold tag
and the count of the word in the training set. The last output is the accuracy.
'''
import sys
import re

def main(argv):
    #open all of command line arguemnets
    testdata = sys.argv[1]
    f = open(testdata, "r")
    test = f.read()
    keydata = sys.argv[2]
    f = open(keydata, "r")
    key = f.read()
    countdata = sys.argv[3]
    f = open(countdata, "r")
    count = f.read()
    test = test.split("\n")
    key = key.split("\n")
    countExcess = count.split("\n")
    del test[-1]
    del key[-1]
    del countExcess[-1]
    #Set up training data so we can get the appropriate counts
    keyer = dict()
    tag = dict()
    keyer = {}
    for t in countExcess:
        tag = {}
        countList = t.split() 
        tag["tag"] = countList[1]
        tag["count"] = countList[2]
        keyer[countList[0]] = tag
    correct = 0
    # for each item in the test/gold values
    for i in range(len(key)-1):
        if(test[i] == key[i]): # if they are the same count it as correct
            correct += 1
        #Split the word from the tag
        temp = re.split(r'(?<!\\)/', test[i]) 
        temp2 = re.split(r'(?<!\\)/', key[i])
        if temp[0] in keyer: # If the word occurs in the test data get the count
            temp3 = keyer[temp[0]]
            counter = temp3["count"]
        else:
            counter = 0
        print("%s %s %s :%s\n" % (temp[0], temp[1], temp2[1], counter) ) # print word, test tag, gold tag and count
    accuracy  = (correct/len(key)) * 100 # Calculate accuracy
    print(accuracy) # print accuracy



main(sys.argv)

    
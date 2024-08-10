'''
Written by: Alicia John
Date: 11/21/20

Overall - This program predicts the Part of Speech Tag of words in a testing 
set based on the most frequent tag in the training data and a set of rules 
for words in the training set and not in the training set. Mode 0 will ignore
rules and mode 1 will account for rules.

Example -
No/DT
,/,
it/PRP
was/VBD
n't/RB
Black/NNP
Monday/NNP
./.

Algorithm - This program takes in the mode, training data and testing set. 
The first thing the program does is tokenize the training data and testing set
The initial tagging will tag it based on the most frequent tag in the training data
and NNN if its not in the training data. If it is mode one, 5 rules are applied
to the known words and 5 differnet words are applied to the unknown words.
The five known word rules are if the word is not tagged as VB and the previous
word is tagged as RB and the count is less than 5 change to VB,f the word is not 
tagged as VB and the previous word is tagged as TP and the count is 
less than 5 change to VB, if a word starts with a capitial letter, the count is 
less tahn 200 and ends with an s  change to NNPS, if it ends with ed and 
the count is less than 5 change to VBN and if it ends with ing and 
the count is less than 5 change to VBG. The five rules for unknown values are 
if the word ends with ing change to VBG, if the word contains a number change to 
CD, if the word starts with a capitial letter change to NNP and if the word 
ends with an ly change to an ly and if the word contains an hypen split it.
Find the tags of each word in the hypened word. If all words have the same
tag set the word as that tag. If only one word has a tag set it as that tag.
If the words have different tags set it as JJ and if none of the words have
tags set it as NNN. The out put for this is the "word"/"tag".
'''

import re
import sys

def main(argv):
# Open all of the command line arguements
    mode = sys.argv[1]
    traindata = sys.argv[2]
    f = open(traindata, "r")
    training = f.read()
    testdata = sys.argv[3]
    f = open(testdata, "r")
    testing = f.read()
    Parser(training, testing, mode)

def Parser(train, test, mode):
    key = dict()
    tag = dict()
    key = {}
    trainerLines = train.split("\n") # tokenized the training list by lines
    del trainerLines[-1]
    for t in trainerLines: #Associates each word with its tag and count
        tag = {}
        trainList = t.split() 
        tag["tag"] = trainList[1]
        tag["count"] = trainList[2]
        key[trainList[0]] = tag
    testList = test.split("\n")
    txt = "pos-test-" + mode +".txt"
    outf = open(txt, "w") # Prepares file for output
    tagList = []
    i = 0
    for t in testList: #Tagging the test words
        if t in key: # If word occurs in test data
            if int(mode) == int(1): # mode 1
                temp = key[t]
                tag = temp["tag"] #inital tagging
                tag = KnownEnhance(t, key, tag, tagList, i, int(temp["count"])) # Sends to known rules
            else: # mode 0
                temp = key[t]
                tag = temp["tag"]
        else: # If the word is not in the training data
            if(int(mode) == int(1)): # mode 1
                tag = UnknownEnhance(t, key) # send to unknown rules
            else:
                tag = "NNN"
        tagList.append(tag)
        i += 1
        outf.write("%s/%s\n" % (t ,tag))
        

def UnknownEnhance(word, key): 
    if bool(re.match(r'\b\w+(ing)\b', word)): #A-1
        tag = "VBG"
    elif bool(re.match(r'\d', word)): #A-2
        tag = "CD"
    elif bool(re.match(r'\b^[A-Z]', word)): #A-3
        tag = "NNP"
    elif bool(re.match(r'\w+(ly)\b', word)):#A-4
        tag = "RB"
    elif (word.find("-")): #A-5
        hypenList = word.split("-") # Split by -
        tagList = list()
        for t in hypenList: # Each word in hyphen
            if(t in key): # If word is in key assign it a tag
                temp = key[t]
                tag = temp["tag"]
                tagList.append(tag)
        if(len(tagList) > 1): # If there is more than one tag
            #Check if all of the words have the same tag
            ele = tagList[0]
            c = True
            for t in tagList:
                if (c is True) and (ele != t):
                    c = False
            if(c is True):
                tag = ele
            else:
                tag = "JJ"
        elif(len(tagList) == 1): # if there is one tag set it as the tag
            tag = tagList[0]
        else: # if there are no tags set as NNN
            tag = "NNN"
    else:
        tag = "NNN"
    return tag

def KnownEnhance(word, key, tag, tagList, i, count):
    if((tag != "VB") and (i>0) and (tagList[i-1] == "RB") and count < 5): #B-1
        tag = "VB"

    elif((tag != "VB") and (i>0) and (tagList[i-1] == "TO") and count < 5): #B-2
        tag = "VB"
    elif(bool(re.match(r'\b^[A-Z]', word)) and bool(re.match(r'\b\w+(ed)\b', word)) and (count < 15)): #B-3
        tag = "NNPS"
    elif (bool(re.match(r'\b\w+(ing)\b', word)) and count < 5) : #B-4
        tag = "VBG"
    elif (bool(re.match(r'\b\w+(ed)\b', word)) and count < 5): #B-5
        tag = "VBN"
    
    return tag



main(sys.argv)


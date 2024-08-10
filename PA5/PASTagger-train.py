'''
Written by: Alicia John
Date: 11/19/20

Overall - This program goes through a set of training words and counts all

of the tags associated with each word. The tag that occurs most often will be
set as the tag of that word.

Example - 
Pierre NNP 6
Vinken NNP 2
, , 63251
61 CD 30

Algorithm - This program takes in a set of training data and tokensizes it. 
The word and tag are separated from each other and counted. The occurance 
of each tag with each word will be monitered. The tag that occurs most 
frequently is the tag associated with the word. The output is "word" "tag" "tag count".
'''
import re
import sys


def main(argv):
# Get the the training  data
    data = sys.argv[1] 
    f = open(data, "r")
    training = f.read()
#Send data to paser
    tagfreq = parser(training)
# Output results
    output(tagfreq)
    
    

def parser(data):
#Split data by new line
    dataList = data.split("\n")
    del dataList[-1]
    words = dict() #will contain all words
    tags = dict() # will contain all tags with each word
# For each line in the traing set
    for i in dataList:
        line = re.split(r'(?<!\\)/', i) # Split each by / unless a \ occurs before it 
        if(line[0] in words): # if the word already occured once
            temp = words[line[0]] 
            if(line[1] in temp): # If the tag already occured once with the current word
                words[line[0]][line[1]] += 1 # increment tag
            else: # add the tag
                words[line[0]][line[1]] = 1
        else: # Add the word and tag
            words[line[0]] = {}
            tags = {}
            tags[line[1]] = 1
            words[line[0]] = tags
        
    return words

def output(tagfreq):
    txt = "tagger-train-prob.txt"
    outf = open(txt, "w")# open a file for output
    for i in tagfreq:
        tag = tagfreq[i]
        key = max(tag, key=tag.get) # get the tag that occurs most frequently
        outf.write("%s %s %s\n" % (i ,key, tag[key])) # for each word output the word tag and theh frequency of tag
        

main(sys.argv)
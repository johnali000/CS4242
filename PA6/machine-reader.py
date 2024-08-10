'''
Written by: Alicia John
Date: 12/10/20

Overall - This is a program that takes the MCTEST by employing a sliding window in both modes and Part 
od Speech Tagging and Named Entities recognition in mode 1. The program will pick an answer based 
on the Answer with the highest score. 

Example - 
A A A A



Algorithm - 
PRE PROCESSING:
This program separates the file by tests by newlines. Then each test are separated 
by tabs. The story is keepp and the questions and answers are kept. The question and answers
are kept togeter using a dictionary. 

SLIDING WINDOW 

The sliding window size is determined by adding together the word count in the question and the answer it is
currently analyzing. The unique words in the question and answers are kept together in a list.
The sliding window looks at the story and it matches every word in the window with the 
unique words. That window is then assigned a score based on the words that are matched.
The score the answer is assigned is based on the window with the highest score.

MODE 1
 This mode will add to the score the answer is assigned from the sliding window.
 This will analyze the words in the question and answer and add points to the score based 
 on if all the criteria matched. 
'''
import re
import sys
import math
import spacy

def main(argv): 
    mode = sys.argv[1] # GET mode
    sysfile = sys.argv[2] # GET data files
    f = open(sysfile, "r")
    data = f.read()
    #data.lower()
    Parser(mode, data) # Parser function that picks an answer for each question

def Parser(mode,data):
    questions = data.split("\n")
    del questions[-1]
    for q in questions: # For each test
        questions = dict()
        story = list()
        allAnswers = list()
        temp = q.split("\t")
        story = temp[2] # The save the story
        story = re.sub(r'([.?,!-]+)', "", story)# removes puncuation for the story
        story = story.split()
        i = 3
        while( i < len(temp)): # for every item in the list after the 2 index
            options = list()
            question = temp[i] # Assgin the question
            question = re.sub(r'([?]+)', "", question) # Removes the question mark form the story
            for j in range(4): # the next four are the answer to the question
                i +=1 
                options.append(temp[i])
            questions[question] = options
            i +=1
        for key in questions: # For each question
            trueScore = list()
            for ans in questions[key]: #For each answer
                allScores = list()
                window = 0
                i=0
                endindex = 0
                slideWords = key + " " + ans # Combines question and answer string
                slideWords = slideWords.split()
                window  = len(slideWords) # Gets the number of words to create the sliding window size
                uniqueSlideWordes = set(slideWords) # Get all unique words
                for i in range(len(story)): #Goes through the story
                    j=0
                    j = i 
                    endindex = j + window  -1 # End index is the current first index + window size -1
                    score = 0        
                    if endindex < (len(story)): # Goes until the endindex is = the number of words in the story
                        while j < (endindex): # Goes through each word in the current window
                            c = 0
                            if story[j] in uniqueSlideWordes:
                                c = story.count(story[j])
                                score += math.log2(1 + (1/c)) # If a matched word is found add to the score
                            j += 1
                    allScores.append(score) # Keep the window score
                assignedScore = max(allScores) # Get the windoe wit the highest score
                if(mode == "1"):
                    #POS TAGGING
                    sp = spacy.load('en_core_web_sm')
                    ansTag = sp(ans)
                    questionTag = sp(key)
                    if("What" in key): # If what is in the question and the answer contains a noun increase the score
                      for t in range(len(ansTag)):
                             if((ansTag[t].tag_ == "NN") or ansTag[t].tag_ == "NNS"):
                                assignedScore += .3
                    elif(("Who" in key) or ("Where" in key)):# If who or where is in the question and the answer contains a proper noun increase the score
                        for t in range(len(ansTag)):
                            if((ansTag[t].tag_ == "NNP")):
                                assignedScore += .3
                            if((ansTag[t].ent_type_ == "LOC") and ("Where" in key)): # Named Entity is a Location 
                                assignedScore += .1
                            if(((ansTag[t].ent_type_ == "PERSON") or (ansTag[t].ent_type_ == "ORG"))  and ("Who" in key)):  # Named Entity is a Person or ORG
                                assignedScore += .1
                    elif(("many" in key) or ("old" in key)):
                        for t in range(len(ansTag)):
                            if((ansTag[t].tag_ == "CD")):
                               assignedScore += .3
                    #Named entites
                    #If the question contains a person and the answer contains a he or she increase the score
                    for r in range(len(questionTag)):
                        if(questionTag[r].ent_type_ == "PERSON"):
                            for t in range(len(ansTag)):
                                if(("He" in ans) or ("he" in ans) or ("She" in ans) or ("She" in ans)):
                                    assignedScore += .1
                        
                trueScore.append(assignedScore) # All score for each answer
            answerIndex = trueScore.index(max(trueScore)) # Gets the index of the score with the highest answer
            answer = ""
            if(answerIndex == int(0)):
                answer = "A"
            elif(answerIndex == int(1)):
                answer = "B"
            elif(answerIndex == int(2)):
                answer = "C"
            elif(answerIndex == int(3)):
                answer = "D"
            else:
                answer = "void"
            allAnswers.append(answer)
        print("%s\t%s\t%s\t%s\r" % (allAnswers[0], allAnswers[1], allAnswers[2], allAnswers[3]))



main(sys.argv)

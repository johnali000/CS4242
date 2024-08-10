'''
Written by:Alicia John
Date: 12/10/20

Overall - This program compares the answers from the programs and the gold answers
to see the accuracy of the MCTEST program

Example -
A A A A | A B C A | 2

Algorithm - This program goes by test by test to see how many answers are incorrect in the question 
and keeps track of how many answers are correct overall.
'''
import sys

def main(argv):
    ansFile = sys.argv[1]
    goldFile = sys.argv[2]
    f = open(ansFile, "r")
    ans = f.read()
    f = open(goldFile, "r")
    gold = f.read()
    ans = ans.split("\n")
    gold = gold.split("\n")
    del ans[-1]
    del gold[-1]
    total = 0
    correct = 0
    for i in range(len(gold)):
        #print(i)
        anscom = ans[i].split("\t")
        goldcom = gold[i].split("\t")
        incorrect = 0
        for j in range(4):
            total += 1
            if (anscom[j] is goldcom[j]):
                #print(total)
                correct += 1
            else:
                incorrect += 1
        print("%s | %s | %s \n" % (str(gold[i]),str(ans[i]),incorrect))
    print(correct/total)


main(sys.argv)
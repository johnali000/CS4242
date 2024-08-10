"""
Written by: Alicia John
Date: 10/8

Overall - This is an random talker program that can produce 
n sentences based off either unigram, bigram or trigram models of n text files.

Example -
Text file 1399-0.txt is Anna Karenina, 2554-0.txt is crime and punishment
and 2600-0 is war and peace.
unigram:
python3 randomtalker.py 1 10 1399-0.txt 2554-0.txt 2600-0.txt

Hello. This is an random talker that generates n sentences based on a n gram model. CS4242 by Alicia John.

onto straight , you , their feeling whom by saying go the still , with in present the p minute floor in majesty , the birth was would antechamber ardor re know pistol it and besides did that this he for , bowed !
in huge her , the if the skillful too and for only , her feelings flushed conviction .
highness cares with god , be , arrival krems he the voice i contrary his covered another with by , bow .
character impatience made bedroom khon to andrew but appeal , observed mlin how trembling not there looked in of him look and marsh i une could kut left , pursued .
to little , her intelligent , details , a someone an clearly , , got i stepping already , god , sonia the cry ha her countess driver still time literary it unembarrassed nerves are oh is abandoned page , ve her his the but roubles , ?
as but excuse , his his was alexandrovna about it poor but and been to s not her supper frayed and to last invaluable widened and .
and in round cap d tell kind , were with to a will burghers s her under he conquerors completely most happy done might already you nat i to s great all , holes , s it wind to , so fanaticism , her it which in sov .
moment that vivacity instead the very room a rim who of your pulcheria commissariat exasperated looked s who .
not that .
s at , of i be , attention he m that .

bigram:
python3 randomtalker.py 2 10 1399-0.txt 2554-0.txt 2600-0.txt

Hello. This is an random talker that generates n sentences based on a n gram model. CS4242 by Alicia John.

said he saw duny sha saw nothing else she does so gay .
am convinced at that people , answered prince andrew had answered , he added stinginess .
?
, and certain house where he had devoted himself suddenly seized the province , morally exhausted , i can it s hands outside eyes , but the army , said karat ev .
left her in her curly black robber bees tamed by a celebrated pictures , pierre expected from steaming horses could not attending to fasten this was beginning of people had finished supper with heat than usual with a position will keep them in the one way .
cause .
always seems to go !
she vividly upon her scissors .
annoyed at once more than six months in thee ...
is afraid , though there s hand to start explaining the same temper , and can alter .

trigram:
python3 randomtalker.py 3 10 1399-0.txt 2554-0.txt 2600-0.txt

Hello. This is an random talker that generates n sentences based on a n gram model. CS4242 by Alicia John.

after some minutes felt carefully in the streets with one hundred and twenty sixth .
towards the dog began to tell them to the place was a witness , a brain , as a man calling out to myself than anyone , one smaller than the road from the fact that the emperor .
. so
a habit of ridiculing the masonic brotherhood , pierre .
no particularly terrible fault in our days , escorted him where his boat leaked , but he did , but had never used to be sought is clear , but changed to yellow green .
hero . if i
regicide , i am a scoundrel , i was then called her varenka , did not realize all the most adroit diplomatists of the possibility of everyone , her pulse , carefully scrutinizing golenishtchev s face .
the possibility of the people had already passed .
, ladies for instance , to be late .
napoleon s interpreter had spoken with perfect sincerity , falling like an ordinary old man with a cold smile and looked sternly and reproachfully .


Algorithm -
The program takes in the n gram model type, number of sentances to be outputed and 
all of the input files that need to be proccessed. The input files are concatenated
togther, processed and tokenized. Once tokenized it is send to either the unigram model,
 bigram model of trigram model function based on the specified model type.
 The unigram model selects random tokens until an end of sentance token is picked
 The bigram model selects a random first token and uses is as a key to start generating sentances.
 Each word is a key that points to a list of every word that comes after it.
 The trigram model selects a random pair of words as its first key. Each key points to 
 a list of every word that comes after that pair of words. 
"""
import sys
import re
import random
from collections import defaultdict

def main(argv):
	print(f"Hello. This is n random talker that generates "
	+ "n sentences based on a n gram model. CS4242 by Alicia John.\n")
	modelType = int(sys.argv[1]) # gets the n gram model type
	sentences = int(sys.argv[2]) # gets the number of sentences
	files = sys.argv[3:] # points to the files
	k=3
	megaBook = ""
	for k in files: # This opens all of the files and concatenates each file together
		with open(k, "r") as stream:
			book = stream.read()
			megaBook = megaBook + book
			stream.close()
	megaBook=megaBook.lower() #All letters are lowercase now
	tokens = re.sub(r'([.?,!]+)', r' \1', megaBook) #Adds a space before any punctuation
	tokens = re.sub(r'([^a-z.,?!])', '\n', tokens) # Removes all non lower case letters, numbers, and non punctuation special characters
	tokenList = tokens.split() # Tokenizes the string
	if modelType == 1:
		unigram(sentences,tokenList)
	elif modelType == 2:
		bigram(sentences,tokenList)
	elif modelType == 3: 
		trigram(sentences,tokenList)
	return 0

def unigram(sentences,tokenList):
	endchar = None
	i = 0
	while(i < sentences): # this continues until all sentences are outputed
		j = random.randint(0, len(tokenList)-1)  #Selects random number
		endchar = tokenList[j] # gets random word
		if(re.match(r'[.!?]', endchar)): # increments the sentence counter if end punctuation is encountered
			i+=1
			print(endchar)
		else: # Print character
			print(endchar, end = " ")
		

def bigram(sentences,tokenList):
	k=0 
	l= 1
	allKeys = defaultdict(list)
	for k in range(len(tokenList)): # for each word(the key) add the word after it to a list of words that occur after that key
		if k != (len(tokenList)-1):
			key = tokenList[k]
			value = tokenList[l]
			l+=1
			allKeys[key].append(value)
	i = 0
	c = 0
	while(i < sentences):
		if(c==0): # If this is first token, do not find a new character, set it as the key and output
			j = random.randint(0, len(tokenList)-1)
			endchar = tokenList[j] # select random first character
			c+=1 # increase so it does not return until it a new sentence
		else:
			vlist = []
			vlist = allKeys[endchar] # obtain list of words that come after the key
			j = random.randint(0, len(vlist)-1)	
			endchar = vlist[j] # select random word in list

		if(re.match(r'[.!?]', endchar)):# increments the sentence counter if end punctuation is encountered 
			i+=1
			c=0
			print(endchar)
		else:

			print(endchar, end = " ")
			c+=1

def trigram(sentences,tokenList):
	allKeys = defaultdict(list)
	k = 0
	l = 1
	m = 2
	for k in range(len(tokenList)):# for each pair of words(the key) add the word after it to a list of words that occur after that key
		if m != (len(tokenList)-1):
			key = tokenList[k] +" " + tokenList[l]
			value = tokenList[m]
			l+=1
			m+=1
			allKeys[key].append(value)
	k = 0
	l = 1
	biList = []
	while k != (len(tokenList)-2): # creates tokens made of pairs of words 
		key = tokenList[k] + " " + tokenList[l]
		biList.append(key)
		l+=1
		k+=1
	i = 0
	c = 0
	while(i < sentences):
		if(c==0):
			j = random.randint(0, len(biList)-1) 
			endchar = biList[j] # get first pair of words
			newkey = endchar #set pair as key
		else:# get a output value with the key
			vlist = allKeys[newkey]
			j = random.randint(0, len(vlist)-1)
			endchar = vlist[j]

		if((re.match(r'[.!?]', endchar) or (re.match(r'[.!?]', newkey)))):# increments the sentence counter if end punctuation is encountered
			i+=1
			c=0
			print(endchar)
		else:
			print(endchar, end = " ")
			if c != 0: #if its not the first token create the new key with the last word of the old key and the output
				oldchar = newkey.split()
				newkey = oldchar[1] +" "+ endchar
				c+=1
			else:# if its first pair don't make a new key
				c+=1

	


main(sys.argv)
	

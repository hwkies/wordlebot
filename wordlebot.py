from random import randint
import os
import sys

#represent possible colors as numbers with 0 being black, 
#1 being yellow, and 2 being green
class letterState: Black, Yellow, Green = range(3)

#create an accessible array of lines from the wordlist
wordlist = open(os.path.join(sys.path[0], "wordlist.txt"))
words = wordlist.readlines()

#get a random word in the available words
def getRandWord():
    #number of words in the list
    numWords = len(words) - 1

    #random word in the list of words
    randNum = randint(0, numWords)
    randWord = words[randNum]

    return randWord

print(getRandWord())

#take in an array of integers representing green, yellow, or black letters
#choose next available possible word from wordlist
from random import randint
import os
import sys
import socket
import json
import ssl

#NEED TO DO
#1. rewrite yellow letter handling
#2. figure out how to run it with ./client
#3. fill in README.md
#4. fill in empty makefile so grandescope grader compiles
#5. OPTIONAL: write more comprehensive wordle bot

#create an accessible array of lines from the wordlist
wordlist = open(os.path.join(sys.path[0], "wordlist.txt"))
words = wordlist.readlines()
yellow = []

# def yellowLetters(word):
#     for letter in yellow:
#         for i in range(5):
#             if word[i] == letter:
#                 return True
#             else:
#                 return False    

def shrinkWordlist(marks, guessedWord):
    # for j in range(5):
    #     if marks[j] == 1:
    #         yellow.append(guessedWord[j])
    newWords = []
    for word in words:
        for i in range(5):
            if guessedWord[i] == word[i] and marks[i] == 0:
                newWords.append(word)
                break
            elif guessedWord[i] != word[i] and marks[i] == 2:
                newWords.append(word) 
                break
            # elif yellowLetters(word) == False:
            #     newWords.append(word)   
            #     break           
    for line in newWords:
        words.remove(line)                   
            

#get a random word in the available words
def getRandWord():
    #number of words in the list
    numWords = len(words)

    #random word in the list of words
    randNum = randint(1, numWords)
    randWord = words[randNum - 1]

    return randWord[:5]

def communicateTCP(hostname, user):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connect to the server with the specified hostname and port
    dataHandler(client, hostname, user)

def communicateTLS(hostname, user):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    encryptclient = context.wrap_socket(client, server_hostname=hostname)
    dataHandler(encryptclient, hostname, user)

def dataHandler(client, hostname, user):
    client.connect((hostname, port))
    #send data to the server including user
    hello = json.dumps({'type': 'hello', 'northeastern_username': user}) + '\n'
    client.send(hello.encode())
    #what is the server response?
    response = client.recv(25600)
    response = response.decode()
    #un-jsonify server response
    stringResp = json.loads(response)
    print(responseHandler(stringResp, client))

def responseHandler(response, client):
    stringResp = response
    #if start message, get id and make a guess
    if stringResp["type"] == "start":
        id = stringResp["id"]
        guess = json.dumps({'type': 'guess', 'id': id, 'word': getRandWord()}) + '\n'
        client.send(guess.encode())
        stringResp = json.loads(client.recv(25600).decode())
    #while guess is incorrect, make new guess    
    while stringResp["type"] == "retry":
        #edit wordlist and try new word
        lastGuess = stringResp["guesses"][len(stringResp["guesses"]) - 1]
        shrinkWordlist(lastGuess["marks"], lastGuess["word"])
        guess = json.dumps({'type': 'guess', 'id': id, 'word': getRandWord()}) + '\n'
        client.send(guess.encode())
        stringResp = json.loads(client.recv(25600).decode())
    #print the final flag
    return(stringResp["flag"])

#command line stuff, NEEDS TO BE FLESHED OUT
args = sys.argv[1:]
numArgs = len(args)
#all commands were given
if numArgs == 5 and args[0] == "-p" and args[2] == "-s":
    port = int(args[1])
    communicateTLS(args[3], args[4])
elif numArgs == 3 and args[0] == "-s":
    #base port for tls connection
    port = 27994
    communicateTLS(args[1], args[2])
elif numArgs == 4 and args[0] == "-p":
    port = int(args[1])
    communicateTCP(args[2], args[3])
else:
    port = 27993
    communicateTCP(args[0], args[1])   


#take in an array of integers representing green, yellow, or black letters
#choose next available possible word from wordlist
#proj1.3700.network kiesman.h
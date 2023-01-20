The first step I made in my client was to offer connection to both TCP and TLS-ecnrypted ports. 
I created two methods, communicateTCP and communicateTLS to create socket connections for TCP 
ports and TLS-ecnrypted ports. These methods also call the dataHandler method which will be mentioned 
later.

I then created a method getRandWord which pulls a random word from a list of words. 

The dataHandler method takes in a client parameter from the communicateTCP/TLS methods, the server hostname, 
and the user. This method then connects to the given server on the client parameter, sends the initial "hello" 
message to the server, and parses the server response. It then prints the output of another method, 
responseHandler.

The responseHandler method takes in a client and a String response (response) that it gets from the original 
dataHandler method. It then parses the response parameter and determines if it is a "start" message. If so, 
it finds the id variable from the server response and sets a local variable id to that String. My method then 
makes a guess using a random word from the possible words using getRandWord. My code then checks to see if the 
server response is a "retry" message. While it is a "retry" message, my code parses the server response to 
get the last word I guessed and the marks for that word. It the calls the shrinkWordlist method with the 
marks and word that I last guessed. Finally, if my code does not get a "retry" or "start" message, it will 
return the flag found in what must be the "bye" server message.

The shrinkWordlist method takes in the marks of a guessed word and the guessed word itself. It then loops 
through my list of possible words and checks each letter in each word. It compares the marks and guessed word 
with each word in my wordlist and if a word should be removed, it is added to an array newWords. This method 
then removes all words in newWords from my wordlist, shrinking my wordlist to be only possible answers. The reason for the creation of a new array of words to be removed is to ensure there are no indexing issues when looping through my wordlist to shrink it.

The strategy used to shrink the wordlist is as follows. If a letter is in the same spot in the wordlist word and my guessed word and the letter is marked 0, remove the word from the wordlist. If a letter in my guessed word is marked 2 and the same spot in the wordlist word is not that letter, remove the word. If a letter is in the same spot in the wordlist word and my guessed word and is marked 1, remove that word. If a yellow letter is not present at all in the wordlist word, remove the word.

I tested rigorously all methods against the server. I started by testing to see if I got server response after creating my clients. I then created my guessing algorithm and tested to see that it properly shrunk the wordlist. 
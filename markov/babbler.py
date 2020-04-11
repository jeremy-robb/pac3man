
import random
import glob
import sys

"""
Markov Babbler

After being trained on text from various authors, can
'babble', or generate random walks, and produce text that
vaguely sounds like the author.
"""

class Babbler:
   model = {"Fstart": []}  # this is the dictionary where the markov chain will be stored
   def __init__(self, n=3, seed=None):
       """
       n is the length of an n-gram for state.
       seed is the seed for a random number generation. If none given use the default.
       """
       self.n = n
       if seed != None:
           random.seed(seed)
       # TODO: your code goes here
       #101001010101 idk what goes here


   def addToDict(self, word, parent): #adds to the ngram, word is.. the word, and first is whether it start a sentance
       if (parent == "Fstart"): #if it starts a sentence
           tempList = self.model['Fstart']
           tempList.append(word)
           self.model['Fstart'] = tempList
       if (len(word) >= 3): #check if the word ends in EOL
           if word not in self.model and word[len(word)-3:] != "EOL":
               self.model[word] = []
       else: #if the word is less than 3 characters, just check if it's a key
           if word not in self.model:
               self.model[word] = []
       if (parent != "Fstart"):
           tempList = self.model[parent]
           tempList.append(word)
           self.model[parent] = tempList
       pass
   def add_sentence_helper(self, list): #munches up a list and adds it to the markov model (a dictionary)
       if (len(list) == 1):
           list[0] = list[0] + "EOL"
       tempWord = " ".join(list[0])
       self.addToDict(" ".join(list.pop(0)), "Fstart")
       while (len(list) > 1):
           self.addToDict(" ".join(list[0]), tempWord)
           tempWord = " ".join(list.pop(0));
       #now all that's left is the last ngram
       list[0] = " ".join(list[0]) + "EOL";
       self.addToDict(list[0], tempWord)
       list.pop(0)
       pass
   def add_sentence(self, sentence):
       """
       Process the given sentence.
       The sentence is a string separated by spaces. Break it into
       words using split(). Convert each word to lowercase using lower().
       Then start processing n-grams and updating your states.
       Remember to track starters (i.e. n-grams that being sentences),
       stoppers (i.e. n-grams that end a sentence), and that
       any n-grams that stops a sentence should be followed by the
       special symbol 'EOL' in the state transition table. 'EOL' is short
       for 'end of line', and since it is capitalized and all of the
       text from the book is lower-case, it will be unambiguous.
       """
       #I think this is where I'll make the "tier" system
       #so maybe I should make a dictionary which holds a list of strings, those strings each have
       #their own key - list bit, and that way we start getting a tier system

       #the first guy we want to add to the Fstart list, then using that word as a temp variable, we want
       #to look if there's a key with that word (if not then create) and if there is, add the next word to the list
       #then repeat

       givenList = sentence.split(" ")
       #print(newList) to see the chains made
       #this gives us ['a', 'b', 'c', 'd', '.']
       newList = []
       for i in (givenList):
           i.lower()
       while (len(givenList) >= self.n):
           newList.append(givenList[0:self.n])
           givenList.pop(0)
       #this makes it so n is good once again
       #I can use pop to get the first index and then have the rest of the array
       #so make a method that takes in this givenList and demolishes it by putting it in a dictionary

       self.add_sentence_helper(newList)
       pass

   def check(self, word):
       #this checks if a word has EOL, if it does then we get rid of it
       if (len(word) > 3):
           if(word[len(word)-3:] == "EOL"):
               word = word[:len(word)-3]
       return word
       pass
   def add_file(self, filename):
       """
       This method done for you. It just calls your add_sentence() method
       for each line of an input file. We are assuming that the input data
       has already been pre-processed so that each sentence is on a separate line.
       """
       for line in [line.rstrip().lower() for line in open(filename, errors='ignore').readlines()]:
           self.add_sentence(line)

   def get_starters(self):
       """
       Return a list of all of the n-grams that start any sentence we've seen.
       The resulting list may contain duplicates, because one n-gram may start
       multiple sentences.
       """

       print(f'this is the list of starters: {self.model["Fstart"]}' )
       return self.model["Fstart"]
       pass

   def get_stoppers(self):
       """
       Return a list of all the n-grams that stop any sentence we've seen.
       The resulting value may contain duplicates, because one n-gram may stop
       multiple sentences.
       """
       flattened_list = [y for x in self.model.values() for y in x]
       listThing = list(filter(lambda x: x[len(x)-3:] == "EOL", flattened_list))
       print(f'Here is the list of all ending words:{listThing}')
       return listThing
       pass

   def get_successors(self, ngram):
       """
       Return a list of words that may follow a given n-gram.
       The resulting list may contain duplicates, because each
       n-gram may be followed by different words. For example,
       suppose an author has the following sentences:
       'the dog dances quickly'
       'the dog dances with the cat'
       'the dog dances with me'

       If n=3, then the n-gram 'the dog dances' is followed by
       'quickly' one time, and 'with' two times.

       If the given state never occurs, return an empty list.
       """
       #use rfind()

       #someList = self.model['Fstart']
       #wordChecking = self.model['Fstart'][0]
       #flattenList = [y for x in self.model[ngram] for y in x]
       listGiven =  self.model[ngram]
       for i in range(0, len(listGiven)):
           listGiven[i] = listGiven[i][listGiven[i].rfind(" ")+1:]
           self.check(listGiven[i])
       print(f'for the ngram "{ngram}" here are the words after: {listGiven}')
       pass

   def get_all_ngrams(self):
       """
       Return all the possible n-grams, or n-word sequences, that we have seen
       across all sentences.
      
       Probably a one-line method.
       """
       flattened_list = [y for x in self.model.values() for y in x]
       print(f'This is every possible n gram {flattened_list}')
       return flattened_list
       pass

   def has_successor(self, ngram):
       """
       Return True if the given ngram has at least one possible successor
       word, and False if it does not. This is another way of asking
       if we have ever seen a given ngram, because ngrams with no successor
       words must not have occurred in the training sentences.
       """

       if ngram in self.model.keys():
           return True
       return False
       pass

   def get_random_successor(self, ngram):
       """
       Given an n-gram, randomly pick from the possible words
       that could follow that n-gram. The randomness should take into
       account how likely a word is to follow the given n-gram.
       For example, if n=3 and we train on these three sentences:
       'the dog dances quickly'
       'the dog dances with the cat'
       'the dog dances with me'
      
       and we call get_random_next_word() for the state 'the dog dances',
       we should get 'quickly' about 1/3 of the time, and 'with' 2/3 of the time.
       """
       listGiven = self.model[ngram]
       for i in range(0, len(listGiven)):
           listGiven[i] = listGiven[i][listGiven[i].rfind(" ") + 1:]
           self.check(listGiven[i])
       return " " + random.choice(listGiven)
       pass
  
   def get_random_starter(self):
       listGiven = self.model["Fstart"]
       for i in range(0, len(listGiven)):
           self.check(listGiven[i])
       return random.choice(listGiven)
       pass

   def findnth(self, string, substring, n):
       if (n<0):
           return 0
       parts = string.split(substring, n + 1)
       return len(string) - len(parts[-1]) - len(substring)+1
       pass

   def babble(self):
       """
       Generate a random sentence using the following algorithm:
      
       1: Pick a starter ngram. This is the current ngram, and also
       the current sentence so far.
       Suppose the starter ngram is 'a b c'
      
       2: Choose a successor word based on the current ngram.
       3: If the successor word is 'EOL', then return the current sentence.
       4: Otherwise, add the word to the end of the sentence
       (meaning sentence is now 'a b c d')
       5: Also add the word to the end of the current ngram, and
       remove the first word from the current ngram.
       This produces 'b c d' for our example.
       6: Repeat step #2 until you generate 'EOL'.
       """
       startWord = self.get_random_starter()

       x = -1

       while True:
           startWord += self.get_random_successor(startWord[self.findnth(startWord, " ", x):])
           if (self.has_successor(startWord[self.findnth(startWord, " ", x+1):])):
               x = x + 1
           else:
               break
       return startWord[:len(startWord)-3]
       pass
          

def main(n=3, filename='tests/austen-emma.txt', num_sentences=5):
   """
   Simple test driver.
   """
  
   print(filename)
   babbler = Babbler(2)
   babbler.add_file(filename)
   print(f'num starters {len(babbler.get_starters())}')
   print(f'num ngrams {len(babbler.get_all_ngrams())}')
   print(f'num stoppers {len(babbler.get_stoppers())}')
  # print(f'num after {babbler.get_successors("of the lord")}')
  # print(f'check true haskey: {babbler.has_successor("of the lord")}')
  #  print(f'check false haskey: {babbler.has_successor("shaketh the wilderness")}')
  # print(f'get random successor: {babbler.get_random_successor("of the lord")}')
   print("---------------------------------------------------------------------------------------------------")
   for _ in range(num_sentences):
       print(babbler.babble())


if __name__ == '__main__':
   # remove the first parameter, which should be babbler.py, the name of the script
   sys.argv.pop(0)
   n = 3
   filename = 'tests/austen-sense.txt'
   num_sentences = 5
   if len(sys.argv) > 0:
       n = int(sys.argv.pop(0))
   if len(sys.argv) > 0:
       filename = sys.argv.pop(0)
   if len(sys.argv) > 0:
       num_sentences = int(sys.argv.pop(0))
   print(n)
   main(n, filename, num_sentences)




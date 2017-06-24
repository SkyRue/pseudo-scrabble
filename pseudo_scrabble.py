

import math
import random
import string
from unittest import mock
import sys

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '!': 0      
}

# -----------------------------------


WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def test_play_game(word_list, hands, replaced_letter = None):
    """
    Allows you to play a series of pre-specified hands. 
    Will allow you to play your game while 
    specifying what hands you want the computer to deal, and optionally
    what letter should be "chosen" to be added in the hand
    when you call substitute_hand. 

    
    ----ARGUMENTS----
    word_list: list of lowercase strings of valid words
    hands: list of dictionaries of the hands you want to play in order
                              
    replaced_letter: string letter that you want substitute_hand
                     to chose as a new letter
                     

    
    """
    def replace_letter_mock(hand, letter):
        num = hand[letter]
        del hand[letter]
        hand[replaced_letter] = num
        return hand
    deal_hand_function = sys.modules[__name__].deal_hand 
    substitute_hand_function = sys.modules[__name__].substitute_hand
    sys.modules[__name__].deal_hand = mock.Mock(side_effect=hands)
    if replaced_letter:
        sys.modules[__name__].substitute_hand = mock.Mock(side_effect=replace_letter_mock)
    play_game(word_list)
    sys.modules[__name__].substitute_hand = substitute_hand_function
    sys.modules[__name__].deal_hand = deal_hand_function


# -----------------------------------


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            9*wordlen - 4*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word = word.lower()
    
    comp_one = 0 #component 1 of the score (sum of points for each letter)
    for letter in word:
        comp_one += SCRABBLE_LETTER_VALUES[letter]
        
    comp_two = 9 * len(word) - 4 * (n - len(word))  #component 2, checks if its greater than 1
    if comp_two < 1:
        comp_two = 1
        
    return comp_one * comp_two

    




def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

    

#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n - 1):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    hand["!"] = 1
    
    return hand


#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand are ignored. Letters that appear in word more times
    than in hand never result in a negative count 
            
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    word = word.lower()
    new_hand = hand.copy()    #create a copy of hand as to not alter hand
    
    for letter in word:
        new_hand[letter] = new_hand.get(letter, 0) - 1  #subtract 1 from word frequency (value) for each letter in user's "word"
     
    new_hand_copy = new_hand.copy()  #create another copy so we can iterate and delete new_hand keys simultaneously
           
    for letter in new_hand_copy.keys(): #deletes any letter that has a frequency of 0 in the new_hand 
        if new_hand_copy[letter] < 1:
            del(new_hand[letter])
    
    return new_hand

#print(update_hand({'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}, "l"))


#
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word = word.lower()
    
    if ("!" not in word) and (word not in word_list): #if it's not an actual word, automatically return false (in this case there is no "!" to deal with)   
        return False
    if "!" in word:
        valid_wcard_word = False    #stores whether or not the user's wildcard word is valid
        for consonant in CONSONANTS:
            if word.replace("!", consonant, 1) in word_list:   #if a consonant exists that makes this a real world, valid_wcard_word is true
                valid_wcard_word = True
                break
        if not valid_wcard_word:    #if no consonant in place of ! can make the word valid, informs user
            return False
    
    hand_copy = hand.copy()

    for letter in word: #for each letter in user's word, subtract one from its frequency in hand_copy
        hand_copy[letter] = hand_copy.get(letter, 0) - 1 
        if hand_copy[letter] < 0:  #if any letter is used more than the frequency allows, automatically return false
            return False
        
    return True
    
#print(is_valid_word("!oney", {'n': 1, 'o': 1, '!': 1, 'd':1, 'w':1, 'e': 2}, ["honey"] )  )  
    


#
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    length = 0
    for letter in hand.keys():
        for i in range(hand[letter]):
            length += 1
    return length

#print(calculate_handlen({'n': 1, 'o': 1, '!': 1, 'd':1, 'w':1, 'e': 2}))
            
    

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, user
      is asked to input another word.

    * sum of the word scores is displayed when the hand finishes.

    * hand finishes when there are no more unused letters
      The user can also finish playing the hand by entering
      '*END*' instead of an actual word

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    cum_points = 0
    while calculate_handlen(hand) > 0:
        print()
        print("Current Hand:")
        display_hand(hand)   #displays current hand
        word = input("Enter word, or '*END*' to indicate that you are finished: ")
        
        if word == "*END*":   
            break
        else: 
            if is_valid_word(word, hand, word_list):   #if word is valid, we calc score, add it to cumulative score, report to user
                points = get_word_score(word, calculate_handlen(hand))
                cum_points += points
                print(word + " earned " + str(points) + " points. Total: " + str(cum_points) )
            else:   #for invalid word
                print("That is not a valid word. Please choose another word.")
            hand = update_hand(hand, word)    #updates hand
                
    print(" Total score for this hand: " + str(cum_points))
    
    return cum_points
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is *END*:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not *END*):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '*END*' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function

#play_hand({'n': 1, 'o': 1, '!': 1, 'd':1, 'w':1, 'e': 2}, ["nod", "w"])

# 


def substitute_hand(hand, letter):
    """ 
    
    Allows user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from VOWELS if the user chooses a VOWEL and 
    CONSONANTS if the user chooses a CONSONANT). The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.
    
    assumes letter is in the hand. Users can not substitute
    the wildcard, so assumes letter is not '!'.

    the new letter cant be the same as a letter that already exists in hand

    If user substitutes a VOWEL, they only get back a VOWEL.
         same with consonants 

    Has no side effects: does not mutate hand.
    

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand. The new letter should not be 'a','e', 'i','o', or 'u'
    as a consonant should only be subsituted for a consonant.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    freq = hand[letter]
    hand_copy = hand.copy()
    
    if letter in CONSONANTS:
        choose_from = list(CONSONANTS[:])
        for consonant in CONSONANTS:
            if consonant in hand.keys():
                choose_from.remove(consonant)
    else:
        choose_from = list(VOWELS[:])
        for vowel in VOWELS:
            if vowel in hand.keys():
                choose_from.remove(vowel)
    
    subst_letter = random.choice(choose_from)
    del(hand_copy[letter])
    hand_copy[subst_letter] = freq
             
    return hand_copy

    
    
       
    
def play_game(word_list):
    """
    Allow user to play a series of hands

    Asks the user to input a total number of hands

    Accumulates the score for each hand into a total score for the 
    entire series
 
    For each hand, before playing, asks user if they want to substitute
    one letter for another. If the user inputs 'yes', asks for 
    desired letter. This can only be done once during game. Once 
    substitue option is used, user shouldn't be asked if they want to
    substitute letters in the future

    For each hand, asks user if they would like to replay hand.
    If user inputs 'yes', they will replay the hand and keep 
    the better of the two scores for the hand (ie the better of the two
    is added to the total score for the game)  This can only be done once 
    during game. Once replay is used, the user is not longr asked
    if they want to replay future hands. Replaying the hand does
    not count as one of the total number of hands the user initially
    wants to play

    if you replay a hand, you do not get the option to substitute
    a letter - you must play whatever hand you just had.
      
    Returns total score for the series of hands

    word_list: list of lowercase strings
    """
    
    
    sub_used_this_game = False  #tracks if substitution was used in game...once it's used will stay True
    sub_asked_this_hand = False  #tracks if user was prompted for substitution for given hand, since substitutions reset every hand
    replay_used = False  #tracks if replay was used
    replay_condition = False #when this is true, different if statments will be used (score is calculated differently, number of hands remaining does not change)
    cum_points = 0   #keeps track of points for the whole game
    hand_points = 0  #keeps track of points for the hand
    old_hand_points = 0 #used only for replay to compare replay points to original points
    num_hands = float(input("Enter total number of hands: "))
    hand = deal_hand(HAND_SIZE) 
    orig_hand = hand.copy()   #need to store the orig hand in case user wants to replay
      
             
    while num_hands > 0:
        
         print()
         print("Current Hand:")
         display_hand(hand)   #displays current hand
    
         if (not sub_used_this_game) and (not sub_asked_this_hand):   #if substitution hasnt already been used for the game, and if user hasnt already been prompted for this hand, ask user if want to sub, if so, sub and display new hand
            substitute = input("Would you like to substitute a letter? ")
            substitute.lower()
            if substitute == "yes":
                replace_let = input("Which letter would you like to replace: ")
                replace_let.lower()
                hand = substitute_hand(hand, replace_let)
                orig_hand = hand.copy()   #the original hand changes when sub is used, must store in case user wants to replay
                sub_used_this_game = True
                print("Current Hand:")
                display_hand(hand) 
         sub_asked_this_hand = True
         
           
         word = input("Enter word, or '*END*' to indicate that you are finished: ")
         if word != "*END*":
            if is_valid_word(word, hand, word_list):   #if word is valid, we calc score, add it to cumulative score and hand score, report to user
                points = get_word_score(word, calculate_handlen(hand))
                hand_points += points
                print(word + " earned " + str(points) + " points. Total: " + str(hand_points) )
            else:   #for invalid word
                print("That is not a valid word. Please choose another word.")
            hand = update_hand(hand, word)    #updates hand (penalty)
        
         if (calculate_handlen(hand) < 1) or (word == "*END*"):  #if any hand ending conditions are met, print total hand score, ask user to replay (if hasnt already replayed)
            print("Total score for this hand: " + str(hand_points))
            print("----------")
            if replay_condition:   #if the user selected replay after last hand, this picks the best hand score to add to cum_points, and resets special replay condition to false
                 if hand_points < old_hand_points:
                     hand_points = old_hand_points
                 replay_condition = False
            if not replay_used:    #only prompt if replay hasn't been used
                 replay = input("Would you like to replay the hand? ")
                 replay.lower()
                 if replay == "yes":   #if user decides to replay, must store points from current hand before resetting hand points hand
                     old_hand_points = hand_points
                     replay_condition = True
                     replay_used = True
                     hand = orig_hand.copy()   #reset hand to the hand from last hand
            if not replay_condition:  #if replay isnt currently underway, add hand points to cum_points, decrease hand number count
                cum_points += hand_points
                num_hands -= 1          
                if num_hands > 0:    #as long as the game isnt over, deal a new hand
                    hand = deal_hand(HAND_SIZE)
                    orig_hand = hand.copy()
                
            hand_points = 0            #reset hand_points for new hand, reset substitution asked for new hand
            sub_asked_this_hand = False
                
                     
    #print and return cumulative score for all hands
    print("Total score over all hands: " +str(cum_points))
#    print("----------")
    return cum_points

  
    

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)


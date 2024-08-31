#Wordle Solver
#By Colin Takushi

#Getting words from txt file and placing them into a list
import os
print(os.getcwd())
myFile = open('include/words.txt', 'r')
data = myFile.read()
wordList = data.replace('"','').split(',')

#initializing lists
inPosList = []
guessList = []
notInList = []
guessString = ['0', '0', '0', '0', '0']
#if on first guess initalized guessList to have all words in word list
firstGuess = True
resetTrigger = False

#grabs user input
def guessInput(guessList):
    
    while True:
        guess = input("Enter your guess:")
        if guess == 'r':
            break
        elif len(guess) != 5 or not guess.isalpha():
            print("Invalid Input.")
        elif guess not in guessList and len(guessList) > 0 :
            print("Guess Not in guess. Choose from the list given. ")
        else:
            break
    while True:
        if guess == 'r':
            guessVal = []
            break
        guessVal = input("Enter value for each letter: ")
        if len(guessVal) != 5 or not guessVal.isnumeric():
            print("Invalid Input.")
        else: 
            break

    return guess, guessVal

#removes unwanted words
def filter(guess, guessVal):
    global firstGuess, resetTrigger, inPosList, guessList, notInList, guessString
    while guess != '-1':
        inWordList = []

        if resetTrigger:
            print(guess)
            print(guessVal)

        for pos, char in enumerate(guessVal):
            if char == '2':
                inPosList.append(pos)
            elif char == '1':
                inWordList.append(pos)
            elif char == '0':
                notInList.append(guess[pos])

        for pos in inPosList:
            guessString[pos] = guess[pos]

        notInPosList = ['0', '0', '0', '0', '0']
        for pos in inWordList:
            notInPosList[pos] = guess[pos]
            

        if firstGuess:
            guessList = wordList
            firstGuess = False

        if resetTrigger:
            print("reset trigger")
            print()
            print(len(guessList))

        #removing words that dont contain correct letters and words 
        #with wrong letter placements
        if inWordList:
            for word in guessList[:]:
                for pos, char in enumerate(notInPosList):
                    if char != '0' and char not in word or char in word[pos] :
                        break
            
        #removing words that contain incorrect letters

        for word in guessList[:]:
            for char in notInList:
                if char in word:
                    if char in guessString:
                        if char not in word[guessString.index(char)]:
                            print(char)
                            print(guessString.index(char))
                            print(word[guessString.index(char)])
                            print(word)
                            continue
                    else:
                        guessList.remove(word)
                    break

        #removing words that dont have correct positioned letters
        for word in guessList[:]:
            for pos, char in enumerate(guessString):
                if char == '0': continue
                elif char not in word[pos]:
                    guessList.remove(word)
                    break

        print(guessList)
        guess, guessVal = guessInput(guessList)

        #Reset function
        if guess == 'r':
            print("------------RESET-------------")
            firstGuess = True
            resetTrigger = True
            inPosList = []
            guessList = []
            notInList = []
            inWordList = []
            guessString = ['0', '0', '0', '0', '0']
            guess, guessVal = guessInput(guessList)

def main():
    print("Enter your guess then enter the value of the guessed letters:")
    print("0 = not in word, 1 = in word, 2 = in position")
    guess, guessVal = guessInput(guessList)
    filter(guess, guessVal)


# __name__
if __name__ == "__main__":
    main()
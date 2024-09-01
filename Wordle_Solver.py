#Wordle Solver
#By Colin Takushi

#Getting words from txt file and placing them into a list
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QListWidget
)
import sys
import os
import requests

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #initializing lists
        self.inPosList = []
        self.guessList = []
        self.notInList = []
        self.guessString = ['0', '0', '0', '0', '0']
        #if on first guess initalized guessList to have all words in word list
        self.firstGuess = True
        self.resetTrigger = False

        self.setWindowTitle("Wordle Solver")

        self.wordLabel = QLabel()
        self.wordLabel.setText("Enter your guess then enter the value of the guessed letters:")
        self.wordInput = QLineEdit()
        self.wordInput.setPlaceholderText("Word Guess")

        self.valueLabel = QLabel()
        self.valueLabel.setText("0 = not in word, 1 = in word, 2 = in position:")
        self.valueInput = QLineEdit()
        self.valueInput.setPlaceholderText("Value of guess")
        self.valueInput.returnPressed.connect(self.return_pressed)

        self.warnLabelWord = QLabel()
        self.warnLabelVal = QLabel()
        self.listOfWords = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.wordLabel)
        layout.addWidget(self.wordInput)
        layout.addWidget(self.valueLabel)
        layout.addWidget(self.valueInput)
        layout.addWidget(self.warnLabelWord)
        layout.addWidget(self.warnLabelVal)
        layout.addWidget(self.listOfWords)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Go to input check
    def return_pressed(self):
        guessBool = False
        valBool = False
        guess = self.wordInput.text()
        guessVal = self.valueInput.text()
        if guess == 'r':
            guessVal = []
        elif len(guess) != 5 or not guess.isalpha():
            self.warnLabelWord.setText("Invalid word input.")
        elif guess not in self.guessList and len(self.guessList) > 0 :
            self.warnLabelWord.setText("Guess Not in guess. Choose from the list given.")
        else:
            guessBool = True

        if len(guessVal) != 5 or not guessVal.isnumeric():
            print("Invalid Input.")
            self.warnLabelVal.setText("Invalid input value input.")
        else: 
            valBool = True
        
        if guessBool and valBool:
            self.filter(guess, guessVal)

        self.wordInput.setText("")
        self.valueInput.setText("")
        self.wordInput.setFocus()

    #removes unwanted words from master list
    def filter(self, guess, guessVal):
        global wordList
        inWordList = []
        if self.resetTrigger:
            print(guess)
            print(guessVal)
       
        #Create lists for letters in position, in the word, and not in the word
        for pos, char in enumerate(guessVal):
            if char == '2':
                self.inPosList.append(pos)
            elif char == '1':
                inWordList.append(pos)
            elif char == '0':
                self.notInList.append(guess[pos])

        #Track the letters in position
        for pos in self.inPosList:
            self.guessString[pos] = guess[pos]

        #Track the letters not in position
        notInPosList = ['0', '0', '0', '0', '0']
        for pos in inWordList:
            notInPosList[pos] = guess[pos]
            
        if self.firstGuess:
            self.guessList = wordList
            self.firstGuess = False

        if self.resetTrigger:
            print("reset trigger")
            print()
            print(len(self.guessList))

        #removing words that don't contain the letters with value 1 
        #and 
        #removing words that have letters with value 1 in current position
        if inWordList:
            for word in self.guessList[:]:
                for pos, char in enumerate(notInPosList):
                    if char != '0' and char not in word or char in word[pos]:
                        self.guessList.remove(word)
                        break
                            
        #removing words that contain the letters with value 0
        for word in self.guessList[:]:
            for char in self.notInList:
                if char in word:
                    if char in self.guessString:
                        if char not in word[self.guessString.index(char)]:
                            print(char)
                            print(self.guessString.index(char))
                            print(word[self.guessString.index(char)])
                            print(word)
                            continue
                    else:
                        self.guessList.remove(word)
                    break

        #removing words that dont have correct positioned letters with value 2
        for word in self.guessList[:]:
            for pos, char in enumerate(self.guessString):
                if char == '0': continue
                elif char not in word[pos]:
                    self.guessList.remove(word)
                    break
        
        self.listOfWords.clear()
        self.listOfWords.addItems(self.guessList)
        # need to request for user input again
        # print(self.guessList)

        #Reset function
        if guess == 'r':
            print("------------RESET-------------")
            firstGuess = True
            self.resetTrigger = True
            self.inPosList = []
            self.guessList = []
            self.notInList = []
            self.inWordList = []
            self.self.guessString = ['0', '0', '0', '0', '0']
            # guess, guessVal = self.guessInput(self.guessList)   


# Get word list
def get_words():
    url = 'https://gist.githubusercontent.com/cfreshman/d97dbe7004522f7bc52ed2a6e22e2c04/raw/633058e11743065ad2822e1d2e6505682a01a9e6/wordle-nyt-words-14855.txt'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            words = response.text
            return words
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def main():
    words = get_words()
    global wordList
    if words:
        print("Found words from api")
        wordList = list(words.split("\n"))
    else:
        print("No words found from api, using local list")
        print(os.getcwd())
        myFile = open('include/words.txt', 'r')
        data = myFile.read()
        wordList = data.replace('"','').split(',')    
        f = open("test.txt", "w")
        f.write(wordList)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()

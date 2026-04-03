import random
import tkinter as tk
from tkinter import messagebox

colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'teal']
gridSize = 16
startingScore = 20

class MemoryGame:
    '''Initialize memory game class'''
    def __init__(self):
        self.colors  = []
        self.score = startingScore
        self.flipped = []
        self.matched = set()
        self.gameOver = False
        self.deal()

    def deal(self):
        '''Shuffle 8 color pairs into 16 board positions'''
        self.colors = colors * 2
        random.shuffle(self.colors)

    def selectCard(self, index: int) -> str:
        '''Select a card at the given index'''
        if self.gameOver:
            return 'Game Over'
        if index in self.matched:
            return 'Card already matched'
        if index in self.flipped:
            return 'Card already flipped'
        if len(self.flipped) == 2:
            return 'Two cards already flipped'
        
        self.flipped.append(index)

        if len(self.flipped) == 1:
            return 'First card flipped'
        return self.checkMatch()

    def checkMatch(self) -> str:
        '''Check if the two flipped cards match'''
        first, second = self.flipped
        if self.colors[first] == self.colors[second]:
            self.matched.add(first)
            self.matched.add(second)
            self.flipped = []
            return 'Match'
        else:
            self.score -= 1
            self.flipped = []
            if self.score <= 0:
                self.gameOver = True
                return 'Game Over'
            return 'No Match'
        
    def reset(self):
        '''Reset the game'''
        self.score = startingScore
        self.flipped = []
        self.matched = set()
        self.gameOver = False
        self.deal()

    def isWinner(self) -> bool:
        '''Check if the player has won'''
        return len(self.matched) == gridSize

    def isLoser(self) -> bool:
        '''Check if the player has lost'''
        return self.gameOver

    def getColor(self, index: int) -> str:
        '''Get the color of the card at the given index'''
        return self.colors[index]

    def isMatched(self, index: int) -> bool:
        '''Check if the card at the given index is matched'''
        return index in self.matched

    def isFlipped(self, index: int) -> bool:
        '''Check if the card at the given index is flipped'''
        return index in self.flipped

class MemoryGameGUI:
    '''Create a GUI for the Memory Game using Tkinter'''

    def __init__(self, root):
        self.root = root
        self.root.title("Memory Matching Game")
        self.root.resizable(False, False)
        self.game = MemoryGame()
        self.cards = []
        self.locked = False
        self.buildUI()

    def buildUI(self):
        '''Build the user interface'''
        self.scoreLabel = tk.Label(
            self.root,
            text=f'Score: {self.game.score}',
            font=('Arial', 14, 'bold')
        )
        self.scoreLabel.grid(row=0, column=0, columnspan=4, pady=(12, 4))

        for i in range(gridSize):
            row = (i // 4) + 1
            col = i % 4
            card = tk.Label(
                self.root,
                text='?',
                width=8,
                height=4,
                bg='gray',
                fg='white',
                font=('Arial', 12, 'bold'),
                relief=tk.RAISED,
                cursor='hand2'
            )
            card.grid(row=row, column=col, padx=6, pady=6)
            card.bind('<Button-1>', lambda e, idx=i: self.onCardClick(idx))
            self.cards.append(card)

        self.resetButton = tk.Button(
            self.root,
            text='Reset',
            font=('Arial', 12),
            width=16,
            command=self.onReset
        )
        self.resetButton.grid(row=5, column=0, columnspan=4, pady=(4, 12))
    
    def onCardClick(self, index):
        '''Handle card click events'''
        if self.locked:
            return
        if self.game.isMatched(index):
            return
        
        self.locked = True

        wasAlreadyOver = self.game.gameOver
        result = self.game.selectCard(index)

        if result in ('Card already flipped', 'Two cards already flipped'):
            self.locked = False
            return
        if result == 'Game Over' and wasAlreadyOver:
            self.locked = False
            return
        
        self.revealCard(index)

        if result == 'First card flipped':
            self.locked = False

        elif result == 'Match':
            for i in self.game.matched:
                self.lockMatchedCard(i)
            self.updateScoreLabel()
            self.root.update_idletasks()
            self.locked = False
            if self.game.isWinner():
                messagebox.showinfo('Congratulations!', 'You matched all the cards!')
                
        elif result == 'No Match':
            self.updateScoreLabel()
            self.root.after(800, self.hideUnmatchedCards)

        elif result == 'Game Over':
            self.updateScoreLabel()
            self.root.after(800, self.showGameOver)

    def revealCard(self, index):
        '''Reveal the color of the card at the given index'''
        cardColor = self.game.getColor(index)
        self.cards[index].config(bg=cardColor, text='', fg=cardColor, relief=tk.SUNKEN)
        self.root.update_idletasks()

    def lockMatchedCard(self, index):
        '''Locks the matched card'''
        cardColor = self.game.getColor(index)
        self.cards[index].config(bg=cardColor, text='', fg=cardColor, relief=tk.SUNKEN, cursor='')
    
    def hideUnmatchedCards(self):
        '''Hide the colors of unmatched cards'''
        for i in range(gridSize):
            if not self.game.isMatched(i):
                self.cards[i].config(bg='gray', text='?', fg='white', relief=tk.RAISED)
        self.root.update_idletasks()
        self.locked = False

    def updateScoreLabel(self):
        '''Update the score label'''
        self.scoreLabel.config(text=f'Score: {self.game.score}')

    def showGameOver(self):
        '''Show a game over message'''
        self.locked = False
        messagebox.showinfo('Game Over', 'You ran out of turns. Better luck next time!')
        self.onReset()

    def onReset(self):
        '''Reset the game and update the UI'''
        self.game.reset()
        self.locked = False
        for card in self.cards:
            card.config(bg='gray', text='?', fg='white', state=tk.NORMAL, cursor='hand2')
        self.updateScoreLabel()

if __name__ == "__main__":
    root = tk.Tk()
    MemoryGameGUI(root)
    root.mainloop()
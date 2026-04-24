import random
import tkinter as tk
from tkinter import messagebox

# The eight unique card colors. Each appears exactly twice on the board
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'teal']
gridSize = 16 # Total number of cards on the 4×4 grid

# Maps each difficulty label to the number of mistakes the player is allowed
DIFFICULTY_LIMITS = {
    'Easy': 20,
    'Medium': 15,
    'Hard': 10,
    'Impossible': 1,
}

class MemoryGame:
    '''Initialize memory game class'''
    def __init__(self, difficulty: str):
        if difficulty not in DIFFICULTY_LIMITS:
            raise ValueError(f'Invalid difficulty level: {difficulty}')
        self._difficulty = difficulty
        self.colors  = []
        self.score = DIFFICULTY_LIMITS[difficulty]
        self.flipped = []
        self.matched = set()
        self.gameOver = False
        self.deal()

    def deal(self): # Duplicate the 8-color list to create one pair of each color, then randomise position so every game layout is unique
        '''Shuffle 8 color pairs into 16 board positions'''
        self.colors = colors * 2
        random.shuffle(self.colors)

    def selectCard(self, index: int) -> str:
        '''Select a card at the given index'''
        if self.gameOver: # Block selections when the game has already ended
            return 'Game Over'
        if index in self.matched: # Prevent re-selecting a card that is permanently matched
            return 'Card already matched'
        if index in self.flipped: # Prevent re-selecting the same face-up card
            return 'Card already flipped'
        if len(self.flipped) == 2: # Only two cards may be face-up at a time
            return 'Two cards already flipped'
        
        self.flipped.append(index)

        if len(self.flipped) == 1:
            return 'First card flipped'
        return self.checkMatch() # Check if two selected cards match

    def checkMatch(self) -> str:
        '''Check if the two flipped cards match'''
        first, second = self.flipped
        if self.colors[first] == self.colors[second]: # Successful match: move both indices into the permanent matched set and clear the temporary flipped list for the next turn
            self.matched.add(first)
            self.matched.add(second)
            self.flipped = []
            return 'Match'
        else:
            self.score -= 1 # Unsuccessful match: decrement score and clear flipped list for the next turn. If score reaches 0, set gameOver to True
            self.flipped = []
            if self.score <= 0:
                self.gameOver = True
                return 'Game Over'
            return 'No Match'
        
    def reset(self, difficulty: str = None):
        '''Reset the game'''
        if difficulty is not None:
            if difficulty not in DIFFICULTY_LIMITS:
                raise ValueError(f'Invalid difficulty level: {difficulty}')
            self._difficulty = difficulty # Check difficulty
        self.score = DIFFICULTY_LIMITS[self._difficulty] # Reset score based on current difficulty
        self.flipped = []
        self.matched = set()
        self.gameOver = False
        self.deal() # Reshuffle the cards for a new game

    def getDifficulty(self) -> str:
        '''Get the current difficulty level'''
        return self._difficulty

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
        self.difficultyVar = tk.StringVar(value='Medium') # Default difficulty selection in the dropdown menu
        self.game = MemoryGame('Medium')  # Default difficulty
        self.cards = [] # List to hold references to the card widgets for easy access
        self.locked = False # Flag to prevent user input while cards are being compared
        self.buildUI()

    def buildUI(self):
        '''Build the user interface'''
        headerFrame = tk.Frame(self.root)
        headerFrame.grid(row=0, column=0, columnspan=4, sticky='ew', padx=6, pady=(10, 4))
        headerFrame.columnconfigure(0, weight=1) # Score label stretches to fill space

        self.scoreLabel = tk.Label(
            headerFrame,
            text=f'Score: {self.game.score}',
            font=('Arial', 14, 'bold'),
            anchor='w',
        )
        self.scoreLabel.grid(row=0, column=0, sticky='w')

        difficultyFrame = tk.Frame(headerFrame) # Difficulty selection dropdown is right-aligned in the header
        difficultyFrame.grid(row=0, column=1, sticky='e')

        tk.Label(
            difficultyFrame,
            text='Difficulty:',
            font=('Arial', 11),
        ).grid(row=0, column=0, padx=(0, 4))

        difficultyMenu = tk.OptionMenu( # Create a dropdown menu for selecting difficulty levels, which triggers a game reset with the new difficulty when changed
            difficultyFrame,
            self.difficultyVar,
            *DIFFICULTY_LIMITS.keys(), # Populate the dropdown options with the keys from the DIFFICULTY_LIMITS dictionary
            command=self.onDifficultyChange,
        )
        difficultyMenu.config(font=('Arial', 11), width=9)
        difficultyMenu.grid(row=0, column=1)

        for i in range(gridSize):
            row = (i // 4) + 1 # Calculate row and column for each card based on its index to create a 4x4 grid
            col = i % 4 # The column is the remainder when the index is divided by 4
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
            card.grid(row=row, column=col, padx=6, pady=6) # Add some padding around each card for better visual separation
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
    
    def onDifficultyChange(self, selected: str):
        '''Handle difficulty change events'''
        self.doReset(difficulty=selected) # Reset the game with the new difficulty level when the dropdown selection changes

    def onCardClick(self, index):
        '''Handle card click events'''
        if self.locked:
            return
        if self.game.isMatched(index):
            return
        
        self.locked = True # Lock the UI to prevent additional clicks while processing the current selection

        wasAlreadyOver = self.game.gameOver
        result = self.game.selectCard(index)

        if result in ('Card already flipped', 'Two cards already flipped'): # If the user clicks a card that is already flipped or tries to flip a third card, ignore the click and unlock the UI without making any changes
            self.locked = False
            return
        if result == 'Game Over' and wasAlreadyOver:
            self.locked = False
            return
        
        self.revealCard(index) # Reveal the selected card's color immediately after selection, regardless of the outcome

        if result == 'First card flipped':
            self.locked = False # Unlock the UI to allow the user to select a second card after flipping the first card

        elif result == 'Match':
            for i in self.game.matched: # Lock matched cards
                self.lockMatchedCard(i)
            self.updateScoreLabel()
            self.root.update_idletasks()
            self.locked = False
            if self.game.isWinner(): # Check if that match won the game
                messagebox.showinfo('Congratulations!', 'You matched all the cards!')
                
        elif result == 'No Match':
            self.updateScoreLabel()
            self.root.after(800, self.hideUnmatchedCards) # After a short delay to allow the player to see the second card, hide both unmatched cards and unlock the UI for the next turn

        elif result == 'Game Over':
            self.updateScoreLabel()
            self.root.after(800, self.showGameOver) # After a short delay to allow the player to see the second card, show the game over message and reset the game

    def revealCard(self, index):
        '''Reveal the color of the card at the given index'''
        cardColor = self.game.getColor(index)
        self.cards[index].config(bg=cardColor, text='', fg=cardColor, relief=tk.SUNKEN)
        self.root.update_idletasks() # Update the UI immediately to show the revealed card

    def lockMatchedCard(self, index):
        '''Locks the matched card'''
        cardColor = self.game.getColor(index)
        self.cards[index].config(bg=cardColor, text='', fg=cardColor, relief=tk.SUNKEN, cursor='') # Matched cards remain revealed and are no longer clickable, so we change the cursor to the default to indicate that they cannot be interacted with
    
    def hideUnmatchedCards(self):
        '''Hide the colors of unmatched cards'''
        for i in range(gridSize):
            if not self.game.isMatched(i): # Only hide cards that are not matched, so that matched cards remain visible while unmatched cards are hidden again
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
        self.game.reset() # Reset the game state without changing the difficulty level
        self.locked = False
        for card in self.cards:
            card.config(bg='gray', text='?', fg='white', state=tk.NORMAL, cursor='hand2')
        self.updateScoreLabel() # Update the score label to reflect the reset score based on the current difficulty level

    def doReset(self, difficulty: str):
        '''Reset the game with a new difficulty level'''
        self.game.reset(difficulty=difficulty)
        self.difficultyVar.set(difficulty) # keep the dropdown menu selection in sync
        self.locked = False
        for card in self.cards: # Reset all cards to the default face-down state and make them clickable again
            card.config(bg='gray', text='?', fg='white', state=tk.NORMAL, cursor='hand2')
        self.updateScoreLabel()

if __name__ == "__main__":
    root = tk.Tk()
    MemoryGameGUI(root)
    root.mainloop()
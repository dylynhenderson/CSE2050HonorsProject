import random

colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'teal']
gridSize = 16
startingScore = 20

class memorygame:
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

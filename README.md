# CSE2050 Honors Project
Python matching memory game to demonstrate honors-level understanding of OOP, GUI design, data structures, and iterative development

## How to Play

 **Objective:** Find all eight matching pairs of colored cards before you run out of allowed mistakes.

**Setup:** The board shows 16 face-down cards arranged in a 4×4 grid. Behind each card is one of eight colors. Every color appears exactly twice.

**Taking a turn:**
1. Click any face-down card to reveal its color.
2. Click a second card to reveal its color.
3. If the two colors match, both cards stay face-up and are permanently removed from play.
4. If the colors do not match, both cards flip back over after a short pause, so pay attention while they are visible!

**Difficulty:** Use the dropdown in the top-right corner to choose how many mistakes you are allowed before the game ends.

| Difficulty | Allowed Mistakes |
|------------|-----------------|
| Easy       | 20              |
| Medium     | 15              |
| Hard       | 10              |
| Impossible | 1               |

**Winning:** Match all 16 cards before your score count reaches zero, and a congratulations message appears.

**Losing:** If your remaining score hits zero on a mismatch, a game-over message appears, and the board resets automatically.

**Reset:** Press the Reset button at any time to shuffle the board and reset the score for the current difficulty. Changing the difficulty also resets the game!

## How to Run

Navigate to the project directory in your terminal and run:

```
python memory_game.py
```
> [!NOTE]
> Python 3 and Tkinter are required.

## Code Structure

The project is contained in two files: `memory_game.py` holds all the source code, and `test_memory_game.py` holds the test cases.

### `memory_game.py`

The file is organized into two classes.

**`DIFFICULTY_LIMITS` (module-level constant)**
A dictionary mapping the four difficulty names to their integer scores. Both `MemoryGame` and the GUI read from this dictionary for changing the UI and logic.

**`MemoryGame`**
The class handles all actions of the game; it creates the cards, shuffles them, and keeps track of their position and state.

The class accepts a `difficulty` parameter in both its constructor and its `reset` method, making it straightforward to test all difficulty boundaries independently of the GUI.

**`MemoryGameGUI`**

Made using Tkinter.

It creates the root window, constructs all widgets in `buildUI`, and wires every user event: card clicks, the reset button, and the difficulty selector, to methods on this class. Those event handlers translate the user's input into a `selectCard` or `reset` call on the `MemoryGame` instance, interpret the returned status string, and update the relevant widgets.

The header row is built inside a `tk.Frame` so the score label and difficulty selector can sit on opposite sides of the same row without fighting with the card grid's column constraints.

### `test_memory_game.py`

The test suite tests all of the logic of the game using Python's built-in 'unittest' module.

## Key Algorithms

### Shuffling

`deal()` creates the 16-card board by duplicating the 8-color list with Python's `*` operator and then calling `random.shuffle()` in-place. This guarantees exactly two copies of each color in an unpredictable order each game, without any manual swap logic.

```python
self.colors = colors * 2
random.shuffle(self.colors)
```

### Matching Logic

`selectCard` acts as the turn gate. It checks for illegal moves, game already over, card already matched, card already flipped, or a third card attempted while two are pending. Only when two legal cards are selected does it call `checkMatch`, which compares the two color values and either moves both indices into the permanent `matched` set when matched, or decrements the score and checks for game-over, when mismatched. Clearing `flipped` at the end of every two-card evaluation is what allows the next turn to start cleanly.

### UI Lock

The `self.locked` flag blocks `onCardClick` for the entire duration of the delay, preventing a third or fourth card from being "selected" while two mismatched cards are still visible. The flag is released inside `hideUnmatchedCards` once the cards have been flipped back, so the player cannot act during the window.

## Reflection
Developing this project was a bit of a milestone for me, primarily because this was my first time designing a UI. It was a decent struggle at first, trying to figure out how to make the UI look right and function intuitively was trickier than I anticipated. I spent a lot of time troubleshooting and figuring out the right size for everything, making it all fit nicely. The process forced me to think about my code from a different perspective.

One of the biggest takeaways from this process was discovering my own way to do things. In my original project proposal, I planned to build the game incrementally, toggling back and forth between the UI and the logic. I drafted that plan before I ever touched Tkinter. However, once I began coding, I quickly realized that wasn't teh best approach for me. In practice, I wrote all of the game logic before ever starting the UI. By having a working logical foundation beforehand, I could focus entirely on the design and connecting it all. It was a quick departure from my plan, but it made the process flow better, and I will definitely keep it in mind for future projects.

# 8 colors, duplicated to make 16 cards
from logging import root
from tkinter.ttk import Button


colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "teal"] * 2

# cards are placed into a 4x4 grid of buttons
for i, color in enumerate(colors):
    row = i // 4
    col = i % 4
    button = Button(root, bg=color, width=10, height=5)
    button.grid(row=row, column=col)
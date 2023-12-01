import tkinter as tk
from tkinter import messagebox

def change_content(card_num):
    def submit():
        new_content = entry.get()
        cards[card_num].config(text=new_content)
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Edit Card Content")

    label = tk.Label(top, text="Enter new content:")
    label.pack()

    entry = tk.Entry(top)
    entry.pack()

    submit_button = tk.Button(top, text="Submit", command=submit)
    submit_button.pack()

root = tk.Tk()
root.title("Memory Cards")

# Create 9 memory cards
cards = []
for i in range(9):
    card = tk.Button(root, text=f"Card {i+1}", width=10, height=5, command=lambda i=i: change_content(i))
    card.grid(row=i//3, column=i%3)
    cards.append(card)

root.mainloop()

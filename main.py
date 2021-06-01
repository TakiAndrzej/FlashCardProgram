from tkinter import *
import pandas as pd
import random
import time

# read data from csv

try:
    data = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("./data/french_words.csv")
finally:
    data = data.to_dict(orient="records")

#
def change_to_eng(current_word):
    global should_remove
    global data
    card.itemconfig(photo, image=english_photo)
    card.itemconfig(word, text=current_word["English"], fill="white")
    card.itemconfig(text, text="English", fill="white")


def draw_word():
    global change_timer
    global current_word
    current_word=random.choice(data)
    window.after_cancel(change_timer)
    card.itemconfig(photo, image=french_photo)
    card.itemconfig(word, text=current_word["French"], fill="black")
    card.itemconfig(text, text="French", fill="black")
    change_timer = window.after(3000, change_to_eng, current_word)

def is_known():
    global data
    global current_word
    data.remove(current_word)
    save_data = pd.DataFrame.from_dict(data)
    save_data.to_csv("./data/words_to_learn.csv", index=False)
    draw_word()

#UI

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

change_timer = window.after(3000, func=draw_word)
current_word = random.choice(data)

no_image = PhotoImage(file="./images/wrong.png")
no_button = Button(image=no_image, highlightthickness=0, command=draw_word)
no_button.grid(column=0, row=1)

yes_image = PhotoImage(file="./images/right.png")
yes_button = Button(image=yes_image, highlightthickness=0, command=is_known)
yes_button.grid(column=1, row=1)


card = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
english_photo = PhotoImage(file="./images/card_back.png")
french_photo = PhotoImage(file="./images/card_front.png")
photo = card.create_image(400, 263, image=french_photo)
text = card.create_text(400, 130, text="", fill="black", font=("Arial", 24, "italic"))
word = card.create_text(400, 260, text="", fill="black", font=("Arial", 36, "bold"))
card.grid(column=0, row=0, columnspan=2)

draw_word()



window.mainloop()
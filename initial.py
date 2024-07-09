import clips
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
from PIL import Image, ImageTk

# Initialize CLIPS environment
env = clips.Environment()
env.load('fact3.clp')
env.reset()

# Define the new rule for the drink promotion
env.build("""
(defrule promocja-3-drinki-1-za-darmo
   ?f1 <- (UserSelection (drink ?drink) (drink_count ?drink_count&:(>= ?drink_count 4)))
   ?drink_fact <- (Drink (name ?drink) (price ?drink_price))
   =>
   (bind ?free_drinks (div ?drink_count 4)) ;; Number of free drinks
   (bind ?paid_drinks (- ?drink_count ?free_drinks)) ;; Drinks to be paid
   (bind ?cena-promocyjna (* ?paid_drinks ?drink_price)) ;; Promotional price for drinks
   (bind ?oszczednosc (* ?free_drinks ?drink_price)) ;; Savings from the promotion
   (assert (PromocjaNapoje (drink ?drink) (size none) (ilosc ?free_drinks) (cena ?cena-promocyjna) (oszczednosc ?oszczednosc))))
""")

env.run()
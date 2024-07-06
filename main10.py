import clips
import tkinter as tk
from tkinter import messagebox

# Initialize CLIPS environment
clips_env = clips.Environment()
clips_env.load("fact10.clp")

# Define GUI
root = tk.Tk()
root.title("Pizza Order")

# Create dropdown menu for pizza selection
pizza_var = tk.StringVar()
pizza_options = ["margarita", "pepperoni", "hawaiian", "vegetarian"]
pizza_dropdown = tk.OptionMenu(root, pizza_var, *pizza_options)
pizza_dropdown.pack()

# Create dropdown menu for size selection
size_var = tk.StringVar()
size_options = ["small", "medium", "large"]
size_dropdown = tk.OptionMenu(root, size_var, *size_options)
size_dropdown.pack()

# Create text entry for drink selection
drink_var = tk.StringVar()
drink_entry = tk.Entry(root, textvariable=drink_var)
drink_entry.pack()

# Create button to submit order
def submit_order():
    # Get selected pizza, size, and drink
    pizza = pizza_var.get()
    size = size_var.get()
    drink = drink_var.get()

    # Send order to CLIPS
    clips_env.assert_string("(order (pizza {}) (size {}) (drink {}))".format(pizza, size, drink))

    # Run CLIPS rules to calculate total price
    clips_env.run()

    # Get total price from CLIPS
    total_price = clips_env.facts("total-price")[0]["price"]

    # Display total price in message box
    messagebox.showinfo("Total Price", "Total price: ${:.2f}".format(total_price))

submit_button = tk.Button(root, text="Submit Order", command=submit_order)
submit_button.pack()

root.mainloop()
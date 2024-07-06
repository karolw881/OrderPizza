import clips
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Added for the Spinbox widget
import sys
import io

# Initialize CLIPS environment
env = clips.Environment()
env.load('facts_and_rules.clp')  # Adjust the path as necessary
env.reset()
env.run()

class PizzaSelector:
    def __init__(self, root, env):
        self.env = env
        self.root = root
        self.root.title("Pizza Selector")

        self.drink_var = tk.StringVar()
        self.pizza_var = tk.StringVar()
        self.promotion_var = tk.StringVar()
        self.pizza_count = tk.IntVar(value=1)  # Number of pizzas

        # Drink selection
        tk.Label(root, text="Select Drink:").pack()
        drinks = ["cola", "pepsi", "sprite", "water"]
        for drink in drinks:
            tk.Radiobutton(root, text=drink, variable=self.drink_var, value=drink).pack()

        # Pizza selection
        tk.Label(root, text="Select Pizza:").pack()
        pizzas = ["margarita", "pepperoni", "hawajska", "wiejska", "polska", "morska"]
        for pizza in pizzas:
            tk.Radiobutton(root, text=pizza, variable=self.pizza_var, value=pizza).pack()

        # Number of pizzas
        tk.Label(root, text="Number of Pizzas:").pack()
        tk.Spinbox(root, from_=1, to=10, textvariable=self.pizza_count).pack()

        # Promotion selection
        tk.Label(root, text="Select Promotion:").pack()
        promotions = ["2_big_pizzas", "student", "kods"]
        for promotion in promotions:
            tk.Radiobutton(root, text=promotion, variable=self.promotion_var, value=promotion).pack()

        # Submit button
        tk.Button(root, text="Submit", command=self.submit).pack()

        # Result display
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def submit(self):
        selected_drink = self.drink_var.get()
        selected_pizza = self.pizza_var.get()
        selected_promotion = self.promotion_var.get()
        selected_pizza_count = self.pizza_count.get()

        if not selected_drink or not selected_pizza or not selected_promotion:
            messagebox.showerror("Error", "Please select a drink, pizza, and promotion")
            return

        # Reset environment to clear previous user facts
        self.env.reset()

        # Assert initial facts again
        self.env.assert_string("(initial-facts)")

        # Assert user selection to CLIPS
        print(f"Asserting UserSelection with drink={selected_drink}, pizza={selected_pizza}, promotion={selected_promotion}, count={selected_pizza_count}")
        self.env.assert_string(
            f'(UserSelection (drink {selected_drink}) (pizza {selected_pizza}) (promotion {selected_promotion}) (count {selected_pizza_count}))')

        # Capture CLIPS output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        self.env.run()
        clips_output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        print("CLIPS output:")
        print(clips_output)

        # Get the result from CLIPS
        result_text = ""
        found_result = False
        for fact in self.env.facts():
            print(f"Fact: {fact}")
            if fact.template.name == 'Result':
                drink = fact['drink']
                pizza = fact['pizza']
                promotion = fact['promotion']
                total_price = fact['total-price']
                unit_price = fact['unit-price']
                total_price_no_discount = unit_price * selected_pizza_count

                result_text = (
                    f"Drink: {drink}\n"
                    f"Pizza: {pizza}\n"
                    f"Number of Pizzas: {selected_pizza_count}\n"
                    f"Promotion: {promotion}\n"
                    f"Unit Price: {unit_price} EUR\n"
                    f"Total Price without Discount: {total_price_no_discount} EUR\n"
                    f"Total Price with Discount: {total_price} EUR"
                )
                found_result = True
                break

        if not found_result:
            result_text = "No result fact found. Please check the CLIPS rules."

        self.result_label.config(text=result_text)

# Initialize Tkinter root
root = tk.Tk()
app = PizzaSelector(root, env)
root.mainloop()

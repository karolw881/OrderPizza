import clips
import tkinter as tk
from tkinter import messagebox
import sys
import io

# Initialize CLIPS environment
env = clips.Environment()
env.load('fact2.clp')
env.reset()
env.run()


class PizzaSelector:
    def __init__(self, root, env):
        self.env = env
        self.root = root
        self.root.title("Pizza Selector")

        self.drink_var = tk.StringVar()
        self.pizza_vars = {}
        self.pizza_sizes = {}
        self.pizza_counts = {}

        # Drink selection
        tk.Label(root, text="Select Drink:").pack()
        drinks = ["cola", "pepsi", "sprite", "water"]
        for drink in drinks:
            tk.Radiobutton(root, text=drink, variable=self.drink_var, value=drink).pack()

        # Pizza selection
        tk.Label(root, text="Select Pizza, Size, and Quantity:").pack()
        pizzas = ["margarita", "pepperoni", "hawajska", "wiejska", "polska", "morska"]
        sizes = ["small", "medium", "large"]
        for pizza in pizzas:
            var = tk.IntVar()
            self.pizza_vars[pizza] = var
            frame = tk.Frame(root)
            frame.pack()
            tk.Checkbutton(frame, text=pizza, variable=var).pack(side=tk.LEFT)
            size_var = tk.StringVar()
            self.pizza_sizes[pizza] = size_var
            for size in sizes:
                tk.Radiobutton(frame, text=size, variable=size_var, value=size).pack(side=tk.LEFT)
            self.pizza_counts[pizza] = tk.Spinbox(frame, from_=1, to=10, width=5)
            self.pizza_counts[pizza].pack(side=tk.RIGHT)

        # Submit button
        tk.Button(root, text="Submit", command=self.submit).pack()

        # Result display
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def submit(self):
        selected_drink = self.drink_var.get()

        selected_pizzas = {}
        for pizza, var in self.pizza_vars.items():
            if var.get() == 1:
                size = self.pizza_sizes[pizza].get()
                count = int(self.pizza_counts[pizza].get())
                selected_pizzas[pizza] = (size, count)

        if not selected_drink or not selected_pizzas:
            messagebox.showerror("Error", "Please select a drink and at least one pizza with size")
            return

        # Reset environment to clear previous user facts
        self.env.reset()

        # Assert initial facts again
        self.env.assert_string("(initial-facts)")

        # Assert user selection to CLIPS
        for pizza, (size, count) in selected_pizzas.items():
            print(f"Asserting UserSelection with drink={selected_drink}, pizza={pizza}, size={size}, count={count}")
            self.env.assert_string(
                f'(UserSelection (drink {selected_drink}) (pizza {pizza}) (size {size}) (count {count}))')

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
                total_price = fact['total-price']
                drink = fact['drink']
                pizza = fact['pizza']
                size = fact['size']
                count = fact['count']
                result_text += f"Drink: {drink}\nPizza: {pizza} ({size}) x{count}\nTotal Price: {total_price} EUR\n\n"
                found_result = True

        if not found_result:
            result_text = "No result fact found. Please check the CLIPS rules."

        self.result_label.config(text=result_text)


# Initialize Tkinter root
root = tk.Tk()
app = PizzaSelector(root, env)
root.mainloop()

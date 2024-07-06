import clips
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys
import io

# Initialize CLIPS environment
env = clips.Environment()
env.load('fact10.clp')
env.reset()
env.run()


class PizzaSelector:
    def __init__(self, root, env):
        self.env = env
        self.root = root
        self.root.title("Pizza Selector")

        self.pizza_vars = {}
        self.pizza_sizes_counts = {}
        self.drink_vars = {}  # Dodaj nową zmienną do przechowywania wyborów drinków i ich ilości dla każdej pizzy

        # Pizza selection
        tk.Label(root, text="Select Pizza, Size, Quantity, and Drink:").pack()
        pizzas = ["margarita", "pepperoni", "hawajska", "wiejska", "polska", "morska"]
        sizes = [("small", 20), ("medium", 35), ("large", 50)]
        drinks = [("none", 0), ("cola", 10), ("pepsi", 10), ("sprite", 10), ("water", 10)]

        for pizza in pizzas:
            var = tk.IntVar()
            self.pizza_vars[pizza] = var
            frame = tk.Frame(root)
            frame.pack()
            tk.Label(frame, text=pizza).pack(side=tk.LEFT)
            size_count_vars = {}
            for size, price in sizes:
                size_frame = tk.Frame(frame)
                size_frame.pack(side=tk.LEFT)
                tk.Label(size_frame, text=f"{size} - {price} EUR").pack(side=tk.LEFT)
                count_var = tk.Spinbox(size_frame, from_=0, to=10, width=5)
                count_var.pack(side=tk.LEFT)
                size_count_vars[size] = count_var
            self.pizza_sizes_counts[pizza] = size_count_vars

            # Dodaj wybór drinka i jego ilości dla każdej pizzy
            drink_frame = tk.Frame(frame)
            drink_frame.pack(side=tk.LEFT)
            tk.Label(drink_frame, text="Drink:").pack(side=tk.LEFT)
            drink_var = tk.StringVar(value="none")
            drink_menu = ttk.Combobox(drink_frame, textvariable=drink_var, values=[drink for drink, _ in drinks])
            drink_menu.pack(side=tk.LEFT)
            drink_count_var = tk.Spinbox(drink_frame, from_=0, to=10, width=5)
            drink_count_var.pack(side=tk.LEFT)
            self.drink_vars[pizza] = (drink_var, drink_count_var)

        # Submit button
        tk.Button(root, text="Submit", command=self.submit).pack()

        # Result display
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()
        # Order button
        tk.Button(root, text="Skladam Zamowienie", command=self.display_order).pack()
        self.order_label = tk.Label(root, text="")
        self.order_label.pack()

    def submit(self):
        selected_pizzas = []
        for pizza, size_count_vars in self.pizza_sizes_counts.items():
            for size, count_var in size_count_vars.items():
                count = int(count_var.get())
                if count > 0:
                    drink_var, drink_count_var = self.drink_vars[pizza]
                    selected_drink = drink_var.get()
                    drink_count = int(drink_count_var.get())
                    selected_pizzas.append((pizza, size, count, selected_drink, drink_count))

        if not selected_pizzas:
            messagebox.showerror("Error", "Please select at least one pizza with size, quantity, and drink")
            return

        # Reset environment to clear previous user facts
        self.env.reset()

        # Assert initial facts again
        self.env.assert_string("(initial-facts)")

        # Assert user selection to CLIPS
        for pizza, size, count, drink, drink_count in selected_pizzas:
            print(
                f"Asserting UserSelection with drink={drink}, drink_count={drink_count}, pizza={pizza}, size={size}, count={count}")
            self.env.assert_string(
                f'(UserSelection (drink {drink}) (drink_count {drink_count}) (pizza {pizza}) (size {size}) (count {count}))')

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
        total_price = 0
        for fact in self.env.facts():
            print(f"Fact: {fact}")
            if fact.template.name == 'Result':
                item_price = fact['total-price']
                total_price += item_price
                drink = fact['drink']
                drink_count = fact['drink_count']
                pizza = fact['pizza']
                size = fact['size']
                count = fact['count']
                result_text += f"Drink: {drink} x{drink_count}\nPizza: {pizza} ({size}) x{count}\nItem Price: {item_price} EUR\n\n"
                found_result = True

        result_text += f"Total Price: {total_price} EUR\n"

        if not found_result:
            result_text = "No result fact found. Please check the CLIPS rules."

        self.result_label.config(text=result_text)

    def display_order(self):
        order_text = ""

        for pizza, size_count_vars in self.pizza_sizes_counts.items():
            for size, count_var in size_count_vars.items():
                count = int(count_var.get())
                if count > 0:
                    drink_var, drink_count_var = self.drink_vars[pizza]
                    drink = drink_var.get()
                    drink_count = int(drink_count_var.get())
                    order_text += f"Pizza: {pizza} ({size}) x{count}\nDrink: {drink} x{drink_count}\n"

        self.order_label.config(text=order_text)


# Initialize Tkinter root
root = tk.Tk()
app = PizzaSelector(root, env)
root.mainloop()

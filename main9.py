import clips
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
import sys
import io

# Initialize CLIPS environment
env = clips.Environment()
env.load('fact9.clp')
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


class PizzaSelector:
    def __init__(self, root, env):
        self.env = env
        self.root = root
        self.root.title("Pizza Selector")

        self.pizza_vars = {}
        self.pizza_sizes_counts = {}
        self.drink_vars = {}

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

            # Add drink selection and its quantity for each pizza
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
        tk.Button(root, text="valuations", command=self.submit).pack()

        # Result display
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        # Order button
        tk.Button(root, text="Order", command=self.display_order).pack()

        # Order details display
        self.order_text = scrolledtext.ScrolledText(root, width=35, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.order_text.pack()

        # Discount and total price labels
        self.promotion_label = tk.Label(root, text="Total Promotion Savings: 0 EUR")
        self.promotion_label.pack()
        self.total_price_label = tk.Label(root, text="Total Price: 0 EUR")
        self.total_price_label.pack()

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
        self.total_price = 0  # Initialize total price
        self.total_promotion_savings = 0  # Initialize total promotion savings
        for fact in self.env.facts():
            print(f"Fact: {fact}")
            if fact.template.name == 'Result':
                item_price = fact['total-price']
                self.total_price += item_price
                drink = fact['drink']
                drink_count = fact['drink_count']
                pizza = fact['pizza']
                size = fact['size']
                count = fact['count']
                result_text += f"Drink: {drink} x{drink_count}\nPizza: {pizza} ({size}) x{count}\nItem Price: {item_price} EUR\n\n"
                found_result = True
            elif fact.template.name == 'Promocja':
                promocja_ilosc = fact['ilosc']
                promocja_cena = fact['cena']
                promocja_oszczednosc = fact['oszczednosc']
                pizza = fact['pizza']
                size = fact['size']
                result_text += f"PROMOTION: Pizza: {pizza} ({size}) x{promocja_ilosc} za połowę ceny. Cena: {promocja_cena} EUR. Oszczędzasz: {promocja_oszczednosc} EUR\n"
                self.total_price -= promocja_oszczednosc
                self.total_promotion_savings += promocja_oszczednosc
                result_text += "Promocja została uwzględniona.\n"
            elif fact.template.name == 'PromocjaNapoje':
                promocja_ilosc = fact['ilosc']
                promocja_cena = fact['cena']
                promocja_oszczednosc = fact['oszczednosc']
                drink = fact['drink']
                result_text += f"PROMOTION: Drink: {drink} x{promocja_ilosc} za darmo. Cena: {promocja_cena} EUR. Oszczędzasz: {promocja_oszczednosc} EUR\n"
                self.total_price -= promocja_oszczednosc
                self.total_promotion_savings += promocja_oszczednosc
                result_text += "Promocja została uwzględniona.\n"

        result_text += f"Total Price: {self.total_price} EUR\n"

        if not found_result:
            result_text = "No result fact found. Please check the CLIPS rules."

        self.result_label.config(text=result_text)


    def display_order(self):
        self.order_text.config(state=tk.NORMAL)
        self.order_text.delete(1.0, tk.END)

        order_text = ""

        for pizza, size_count_vars in self.pizza_sizes_counts.items():
            for size, count_var in size_count_vars.items():
                count = int(count_var.get())
                if count > 0:
                    drink_var, drink_count_var = self.drink_vars[pizza]
                    drink = drink_var.get()
                    drink_count = int(drink_count_var.get())
                    order_text += f"Pizza: {pizza} ({size}) x{count}\nDrink: {drink} x{drink_count}\n"

        self.order_text.insert(tk.END, order_text)
        self.order_text.config(state=tk.DISABLED)
        self.promotion_label.config(text=f"Total Promotion Savings: {self.total_promotion_savings} EUR")
        self.total_price_label.config(text=f"Total Price: {self.total_price} EUR")


# Initialize Tkinter root
root = tk.Tk()
app = PizzaSelector(root, env)
root.mainloop()

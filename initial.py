import clips
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import sys
import io

# Initialize CLIPS environment
env = clips.Environment()
env.load('fact3.clp')
env.reset()

# Define the new rule for the drink promotion
env.build("""
(defrule promocja-3-drinki-1-za-darmo
    ?f1 <- (UserSelection (drink ?drink) (drink_count ?drink_count &:(>= ?drink_count 4)))
    ?drink_fact <- (Drink (name ?drink) (price ?drink_price))
    =>
    (bind ?free_drinks (div ?drink_count 4)) ;; Number of free drinks
    (bind ?paid_drinks (- ?drink_count ?free_drinks)) ;; Drinks to be paid
    (bind ?cena-promocyjna (* ?paid_drinks ?drink_price)) ;; Promotional price for drinks
    (bind ?oszczednosc (* ?free_drinks ?drink_price)) ;; Savings from the promotion
    (assert (PromocjaNapoje (drink ?drink) (size none) (ilosc ?free_drinks) (cena ?cena-promocyjna) (oszczednosc ?oszczednosc)))
)
""")

env.run()

class PizzaSelector:
    def __init__(self, root, env):
        self.env = env
        self.root = root
        self.root.title("Pizza Selector")
        self.root.configure(bg='#f0f0f0')

        # Load and display image
        image = Image.open("pizza.jpg")
        image = image.resize((400, 200), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(root, image=self.photo, bg='#f0f0f0')
        image_label.pack(pady=10)

        title = tk.Label(root, text="Pizza Order Selection", bg='#f0f0f0', font=('Helvetica', 20, 'bold'))
        title.pack(pady=10)

        frame = tk.Frame(root, bg='#f0f0f0')
        frame.pack(pady=10)

        font = ('Helvetica', 14)

        # Get available pizzas and drinks from CLIPS environment
        self.pizzas = self.get_available_pizzas()
        self.sizes = ["small", "medium", "large"]
        self.drinks = self.get_available_drinks()

        # Pizza dropdown
        tk.Label(frame, text="Select Pizza:", bg='#f0f0f0', font=font).grid(row=0, column=0, sticky='w')
        self.pizza_var = tk.StringVar()
        self.pizza_menu = ttk.Combobox(frame, textvariable=self.pizza_var, values=list(self.pizzas.keys()), font=font, state='readonly')
        self.pizza_menu.grid(row=0, column=1, padx=10, pady=5)

        # Size dropdown
        tk.Label(frame, text="Select Size:", bg='#f0f0f0', font=font).grid(row=1, column=0, sticky='w')
        self.size_var = tk.StringVar()
        self.size_menu = ttk.Combobox(frame, textvariable=self.size_var, values=self.sizes, font=font, state='readonly')
        self.size_menu.grid(row=1, column=1, padx=10, pady=5)

        # Quantity spinbox
        tk.Label(frame, text="Quantity:", bg='#f0f0f0', font=font).grid(row=2, column=0, sticky='w')
        self.quantity_var = tk.StringVar(value='1')
        self.quantity_spinbox = tk.Spinbox(frame, from_=1, to=10, textvariable=self.quantity_var, font=font, width=5)
        self.quantity_spinbox.grid(row=2, column=1, padx=10, pady=5)

        # Drink dropdown
        tk.Label(frame, text="Select Drink:", bg='#f0f0f0', font=font).grid(row=3, column=0, sticky='w')
        self.drink_var = tk.StringVar()
        self.drink_menu = ttk.Combobox(frame, textvariable=self.drink_var, values=list(self.drinks.keys()), font=font, state='readonly')
        self.drink_menu.grid(row=3, column=1, padx=10, pady=5)

        # Drink quantity spinbox
        tk.Label(frame, text="Drink Quantity:", bg='#f0f0f0', font=font).grid(row=4, column=0, sticky='w')
        self.drink_quantity_var = tk.StringVar(value='1')
        self.drink_quantity_spinbox = tk.Spinbox(frame, from_=1, to=10, textvariable=self.drink_quantity_var, font=font, width=5)
        self.drink_quantity_spinbox.grid(row=4, column=1, padx=10, pady=5)

        # Order button
        self.order_button = tk.Button(root, text="Place Order", command=self.place_order, font=font, bg='#4caf50', fg='#ffffff')
        self.order_button.pack(pady=10)

        # Result display
        self.result_label = tk.Label(root, text="", bg='#f0f0f0', font=font)
        self.result_label.pack(pady=10)

        # Order details
        self.order_text = scrolledtext.ScrolledText(root, height=10, font=font, state=tk.DISABLED)
        self.order_text.pack(pady=10)

        # Promotion savings
        self.promotion_label = tk.Label(root, text="Total Promotion Savings: 0 EUR", bg='#f0f0f0', font=font)
        self.promotion_label.pack(pady=5)

        # Initialize totals
        self.total_promotion_savings = 0
        self.total_price = 0

    def get_available_pizzas(self):
        pizzas = {}
        for fact in self.env.facts():
            if fact.template.name == "Pizza":
                name = fact['name']
                size = fact['size']
                if name not in pizzas:
                    pizzas[name] = []
                pizzas[name].append(size)
        return pizzas

    def get_available_drinks(self):
        drinks = {}
        for fact in self.env.facts():
            if fact.template.name == "Drink":
                name = fact['name']
                drinks[name] = True
        return drinks

    def place_order(self):
        pizza = self.pizza_var.get()
        size = self.size_var.get()
        quantity = int(self.quantity_var.get())
        drink = self.drink_var.get()
        drink_quantity = int(self.drink_quantity_var.get())

        if not pizza or not size or not drink:
            messagebox.showerror("Input Error", "Please make a selection for each category.")
            return

        self.env.assert_string(
            f"(UserSelection (drink {drink}) (drink_count {drink_quantity}) (pizza {pizza}) (size {size}) (count {quantity}))"
        )
        self.env.run()

        self.display_order()

    def display_order(self):
        self.order_text.config(state=tk.NORMAL)
        self.order_text.delete(1.0, tk.END)

        pizza = self.pizza_var.get()
        size = self.size_var.get()
        quantity = int(self.quantity_var.get())
        drink = self.drink_var.get()
        drink_quantity = int(self.drink_quantity_var.get())

        order_text = f"Pizza: {pizza} ({size}) x {quantity}\nDrink: {drink} x {drink_quantity}\n"
        self.order_text.insert(tk.END, order_text)
        self.order_text.config(state=tk.DISABLED)

        # Calculate and display total price and promotions
        result_text = ""
        found_result = False
        for fact in self.env.facts():
            if fact.template.name == "Result":
                result_text += f"Total Price: {fact['total-price']} EUR\n"
                found_result = True

            if fact.template.name == "Promocja":
                promocja_ilosc = fact['ilosc']
                promocja_cena = fact['cena']
                promocja_oszczednosc = fact['oszczednosc']
                result_text += f"Promotion: Buy {promocja_ilosc} get {promocja_ilosc} free. Price: {promocja_cena} EUR. Savings: {promocja_oszczednosc} EUR\n"
                self.total_price -= promocja_oszczednosc
                self.total_promotion_savings += promocja_oszczednosc
                result_text += "Promotion applied.\n"

        if not found_result:
            result_text = "No result fact found. Please check the CLIPS rules."

        self.result_label.config(text=result_text)
        self.promotion_label.config(text=f"Total Promotion Savings: {self.total_promotion_savings} EUR")
        self.total_price_label.config(text=f"Total Price: {self.total_price} EUR")


# Initialize Tkinter root
root = tk.Tk()
app = PizzaSelector(root, env)
root.mainloop()

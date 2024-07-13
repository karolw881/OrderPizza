# Pizza Order Selector

## Overview

Pizza Order Selector is a Python-based GUI application for selecting and ordering pizzas and drinks. The application dynamically integrates with the CLIPS (C Language Integrated Production System) environment to handle business rules and logic, enabling real-time updates and dynamic rule integration. This allows users to benefit from various promotions and dynamic pricing based on the rules defined in CLIPS.

## Technologies Used

- **Python**: The primary programming language for the application.
- **Tkinter**: For creating the graphical user interface (GUI).
- **PIL (Pillow)**: For image processing and displaying.
- **CLIPS**: A rule-based programming language used to define and manage business rules and logic.

## Features

1. **Dynamic Rule Integration**: One of the key functionalities of this application is the ability to dynamically add rules. Any new rule added to the CLIPS environment is immediately reflected in the GUI, allowing real-time updates without the need for restarting the application.

2. **Promotional Pricing**: 
    - If a user orders 3 large pizzas, they receive a discount, making the total cost lower.
    - If a user orders 4 or more drinks, they receive one drink for free for every 4 drinks ordered.

3. **User-Friendly Interface**: The application provides an intuitive and easy-to-use interface for selecting pizzas, choosing sizes, and ordering drinks.

## Installation

1. **Clone the repository**:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install the required packages**:
    ```sh
    pip install clips
    pip install pillow
    ```

3. **Ensure the CLIPS environment is set up**. The rule file (`fact3.clp`) should be in the same directory as the script.

## Usage

1. **Run the application**:
    ```sh
    python pizza_order_selector.py
    ```

2. **Select Pizza and Drinks**: Use the dropdown menus to select the pizza type, size, and the number of drinks.

3. **Place Order**: Click the "Place Order" button to process your order and apply any relevant promotions.

## Code Explanation

### Initializing CLIPS Environment

The CLIPS environment is initialized, and the predefined rules are loaded from `fact3.clp`. The environment is reset to start fresh.

### Defining Rules

A new rule for drink promotion is built and added to the environment. This rule provides a free drink for every four drinks ordered.

### GUI Setup

Using Tkinter, a GUI is created which includes dropdown menus for pizza selection, size, and drink selection. An order button processes the user's selections and applies any relevant promotions.

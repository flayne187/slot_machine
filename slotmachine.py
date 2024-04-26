import tkinter as tk
import random

# Constants
MAX_LINES = 3
MAX_BET = 1000
MIN_BET = 1
ROWS = 3
COLS = 3

# Define the symbols, their count, and values
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

# Create the main window
root = tk.Tk()

# Create a label and entry widget to input the deposit
deposit_label = tk.Label(root, text="Deposit:")
deposit_label.pack()
deposit_entry = tk.Entry(root)
deposit_entry.pack()

# Create a function to handle the deposit button click
def handle_deposit():
    global balance
    deposit = int(deposit_entry.get())
    balance = deposit
    # do something with the deposit amount

# Create a label and entry widget to input the bet
bet_label = tk.Label(root, text="Bet per line:")
bet_label.pack()
bet_entry = tk.Entry(root)
bet_entry.pack()

# Create a label and entry widget to input the number of lines
lines_label = tk.Label(root, text="Number of lines:")
lines_label.pack()
lines_entry = tk.Entry(root)
lines_entry.pack()

# Create a balance label
balance_label = tk.Label(root, text="Balance: $0")
balance_label.pack()

# Initialize the balance
global balance
balance = 0

# Create a function to handle the spin button click
def handle_spin():
    global bet, lines, balance
    bet = int(bet_entry.get())
    lines = int(lines_entry.get())
    if bet * lines > balance:
        print("Insufficient balance")
        return

    balance -= bet * lines
    slot_machine = get_slot_machine_spin(ROWS, COLS, symbol_count)
    update_slot_machine(slot_machine)
    winnings, winning_lines = check_winnings(slot_machine, symbol_value, lines, bet)
    balance += winnings
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines)
    balance_label.config(text=f"Balance: ${balance}")

# Create a spin button
spin_button = tk.Button(root, text="Spin", command=handle_spin)
spin_button.pack()

# Create a canvas to display the slot machine
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Create a function to update the slot machine display
def update_slot_machine(slot_machine):
    # Clear the previous slot machine display
    for widget in canvas.winfo_children():
        widget.destroy()

    # Create a grid of labels to display the symbols
    symbols = ["A", "B", "C", "D"]
    for row in range(ROWS):
        for col in range(COLS):
            symbol = slot_machine[row][col]
            x = col * 100
            y = row * 100
            label = tk.Label(canvas, text=symbol, font=("Helvetica", 32), bg="white", fg="black",
                             width=1, height=1, bd=0, relief="solid")
            label.place(x=x, y=y)
            canvas.create_window(x, y, anchor="nw", window=label)

# Add your slot machine functions here
def get_slot_machine_spin(rows, cols, symbol_count):
    slot_machine = []
    for row in range(rows):
        row_list = []
        for col in range(cols):
            rand_num = random.randint(0, sum(list(symbol_count.values())))
            for symbol, count in symbol_count.items():
                if rand_num < count:
                    row_list.append(symbol)
                    break
                else:
                    rand_num -= count

        slot_machine.append(row_list)

    return slot_machine

def check_winnings(slot_machine, symbol_value, lines, bet):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbols = []
        for row in range(ROWS):
            col = cols - (line % COLS) - 1
            symbols.append(slot_machine[row][col])
        value = 0
        for symbol in symbols:
            value += symbol_value[symbol]
        if value > 0:
            winnings += bet
            winning_lines.append(line)
    return winnings, winning_lines

# Create the main loop
root.mainloop()
import tkinter as tk
from tkinter import messagebox, font as tkfont
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

DATA_FILE = "bmi_data.json"

# --- BMI Logic ---
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight" 
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def save_data(username, bmi):
    record = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "bmi": bmi}
    data = {}

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

    if username not in data:
        data[username] = []

    data[username].append(record)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def show_history(username):
    if not os.path.exists(DATA_FILE):
        messagebox.showinfo("History", "No data available.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if username not in data:
        messagebox.showinfo("History", "No data for this user.")
        return

    dates = [entry["date"] for entry in data[username]]
    bmis = [entry["bmi"] for entry in data[username]]

    plt.style.use("dark_background")
    plt.plot(dates, bmis, marker='o', color='orange')
    plt.xticks(rotation=45)
    plt.title(f"BMI History for {username}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.tight_layout()
    plt.show()

# --- GUI Logic ---
def on_calculate():
    try:
        username = entry_name.get().strip()
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        if not username:
            raise ValueError("Name is required.")

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        result_label.config(text=f"BMI: {bmi:.2f} ({category})", fg="orange")
        save_data(username, bmi)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# --- GUI Setup ---
root = tk.Tk()
root.title("BMI Calculator")
root.configure(bg="#1e1e1e")
root.geometry("400x400")
root.resizable(False, False)

custom_font = tkfont.Font(family="Helvetica", size=11)
heading_font = tkfont.Font(family="Helvetica", size=14, weight="bold")

def styled_label(text, row):
    label = tk.Label(root, text=text, bg="#1e1e1e", fg="white", font=custom_font)
    label.grid(row=row, column=0, sticky="e", padx=10, pady=8)

styled_label("Name:", 0)
styled_label("Weight (kg):", 1)
styled_label("Height (m):", 2)

entry_name = tk.Entry(root, font=custom_font, bg="#212020", fg="white", insertbackground="white")
entry_weight = tk.Entry(root, font=custom_font, bg="#212020", fg="white", insertbackground="white")
entry_height = tk.Entry(root, font=custom_font, bg="#212020", fg="white", insertbackground="white")

entry_name.grid(row=0, column=1, padx=10, pady=8)
entry_weight.grid(row=1, column=1, padx=10, pady=8)
entry_height.grid(row=2, column=1, padx=10, pady=8)

def styled_button(text, command, row):
    button = tk.Button(root, text=text, command=command,
                       bg="orange", fg="black", font=custom_font, 
                       activebackground="#ff9933", padx=10, pady=5)
    button.grid(row=row, column=0, columnspan=2, pady=10)

styled_button("CALCULATE BMI", on_calculate, 3)
styled_button("SHOW HISTORY", lambda: show_history(entry_name.get()), 4)

result_label = tk.Label(root, text="", font=heading_font, bg="#1e1e1e", fg="orange")
result_label.grid(row=5, column=0, columnspan=2, pady=20)

root.mainloop()


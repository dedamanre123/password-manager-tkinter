from json import JSONDecodeError
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


DEFAULT_EMAIL = "your_email@example.com"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    random_letter = [random.choice(letters) for _ in range(random.randint(5, 8))]
    random_symbols = [random.choice(symbols) for _ in range(random.randint(3, 5))]
    random_numbers = [random.choice(numbers) for _ in range(random.randint(4, 5))]

    password_list = random_letter + random_symbols + random_numbers
    random.shuffle(password_list)
    shuffle_list = password_list
    random.shuffle(shuffle_list)
    password = ''.join(shuffle_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_name = website_entry.get()
    password_en = password_entry.get()
    email = username_entry.get()
    new_data = {
        website_name: {
            'email': email,
            'password': password_en,
        }
    }
    if website_name == '' or password_en == '' or email == '':
        messagebox.showinfo(title='Error', message='Please enter a valid value in all fields')
    else:
        try:
            with open('password.json', 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            data = {}
        data.update(new_data)
        with open('password.json', 'w') as file:
            json.dump(data, file, indent=4)
        clear()

def clear():
    website_entry.delete(0, END)
    if username_entry.get() != DEFAULT_EMAIL:
        username_entry.delete(0, END)
        username_entry.insert(0, DEFAULT_EMAIL)
    password_entry.delete(0, END)

def search():
    website = website_entry.get()
    try:
        with open('password.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found.")
        return
    except JSONDecodeError:
        messagebox.showerror(title="Error", message="Data file is corrupted.")
        return

    if website in data:
        credentials = data[website]
        email = credentials.get('email', 'No email found')
        password = credentials.get('password', 'No password found')
        messagebox.showinfo(
            title=website,
            message=f"Email: {email}\nPassword: {password}"
        )
        pyperclip.copy(password)
    else:
        messagebox.showinfo(
            title="Not found",
            message=f"No details for '{website}' exists."
        )

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
try:
    picture = PhotoImage(file='logo.png')
    canvas = Canvas(window, width=200, height=200)
    canvas.create_image(100, 100, image=picture)
    canvas.grid(row=0, column=1)
except FileNotFoundError:
    Label(window, text="🔑 PASSWORD MANAGER", font=("Arial", 14, "bold")).grid(row=0, column=1, pady=20)

# Labels
Label(window, text="Website:").grid(row=1, column=0)
Label(window, text="Email/Username:").grid(row=2, column=0)
Label(window, text="Password:").grid(row=3, column=0)

# Entry fields
website_entry = Entry(window, width = 21)
website_entry.grid(row=1, column=1)
website_entry.focus()

username_entry = Entry(window, width=35)
username_entry.grid(row=2, column=1, columnspan=2)
username_entry.insert(0, DEFAULT_EMAIL)

password_entry = Entry(window, width=21)
password_entry.grid(row=3, column=1)

# Buttons
Button(window, text="Generate Password", width = 14, command=generate_password).grid(row=3, column=2)
Button(window, text="Add", width=36, command=save).grid(row=4, column=1, columnspan=2)
Button(window, text="Search", width = 14, command=search).grid(row=1, column=2)

window.mainloop()
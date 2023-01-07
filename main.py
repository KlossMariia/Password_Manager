from tkinter import *
from tkinter import messagebox
import random
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    # gets lists of random letters/symbols/numbers and unites them to one "password" list
    password = [random.choice(letters) for _ in range(random.randint(5, 7))]
    password += [random.choice(numbers) for _ in range(random.randint(4, 7))]
    password += [random.choice(symbols) for _ in range(random.randint(3, 5))]

    # shuffles password list
    random.shuffle(password)

    # turns "password" list into str
    password = "".join(password)

    # clears password entry
    password_entry.delete(0, END)
    # inserts password to password entry
    password_entry.insert(0, password)

# ---------------------------- SEARCH FOR DATA ------------------------------#
# this function gets you passwords which have been already saved before
def data_search():

    website = website_entry.get()
    user = username_entry.get()
# it tries to open data file, if it doesn't exist, it asks to add some data
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oooops!", message="No Data File found. At first add some data.")
    else:
        # if file exists, it tries to find needed data
        try:
            password = data[website]["password"]
            if user != data[website]["email"]:
                raise KeyError
        # if there is no needed data, raises an error
        except KeyError:
            messagebox.showerror(message="No details for the website exists")
        else:
            messagebox.showinfo(title=website, message=f"Email: {user}, \nPassword: {password}")
            password_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

# this function saves data to json file
def save_data():
    website = website_entry.get().capitalize()
    email = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    # checks if there are empty fields
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Ooooops!", message="Some fields are empty")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \n Email: {email} \n "
                                                      f"Password: {password} \n Is it ok to save?")

        if is_ok:
            try:
                # tries to open file
                with open("data.json", mode="r") as data_file:
                    data = json.load(data_file)
            # if no file found, it creates new file and writes data
            except FileNotFoundError or ValueError:
                with open("data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            # if file exists, adds data to it
            else:
                with open("data.json", mode="w") as data_file:
                    data.update(new_data)
                    json.dump(data, data_file, indent=4)
            # clears entries
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
#creating gui
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=190)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 95, image=image)
canvas.grid(column=0, row=0, columnspan=3)

Label(text="Website:").grid(column=0, row=1)
Label(text="Email/Username:").grid(column=0, row=2)
Label(text="Password:").grid(column=0, row=3)

website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()
username_entry = Entry(width=38)
username_entry.grid(column=1, row=2, columnspan=2)
username_entry.insert(0, "masha26.0251@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save_data)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=13, command=data_search)
search_button.grid(column=2, row=1)

window.mainloop()

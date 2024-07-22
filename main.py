import json
import string
from random import choice, randint, shuffle
from tkinter import *
from tkinter import messagebox

import pyperclip


# -------------------------- SEARCH PASSWORDS ------------------------- #
def search():
    website = website_entry.get()
    if website != '':
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
                entry = data[website]
        except FileNotFoundError:
            messagebox.showinfo(title='File not found', message='No existing data file found.')
        except KeyError:
            messagebox.showinfo(title='Entry not found', message='No existing website entry found.')
        else:
            email = entry['email']
            password = entry['password']
            messagebox.showinfo(title=website, message=f'Email: {email}\nPassword: {password}')


# ------------------------- GENERATE PASSWORD ------------------------- #
def generate():
    random_letters = [choice(string.ascii_letters) for _ in range(randint(8, 10))]
    random_symbols = [choice(string.digits) for _ in range(randint(2, 4))]
    random_numbers = [choice(string.punctuation) for _ in range(randint(2, 4))]
    password_list = random_letters + random_symbols + random_numbers
    shuffle(password_list)
    password = ''.join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# --------------------------- SAVE PASSWORD --------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            'email': email,
            'password': password
        }
    }

    if website == '' or email == '' or password == '':
        messagebox.showerror(title='Invalid input', message="Please don't leave any fields empty!")
    else:
        entry_ok = messagebox.askokcancel(title=website,
                                          message=f'These are the details entered: \n\n'
                                                  f'Email: {email} \n'
                                                  f'Password: {password} \n\n'
                                                  f'Is it ok to save?')
        if entry_ok:
            try:
                with open('data.json', 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open('data.json', 'w') as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg='white')

# Padlock image
canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Website label
website_label = Label(text='Website:', bg='white')
website_label.grid(column=0, row=1, sticky=W)

# Website entry
website_entry = Entry(width=30)
website_entry.grid(column=1, row=1, sticky=W)
website_entry.focus()

# Search button
generate_button = Button(text="Search", command=search, width=15)
generate_button.grid(column=2, row=1, sticky=W)

# Email/username label
email_label = Label(text='Email/Username:', bg='white')
email_label.grid(column=0, row=2, sticky=W)

# Email/username entry
email_entry = Entry(width=30)
email_entry.grid(column=1, row=2, sticky=W)
email_entry.insert(0, 'me@email.com')

# Password label
password_label = Label(text='Password:', bg='white')
password_label.grid(column=0, row=3, sticky=W)

# Password entry
password_entry = Entry(width=30)
password_entry.grid(column=1, row=3, sticky=W)

# Generate password button
generate_button = Button(text="Generate Password", width=15, command=generate)
generate_button.grid(column=2, row=3, stick=W)

# Add password button
add_button = Button(text="Add", width=25, command=save)
add_button.grid(column=1, row=5, sticky=W)

window.mainloop()

import json
import string
from random import choice, randint, shuffle
from tkinter import *
from tkinter import messagebox

import pyperclip


# -------------------------- SEARCH PASSWORDS ------------------------- #
def get_entry(website):
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            entry = data[website]
    except FileNotFoundError:
        return None, None
    except KeyError:
        return None, None
    else:
        email = entry['email']
        password = entry['password']
        return email, password


def search():
    website = website_entry.get()
    if website != '':
        email, password = get_entry(website)
        if email is None and password is None:
            messagebox.showinfo(title='Entry not found',
                                message='No existing website entry found.')
        else:
            pyperclip.copy(password)
            messagebox.showinfo(title=website, message=f'Email: {email}\nPassword: {
                password}\n\nPassword copied to the clipboard.')


# -------------------------- DELETE PASSWORD -------------------------- #
def delete():
    website = website_entry.get()
    if website != '':
        email, password = get_entry(website)
        if email is None and password is None:
            messagebox.showinfo(title='Entry not found',
                                message='No existing website entry found.')
        else:
            entry_ok = messagebox.askokcancel(title=website,
                                              message=f'Details found: \n\n'
                                              f'Email: {email} \n'
                                              f'Password: {password} \n\n'
                                              f'Ok to delete existing entry?\n')
            if entry_ok:
                with open('data.json', 'r') as file:
                    data = json.load(file)
                    del data[website]
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
                # website_entry.delete(0, END)


# ------------------------- GENERATE PASSWORD ------------------------- #


def generate():
    random_letters = [choice(string.ascii_letters)
                      for _ in range(randint(8, 10))]
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
        messagebox.showerror(title='Invalid input',
                             message="No field can be empty.")
    else:
        entry_ok = messagebox.askokcancel(title=website,
                                          message=f'Details entered: \n\n'
                                          f'Email: {email} \n'
                                          f'Password: {password} \n\n'
                                          f'Ok to save new entry/overwrite existing entry?\n')
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


# ---------------------------- CLEAR FIELDS --------------------------- #
def clear():
    website_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)


# ------------------------------ UI SETUP ----------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg='white')
window.rowconfigure(4, minsize=70)

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
generate_button = Button(text="Search", command=search, width=6)
generate_button.grid(column=2, row=1, sticky=W)

# Delete button
delete_button = Button(text="Delete", command=delete, width=6)
delete_button.grid(column=3, row=1, sticky=E)

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
generate_button.grid(column=2, row=3, columnspan=2, stick=W)

# Add password button
add_button = Button(text="Add", width=25, command=save)
add_button.grid(column=1, row=4, sticky=W)

# Clear fields button
clear_button = Button(text="Clear All Fields", width=15, command=clear)
clear_button.grid(column=2, row=4, columnspan=2, stick=W)

window.mainloop()

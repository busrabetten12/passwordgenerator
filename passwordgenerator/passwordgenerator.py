# importing libraries

import customtkinter
import string
import random
import os
from PIL import Image

# creating image objects for the buttons

file_path = os.path.dirname(os.path.realpath(__file__))

image_generate = customtkinter.CTkImage(Image.open(file_path + "/generate.png"), size=(24, 24))
image_copy = customtkinter.CTkImage(Image.open(file_path + "/copy.png"), size=(24, 24))

# setting the theme

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# some declarations

attributes = ["Uppercase", "Lowercase", "Numbers", "Symbols"]
checkbox_vars = {}
checkboxes = []
copy_button = None

# functions


def copy_to_clipboard():
    text_to_copy = label.cget("text")
    root.clipboard_clear()
    root.clipboard_append(text_to_copy)
    root.update()


def generate_password():
    global copy_button
    length = int(slider.get())
    password = ""

    selected_attributes = [attr for attr, var in checkbox_vars.items() if var.get()]

    if not selected_attributes:
        label.configure(text="Please select at least one attribute.")
        if copy_button:
            copy_button.destroy()
        return

    for _ in range(length):
        choice = random.choice(selected_attributes)
        if choice == "Uppercase":
            password += random.choice(string.ascii_uppercase)
        elif choice == "Lowercase":
            password += random.choice(string.ascii_lowercase)
        elif choice == "Numbers":
            password += random.choice(string.digits)
        elif choice == "Symbols":
            password += random.choice(string.punctuation)

    label.configure(text=password)

    for var in checkbox_vars.values():
        var.set(False)

    slider.set(0)

    slider_label.configure(text="Value: 0")

    if copy_button:
        copy_button.destroy()

    copy_button = customtkinter.CTkButton(master=root,
                                          text="Copy",
                                          command=copy_to_clipboard,
                                          fg_color=("black", "gray"),
                                          image=image_copy)
    copy_button.pack(pady=10)

    if length == 0:  # if the preferred length is equal to 0 then we shouldn't be able to see copy button
        copy_button.destroy()
        return


def update_label(value):
    slider_label.configure(text=f"Value: {int(value)}")


# root settings

root = customtkinter.CTk()
root.geometry("600x600")
root.title("Password Generator")

# widgets

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=30, padx=30, fill="both")

label = customtkinter.CTkLabel(master=frame,
                               text="Select all required attributes for your password",
                               font=("Roboto", 24))
label.pack(pady=12, padx=5)

label = customtkinter.CTkLabel(master=frame,
                               text="Preferred Length",
                               font=("Roboto", 22))
label.pack(pady=12, padx=10)

slider = customtkinter.CTkSlider(master=frame,
                                 from_=0, to=25, orientation="horizontal",
                                 command=update_label)
slider.set(0)
slider.pack()

slider_label = customtkinter.CTkLabel(master=frame,
                                      text="Value: 0")
slider_label.pack()

for attribute in attributes:
    checkbox_var = customtkinter.BooleanVar()
    checkbox = customtkinter.CTkCheckBox(master=frame,
                                         text=attribute,
                                         variable=checkbox_var)
    checkbox.pack(padx=10, pady=10)
    checkbox_vars[attribute] = checkbox_var
    checkboxes.append(checkbox)

button = customtkinter.CTkButton(master=frame,
                                 text="Generate",
                                 command=generate_password,
                                 fg_color=("black", "gray"),
                                 image=image_generate)
button.pack(pady=12, padx=10)

label = customtkinter.CTkLabel(master=root,
                               text="",
                               font=("Roboto", 28))
label.pack(pady=5, padx=5)

root.mainloop()

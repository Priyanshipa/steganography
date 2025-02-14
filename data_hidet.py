from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from stegano import lsb

root = Tk()
root.title("Steganography - Hide a Secret Message in Image")
root.geometry("700x500+150+180")
root.resizable(False, False)
root.configure(bg="#2f4155")

filename = None
secret = None  # Global variable to store the encoded image


def showimage():
    global filename, img
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Image File',
                                          filetypes=[("PNG file", "*.png"), ("JPG File", "*.jpg"), ("All Files", "*.*")])

    if filename:
        img = Image.open(filename)
        img = img.resize((250, 250))  # Resize image
        img = ImageTk.PhotoImage(img)
        lbl.configure(image=img, width=250, height=250)
        lbl.image = img


def Hide():
    global secret
    if filename:
        Message = text1.get(1.0, END).strip()  # Strip extra spaces/newlines
        if Message:
            secret = lsb.hide(filename, Message)  # Hide message inside image
            text1.delete(1.0, END)
            text1.insert(END, "Message hidden successfully!")
        else:
            text1.delete(1.0, END)
            text1.insert(END, "Error: No message to hide!")
    else:
        text1.delete(1.0, END)
        text1.insert(END, "Error: No image selected!")


def Show():
    if filename:
        try:
            clear_message = lsb.reveal(filename)
            if clear_message:
                text1.delete(1.0, END)
                text1.insert(END, clear_message)
            else:
                text1.delete(1.0, END)
                text1.insert(END, "No hidden message found!")
        except Exception as e:
            text1.delete(1.0, END)
            text1.insert(END, f"Error: {e}")
    else:
        text1.delete(1.0, END)
        text1.insert(END, "Error: No image selected!")


def save():

    if secret:
        save_path = os.path.join(os.getcwd(), "hidden.png")  # Save in the current directory
        try:
            secret.save(save_path)
            text1.delete(1.0, END)
            text1.insert(END, f"Hidden image saved as {save_path}")
        except Exception as e:
            text1.delete(1.0, END)
            text1.insert(END, f"Error saving image: {e}")
    else:
        text1.delete(1.0, END)
        text1.insert(END, "Error: No encoded image to save!")


# Icon
try:
    image = Image.open("logo.jpg")
    image_icon = ImageTk.PhotoImage(image)
    root.iconphoto(False, image_icon)
except FileNotFoundError:
    print("Warning: logo.jpg not found, skipping icon setup.")

# Logo
try:
    image_logo = Image.open("finger.jpg")
    image_logo = image_logo.resize((75, 75))
    logo = ImageTk.PhotoImage(image_logo)
    Label(root, image=logo, bg="#2f4155").place(x=10, y=10)
except FileNotFoundError:
    print("Warning: finger.jpg not found, skipping logo.")

Label(root, text="CYBER SCIENCE", bg="#2f4155", fg="white", font="arial 25 bold").place(x=100, y=30)

# First Frame (For Image)
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=90)
lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

# Second Frame (For Text Entry)
frame2 = Frame(root, bd=3, width=340, height=280, bg="white", relief=GROOVE)
frame2.place(x=350, y=90)

text1 = Text(frame2, font="Roboto 15", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)

# Scrollbar
Scrollbar1 = Scrollbar(frame2)
Scrollbar1.place(x=320, y=0, height=295)
Scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=Scrollbar1.set)

# Third Frame (Buttons for Image Selection & Save)
frame3 = Frame(root, bd=3, bg="#2f4155", width=340, height=100, relief=GROOVE)
frame3.place(x=10, y=370)
Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", command=showimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=30)
Label(frame3, text="Picture, Image, Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

# Fourth Frame (Buttons for Hiding & Showing Data)
frame4 = Frame(root, bd=3, bg="#2f4155", width=340, height=100, relief=GROOVE)
frame4.place(x=350, y=370)
Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", command=Hide).place(x=20, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", command=Show).place(x=180, y=30)
Label(frame4, text="Picture, Image, Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

root.mainloop()

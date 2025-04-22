from tkinter import*
from tkinter import filedialog
import tkinter as tk
from PIL import Image,ImageTk
import os

def showimage():
    filename=filedialog.askopenfilenmae(initialdir=os.getcwd(),title="select image file",filetype=(("JPG file","*.jpg"),("PNG file","*.png"),("ALL file")))
    img=Image.open(filename)
    img=ImageTk.PhotoImage(img)
    label.congigure(image=img)
    label.image=img
root=tk()

fram=Frame(root)
fram.pack(side=BOTTOM,padx=15 ,pady=15)
label =Label(root)
label.pack()

btn=Button(fram,text="Select Image",command=showimage )
btn.pack(side=tk.LEFT)

btn=Button(fram,text="Exit",command=lambda:exit() )
btn.pack(side=tk.LEFT,padx=12)

root.title("Image Viewer")
root.geometry("400x450")
root.mainloop
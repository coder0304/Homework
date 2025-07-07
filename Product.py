
from tkinter import *
from datetime import date

root = Tk()
root.title('Getting Started with Widgets')
root.geometry('400x300')

lbl = Label(text="Let's Multiply Two Numbers",
            fg="white",
            bg="#072F5F",
            height=1,
            width=300)

n1_lbl = Label(text="Enter Number 1", bg="#3895D3")
n1_entry = Entry()

n2_lbl = Label(text="Enter Number 2", bg="#3895D3")
n2_entry = Entry()


def multiply():
	
	n1 = int(n1_entry.get())
	n2 = int(n2_entry.get())
	product = n1 * n2

	text_box.insert(END, "Here's the final product...\n")
	text_box.insert(END, product)


text_box = Text(height=3)

btn = Button(text="Calculate",
             command=multiply,
             height=1,
             bg="#1261A0",
             fg='white')


lbl.pack()
n1_lbl.pack()
n1_entry.pack()
n2_lbl.pack()
n2_entry.pack()
btn.pack()
text_box.pack()
root.mainloop()

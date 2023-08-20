#!/usr/bin/env python3



# PyPad - Python Organized ScratchPad for scientific purposes
#
# v0.0.1 Beta
# Date: 8-19-2023
# Author: Tom Smith (Thomas DOT Briggs DOT Smith AT Gmail DOT com)




from tkinter import *
#import tkMessageBox
import tkinter


root = Tk()
root.geometry("777x575")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)

root.rowconfigure(0, weight=1)


### Setup our Parent Menubar
menubar = Menu(root)

# File
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command="")
filemenu.add_command(label="Save", command="")
filemenu.add_command(label="Close", command="")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# Edit



# Help
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="User Manual", command="")
helpmenu.add_command(label="Website", command="")
helpmenu.add_separator()
helpmenu.add_command(label="About", command="")
menubar.add_cascade(label="Help", menu=helpmenu)


# Stack our config
root.config(menu=menubar)


### UI Interface layout
#pane_window = PanedWindow(root)
#pane_window.pack(fill=BOTH, expand=1)

# Setup our organizing frames
left_frame = Frame(root, bg="red")
left_frame.pack(side="left", fill="y")

right_frame = Frame(root, bg="green")
right_frame.pack(side="right", fill="both", expand=1)


# Category Add, Edit, Delete buttons
cat_btn_frame = Frame(left_frame)
cat_btn_frame.pack(side="top")

cat_add = Button(cat_btn_frame, text="Add", command="")
cat_add.pack(side="left", fill="x", expand=1)

cat_edit = Button(cat_btn_frame, text="Edit", command="")
cat_edit.pack(side="left", fill="x", expand=1)

cat_del = Button(cat_btn_frame, text="Delete", command="")
cat_del.pack(side="left", fill="x", expand=1)


# Category listview
cat_list_frame = Frame(left_frame)
cat_list_frame.pack(side="top")

cat_list = Listbox(cat_list_frame)
cat_list.insert(1, "Hello")
cat_list.insert(2, "World")
cat_list.insert(3, "Ciao")
cat_list.insert(4, "Topic")
cat_list.insert(5, "Category")
cat_list.pack(side="top")


# File listview
file_list_frame = Frame(left_frame)
file_list_frame.pack(side="top")

file_list = Listbox(file_list_frame)
file_list.insert(0, "species.txt")
file_list.insert(1, "recipes.txt")
file_list.insert(2, "procedures.txt")
file_list.insert(3, "notes.txt")
file_list.pack(side="top")


# Our notepad window
notepad = Text(right_frame)
notepad.pack(side="right", fill="both", expand=1)




# __main__ loop()
root.mainloop()
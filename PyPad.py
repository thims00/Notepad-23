#!/usr/bin/env python3



# PyPad - Python Organized ScratchPad for scientific purposes
#
# v0.0.1 Beta
# Date: 8-19-2023
# Author: Tom Smith (Thomas DOT Briggs DOT Smith AT Gmail DOT com)



import os
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox



# Environment variables
user_data = "userData"
categ_path = "./" + user_data + "/Categories/"




### Initialize some information about our data directory
### and do some mild existence/access checks
# Ensure "Categories" exists and generate a dirList[]
if path.isdir(categ_path):
    categories = os.listdir(categ_path)
    categories.sort()
else:
    print("ERROR: ", categ_path, ": does not exist.")
    os.exit(1)



'''
Global Function Delcarations
'''
def add_categ():
    ctg_win = Toplevel(root)
    ctg_win.geometry("200x200")
    ctg_win.title("Child Window")
    
    lbl = Label(ctg_win, text="Label:")
    lbl.pack(side="left")
    
    add_categ_var = ""
    entry = Entry(ctg_win, textvariable=add_categ_var)
    entry.pack(side="right")
    
    btn = Button(ctg_win, text="Ok", command=ctg_win.destroy)
    btn.pack(side="bottom")
    print(add_categ_var)


# Populate a list of files from userData/Categories/AAA
def get_files(Category):
    file_list = []
    
    for file in os.listdir("./userData/Categories/" + Category):
        print(file)
        file_list.append(file)
            
    print(file_list)
    return file_list
            


root = Tk()
root.geometry("777x575")
root.minsize(777, 575)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=200)

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


### UI Interface layout ###
# Setup our organizing frames
left_frame = Frame(root)
left_frame.pack(side="left", fill="y")

right_frame = Frame(root)
right_frame.pack(side="right", fill="both", expand=1)


# Category Add, Edit, Delete buttons
cat_btn_frame = Frame(left_frame)
cat_btn_frame.pack(side="top")

cat_add = Button(cat_btn_frame, text="Add", command=add_categ)
cat_add.pack(side="left")

cat_edit = Button(cat_btn_frame, text="Edit", command="")
cat_edit.pack(side="left")

cat_del = Button(cat_btn_frame, text="Delete", command="")
cat_del.pack(side="left")

# Category list double click event
def categ_dc(event):
    lbox = cat_list.curselection()[0]
    selctn = cat_list.get(lbox)

    print(selctn)
    
    # Clear the filename listbox
    file_list.delete(0, file_list.size())
    
    # Get our files from userData
    files = get_files(selctn)
    
    # Update our file listbox
    
    for file in files:
        file_list.insert(END, file)
    
    
    
# Category listview
cat_list_frame = Frame(left_frame)
cat_list_frame.pack(side="top")

cat_list = Listbox(cat_list_frame)
n = 0
for categ in categories:
    cat_list.insert(n, categ)
    cat_list.bind('<Double-1>', categ_dc)
    n += 1
    
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
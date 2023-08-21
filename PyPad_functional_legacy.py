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

slctn_path = {'ctgry' : '', 'file' : ''}


# Operation Variables



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


# Populate a list of files from userData/Categories/AAA
def get_files(Category):
    file_list = []
    
    for file in os.listdir("./userData/Categories/" + Category):
        file_list.append(file)
            
    return file_list


# Open our text document and write contents to Text()
def change_notepad(event):
    indx = file_list.curselection()[0]
    read_file = file_list.get(indx)
    slctn_path['file'] = read_file
    
    try:
        fd = os.open("./userData/Categories/" + slctn_path['ctgry'] + "/" + slctn_path['file'], os.O_RDONLY)
    except FileNotFoundError:
        print("ERROR: that file does not exist. TODO: Make this a messageBOX")
    
    notepad.delete("0.0", END)
    
    chunk = os.read(fd, 1024)
    while chunk != b'':
        notepad.insert(END, chunk)
        chunk = os.read(fd, 1024)
    
    os.close(fd)


# Category list double click event
def categ_dc_event(event):
    clear_notepad()
    
    lbox = cat_list.curselection()[0]
    selctn = cat_list.get(lbox)
    slctn_path['ctgry'] = selctn
    
    # Clear the filename listbox
    file_list.delete(0, END)
    
    # Get our files from userData
    files = get_files(selctn)
    
    # Update our file listbox
    
    for file in files:
        file_list.insert(END, file)
        file_list.bind('<Double-1>', change_notepad)




# Clear notepad, saving first
def clear_notepad():
    save_notepad()
    notepad.delete("0.0", END)


# Save contents of notepad
def save_notepad():
    try:
        fd = os.open("./userData/Categories/" + slctn_path['ctgry'] + "/" \
            + slctn_path['file'], os.O_WRONLY|os.O_CREAT)
    except FileNotFoundError:
        print("ERROR: A weird one.")
        
    # TODO: Make this section write through chunks from notepad
    blob = notepad.get("0.0", END).encode()
    os.write(fd, blob)
    
    os.close(fd)




# Get the present category directories
if path.isdir(categ_path):
    categories = os.listdir(categ_path)
    categories.sort()
else:
    print("ERROR: ", categ_path, ": does not exist.")
    os.exit(1)

        
root = Tk()
root.geometry("777x575")
root.minsize(777, 575)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=200)

root.rowconfigure(0, weight=1)


### File Bar
menubar = Menu(root)

# File
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command="")
filemenu.add_command(label="Save", command=save_notepad)
filemenu.add_command(label="Close", command="")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


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
# Frames
left_frame = Frame(root)
left_frame.pack(side="left", fill="y")

right_frame = Frame(root)
right_frame.pack(side="right", fill="both", expand=1)


# Category Buttons
cat_btn_frame = Frame(left_frame)
cat_btn_frame.pack(side="top")

cat_add = Button(cat_btn_frame, text="Add", command=add_categ)
cat_add.pack(side="left")

cat_edit = Button(cat_btn_frame, text="Edit", command="")
cat_edit.pack(side="left")

cat_del = Button(cat_btn_frame, text="Delete", command="")
cat_del.pack(side="left")


# Categories Listview
cat_list_frame = Frame(left_frame)
cat_list_frame.pack(side="top")

cat_scrllbr = Scrollbar(cat_list_frame)
cat_scrllbr.pack(side=RIGHT, fill=Y)

cat_list = Listbox(cat_list_frame, yscrollcommand=cat_scrllbr.set)
n = 0
for categ in categories:
    cat_list.insert(n, categ)
    cat_list.bind('<Double-1>', categ_dc_event)
    n += 1
    
cat_list.pack(side="top")


# File listview
file_list_frame = Frame(left_frame)
file_list_frame.pack(side="top")

file_scrllbr = Scrollbar(file_list_frame)
file_scrllbr.pack(side=RIGHT, fill=Y)

file_list = Listbox(file_list_frame, yscrollcommand=file_scrllbr.set)
file_list.insert(0, "species.txt")
file_list.insert(1, "recipes.txt")
file_list.insert(2, "procedures.txt")
file_list.insert(3, "notes.txt")
file_list.pack(side="top")


# Notepad Window
notepad = Text(right_frame)
notepad.pack(side="right", fill="both", expand=1)




# __main__ loop()
root.mainloop()
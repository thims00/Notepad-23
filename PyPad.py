#!/usr/bin/env python3

# PyPad - Python Organized ScratchPad for scientific purposes
#
# v0.0.1 Beta
# Date: 8-19-2023
# Author: Tom Smith (Thomas DOT Briggs DOT Smith AT Gmail DOT com)


import os
from os import path
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class EditableListbox(tk.Listbox):
    """A listbox where you can directly edit an item via double-click

    SEE: https://stackoverflow.com/questions/64609658/python-tkinter-listbox-text-edit-in-gui"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.edit_item = None
        self.bind("<Double-1>", self._start_edit)

    def _start_edit(self, event):
        index = self.index(f"@{event.x},{event.y}")
        self.start_edit(index)
        return "break"

    def start_edit(self, index, accept_func=None,cancel_func=None):
        self.edit_item = index
        text = self.get(index)
        y0 = self.bbox(index)[1]
        entry = tk.Entry(self, borderwidth=0, highlightthickness=1)
        entry.bind("<Return>", self.accept_edit)
        entry.bind("<Escape>", self.cancel_edit)

        entry.insert(0, text)
        entry.selection_from(0)
        entry.selection_to("end")
        entry.place(relx=0, y=y0, relwidth=1, width=-1)
        entry.focus_set()
        entry.grab_set()

    def cancel_edit(self, event):
        event.widget.destroy()

    def accept_edit(self, event):
        new_data = event.widget.get()
        self.delete(self.edit_item)
        self.insert(self.edit_item, new_data)
        event.widget.destroy()


class PyPadGUI():
    ctgry_path = "./userData/Categories/"
    slctn_path = {'ctgry' : None, 'file' : None}


    ''' Local GUI __init__'''
    def __init__(self):
        self.__GUI__()
        self.__file_menu__()
        self.__ui_frames__()
        self.__categories__()
        self.__files__()
        self.__notepad__()
        self.__event_handler__()


    ''' Local GUI Methods'''
    def __GUI__(self):
        self.root = tk.Tk()
        self.root.geometry("777x575")
        self.root.minsize(777, 575)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=200)

        self.root.rowconfigure(0, weight=1)


    def __event_handler__(self):
        # Navigation pane events
        self.ctgry_list.bind('<Double-1>', self.category_dblClick_event)
        
        self.file_list.bind('<ButtonRelease-1>', self.file_click_event, add="+")
        print(self.file_list.bindtags())
        #self.file_list.bindtags(('.!frame.!frame3.!listbox', 'Listbox', '.', 'all'))

    def __file_menu__(self):
        ### File Bar
        self.menubar = tk.Menu(self.root)

        # File
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command="")
        self.filemenu.add_command(label="Save", command="") #save_notepad)
        self.filemenu.add_command(label="Close", command="")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)


        # Help
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="User Manual", command="")
        self.helpmenu.add_command(label="Website", command="")
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="About", command="")
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        
        # Stack our config
        self.root.config(menu=self.menubar)


    def __ui_frames__(self):
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side="right", fill="both", expand=1)


    def __categories__(self):
        # Category Buttons
        self.cat_btn_frame = tk.Frame(self.left_frame)
        self.cat_btn_frame.pack(side="top")

        self.cat_add = tk.Button(self.cat_btn_frame, text="Add", command=self.category_add) #add_categ)
        self.cat_add.pack(side="left")

        self.cat_edit = tk.Button(self.cat_btn_frame, text="Edit", command=self.category_edit)
        self.cat_edit.pack(side="left")

        self.cat_del = tk.Button(self.cat_btn_frame, text="Delete", command="")
        self.cat_del.pack(side="left")


        # Categories Listview
        self.ctgry_list_frame = tk.Frame(self.left_frame)
        self.ctgry_list_frame.pack(side="top")

        self.cat_scrllbr = tk.Scrollbar(self.ctgry_list_frame)
        self.cat_scrllbr.pack(side="right", fill="y")

        self.ctgry_list = EditableListbox(self.ctgry_list_frame)#, yscrollcommand=cat_scrllbr.set)

        # Populate categories by directory structure
        if path.isdir(self.ctgry_path):
            categories = os.listdir(self.ctgry_path)
            categories.sort()
        else:
            print("ERROR: ", self.ctgry_path, ": does not exist.")
            os.exit(1)

        for categ in categories:
            self.ctgry_list.insert("end", categ)

        self.ctgry_list.pack(side="top")


    def __files__(self):
        # File listview
        self.file_list_frame = tk.Frame(self.left_frame)
        self.file_list_frame.pack(side="top")

        self.file_scrllbr = tk.Scrollbar(self.file_list_frame)
        self.file_scrllbr.pack(side="right", fill="y")

        self.file_list = EditableListbox(self.file_list_frame)#, yscrollcommand=self.file_scrllbr.set)
        self.file_list.pack(side="top")


    def __notepad__(self):
        # Notepad Window
        self.notepad = tk.Text(self.right_frame)
        self.notepad_disable()
        self.notepad.pack(side="right", fill="both", expand=1)


    ''' Public GUI Events'''
    def category_dblClick_event(self, event):
        self.notepad_change()

        lbox = self.ctgry_list.curselection()[0]
        selctn = self.ctgry_list.get(lbox)
        self.slctn_path['ctgry'] = selctn
        self.slctn_path['file'] = ''

        # Clear the filename listbox
        self.file_list.delete(0, "end")

        # Get our files from userData
        files = self.files_get(selctn)

        # Update our file listbox

        for file in files:
            self.file_list.insert("end", file)
            #self.file_list.bind('<Double-1>', self.file_dblClick_event)

        self.notepad_disable()


    def file_click_event(self, event):
        print("file_click_event: Callback.")
        if self.slctn_path['file'] != '':
            self.notepad_save()
        
        print(self.file_list.curselection())
        indx = self.file_list.curselection()[0]
        read_file = self.file_list.get(indx)
        self.slctn_path['file'] = read_file

        self.notepad_clear()
        self.notepad_open(self.slctn_path['file'])


    ''' Public Category Methods'''
    def category_add(self):
        self.ctg_win = tk.Toplevel(self.root)
        self.ctg_win.geometry("200x200")
        self.ctg_win.title("Child Window")

        lbl = tk.Label(self.ctg_win, text="Label:")
        lbl.pack(side="left")

        self.add_categ_var = ""
        self.entry = tk.Entry(self.ctg_win, textvariable=self.add_categ_var)
        self.entry.pack(side="right")

        self.btn = tk.Button(self.ctg_win, text="Ok", command=self.ctg_win.destroy)
        self.btn.pack(side="bottom")
        
        print(self.add_categ_var)


    def category_edit(self):
        if self.slctn_path['ctgry'] != None:
            print("category_edit()")
            indx = self.ctgry_list.curselection()
            print(indx)
            self.ctgry_list.start_edit(indx)


    def category_delete(self):
        pass


    def category_rename(self):
        pass


    ''' Public Files Methods'''
    def files_get(self, event):
        files = []

        for file in os.listdir(self.ctgry_path + self.slctn_path['ctgry']):
            files.append(file)

        return files


    ''' Public Notepad Methods'''
    def notepad_change(self):
        self.notepad_save()
        self.notepad_clear()
        self.notepad.edit_modified(False)


    def notepad_clear(self):
        self.notepad.delete("0.0", "end")


    def notepad_disable(self):
        self.notepad.config(cursor="arrow")
        self.notepad.config(bg="#F0F0F0")
        self.notepad.config(state="disabled")


    def notepad_enable(self):
        self.notepad.config(cursor="xterm")
        self.notepad.config(bg="#ffffff")
        self.notepad.config(state="normal")


    def notepad_open(self, file):
        try:
            fd = open(self.ctgry_path + self.slctn_path['ctgry'] + "/" + file, "r")
        except FileNotFoundError:
            print("ERROR: that file does not exist. TODO: Make this a messageBOX")
            return False
        
        self.notepad_enable()
        
        chunk = fd.read(1024)
        while chunk != '':
            self.notepad.insert("end", chunk)
            chunk = fd.read(1024)
        
        fd.close()
        
        self.notepad.edit_modified(False)


    def notepad_save(self):
        if self.slctn_path['ctgry'] == None or self.slctn_path['file'] == None:
            print("WARNING: slctn_path[] is not set. Nothing saved.")
            return False
            
        elif self.slctn_path['file'] == '':
            print("WARNING: No file path set/selected. Nothing saved.")
            return False
        
        elif not self.notepad.edit_modified():
            return False
            
            
        try:
            fd = open(self.ctgry_path + self.slctn_path['ctgry'] + "/" \
                + self.slctn_path['file'], "w")
        except FileNotFoundError:
            print("ERROR: A weird one.")

        # TODO: Make this section write through chunks from notepad
        blob = self.notepad.get("0.0", "end")
        fd.write(blob)
        fd.close()
        
        self.notepad.edit_modified(False)


    def mainloop(self):
        self.root.mainloop()


# Main loop()
GUI = PyPadGUI()
GUI.mainloop()
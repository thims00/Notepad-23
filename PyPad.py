import os
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox




class PyPadGUI():
    categ_path = "./userData/Categories/"


    def __init__(self):
        self.__GUI__()
        self.__file_menu__()
        self.__ui_frames__()
        self.__categories__()
        self.__files__()
        self.__notepad__()
    
    
    def __GUI__(self):
        self.root = Tk()
        self.root.geometry("777x575")
        self.root.minsize(777, 575)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=200)

        self.root.rowconfigure(0, weight=1)
    
    
    def __file_menu__(self):
        ### File Bar
        self.menubar = Menu(self.root)

        # File
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command="")
        self.filemenu.add_command(label="Save", command="") #save_notepad)
        self.filemenu.add_command(label="Close", command="")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)


        # Help
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="User Manual", command="")
        self.helpmenu.add_command(label="Website", command="")
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="About", command="")
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        
        # Stack our config
        self.root.config(menu=self.menubar)
    
    
    def __ui_frames__(self):
        self.left_frame = Frame(self.root)
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = Frame(self.root)
        self.right_frame.pack(side="right", fill="both", expand=1)
    
    
    def __categories__(self):
        # Category Buttons
        self.cat_btn_frame = Frame(self.left_frame)
        self.cat_btn_frame.pack(side="top")

        self.cat_add = Button(self.cat_btn_frame, text="Add", command="") #add_categ)
        self.cat_add.pack(side="left")

        self.cat_edit = Button(self.cat_btn_frame, text="Edit", command="")
        self.cat_edit.pack(side="left")

        self.cat_del = Button(self.cat_btn_frame, text="Delete", command="")
        self.cat_del.pack(side="left")


        # Categories Listview
        self.cat_list_frame = Frame(self.left_frame)
        self.cat_list_frame.pack(side="top")

        self.cat_scrllbr = Scrollbar(self.cat_list_frame)
        self.cat_scrllbr.pack(side=RIGHT, fill=Y)

        self.cat_list = Listbox(self.cat_list_frame)#, yscrollcommand=cat_scrllbr.set)
        
        # Populate categories by directory structure
        if path.isdir(self.categ_path):
            categories = os.listdir(self.categ_path)
            categories.sort()
        else:
            print("ERROR: ", self.categ_path, ": does not exist.")
            os.exit(1)
        n = 0
        for categ in categories:
            self.cat_list.insert(n, categ)
            self.cat_list.bind('<Double-1>', "") #categ_dc_event)
            n += 1
            
        self.cat_list.pack(side="top")


    def __files__(self):
        # File listview
        self.file_list_frame = Frame(self.left_frame)
        self.file_list_frame.pack(side="top")

        self.file_scrllbr = Scrollbar(self.file_list_frame)
        self.file_scrllbr.pack(side=RIGHT, fill=Y)

        self.file_list = Listbox(self.file_list_frame)#, yscrollcommand=self.file_scrllbr.set)
        self.file_list.insert(0, "species.txt")
        self.file_list.insert(1, "recipes.txt")
        self.file_list.insert(2, "procedures.txt")
        self.file_list.insert(3, "notes.txt")
        self.file_list.pack(side="top")


    def __notepad__(self):
        # Notepad Window
        self.notepad = Text(self.right_frame)
        self.notepad.pack(side="right", fill="both", expand=1)

    
    def mainloop(self):
        self.root.mainloop()
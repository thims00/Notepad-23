import os
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox




class PyPadGUI():
    ctgry_path = "./userData/Categories/"
    slctn_path = {'ctgry' : '', 'file' : ''}
    
    
    
    
    def __init__(self):
        self.__GUI__()
        self.__file_menu__()
        self.__ui_frames__()
        self.__categories__()
        self.__files__()
        self.__notepad__()
    

    '''
    Local GUI Methods
    '''
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
        self.ctgry_list_frame = Frame(self.left_frame)
        self.ctgry_list_frame.pack(side="top")

        self.cat_scrllbr = Scrollbar(self.ctgry_list_frame)
        self.cat_scrllbr.pack(side=RIGHT, fill=Y)

        self.ctgry_list = Listbox(self.ctgry_list_frame)#, yscrollcommand=cat_scrllbr.set)
        
        # Populate categories by directory structure
        if path.isdir(self.ctgry_path):
            categories = os.listdir(self.ctgry_path)
            categories.sort()
        else:
            print("ERROR: ", self.ctgry_path, ": does not exist.")
            os.exit(1)
        n = 0
        for categ in categories:
            self.ctgry_list.insert(n, categ)
            self.ctgry_list.bind('<Double-1>', self.category_dblClick_event)
            n += 1
            
        self.ctgry_list.pack(side="top")


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
        
        
    '''
    Public GUI Events
    '''
    def category_dblClick_event(self, event):
        self.notepad_clear()
    
        lbox = self.ctgry_list.curselection()[0]
        selctn = self.ctgry_list.get(lbox)
        self.slctn_path['ctgry'] = selctn
        
        # Clear the filename listbox
        self.file_list.delete(0, END)
        
        # Get our files from userData
        files = self.files_get(selctn)
        
        # Update our file listbox
        
        for file in files:
            self.file_list.insert(END, file)
            self.file_list.bind('<Double-1>', self.notepad_write)


    '''
    Public Category Methods
    '''
    def category_add(self):
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


    ''' 
    Public Files Methods
    '''
    def files_get(self, event):
        files = []

        for file in os.listdir(self.ctgry_path + self.slctn_path['ctgry']):
            files.append(file)
                
        return files


    '''
    Public Notepad Methods
    '''
    def notepad_write(self, event):
        indx = self.file_list.curselection()[0]
        read_file = self.file_list.get(indx)
        self.slctn_path['file'] = read_file
        
        try:
            fd = os.open(self.ctgry_path + self.slctn_path['ctgry'] + \
                 "/" + self.slctn_path['file'], os.O_RDONLY)
        except FileNotFoundError:
            print("ERROR: that file does not exist. TODO: Make this a messageBOX")
        
        self.notepad.delete("0.0", END)
        
        chunk = os.read(fd, 1024)
        while chunk != b'':
            self.notepad.insert(END, chunk)
            chunk = os.read(fd, 1024)
        
        os.close(fd)
    
    
    def notepad_clear(self):
        #save_notepad()
        self.notepad.delete("0.0", END)
    
    
    def notepad_save(self):
        try:
            fd = os.open("./userData/Categories/" + self.slctn_path['ctgry'] + "/" \
                + self.slctn_path['file'], os.O_WRONLY|os.O_CREAT)
        except FileNotFoundError:
            print("ERROR: A weird one.")
            
        # TODO: Make this section write through chunks from notepad
        blob = self.notepad.get("0.0", END).encode()
        os.write(fd, blob)
        
        os.close(fd)
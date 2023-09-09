#!/usr/bin/env python3

# PyPad - Python Organized ScratchPad for scientific purposes
#
# v0.0.1 Beta
# Date: 8-19-2023
# Author: Tom Smith (Thomas DOT Briggs DOT Smith AT Gmail DOT com)


import os
import os.path
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb


class DataHandle:
    basepath = r'C:\Users\rootp\Documents\Code\Python\GUI\PyPad'
    datapath = r'userData\Categories'
    listbox_elem_type = None
    EditLbox_old_entry = None
    EditLbox_new_entry = None
    slctn_path = {'ctgry' : None, 'file' : None}


class FileOps():
    '''TODO: 
        - Add failsafe datapath so cwd() is used if user definition fails
        - Do better checking on user defined paths existence / (RW)ability
    '''
    def __init__(self, base_path=None, data_path=None):
        if base_path:
            self.path = fr'{os.path.abspath(base_path)}'
        else:
            self.path = fr'{os.getcwd()}'

        if data_path:
            self.path = fr'{self.path}\\{data_path}'

        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path, " non-existent")

        self.dh = DataHandle()

    def get_base(self):
        base = self.path
        ctgry = self.dh.slctn_path['ctgry']
        file = self.dh.slctn_path['file']
        
        try:
            if file:
                base = f'{base}\\{ctgry}\\{file}'
            else:
                base = f'{base}\\{ctgry}'

        except:
            print('ERROR:: FileOps():: get_base():: ValueError')
            
        return base

    def is_file(self):
        file = self.get_base()
        return os.path.isfile(file)

    def is_dir(self):
        file = self.get_base()
        os.path.isdir(file)

    def is_rw(self):
        file = self.get_base()
        os.access(file, os.R_OK & os.W_OK)

    def touch(self):
        file = self.get_base()
        
        if self.is_file():
            print(fr'WARNING: Could not create file "{file}". File exists.')
            return False

        fd = open(file, "x")
        fd.close()

        return True
        
    def mkdir(self):
        file = self.get_base()
        
        if self.is_dir():
            print(fr'ALERT: Did not create directory: "{file}". Directory exists.')
            return False
        else:
            os.mkdir(file)
        
        return True

    def rename(self, new):
        file = self.get_base()
        tmp = file.split("\\")
        new_path = "\\".join(tmp[0:-1])
        print(f"FileOps():: rename():: {new_path}")
        
        os.rename(file, fr'{new_path}\\{new}')

    def delete(self):
        file = self.get_base()

        if self.is_file():
            os.remove(file)
            return True
        else:
            os.rmdir(file)
            return True


class EditableListbox(tk.Listbox):
    """A listbox where you can directly edit an item via double-click
        Source: https://stackoverflow.com/questions/64609658/python-tkinter-listbox-text-edit-in-gui"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.edit_item = None

    def _start_edit(self, event):
        index = self.index(f"@{event.x},{event.y}")
        self.start_edit(index)
        return "break"

    def start_edit(self, index, accept_func=None,cancel_func=None):
        self.accept_func = accept_func
        self.cancel_func = cancel_func

        if self.bbox(index) == None:
            self.see(index)

        self.edit_item = index
        DataHandle.EditLbox_old_entry = self.get(index)
        y0 = self.bbox(index)[1]
        entry = tk.Entry(self, borderwidth=0, highlightthickness=1)
        entry.bind("<Return>", self.accept_edit)
        entry.bind("<Escape>", self.cancel_edit)

        entry.insert(0, DataHandle.EditLbox_old_entry)
        entry.selection_from(0)
        entry.selection_to("end")
        entry.place(relx=0, y=y0, relwidth=1, width=-1)
        entry.focus_set()
        entry.grab_set()

    def cancel_edit(self, event):
        DataHandle.EditLbox_new_entry = None
        event.widget.destroy()

        if self.cancel_func:
            self.cancel_func(self)

    def accept_edit(self, event):
        DataHandle.EditLbox_new_entry = event.widget.get()
        self.delete(self.edit_item)
        self.insert(self.edit_item, DataHandle.EditLbox_new_entry)
        event.widget.destroy()
        

        if self.accept_func:
            self.accept_func(self)


class PyPadGUI():
    #ctgry_path = r'userData/Categories'
    #slctn_path = {'ctgry' : None, 'file' : None}
    #listbox_elem_type = None


    def __init__(self):
        self.fo = FileOps(DataHandle.basepath, DataHandle.datapath)
    
        self.__GUI__()
        self.__file_menu__()
        self.__ui_frames__()
        self.__ui_buttons__()
        self.__categories__()
        self.__files__()
        self.__notepad__()
        self.__event_handler__()


    """ Local GUI Methods"""
    def __GUI__(self):
        self.root = tk.Tk()
        self.root.geometry("777x575")
        self.root.minsize(777, 575)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=200)

        self.root.rowconfigure(0, weight=1)

    def __event_handler__(self):
        # Navigation pane events
        self.ctgry_list.bind('<Double-1>', self.category_dblClick_event, add="+")
        self.file_list.bind('<ButtonRelease-1>', self.file_click_event, add="+")

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

    def __ui_buttons__(self):
        self.ui_btn_frame = tk.Frame(self.left_frame)
        self.ui_btn_frame.pack(side="top")

        self.ui_add = tk.Button(self.ui_btn_frame, text="Add", command=self.listbox_add_clicked)
        self.ui_add.pack(side="left")

        self.ui_edit = tk.Button(self.ui_btn_frame, text="Edit", command=self.listbox_edit_clicked)
        self.ui_edit.pack(side="left")

        self.ui_delete = tk.Button(self.ui_btn_frame, text="Delete", command=self.listbox_delete_clicked)
        self.ui_delete.pack(side="left")    

    def __categories__(self):
        # Categories Listview
        self.ctgry_list_frame = tk.Frame(self.left_frame)
        self.ctgry_list_frame.pack(side="top")

        self.cat_scrllbr = tk.Scrollbar(self.ctgry_list_frame)
        self.cat_scrllbr.pack(side="right", fill="y")

        self.ctgry_list = EditableListbox(self.ctgry_list_frame)#, yscrollcommand=cat_scrllbr.set)

        # Populate categories by directory structure
        categories = os.listdir(DataHandle.datapath)
        categories.sort()

        if len(categories) == 0:
            self.disable_ui_btns()
            
        for categ in categories:
            self.ctgry_list.insert("end", categ)

        self.ctgry_list.pack(side="top")

        self.ctgry_list.elem_type = "category"

    def __files__(self):
        # File listview
        self.file_list_frame = tk.Frame(self.left_frame)
        self.file_list_frame.pack(side="top")

        self.file_scrllbr = tk.Scrollbar(self.file_list_frame)
        self.file_scrllbr.pack(side="right", fill="y")

        self.file_list = EditableListbox(self.file_list_frame)#, yscrollcommand=self.file_scrllbr.set)
        self.file_list.pack(side="top")
        
        self.file_list.elem_type = "file"

    def __notepad__(self):
        # Notepad Window
        self.notepad = tk.Text(self.right_frame)
        self.notepad_disable()
        self.notepad.pack(side="right", fill="both", expand=1)

    def __statusbar__(self):
        pass


    """ Public Event Handling Methods"""
    def category_dblClick_event(self, event):
        self.notepad_change()

        lbox = self.ctgry_list.curselection()[0]
        selctn = self.ctgry_list.get(lbox)
        DataHandle.slctn_path['ctgry'] = selctn
        DataHandle.slctn_path['file'] = None

        # Clear the filename listbox
        self.file_list.delete(0, "end")

        # Get our files from userData
        files = self.files_get(selctn)

        # Update our file listbox

        for file in files:
            self.file_list.insert("end", file)

        self.notepad_disable()
        
        self.file_list.focus_set()

    def file_click_event(self, event):
        if DataHandle.slctn_path['file'] != '':
            self.notepad_save()
        
        try:
            indx = self.file_list.curselection()[0]
        except IndexError:
            indx = 0
        read_file = self.file_list.get(indx)
        DataHandle.slctn_path['file'] = read_file

        self.notepad_clear()
        self.notepad_open(DataHandle.slctn_path['file'])

    def on_focus(self, event):
        pass


    """ Public Listbox Methods"""
    def listbox_add_clicked(self):
        self.listbox_handle("add")

    def listbox_edit_clicked(self):
        self.listbox_handle("edit")

    def listbox_delete_clicked(self):
        self.listbox_handle("delete")

    def listbox_handle(self, func=None):
        lb_widget = self.root.focus_get()

        if lb_widget.size() == 0:
            self.disable_ui_btns()
            self.listbox_add()
            return

        else:
            try:
                indx = lb_widget.curselection()[0]
            except:
                print("WARNING: Supressed error for quiet UI behavior: Unknown circumstance - JJWWUSKKWUU")


        if not lb_widget.elem_type in ['category', 'file']:
            print("WARNING: _listbox_handle():: lb_widget.listbox_name:: ValueError: Undefined")
            return None


        # Process UI event code and make respective handle calls
        if func == "add":
            self.listbox_add(lb_widget)

        elif func == "edit":
            self.listbox_edit(lb_widget)

        elif func == "delete":

            self.listbox_delete(lb_widget)

        else:
            print("WARNING: _listbox_handle(): ", func, " invalid argument.")
            return None

    def listbox_add(self, wdgtObj):
        wdgtObj.insert("end", "New Item")
        indx = wdgtObj.size() - 1
        wdgtObj.start_edit(indx, self.listbox_add_callback)

    def listbox_add_callback(self, wdgtObj):
        if wdgtObj.elem_type == "file":
            self.fo.touch(fr"{DataHandle.slctn_path['ctgry']}\\{DataHandle.EditLbox_new_entry}")
            
        elif wdgtObj.elem_type == "category":
            self.fo.mkdir(DataHandle.EditLbox_new_entry)
        
        else:
            print("ERROR:: listbox_file_add():: Unknown Error - AABBCC93829283")
            return False

    def listbox_edit(self, wdgtObj):
        wdgtObj.start_edit(indx, listbox_edit_callback)

    def listbox_edit_callback(self, wdgtObj):
        self.fo.rename(DataHandle.EditLbox_old_entry, DataHandle.EditLbox_new_entry)
        
    def listbox_delete(self, wdgtObj):
        wdgtObj = self.root.focus_get()
        elem = wdgtObj.get(wdgtObj.curselection()[0])
        del_bool = mb.askyesno("Confirm Delete", f'You are about to delete {elem}.\nAre you sure?')
        
        
        if del_bool:
            self.fo.delete()
            wdgtObj.delete(wdgtObj.curselection()[0])


    """ Public Files Methods"""
    def files_get(self, event):
        files = []

        path = f"{DataHandle.basepath}\\{DataHandle.datapath}\\{DataHandle.slctn_path['ctgry']}"
        for file in os.listdir(path):
            files.append(file)

        return files


    """ Public Notepad Methods"""
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
            fd = open(f"{self.fo.path}\{DataHandle.slctn_path['ctgry']}\{file}", "r")
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
        if DataHandle.slctn_path['ctgry'] == None or DataHandle.slctn_path['file'] == None:
            print("WARNING: slctn_path[] is not set. Nothing saved.")
            return False
            
        elif DataHandle.slctn_path['file'] == '':
            print("WARNING: No file path set/selected. Nothing saved.")
            return False
        
        elif not self.notepad.edit_modified():
            return False
            
            
        try:
            fd = open(f"{self.fo.path}{DataHandle.slctn_path['ctgry']}\{DataHandle.slctn_path['file']}", "w")
        except FileNotFoundError:
            print("ERROR: A weird one. - 9372ieklsfnuwiiojfdsa")

        # TODO: Make this section write through chunks from notepad
        blob = self.notepad.get("0.0", "end")
        fd.write(blob)
        fd.close()
        
        self.notepad.edit_modified(False)

    def mainloop(self):
        self.root.mainloop()

    """ Misc UI Functions"""
    def enable_ui_btns(self):
        self.ui_edit['state'] = 'disabled'
        self.ui_delete['state'] = 'disabled'
        
    def disable_ui_btns(self):
        self.ui_edit['state'] = 'normal'
        self.ui_edit['state'] = 'normal'




# Main loop()
if __name__ == "__main__":
    GUI = PyPadGUI()
    GUI.mainloop()
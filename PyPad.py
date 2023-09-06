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


basepath = r'C:\Users\rootp\Documents\Code\Python\GUI\PyPad'
datapath = r'userData\Categories'


class FileOps():
    def __init__(self, base_path=None, data_path=None):
        if base_path:
            self.path = fr'{os.path.abspath(base_path)}\\'
        else:
            self.path = fr'{os.getcwd()}\\'

        if data_path:
            self.path = fr'{self.path}{data_path}\\'

        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path, " non-existent")

    def get_base(self):
        pass

    def is_file(self, file):
        if isinstance(file, list):
            for x in file:
                ret = os.path.isfile(fr'{self.path}{file}')
                
                if not ret:
                    return False
                    
        else:
            ret = os.path.isfile(fr'{self.path}{file}')
            
        return ret

    def is_dir(self, file):
        if isinstance(file, list):
            for x in file:
                ret = os.path.isdir(fr'{self.path}{file}')
                
                if not ret:
                    return False
                    
        else:
            ret = os.path.isdir(fr'{self.path}{file}')
            
        return ret

    def is_rw(self, file):
        if isinstance(file, list):
            for x in file:
                ret = os.access(fr'{self.path}{file}', os.R_OK & os.W_OK)
                
                if not ret:
                    return False
                    
        else:
            ret = os.access(fr'{self.path}{file}', os.R_OK & os.W_OK)
            
        return ret

    def touch(self, file):
        if self.is_file(file):
            print(fr'WARNING: Could not create file "{self.path}{file}". File exists.')
            return False

        fd = open(fr'{self.path}{file}', "x")
        fd.close()

        return True
        
    def mkdir(self, file):
        if self.is_dir(file):
            print(fr'ALERT: Did not create directory: "{self.path}{file}". Directory exists.')
            return False
        else:
            os.mkdir(fr'{self.path}{file}')
        
        return True

    def rename(self, old, new):
            os.rename(fr'{self.path}{old}', fr'{self.path}{new}')

    def delete(self, file):
        if self.is_file(file):
            os.remove(fr'{self.path}{file}')
        elif self.is_dir(file):
            os.rmdir(fr'{self.path}{file}')
        else:
            raise Exception(fr'FileError: Unknown file operation error: "{self.path}{file}')


class EditableListbox(tk.Listbox):
    """A listbox where you can directly edit an item via double-click
        Source: https://stackoverflow.com/questions/64609658/python-tkinter-listbox-text-edit-in-gui"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.edit_item = None
        self.entry_data = None
        
        # EditableListbox Data Object
        class EditableListboxObj:
            listbox_elem_type = None
            old_data = None
            new_data = None
            
        self.EdList = EditableListboxObj()

    def _start_edit(self, event):
        index = self.index(f"@{event.x},{event.y}")
        self.start_edit(index)
        return "break"

    def start_edit(self, index, accept_func=None,cancel_func=None):
        print("start_edit():: line:: 128 BEGIN")
        self.accept_func = accept_func
        self.cancel_func = cancel_func

        if self.bbox(index) == None:
            self.see(index)

        self.edit_item = index
        self.EdList.old_data = self.get(index)
        y0 = self.bbox(index)[1]
        entry = tk.Entry(self, borderwidth=0, highlightthickness=1)
        print("start_edit():: line:: 139")
        entry.bind("<Return>", self.accept_edit)
        entry.bind("<Escape>", self.cancel_edit)
        print("start_edit():: line:: 142")
        #bt = entry.bindtags()
        #entry.bindtags((bt[1], bt[0], bt[2], bt[3]))
        print(entry.bindtags())

        entry.insert(0, self.EdList.old_data)
        entry.selection_from(0)
        entry.selection_to("end")
        entry.place(relx=0, y=y0, relwidth=1, width=-1)
        entry.focus_set()
        entry.grab_set()
        print("start_edit() END")

    def cancel_edit(self, event):
        print("cancel_edit():: line:: 156:: BEGIN")
        self.EdList.new_data = None
        print("cancel_edit():: line:: 158")
        event.widget.destroy()
        
        print("cancel_edit():: line:: 161")
        if self.cancel_func:
            print("cancel_edit():: line:: 163:: cancel_func() callback(PRE)")
            self.cancel_func(self.EdList)
            print("cancel_edit():: line:: 165:: cancel_func() callback(POST)")
            
        print("cancel_edit():: line:: END")

    def accept_edit(self, event):
        print("accept_edit():: line:: 168:: BEGIN")
        self.EdList.new_data = event.widget.get()
        self.delete(self.edit_item)
        self.insert(self.edit_item, self.EdList.new_data)
        event.widget.destroy()
        

        if self.accept_func:
            print("accept_edit:: accept_func:: callback")
            self.accept_func(self.EdList)
            
        print("accept_edit():: line:: END")


class PyPadGUI():
    ctgry_path = r'userData/Categories'
    slctn_path = {'ctgry' : None, 'file' : None}
    listbox_elem_type = None


    def __init__(self):
        self.fo = FileOps(basepath, datapath)
    
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

        self.ui_add = tk.Button(self.ui_btn_frame, text="Add", command=self.listbox_add_event)
        self.ui_add.pack(side="left")

        self.ui_edit = tk.Button(self.ui_btn_frame, text="Edit", command=self.listbox_edit_event)
        self.ui_edit.pack(side="left")

        self.ui_delete = tk.Button(self.ui_btn_frame, text="Delete", command=self.listbox_delete_event)
        self.ui_delete.pack(side="left")    

    def __categories__(self):
        # Categories Listview
        self.ctgry_list_frame = tk.Frame(self.left_frame)
        self.ctgry_list_frame.pack(side="top")

        self.cat_scrllbr = tk.Scrollbar(self.ctgry_list_frame)
        self.cat_scrllbr.pack(side="right", fill="y")

        self.ctgry_list = EditableListbox(self.ctgry_list_frame)#, yscrollcommand=cat_scrllbr.set)

        # Populate categories by directory structure
        categories = os.listdir(self.ctgry_path)
        categories.sort()

        for categ in categories:
            self.ctgry_list.insert("end", categ)

        self.ctgry_list.pack(side="top")

        # Local Listbox() id
        self.ctgry_list.EdList.listbox_elem_type = "category"

    def __files__(self):
        # File listview
        self.file_list_frame = tk.Frame(self.left_frame)
        self.file_list_frame.pack(side="top")

        self.file_scrllbr = tk.Scrollbar(self.file_list_frame)
        self.file_scrllbr.pack(side="right", fill="y")

        self.file_list = EditableListbox(self.file_list_frame)#, yscrollcommand=self.file_scrllbr.set)
        self.file_list.pack(side="top")
        
        # Local object listbox name identifier
        self.file_list.EdList.listbox_elem_type = "file"

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
        self.slctn_path['ctgry'] = selctn
        self.slctn_path['file'] = ''

        # Clear the filename listbox
        self.file_list.delete(0, "end")

        # Get our files from userData
        files = self.files_get(selctn)

        # Update our file listbox

        for file in files:
            self.file_list.insert("end", file)

        self.notepad_disable()

    def file_click_event(self, event):
        if self.slctn_path['file'] != '':
            self.notepad_save()
        
        indx = self.file_list.curselection()[0]
        read_file = self.file_list.get(indx)
        self.slctn_path['file'] = read_file

        self.notepad_clear()
        self.notepad_open(self.slctn_path['file'])


    """ Public Listbox Methods"""
    def listbox_add_event(self):
        self._listbox_handle("add")
        
    def listbox_edit_event(self):
        self._listbox_handle("edit")
        
    def listbox_delete_event(self):
        self._listbox_handle("del")

    def _listbox_handle(self, func=None):
        self.lb_widget = self.root.focus_get()

        try:
            indx = self.lb_widget.curselection()[0]
        except IndexError:
            mb.showwarning("No List Selected", "A list must be selected to apply a function.")
            return False

        lb_elem_type = self.lb_widget.EdList.listbox_elem_type.lower()
        
        if not lb_elem_type in ['category', 'file']:
            print("WARNING: _listbox_handle():: self.lb_widget.listbox_name:: ValueError: Undefined")
            return None


        # Process UI event code and make respective handle calls
        if func == "add":
            self.lb_widget.insert("end", "New Item")
            indx = self.lb_widget.size() - 1
            self.lb_widget.start_edit(indx, \
                self.listbox_add)


        elif func == "edit":
            self.lb_widget.start_edit(indx)
            
            self.listbox_edit(lb_elem_type, self.lb_widget.old_data, self.lb_widget.new_data)


        elif func == "del":
            
        
            self.listbox_delete(lb_elem_type, name)
            pass

        else:
            print("WARNING: _listbox_handle(): ", func, " unexpected argument.")
            return None


    """Listbox file functions - Add, Edit, Delete
        listbox_*(ftype, name)
            ftype - file type: (category | file)
            file - filesystem level, name of file
    """
    def listbox_add(self, dataObj):
        print("listbox_file_add():: call (BEGIN)")
        print("listbox_file_add():: dataObj->new_data:: ", dataObj.new_data)
        if dataObj.listbox_elem_type == "file":
            self.fo.touch(dataObj.new_data)
            
        elif dataObj.listbox_elem_type == "category":
            self.fo.mkdir(dataObj.new_data)
        
        else:
            print("ERROR:: listbox_file_add():: Unknown Error - AABBCC93829283")
            return False
            
        print("listbox_file_add():: call (END)")


    def listbox_edit(self, ftype, old, new):
        self.fo.rename(old, new)

    def listbox_delete(self, ftype, name):
        pass


    """ Public Files Methods"""
    def files_get(self, event):
        files = []

        for file in os.listdir(self.fo.path + self.slctn_path['ctgry']):
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
            fd = open(f"{self.fo.path}{self.slctn_path['ctgry']}\{file}", "r")
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
            fd = open(f"{self.fo.path}{self.slctn_path['ctgry']}\{self.slctn_path['file']}", "w")
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
if __name__ == "__main__":
    GUI = PyPadGUI()
    GUI.mainloop()
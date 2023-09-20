#!/usr/bin/env python3

# PyPad - Python Organized ScratchPad for scientific purposes
#
# v0.0.1 Beta
# Date: 8-19-2023
# Author: Tom Smith (tom DOT briggs DOT smith AT gmail DOT com)


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
    slctn_path = {'category' : None, 'file' : None}
    lb_last_focus = None
    status = "I've got a lovely bunch of coconuts."


class FileOps():
    '''TODO: 
        - Add failsafe datapath so cwd() is used if user definition fails
        - Do better checking on user defined paths existence / (RW)ability'''
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
        """Return a properly formatted path string, compiled from DataHandle and slctn_path[]"""
        base = self.path
        ctgry = self.dh.slctn_path['category']
        file = self.dh.slctn_path['file']

        try:
            if file:
                base = f'{base}\\{ctgry}\\{file}'
            else:
                base = f'{base}\\{ctgry}'

        except:
            print('ERROR: FileOps():: get_base():: ValueError')

        return base

    def get_files(self):
        """Return a list of files from get_base() or False otherwise."""
        files = []
        path = self.get_base()

        if self.is_file():
            print(f"WARNING: FileOps():: get_files():: '{path}' is a regular file, not iterable")
            return False

        for file in os.listdir(path):
            files.append(file)

        if len(files) <= 0:
            return False

        return files

    def exists(self):
        if self.is_file() or self.is_dir():
            return False
            
        return True

    def is_file(self, file=None):
        if not file:
            file = self.get_base()

        return os.path.isfile(file)

    def is_dir(self):
        file = self.get_base()
        print(f"DEBUG: is_dir():: {file}")
        return os.path.isdir(file)

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
            print(fr'WARNING: Did not create directory: "{file}". Directory exists.')
            return False
        else:
            os.mkdir(file)

        return True

    def rename(self, new):
        file = self.get_base()
        tmp = file.split("\\")
        new_path = "\\".join(tmp[0:-1])

        os.rename(file, fr'{new_path}\\{new}')

    def delete(self):
        file = self.get_base()

        if self.is_file():
            os.remove(file)
            return True
        else:
            files = os.listdir(file)

            for dlt in files:
                os.remove(f'{file}\\{dlt}')

            os.rmdir(file)
            return True


class EditableListbox(tk.Listbox):
    """A listbox where you can directly edit an item via double-click
        Source: https://stackoverflow.com/questions/64609658/python-tkinter-listbox-text-edit-in-gui"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.edit_item = None

    def start_edit(self, index, accept_func=None,cancel_func=None):
        self.cur_index = index
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

        self.selection_clear(0, "end")
        self.selection_set(self.cur_index)

        if self.cancel_func:
            self.cancel_func(self)

    def accept_edit(self, event):
        DataHandle.EditLbox_new_entry = event.widget.get()
        self.delete(self.edit_item)
        self.insert(self.edit_item, DataHandle.EditLbox_new_entry)
        event.widget.destroy()

        self.selection_clear(0, "end")
        self.selection_set(self.cur_index)

        if self.accept_func:
            self.accept_func(self)

    def in_listbox(self, item):
        """Check if item is in listbox and return True / False"""
        items = self.get(0, self.size())
        if item in items:
            return True
        else:
            return False


class PyPadGUI():
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
        self.statusbar()

    """Local GUI Methods"""
    def __GUI__(self):
        self.root = tk.Tk()
        self.root.geometry("777x575")
        self.root.minsize(777, 575)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=200)

        self.root.rowconfigure(0, weight=1)

    def __event_handler__(self):
        self.ctgry_list.bind('<ButtonRelease-1>', self.category_click_event)
        self.file_list.bind('<ButtonRelease-1>', self.file_click_event)

        self.notepad.bind("<KeyPress>", self.notepad_edit_event)
        
        self.ctgry_list.bind("<FocusIn>", self.enable_ui_btns)
        self.file_list.bind("<FocusIn>",  self.enable_ui_btns)
        
        self.ctgry_list.bind("<FocusOut>", self.disable_ui_btns)
        self.file_list.bind("<FocusOut>", self.disable_ui_btns)

    def __file_menu__(self):
        ### File Bar
        self.menubar = tk.Menu(self.root)

        # File
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command="")
        self.filemenu.add_command(label="Save", command=self.notepad_save) #save_notepad)
        self.filemenu.add_command(label="Close", command="")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        
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
        self.upper_frame = tk.Frame(self.root)
        self.upper_frame.pack(side="top", fill="both", expand=1)

        self.left_frame = tk.Frame(self.upper_frame)
        self.left_frame.pack(side="left", fill="both")

        self.right_frame = tk.Frame(self.upper_frame)
        self.right_frame.pack(side="right", fill="both")

        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(side="bottom", fill="x")
        self.status_frame['takefocus'] = False
        self.status_frame['padx'] = 3
        self.status_frame['relief'] = "sunken"

    def __ui_buttons__(self):
        self.ui_btn_frame = tk.Frame(self.left_frame)
        self.ui_btn_frame.pack(side="top")

        self.ui_add = tk.Button(self.ui_btn_frame, text="Add", command=self.listbox_add_clicked)
        self.ui_add.pack(side="left")

        self.ui_edit = tk.Button(self.ui_btn_frame, text="Edit", command=self.listbox_edit_clicked)
        self.ui_edit.pack(side="left")

        self.ui_delete = tk.Button(self.ui_btn_frame, text="Delete", command=self.listbox_delete_clicked)
        self.ui_delete.pack(side="left")
        
        self.disable_ui_btns()
        
    def __categories__(self):
        self.ctgry_list_frame = tk.Frame(self.left_frame)
        self.ctgry_list_frame.pack(side="top")
        
        self.cat_scrllbr = tk.Scrollbar(self.ctgry_list_frame)
        self.cat_scrllbr.pack(side="right", fill="y")

        self.ctgry_list = EditableListbox(self.ctgry_list_frame, yscrollcommand=self.cat_scrllbr.set)

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

        self.file_list = EditableListbox(self.file_list_frame, yscrollcommand=self.file_scrllbr.set)
        self.file_list.pack(side="top")
        
        self.file_list.elem_type = "file"

    def __notepad__(self):
        # Notepad Window
        self.notepad = tk.Text(self.right_frame)
        self.notepad_disable()
        self.notepad.pack(side="right", fill="both", expand=1)

    """Public Functions"""
    def statusbar(self, text=None):
        """Dual purpose tk.Label instantiation / Statusbar update function"""
        try: # if not self.sb
            self.sb
        except: # then
            self.sb = tk.Label(self.status_frame)
            self.sb.pack(side="right", fill="y")
            
        else: # else
            """Update status bar path location and/or included state message."""
            padding = "    "
            pad_char = "-"
            pad = ""

            cat = DataHandle.slctn_path['category']
            if cat:
                cat = cat.capitalize()
                pad = f"{padding}{pad_char}{padding}"
            else:
                cat = ""

            file = DataHandle.slctn_path['file']
            if file:
                file = f" \ {file.capitalize()}"
                pad = f"{padding}{pad_char}{padding}"
            else:
                file = ""

            path = f"{cat}{file}"

            if text:
                DataHandle.status = text
            else:
                DataHandle.status = self.sb['text'].split("-")[-1].strip("    ")
                
            self.sb['text'] = f"{path}{pad}{DataHandle.status}"

    def set_slctn_path(self):
        """Update the UserHandle selection path after environment changes.
        Works based off the highlighted curselection()"""
        print(f"DEBUG: set_slctn_path(PRE):: {DataHandle.slctn_path}")
        wdgt = self.root.focus_get()

        try:
            indx = wdgt.curselection()[0]
            print("DEBUG: set_slctn_path():: Try block")
        except:
            indx = wdgt.size() - 1
            print("DEBUG: set_slctn_path():: Except block")


        if wdgt.elem_type == "file":
            DataHandle.slctn_path['file'] = wdgt.get(indx)

        elif wdgt.elem_type == "category":
            DataHandle.slctn_path['category'] = wdgt.get(indx)
            DataHandle.slctn_path['file'] = None

        else:
            print("ERROR:: PyPadGUI:: set_slctn_path():: unknown circumstance.")

        print(f"DEBUG: set_slctn_path(POST):: {DataHandle.slctn_path}")
        self.statusbar()
        return fr"{DataHandle.slctn_path['category']}\\{DataHandle.slctn_path['file']}"
        
    """Public Event Handling Methods"""
    def category_click_event(self, event):
        self.enable_ui_btns()
        self.notepad_save()
        self.notepad_clear()

        self.set_slctn_path()

        indx = self.ctgry_list.curselection()[0]
        selctn = self.ctgry_list.get(indx)
        DataHandle.slctn_path['category'] = selctn
        DataHandle.slctn_path['file'] = None

        self.file_list.delete(0, "end")
        self.file_list['state'] = "normal"

        files = self.fo.get_files()

        if files:
            for file in files:
                self.file_list.insert("end", file)

        self.notepad_disable()
        DataHandle.lb_last_focus = self.ctgry_list

    def file_click_event(self, event, indx=None):
        if DataHandle.slctn_path['file']:
            self.notepad_save()

        if event.widget.size() > 0:
            try:
                indx = self.file_list.curselection()[0]
            except IndexError:
                print("ERROR: PyPadGUI:: file_click_event():: Index out of range")

            self.set_slctn_path()

            self.notepad_clear()
            self.notepad_open(DataHandle.slctn_path['file'])
            DataHandle.lb_last_focus = self.file_list
            self.notepad.focus_set()
    
    """Public Listbox Methods"""
    def listbox_add_clicked(self):
        self.listbox_handle("add")
        print(f"DEBUG: listbox_add_clicked():: {DataHandle.slctn_path}")

    def listbox_edit_clicked(self):
        self.listbox_handle("edit")

    def listbox_delete_clicked(self):
        self.listbox_handle("delete")

    def listbox_handle(self, func=None):
        lb_widget = self.root.focus_get()

        if lb_widget.size() == 0:
            self.disable_ui_btns()
            self.listbox_add(lb_widget)
            return

        else:
            try:
                indx = lb_widget.curselection()[0]
            except:
                #print("WARNING: Supressed error for quiet UI behavior: Unknown circumstance - JJWWUSKKWUU")
                mb.showwarning("Warning - Nothing Selected", "You must make a selection before applying an operation.")
                return False

        if not lb_widget.elem_type in ['category', 'file']:
            print("WARNING: _listbox_handle():: lb_widget.listbox_name:: ValueError: Undefined")
            return None

        # Process UI event code and make respective handle calls
        if func == "add":
            self.listbox_add(lb_widget)
            print(f"DEBUG: listbox_handle():: {DataHandle.slctn_path}")

        elif func == "edit":
            self.listbox_edit(lb_widget)

        elif func == "delete":
            self.listbox_delete(lb_widget)

        else:
            print("WARNING: listbox_handle(): ", func, " invalid argument.")
            return None

    def listbox_add(self, wdgtObj):
        print(f"DEBUG: listbox_add():: {DataHandle.slctn_path}")
        val = "New Entry"
        entry = val
        
        vals = wdgtObj.get(0, "end")
        if val in vals:
            inc = 1
            while entry in vals:
                entry = f"{val} {inc}"
                inc += 1

        wdgtObj.insert("end", entry)
        indx = wdgtObj.size() - 1
        wdgtObj.start_edit(indx, self.listbox_add_callback, self.listbox_cancel_callback)

    def listbox_add_callback(self, wdgtObj):
        print(f"DEBUG: listbox_add_callback():: {DataHandle.slctn_path}")
        print(f"DEBUG: listbox_add_callback():: winfo_name(wdgtObj):: {wdgtObj.winfo_name()}")
        DataHandle.lb_last_focus.focus_set()
        self.set_slctn_path()
        
        indx = wdgtObj.curselection()[0]
        
        if wdgtObj.elem_type == "file":
            if self.fo.is_file():
                mb.showerror(title="Error - File Exists", message="ERROR: That file already exists.")
                wdgtObj.start_edit(indx, self.listbox_add_callback)
                return False
                
            DataHandle.slctn_path['file'] = DataHandle.EditLbox_new_entry
            self.fo.touch()

        elif wdgtObj.elem_type == "category":
            if self.fo.is_dir():
                mb.showerror(title="Error - File Exists", message="ERROR: That folder already exists.")
                wdgtObj.start_edit(indx, self.listbox_add_callback)
                return False
                
            DataHandle.slctn_path['category'] = DataHandle.EditLbox_new_entry
            self.fo.mkdir()

        else:
            print("ERROR:: listbox_file_add():: Unknown Error - AABBCC93829283")
            return False

        wdgtObj.selection_set(indx)
        self.set_slctn_path()

    def listbox_cancel_callback(self, wdgtObj):
        wdgtObj.delete(wdgtObj.curselection()[0])

    def listbox_edit(self, wdgtObj):
        indx = wdgtObj.curselection()[0]
        wdgtObj.start_edit(indx, self.listbox_edit_callback)
        print("DEBUG: listbox_edit():: Focus returned")

    def listbox_edit_callback(self, wdgtObj):
        self.fo.rename(DataHandle.EditLbox_new_entry)
        DataHandle.slctn_path['category'] = DataHandle.EditLbox_new_entry
        DataHandle.lb_last_focus.focus_set()

    def listbox_delete(self, wdgtObj):
        wdgtObj = self.root.focus_get()
        elem = wdgtObj.get(wdgtObj.curselection()[0])
        del_bool = mb.askyesno("Confirm Delete", f'You are about to delete "{elem}".\nThis will permenantly delete the folder and all files.\n\nAre you sure?')


        if del_bool:
            self.fo.delete()
            wdgtObj.delete(wdgtObj.curselection()[0])

            if wdgtObj.elem_type == "category":
                self.file_list.delete(0, "end")

    """Public Notepad Methods"""
    def notepad_edit_event(self, event):
        if self.notepad.edit_modified():
            self.statusbar("Modified")

    def notepad_enable(self):
        self.notepad.config(cursor="xterm")
        self.notepad.config(bg="#ffffff")
        self.notepad.config(state="normal")

        self.statusbar()

    def notepad_disable(self):
        self.notepad.config(cursor="arrow")
        self.notepad.config(bg="#F0F0F0")
        self.notepad.config(state="disabled")

        self.statusbar("Nothing Open")

    def notepad_clear(self):
        self.notepad.delete("0.0", "end")

    def notepad_open(self, file):
        self.statusbar("Opening...")
        try:
            fd = open(self.fo.get_base(), "r")
        except FileNotFoundError:
            print("ERROR: that file does not exist. TODO: Make this a messageBOX")
            return False

        self.notepad_enable()
        self.notepad_clear()

        chunk = fd.read(1024)
        while chunk != '':
            self.notepad.insert("end", chunk)
            chunk = fd.read(1024)

        fd.close()

        self.statusbar("Opened")
        self.notepad.edit_modified(False)

    def notepad_save(self):
        self.statusbar("Saving...")
        print(f"DEBUG: notepad_save():: {DataHandle.slctn_path}")
        if DataHandle.slctn_path['file'] == None or \
            DataHandle.slctn_path['category'] == None:
            self.statusbar("Nothing to Save")
            return False

        elif not self.notepad.edit_modified():
            self.statusbar("Not Modified")
            return False

        try:
            fd = open(self.fo.get_base(), "w")
        except FileNotFoundError:
            print("ERROR: PyPadGUI:: notepad_save():: File could not be found on system.")

        # TODO: Make this section write through chunks from notepad
        blob = self.notepad.get("0.0", "end")
        fd.write(blob)
        fd.close()

        self.statusbar("Saved")
        self.notepad.edit_modified(False)
        return True

    """Misc UI Functions"""
    def enable_ui_btns(self, event=None):
        self.ui_edit['state'] = 'normal'
        self.ui_delete['state'] = 'normal'

    def disable_ui_btns(self, event=None):
        self.ui_edit['state'] = 'disabled'
        self.ui_delete['state'] = 'disabled'

    """Mainloop()"""
    def mainloop(self):
        self.root.mainloop()
        
    def quit(self):
        self.save()
        self.root.quit()


# Main loop()
if __name__ == "__main__":
    GUI = PyPadGUI()
    GUI.mainloop()
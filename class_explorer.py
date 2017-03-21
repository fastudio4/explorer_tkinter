import os, string
from tkinter import *
from tkinter.ttk import *

class Explorer(object):
    def __init__(self, master):
        self.disk_select = Combobox(master, values=self.Drive())
        self.disk_select.current(0)
        self.disk_select.bind('<<ComboboxSelected>>', self.AddDrivePath)
        self.disk_select.bind('<Return>', self.ManualPath)
        self.list_folder = Listbox(master, selectmode=SINGLE)
        self.list_folder.bind('<Double-Button-1>', self.AddPath)
        self.scroll_list = Scrollbar(master, orient=VERTICAL, command=self.list_folder.yview)
        self.list_folder.config(yscrollcommand=self.scroll_list.set)
        self.disk_select.grid(row=0,column=0, columnspan=2)
        self.list_folder.grid(row=1,column=0)
        self.scroll_list.grid(row=1,column=1, sticky='ns')
        self.string_path = ''

    def Drive(self):
        base_drive = []
        if os.name == 'nt':
            base_drive = ['%s:\\' % d for d in string.ascii_uppercase if os.path.exists('%s:\\' % d)]
        if os.name == 'posix':
            base_drive = [os.sep]
        return base_drive
    
    def AddDrivePath(self, drive):
        self.string_path = ''
        self.string_path += self.disk_select.get()
        self.CreateFolders(self.Folders(self.string_path)[0], self.Folders(self.string_path)[1], self.string_path)

    def ManualPath(self, path):
        try:
            if os.listdir(self.disk_select.get()):
                self.string_path = self.disk_select.get()
                self.CreateFolders(self.Folders(self.string_path)[0], self.Folders(self.string_path)[1], self.string_path)
        except FileNotFoundError:
            list_error = ['Not Found']
            self.CreateFolders(list_error, 'Non')

    def Folders(self, path):
        folders = []
        file = []
        ignor_folders = []
        if os.name == 'posix':
            ignor_folders = ['root', 'lost+found']
        if os.name == 'nt':
            pass
        for ff in [al for al in os.listdir('%s' % path)]:
            if os.path.isdir('%s%s%s' % (path, ff, os.sep)):
                if not ff in ignor_folders:
                    folders.append(ff)
            else:
                file.append(ff)
        return [folders, file]
    
    def CreateFolders(self, folders, file, string_path):
        self.list_folder.delete(0, END)
        # list_file.delete(0, END)
        if len(string_path) > 3:
            self.list_folder.insert(0, '..')
        for fol in folders:
            self.list_folder.insert(END, fol)
        # for fil in file:
        #     list_file.insert(END, fil)
            
    def AddPath(self, path):
        add_path = ''
        if len(self.string_path) <= 3:
            add_path = '%s%s' % (self.Folders(self.string_path)[0][self.list_folder.curselection()[0]], os.sep)
        if len(self.string_path) > 3:
            if self.list_folder.curselection()[0] == 0:
                last_slash = ''
                if os.name == 'nt':
                    last_slash = self.string_path.rindex(os.sep, 0, len(self.string_path)-2)
                if os.name == 'posix':
                    last_slash = self.string_path.rindex(os.sep, 0, len(self.string_path)-1)
                part_direct = self.string_path[:last_slash+1]
                self.CreateFolders(self.Folders(part_direct)[0], self.Folders(part_direct)[1], self.string_path)
                self.string_path = part_direct
    
            else:
                add_path = '%s%s' % (self.Folders(self.string_path)[0][self.list_folder.curselection()[0]-1], os.sep)
        self.string_path += add_path
        self.CreateFolders(self.Folders(self.string_path)[0], self.Folders(self.string_path)[1], self.string_path)
        self.disk_select.set(self.string_path)

def main():
    root = Tk()
    expl = Explorer(root)
    root.mainloop()

if __name__ == '__main__':
    main()

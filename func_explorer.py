#!usr/bin/env python3
# -*- coding: utf-8 -*-

import os, string
from tkinter import *
from tkinter.ttk import *

string_path = ''

def Drive():
    base_drive = []
    if os.name == 'nt':
        base_drive = ['%s:\\' % d for d in string.ascii_uppercase if os.path.exists('%s:\\' % d)]
    if os.name == 'posix':
        base_drive = [os.sep]
    return base_drive

def addDrivePath(drive):
    global string_path
    string_path = ''
    string_path += disk_select.get()
    createFolders(Folders(string_path)[0], Folders(string_path)[1], string_path)

def manualPath(path):
    global string_path
    try:
        if os.listdir(disk_select.get()):
            string_path = disk_select.get()
            createFolders(Folders(string_path)[0], Folders(string_path)[1], string_path)
    except FileNotFoundError:
        list_error = ['Not Found']
        createFolders(list_error, 'Non')

def Folders(path):
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

def createFolders(folders, file, string_path):
    list_folder.delete(0, END)
    list_file.delete(0, END)
    if len(string_path) > 3:
        list_folder.insert(0, '..')
    for fol in folders:
        list_folder.insert(END, fol)
    for fil in file:
        list_file.insert(END, fil)

def addPath(path):
    global string_path
    add_path = ''
    if len(string_path) <= 3:
        add_path = '%s%s' % (Folders(string_path)[0][list_folder.curselection()[0]], os.sep)
    if len(string_path) > 3:
        if list_folder.curselection()[0] == 0:
            last_slash = ''
            if os.name == 'nt':
                last_slash = string_path.rindex(os.sep, 0, len(string_path)-2)
            if os.name == 'posix':
                last_slash = string_path.rindex(os.sep, 0, len(string_path)-1)
            part_direct = string_path[:last_slash+1]
            createFolders(Folders(part_direct)[0], Folders(part_direct)[1], string_path)
            string_path = part_direct

        else:
            add_path = '%s%s' % (Folders(string_path)[0][list_folder.curselection()[0]-1], os.sep)
    string_path += add_path
    createFolders(Folders(string_path)[0], Folders(string_path)[1], string_path)
    disk_select.set(string_path)

root = Tk()
disk_select = Combobox(root, values=Drive(), width=55)
disk_select.current(0)
disk_select.bind('<<ComboboxSelected>>', addDrivePath)
disk_select.bind('<Return>', manualPath)

list_folder = Listbox(root, selectmode=SINGLE, width=25)
list_folder.bind('<Double-Button-1>', addPath)
scr = Scrollbar(root, command=list_folder.yview, orient=VERTICAL)
list_folder.config(yscrollcommand=scr.set)

list_file = Listbox(root, selectmode=SINGLE, width=25)
scr2 = Scrollbar(root, command=list_file.yview, orient=VERTICAL)
list_file.config(yscrollcommand=scr2.set)

disk_select.grid(row=0,column=0, columnspan=4)
list_folder.grid(row=1,column=0)
scr.grid(row=1,column=1, sticky='ns')

list_file.grid(row=1,column=2)
scr2.grid(row=1,column=3, sticky='ns')

root.mainloop()


# coding: utf-8

# In[ ]:


import sys
import os
import numpy as np
import tkinter as tk
import socket
import pickle

import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import messagebox as tkMessageBox
from tkinter import filedialog as tkFileDialog

# Application (GUI) class
class Application(tk.Frame):
    DEBUG_LOG = True
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        
        # 実行
        #TCP setup
        TCP_IP = 'localhost'
        TCP_PORT = 5005
        BUFFER_SIZE = 1024
        
        print("trying to connect")
        #Establish TCP communication 
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((TCP_IP, TCP_PORT))
        self.s.listen(1)
        self.conn, addr = self.s.accept()
        
        data_init=pickle.dumps([[1,1,1,1],[1,1,1,1024],[1,1,1,1],[1,1,1,1]])
        self.conn.send(data_init)
        print("init_data_sent")
        print("connectioin done")

    def create_widgets(self):
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
        
        # PanedWindow
        ##  orient : vertical or horizontal
        ##  bg : boundary color
        pw_main = tk.PanedWindow(self.master, orient='horizontal')
        pw_main.pack(expand=True, fill = tk.BOTH, side="left")

        pw_left = tk.PanedWindow(pw_main, bg="cyan", orient='vertical')
        pw_main.add(pw_left)
        #pw_right = tk.PanedWindow(pw_main, bg="yellow", orient='vertical')
        #pw_main.add(pw_right)
        
        # Frame
        ##  bd ：border width 
        ##  relief ： Frame shape
        fm_select = tk.Frame(pw_left, bd=2, relief="ridge")
        pw_left.add(fm_select)
        
        #  Waypoint Label
        label_fpath1 = tk.Label(fm_select, text="Waypoint 1", width=20)
        label_fpath1.grid(row=0, column=0, padx=2, pady=2)

        label_fpath2 = tk.Label(fm_select, text="Waypoint 2", width=20)
        label_fpath2.grid(row=1, column=0, padx=2, pady=2)

        label_fpath3 = tk.Label(fm_select, text="Waypoint 3", width=20)
        label_fpath3.grid(row=2, column=0, padx=2, pady=2)

        label_fpath4 = tk.Label(fm_select, text="Waypoint 4", width=20)
        label_fpath4.grid(row=3, column=0, padx=2, pady=2)
        
        self.entry_fpath1 = tk.Entry(fm_select, justify="left", width=50)
        self.entry_fpath1.grid(row=0, column=1, sticky=tk.W + tk.E,padx=2, pady=2)
    
        self.entry_fpath2 = tk.Entry(fm_select, justify="left", width=50)
        self.entry_fpath2.grid(row=1, column=1, sticky=tk.W + tk.E,padx=2, pady=2)
        
        self.entry_fpath3 = tk.Entry(fm_select, justify="left", width=50)
        self.entry_fpath3.grid(row=2, column=1, sticky=tk.W + tk.E,padx=2, pady=2)

        self.entry_fpath4 = tk.Entry(fm_select, justify="left", width=50)
        self.entry_fpath4.grid(row=3, column=1, sticky=tk.W + tk.E,padx=2, pady=2)
        
        
        btn_select_file = tk.Button(fm_select, text="Done", command=self.select_file) 
        btn_select_file.grid(row=4, column=1, sticky=tk.W + tk.E, padx=2, pady=2)
    

    def select_file(self):
        try:
            out1 = [int(x) for x in  list(self.entry_fpath1.get().split(','))]
        except:
            out1 = []
        try:
            out2 = [int(x) for x in  list(self.entry_fpath2.get().split(','))]
        except:
            out2 = []
        try:
            out3 = [int(x) for x in  list(self.entry_fpath3.get().split(','))]
        except:
            out3 = []
        try:
            out4 = [int(x) for x in  list(self.entry_fpath4.get().split(','))]
        except:
            out4 = []
        out = [out1,out2,out3,out4]
        data=pickle.dumps(out)
        self.conn.send(data)
        print(out)

root = tk.Tk()        
myapp = Application(master=root)
myapp.master.title("Waypoint Publisher") 
myapp.master.geometry("700x500") 
myapp.mainloop()


# In[1]:


b = ['22', '333', '444', '555']


# In[1]:


int(b[0])


# In[2]:


list(a)


# In[3]:


a = str(444)
a.split()


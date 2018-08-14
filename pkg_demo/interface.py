#!/usr/bin/python3
"""
@project = SnatchTicket
@author = Kuang
@create_time = 2018/8/13 22:59
"""
from tkinter import *

top = Tk()
topframe = Frame(top)
topframe.pack(side=TOP)

bottomframe = Frame(top)
bottomframe.pack(side=BOTTOM)

label_1 = Label(topframe, text="用户名").grid(row=0, column=0)
entry_1 = Entry(topframe).grid(row=0, column=1)

label_2 = Label(topframe, text="密码").grid(row=1, column=0)
entry_2 = Entry(topframe).grid(row=1, column=1)

button_ok = Button(bottomframe, text="抢票")
button_ok.pack()

top.mainloop()

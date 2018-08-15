#!/usr/bin/python3
"""
@project = SnatchTicket
@author = Kuang
@create_time = 2018/8/13 22:59
"""
from tkinter import *
from pkg_demo import demo
from tkinter import messagebox

window = Tk()
window.title("来抢票鸭")
window.geometry("450x300")

Label(window, text="**用户名/User").place(x=50, y=30)
Label(window, text="**密码/Password").place(x=50, y=70)
Label(window, text="网址/Url").place(x=50, y=110)
Label(window, text="时间/Time").place(x=50, y=150)
Label(window, text="显示/Headless").place(x=50, y=190)

var_usr_name = StringVar()
var_usr_name.set("13812345678")
var_password = StringVar()
var_password.set("123456")
var_url = StringVar()
var_url.set("http://www.wentiyun.cn/venue-722.html")
var_time = StringVar()
var_time.set("2")
var_headless = BooleanVar()
var_headless.set(False)

entry_usr_name = Entry(window, textvariable=var_usr_name).place(x=160, y=30)
entry_password = Entry(window, textvariable=var_password, show="*").place(x=160, y=70)

label_url = Label(window, text=var_url.get()).place(x=160, y=110)

radio_time = Radiobutton(window, text="明天", variable=var_time.get(), value=1).place(x=160, y=150)
radio_time = Radiobutton(window, text="今天", variable=var_time.get(), value=2).place(x=220, y=150)

radio_head = Radiobutton(window, text="有", variable=var_headless.get(), value=1).place(x=160, y=190)
radio_head = Radiobutton(window, text="无", variable=var_headless.get(), value=2).place(x=220, y=190)


def go_now():
    name = var_usr_name.get()
    pwd = var_password.get()
    messagebox.showinfo(title="提醒", message="不许动，正在抢票")
    # demo.run(name, pwd)


btn_ok = Button(window, text="抢票", command=go_now, width=10).place(x=170, y=240)

window.mainloop()

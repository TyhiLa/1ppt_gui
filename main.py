# -*- coding: utf-8 -*- 
"""
Project: ppt
Creator: hoshimaemi
Create time: 2021-05-23 08:22
IDE: PyCharm
Introduction:
"""
import os
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import spider
from spider import HEADERS

img_jpg = None


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("第一ppt下载")
        self.resizable(width=False, height=False)

        self.e1text = tk.StringVar()
        self.e1text.set("输入所选内容")
        self.lis = None
        self.can = None

        self.setwigets()
        # self.mainframe = tk.Frame(self, height=600, width=600, bg="pink")
        # self.mainframe.pack()

        # self.showimamge()
    def setwigets(self):
        frame1 = tk.Frame(self, height=200, width=600, bg="white")
        frame1.pack()

        entry1 = tk.Entry(frame1, textvariable=self.e1text)
        entry1.pack()

        tk.Button(frame1, text="下载", command=self.btn1).pack()

        frame2 = tk.Frame(self, width=300, height=300)
        frame2.pack()

        cv1 = tk.Canvas(frame2, bg='#FFFFFF', width=300, height=300, scrollregion=(0, 0, 500, 500))
        hbar = tk.Scrollbar(cv1, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        hbar.config(command=cv1.xview)

        vbar = tk.Scrollbar(cv1, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        vbar.config(command=cv1.yview)

        cv1.config(width=300, height=300)
        cv1.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        cv1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        for inx, cmd in enumerate([x for x in range(1, 20)]):
            tk.Button(cv1, width=10, height=1, text=cmd).pack()

    def listtitle(self):
        cont = tk.Frame(self)
        cont.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH, pady=3)
        cont.config(relief=tk.SUNKEN)
        lis = tk.Listbox(cont)
        lis.pack(side=tk.LEFT, fill=tk.Y)
        can = tk.Canvas(cont)
        can.config(width=300, height=200)
        sbar = tk.Scrollbar(cont)
        sbar.config(command=can.yview)
        can.config(yscrollcommand=sbar.set)
        sbar.pack(side=tk.RIGHT, fill=tk.Y)
        can.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        imglist = [img for img in os.listdir(self.photodirs)]
        for img in imglist:
            lis.insert(tk.END, img)

        lis.bind('<Double-Button-1>', self.viewOne)

        self.lis = lis
        self.can = can

    def btn1(self):
        choice = self.e1text.get()
        if choice == "":
            messagebox.showwarning(title="输入错误", message="输入为空！")
        else:
            print(choice, end="")
        self.e1text.set('')

    def showimamge(self):
        img = Image.open("a.jpg")
        global img_jpg
        img_jpg = ImageTk.PhotoImage(img)
        tk.Label(self.mainframe, image=img_jpg).pack()


if __name__ == '__main__':
    Main().mainloop()

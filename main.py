# -*- coding: utf-8 -*- 
"""
Project: ppt
Creator: hoshimaemi
Create time: 2021-05-23 08:22
IDE: PyCharm
Introduction:
"""
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
        self.setwigets()
        self.mainframe = tk.Frame(self, height=600, width=600, bg="pink")
        self.mainframe.pack()

        self.showimamge()
    def setwigets(self):
        frame1 = tk.Frame(self, height=200, width=600, bg="white")
        frame1.pack()
        entry1 = tk.Entry(frame1, textvariable=self.e1text)
        entry1.pack()
        tk.Button(frame1, text="下载", command=self.btn1).pack()

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

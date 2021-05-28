# -*- coding: utf-8 -*- 
"""
Project: ppt
Creator: hoshimaemi
Create time: 2021-05-23 08:22
IDE: PyCharm
Introduction:
"""
import tkinter as tk


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x800")
        self.title("第一ppt下载")
        self.resizable(width=False, height=False)
        self.e1text = tk.StringVar()
        self.e1text.set("输入所选内容")
        self.setwigets()

    def setwigets(self):
        entry1  = tk.Entry(self, textvariable=self.e1text)
        entry1.pack()
        tk.Button(self, text="下载", command=self.btn1) .pack()

    def btn1(self):
        print(self.e1text.get())


if __name__ == '__main__':
    Main().mainloop()

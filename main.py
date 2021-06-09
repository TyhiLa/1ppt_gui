# -*- coding: utf-8 -*- 
"""
Project: ppt
Creator: hoshimaemi
Create time: 2021-05-23 08:22
IDE: PyCharm
Introduction:
"""
import tkinter as tk
import io
import requests
from PIL import Image, ImageTk
from spider import valueImport, headers, getTitleLink

tk_image = None


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x768")
        self.title("第一ppt下载")
        self.resizable(width=False, height=False)
        # Static variable
        self.value = valueImport()
        self.titlelink = None
        self.imgframe = None
        self.lb2 = None
        self.lb1 = None
        # self.e1text = tk.StringVar()
        # self.e1text.set("输入所选内容")
        self.setwigets()

        # self.showimamge()
    def setwigets(self):
        # frame_TOP = tk.Frame(self)
        # frame_TOP.pack(side=tk.TOP, fill=tk.X)
        frame_Middle = tk.Frame(self, bg='red')
        frame_Middle.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        frame_img = tk.Frame(frame_Middle, bg='pink')
        frame_img.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)
        self.imgframe = frame_img
        # frame_End = tk.Frame(self)
        # frame_End.pack(side=tk.TOP, expand=tk.NO, fill=tk.BOTH)
        # frame_End_left = tk.Frame(frame_End)
        # frame_End_left.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        # frame_End_right = tk.Frame(frame_End)
        # frame_End_right.pack(side=tk.LEFT, fill=tk.BOTH)

        # entry1 = tk.Entry(frame_TOP, textvariable=self.e1text)
        # entry1.pack()

        tk.Button(frame_img, text="下载", command=self.downloadOne).pack(side=tk.BOTTOM, fill=tk.X)

        lb1 = tk.Listbox(frame_Middle)
        lb1.pack(side=tk.LEFT, fill=tk.Y)
        for i in self.value[1]:
            lb1.insert(tk.END, i)

        lb2 = tk.Listbox(frame_Middle)
        lb2.pack(side=tk.LEFT, fill=tk.Y)
        # lb2.insert('下一页')
        # TODO:下一页控件
        # lb1.bind('<Double-Button-1>', lambda value: [lb2.insert(tk.END, x) for x in self.titlelink[0]])
        lb1.bind('<Double-Button-1>', self.lb2insrt)
        lb2.bind('<Double-Button-1>', self.showimage)

        self.lb1 = lb1
        self.lb2 = lb2
        self.img_lb = tk.Label(self.imgframe, text="图片显示区...")
        self.img_lb.pack(padx=5, pady=5)
    # def btn1(self):
    #     choice = self.e1text.get()
    #     if choice == "":
    #         messagebox.showwarning(title="输入错误", message="输入为空！")
    #     else:
    #         print(choice, end="")
    #     self.e1text.set('')
    def lb2insrt(self, _):
        index1 = self.lb1.curselection()
        index2 = self.lb2.curselection()
        print(index1)
        print(self.value)
        title = getTitleLink(self.value[0][index1[0]], 0)
        print(title)
        for i in title[0]:
            self.lb2.insert(tk.END, i)
    def showimage(self, _):
        global tk_image
        index = self.lb2.curselection()
        # img = self.lis.get(index[0])
        data = getTitleLink(self.value[0][index[0]], index[0])
        img_bytes = requests.get(data[1], headers=headers).content
        data_stream = io.BytesIO(img_bytes)
        pil_image = Image.open(data_stream)
        # w, h = pil_image.size
        # fname = url.split('/')[-1]
        # sf = f"{fname} ({w}x{h})"
        tk_image = ImageTk.PhotoImage(pil_image.resize((600, 400), Image.ANTIALIAS))
        self.img_lb.configure(image=tk_image)
    def downloadOne(self):
        pass


if __name__ == '__main__':
    Main().mainloop()

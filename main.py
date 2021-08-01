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
#from spider import valueImport, headers, getTitleLink
import download_engine

tk_image = None


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x768")
        self.title("第一ppt下载")
        self.resizable(width=False, height=False)
        self.value = download_engine.valueImport()
        print(self.value)
        self.data_page = None
        self.titlelink = None
        self.imgframe = None
        self.lb2 = None
        self.lb1 = None
        self.index1 = None
        self.index2 = None
        self.lbv = tk.StringVar()
        self.setwigets()

    def setwigets(self):
        frame_Middle = tk.Frame(self, bg='red')
        frame_Middle.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        frame_img = tk.Frame(frame_Middle, bg='pink')
        frame_img.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)
        self.imgframe = frame_img

        tk.Button(frame_img, text="下载", command=self.downloadOne).pack(side=tk.BOTTOM, fill=tk.X)

        lb1 = tk.Listbox(frame_Middle)
        lb1.pack(side=tk.LEFT, fill=tk.Y)
        for i in self.value[1]:
            lb1.insert(tk.END, i)

        lb2 = tk.Listbox(frame_Middle, listvariable=self.lbv)
        lb2.pack(side=tk.LEFT, fill=tk.Y)
        # TODO:下一页控件
        lb1.bind('<Button-1>', self.lb2insrt)
        lb2.bind('<Button-1>', self.showimage)

        self.lb1 = lb1
        self.lb2 = lb2
        self.img_lb = tk.Label(self.imgframe, text="图片显示区...")
        self.img_lb.pack(padx=5, pady=5)

    def lb2insrt(self, _):
        self.index1 = self.lb1.curselection()
        self.data = download_engine.getTitleLink(self.value[0][self.index1[0]], 0)
        if self.lbv.get() == "":
            for i in self.data[0]:
                self.lb2.insert(tk.END, i)
        else:
            self.lb2.delete(0, tk.END)
            for i in self.data[0]:
                self.lb2.insert(tk.END, i)

    def showimage(self, _):
        global tk_image
        self.index2 = self.lb2.curselection()
        data = download_engine.getTitleLink(self.value[0][self.index1[0]], self.index2[0])
        img_bytes = requests.get(data[1], headers=download_engine.headers).content
        data_stream = io.BytesIO(img_bytes)
        pil_image = Image.open(data_stream)
        tk_image = ImageTk.PhotoImage(pil_image.resize((600, 400), Image.ANTIALIAS))
        self.img_lb.configure(image=tk_image)

    def downloadOne(self):
        download_engine.launch(self.data[2][self.index2[0]])


if __name__ == '__main__':
    Main().mainloop()

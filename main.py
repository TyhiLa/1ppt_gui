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
from spider import valueImport, headers

tk_image = None


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x768")
        self.title("第一ppt下载")
        self.resizable(width=False, height=False)
        # Static variable
        self.value = valueImport()
        self.imgframe = None
        self.lis = None
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
        lb1.bind('<Double-Button-1>', lambda value: [lb2.insert(tk.END, x) for x in self.value[1]])
        lb2.bind('<Double-Button-1>', self.showimage)

        self.lis = lb2
    # def btn1(self):
    #     choice = self.e1text.get()
    #     if choice == "":
    #         messagebox.showwarning(title="输入错误", message="输入为空！")
    #     else:
    #         print(choice, end="")
    #     self.e1text.set('')

    def showimage(self, event):
        global tk_image
        index = self.lis.curselection()
        img = self.lis.get(index)
        print(img, index)
        url = 'https://desk-fd.zol-img.com.cn/t_s960x600c5/g5/M00/00/07/ChMkJl3qNKaIDNA2AARqqK0FxbEAAvnJAJbLQMABGrA592.jpg'
        img_bytes = requests.get(url, headers=headers).content
        data_stream = io.BytesIO(img_bytes)
        pil_image = Image.open(data_stream)
        w, h = pil_image.size
        fname = url.split('/')[-1]
        sf = f"{fname} ({w}x{h})"
        tk_image = ImageTk.PhotoImage(pil_image.resize((600, 400), Image.ANTIALIAS))
        tk.Label(self.imgframe, image=tk_image).pack(padx=5, pady=5)

    def downloadOne(self):
        pass


if __name__ == '__main__':
    Main().mainloop()

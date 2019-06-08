
import time
import datetime

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # import this to fix messagebox error
from tkinter import *
import pymysql
import pickle

import xlsxwriter
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import main

#签到情况查询、
class check(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        labeltxt = tk.Label(self,
                        text = "签到情况查询",
                        font = ("楷体",40),
                        )
        labeltxt.pack()
        labeltxt.place(x = 200,y = 10)

        labelt1 = tk.Label(self,
                            text = "请输入所要查询的人员:",
                            font = ("楷体",20)
                            )
        labelt1.pack(padx=5, pady=10, side=tk.LEFT)
        labelt1.place(x = 100,y = 100)

        f = Figure(figsize=(5, 3.7), dpi=100)
        f_plot = f.add_subplot(111)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().place(x=450, y=220)


        var1 = StringVar()
        var1.set(main.id1)
        e1 = Entry(self,textvariable = var1,)
        e1.pack()
        e1.place(x = 170,y = 140)


        def clock_display():
            db = pymysql.connect("103.248.223.58", "root", "h1613401", "test")
            cursor = db.cursor()
            sql = "select * from history where history.id=%s" % (e1.get())
            try:
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                print('error:' + str(e))
                db.rollback()
            cursor.close()
            db.close()

            # 数据处理
            result = cursor.fetchone()
            name = result[1]
            clock_record = result[-1]
            clock_list = clock_record.split("；")
            y = clock_list[:-1]
            print(type(y))
            lenth = len(clock_list)
            print(lenth)
            x = range(1, lenth)
            a, b, c, d = 0, 0, 0, 0
            for i in y:
                if i == "未迟到 未早退":
                    a += 1
                elif i == "未迟到 早退":
                    b += 1
                elif i == "迟到 未早退":
                    c += 1
                elif i == "迟到 早退":
                    d += 1
            x1 = ["未迟到 未早退", "未迟到 早退", "迟到 未早退", "迟到 早退"]
            y1 = [a, b, c, d]
            f_plot.clear()
            f_plot.bar(x1, y1)
            f_plot.set_title(name + "本月的考勤情况")
            f_plot.set_xlabel("考勤情况")
            f_plot.set_ylabel("天数")
            canvas.draw()
            print("ok")

        b1 = tk.Button(self, text="查询", width=8, font=("楷体", 20), command=clock_display)
        b1.pack(padx=2, pady=20)
        b1.place(x=500, y=110)


        labelt2 = tk.Label(self,
                            text = "查询结果:",
                            font = ("楷体",20),
                            fg = "red"
                            )
        labelt2.pack(padx=5, pady=10, side=tk.LEFT)
        labelt2.place(x = 10,y = 200)

        scrolly = Scrollbar(self)
        scrolly.pack(side=RIGHT, fill=Y)


        l=tk.Listbox(self,width = 70,height = 17,exportselection = False,yscrollcommand=scrolly.set)
        l.pack()
        l.place(x=10,y = 260)
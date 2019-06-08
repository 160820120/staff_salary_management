import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import pymysql
import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator, FuncFormatter


mpl.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
mpl.rcParams['axes.unicode_minus'] = False  # 负号显示


#工资查询
class salary(tk.Frame):
# Label设计
    def __init__(self, parent, root):
        super().__init__(parent)
        labeltxt = tk.Label(self,text = "工资查询",font = ("楷体",40),)
        labeltxt.pack()
        labeltxt.place(x = 200,y = 10)

        labelt1 = tk.Label(self,text = "请输入所要查询的工号:",font = ("楷体",20))
        labelt1.pack(padx=5, pady=10, side=tk.LEFT)
        labelt1.place(x = 100,y = 100)

        f = Figure(figsize=(5, 3.7), dpi=100)
        f_plot = f.add_subplot(111)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().place(x=450, y=220)

        var1 = StringVar()
        e1 = Entry(self,textvariable = var1,)
        e1.pack()
        e1.place(x = 170,y = 140)

        def show1():
            basedata = {
                'host': '103.248.223.58',
                'port': 3306,
                'user': 'root',
                'passwd': 'h1613401',
                'db': 'test',
                'charset': 'utf8'
            }

            # 打开数据库连接
            conn = pymysql.connect(**basedata)

            try:
                # 获取一个光标
                #     cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 返回字典数据类型
                cursor = conn.cursor()  # 返回字典数据类型
                # 定义将要执行的sql语句
                #     sql = 'select name,sex from member where id=%s;'%e1.get()
                if (e1.get() == ""):
                    l.insert(END, "输入为空，请正确输入！")


                sql = 'select * from salary where id=%s;' % e1.get()

                # 拼接并执行sql语句
                cursor.execute(sql)
                if (cursor.execute(sql)== 0):
                    l.insert(END, "查询失败，请重新输入！")
                else:
                    # 取到查询结果
                    ret1 = cursor.fetchone()  # 取一条
                    # ret1 = cursor.fetchall()
                    ret2 = cursor.description  # 获取表字段名

                    cursor.close()
                    conn.close()
                    print(len(ret1))
                    # print(e1.get())
                    l.insert(END, "查询成功")
                    l.insert(END, ret1)

                    f_plot.clear()
                    headings = [item[0] for item in ret2]
                    # print(headings)
                    labels = headings[4:8]
                    fracs = ret1[4:8]
                    explode = [0, 0.1, 0, 0]  # 0.1 凸出这部分，
                    f_plot.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%',
                               shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6
                               )
                    f_plot.set_title(ret1[1]+'月薪组成一览图', fontsize='14')
                    canvas.draw()

                    # 显示表头
                    tree.heading("ID", text=headings[0])
                    tree.heading("Name", text=headings[1])
                    tree.heading("base", text=headings[4])
                    tree.heading("assess", text=headings[5])
                    tree.heading("check", text=headings[6])
                    tree.heading("insurance", text=headings[7])
                    tree.heading("total", text=headings[8])
                    tree.insert("", 0, values=(ret1[0], ret1[1], ret1[4], ret1[5], ret1[6], ret1[7], ret1[8]))
                    tree.pack()


            except:
                print("查询失败")
                # 发生错误时回滚
                conn.rollback()

        def download():
            # basedata = {'host': '103.248.223.58', 'port': 3306, 'user': 'root', 'passwd': '123', 'db': 'test',
            #             'charset': 'utf8'}
            basedata = {
                'host': '103.248.223.58',
                'port': 3306,
                'user': 'root',
                'passwd': 'h1613401',
                'db': 'test',
                'charset': 'utf8'
            }

            # 打开数据库连接
            conn = pymysql.connect(**basedata)

            try:
                # 获取一个光标
                #     cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 返回字典数据类型
                cursor = conn.cursor()  # 返回字典数据类型
                if (e1.get() == ""):
                    l.insert(END, "输入为空，请正确输入！")
                # 定义将要执行的sql语句
                #     sql = 'select name,sex from member where id=%s;'%e1.get()
                sql = 'select * from salary where id=%s;' % e1.get()
                # 拼接并执行sql语句
                cursor.execute(sql)

                if (cursor.execute(sql)== 0):
                    l.insert(END, "查询失败，请重新输入！")
                else:

                    # 取到查询结果
                    ret1 = cursor.fetchone()  # 取一条
                    # ret1 = cursor.fetchall()

                    cursor.close()
                    conn.close()

                    print("已下载")
                    l.insert(END, "已下载")

                    # 新建一个excel文件，起名为expense01.xlsx
                    workbook = xlsxwriter.Workbook(ret1[1]+"当月薪水情况.xlsx")
                    # 添加一个Sheet页，不添写名字，默认为Sheet1
                    worksheet = workbook.add_worksheet()

                    # 准备数据
                    headings = ["ID", "Name", "base", "assess", "check", "insurance", "total"]
                    data = [[ret1[0],ret1[1],ret1[4],ret1[5], ret1[6],ret1[7], ret1[8]]]
                    # print(data)

                    head_style = workbook.add_format({"bold": True, "bg_color": "yellow", "align": "center", "font": 13})
                    # 写数据
                    worksheet.write_row("A1", headings, head_style)
                    for i in range(0, len(data)):
                        worksheet.write_row("A2", data[i])

                    # 添加柱状图
                    chart1 = workbook.add_chart({"type": "column"})
                    chart1.add_series({
                        "name": "",
                        "categories": "=Sheet1!$C$1:$G$1",
                        "values": "=Sheet1!$C$2:$F$2"
                    })

                    # 添加柱状图标题
                    chart1.set_title({"name": "每月薪水柱状图"})
                    # Y轴名称
                    chart1.set_y_axis({"name": "金额/元"})
                    # X轴名称
                    chart1.set_x_axis({"name": "薪水组成"})
                    # 图表样式
                    chart1.set_style(11)

                    # 添加饼图
                    chart2 = workbook.add_chart({"type": "pie"})
                    chart2.add_series({
                        "name": "饼形图",
                        "categories": "=Sheet1!$C$1:$G$1",
                        "values": "=Sheet1!$C$2:$F$2",

                        # 定义各饼块的颜色
                        "points": [
                            {"fill": {"color": "red"}},
                            {"fill": {"color": "blue"}},
                            {"fill": {"color": "yellow"}},
                            {"fill": {"color": "green"}},
                            # {"fill": {"color": "orange"}},
                            # {"fill": {"color": "purple"}}
                        ],
                        'data_labels': {'value': True}
                    })
                    chart2.set_title({"name": "每月薪水组成"})
                    chart2.set_style(3)

                    # 插入图表
                    worksheet.insert_chart("B7", chart1)
                    worksheet.insert_chart("J2", chart2)

                    # 关闭EXCEL文件
                    workbook.close()

            except:
                print("下载失败")
                # 发生错误时回滚
                conn.rollback()


        def history():
            basedata = {
                'host': '103.248.223.58',
                'port': 3306,
                'user': 'root',
                'passwd': 'h1613401',
                'db': 'test',
                'charset': 'utf8'
            }

            # 打开数据库连接
            conn = pymysql.connect(**basedata)

            try:
                # 获取一个光标
                #     cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 返回字典数据类型
                cursor = conn.cursor()  # 返回字典数据类型
                # 定义将要执行的sql语句
                #     sql = 'select name,sex from member where id=%s;'%e1.get()
                if (e1.get() == ""):
                    l.insert(END, "输入为空，请正确输入！")

                sql = 'select * from history where id=%s;' % e1.get()
                # 拼接并执行sql语句
                cursor.execute(sql)
                if (cursor.execute(sql)== 0):
                    l.insert(END, "查询失败，请重新输入！")
                else:
                    # 取到查询结果
                    ret3 = cursor.fetchone()  # 取一条
                    # ret1 = cursor.fetchall()
                    ret4 = cursor.description  # 获取表字段名

                    cursor.close()
                    conn.close()

                    print("已查询")
                    l.insert(END, "已查询")

                    l.insert(END, ret3)

                    # 新建一个excel文件
                    workbook = xlsxwriter.Workbook(ret3[1]+"每月薪水情况.xlsx")
                    # 添加一个Sheet页，不添写名字，默认为Sheet1
                    worksheet = workbook.add_worksheet()

                    # 准备数据
                    headings = [item[0] for item in ret4]
                    data = [[ret3[0],ret3[1],ret3[2],ret3[3],ret3[4],ret3[5], ret3[6],ret3[7], ret3[8],ret3[9], ret3[10],ret3[11], ret3[12]]]

                    print(headings)
                    print(data)
                    head_style = workbook.add_format({"bold": True, "bg_color": "yellow", "align": "center", "font": 13})
                    # 写数据
                    worksheet.write_row("A1", headings, head_style)
                    for i in range(0, len(data)):
                        worksheet.write_row("A2", data[i])

                    # 添加柱状图
                    chart1 = workbook.add_chart({"type": "column"})
                    chart1.add_series({
                        "name": "",
                        "categories": "=Sheet1!$C$1:$N$1",
                        "values": "=Sheet1!$C$2:$N$2"
                    })

                    # 添加柱状图标题
                    chart1.set_title({"name": "各月薪水柱状图"})
                    # Y轴名称
                    chart1.set_y_axis({"name": "金额/元"})
                    # X轴名称
                    chart1.set_x_axis({"name": "薪水组成"})
                    # 图表样式
                    chart1.set_style(11)

                    # 添加柱状图
                    chart2 = workbook.add_chart({"type": "line"})
                    chart2.add_series({
                        "name": "",
                        "categories": "=Sheet1!$C$1:$N$1",
                        "values": "=Sheet1!$C$2:$N$2",
                        'line': {'color': 'red'}
                    })

                    # 添加柱状图标题
                    chart2.set_title({"name": "各月薪水折线图"})
                    # Y轴名称
                    chart2.set_y_axis({"name": "金额/元"})
                    # X轴名称
                    chart2.set_x_axis({"name": "薪水组成"})
                    # 图表样式
                    chart2.set_style(11)

                    # 插入图表
                    worksheet.insert_chart("B7", chart1)
                    worksheet.insert_chart("J2", chart2)

                    # 关闭EXCEL文件
                    workbook.close()

                    f_plot.clear()
                    # x = list(map(int, headings[2:]))
                    x = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12)# 关于数据的部分可以提取出
                    y = ret3[2:14]
                    # print(x,y)
                    f_plot.plot(x, y,color="red", linewidth=1.5)


                    f_plot.set_title(ret3[1]+'各月薪水一览图', fontsize='14')
                    f_plot.grid(True, linestyle='-.')
                    f_plot.set_xlabel('月份/月', color='black')
                    f_plot.set_ylabel('每月薪水/元', color='black')
                    f_plot.axis([1,12,0,10000])
                    xminorLocator = MultipleLocator(1)
                    f_plot.xaxis.set_minor_locator(xminorLocator)
                    canvas.draw()

            except:
                print("下载失败")
                # 发生错误时回滚
                conn.rollback()

        def clear():
            l.delete(0,END)
            x = tree.get_children()
            for item in x:
                tree.delete(item)

        #label设计
        b1=tk.Button(self,text='查询',width = 8,height = 2,activeforeground = "red",command=show1)
        b1.pack(padx = 5, pady = 10)
        b1.place(x=350,y=140)

        b2=tk.Button(self,text='下载',width = 8,height = 2,activeforeground = "red",command=download)
        b2.pack(padx = 5, pady = 20)
        b2.place(x=450,y=140)

        b3=tk.Button(self,text='查看历史',width = 8,height = 2,activeforeground = "red",command=history)
        b3.pack(padx = 5, pady = 20)
        b3.place(x=550,y=140)

        b3=tk.Button(self,text='清除',width = 6,height = 1,activeforeground = "red",command=clear)
        b3.pack(padx = 5, pady = 20)
        b3.place(x=380,y=220)

        labelt2 = tk.Label(self,text = "查询工资的记录:",font = ("楷体",15),fg = "red")
        labelt2.pack(padx=5, pady=10, side=tk.LEFT)
        labelt2.place(x = 10,y = 220)

        scrolly = Scrollbar(self)
        scrolly.pack(side=RIGHT, fill=Y)

        l=tk.Listbox(self,width = 70,height = 5,exportselection = False,yscrollcommand=scrolly.set)
        scrollbar1 = Scrollbar(self)
        scrollbar1.pack(side=RIGHT, fill=Y)
        l.pack()
        l.place(x=10,y = 250)

        labelt3 = tk.Label(self,text = "查询结果展示:",font = ("楷体",15),fg = "red")
        labelt3.pack(padx=5, pady=10, side=tk.LEFT)
        labelt3.place(x = 10,y = 350)

        l1=tk.Listbox(self,width = 50,height = 10,exportselection = False,yscrollcommand=scrolly.set)
        l1.pack()
        l1.place(x=10,y = 380)

        tree = ttk.Treeview(l1, height=18, show="headings", columns=("ID","Name","base","assess", "check","insurance","total"))
        tree.column("ID", width=60)  # 表示列,不显示
        tree.column("Name", width=60)
        tree.column("base", width=60)
        tree.column("assess", width=60)
        tree.column("check", width=60)
        tree.column("insurance", width=60)
        tree.column("total", width=60)

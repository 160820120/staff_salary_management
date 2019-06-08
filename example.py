#!/usr/bin/env python 
# -*- coding:utf-8 -*-

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


mpl.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
mpl.rcParams['axes.unicode_minus'] = False  # 负号显示


class Application(tk.Tk):

    def __init__(self):
        super().__init__()   #super() 函数是用于调用父类(超类)的一个方法。

        self.wm_title("人才管理系统")
        self.geometry("930x600")
        self.resizable(width = 0,height = False)



        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)  #fill 填充整个分配给它的空间
        container.grid_rowconfigure(0, weight=1)#grid 网格
        container.grid_columnconfigure(0, weight=1)

        # 创建一个菜单项，类似于导航栏
        menubar=Menu(self)
        # 创建菜单项
        # menubar.add_cascade(label="登录",command=lambda: self.show_frame(StartPage))
        menubar.add_cascade(label="考勤",command=lambda: self.show_frame(PageNine))
        menubar.add_cascade(label="个人信息注册",command=lambda: self.show_frame(PageTwo))
        menubar.add_cascade(label="个人信息查询",command=lambda: self.show_frame(PageThree))
        menubar.add_cascade(label="部门人员查询",command=lambda: self.show_frame(PageFore))
        menubar.add_cascade(label="专业配置",command=lambda: self.show_frame(PageFive))
        menubar.add_cascade(label="工资查询",command=lambda: self.show_frame(PageSix))
        menubar.add_cascade(label="签到情况查询",command=lambda: self.show_frame(PageSeven))
        menubar.add_cascade(label="人员调动", command=lambda: self.show_frame(PageEight))
        self['menu']=menubar

        self.frames = {}

        for F in (PageNine,PageTwo, PageThree,PageFore,PageSix,PageSeven,PageEight,PageFive):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")  # 四个页面的位置都是 grid(row=0, column=0), 位置重叠，只有最上面的可见！！


        self.show_frame(PageThree)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() # 切换，提升当前 tk.Frame z轴顺序



#登录界面、
class StartPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)



        labeltxt = tk.Label(self,
                        text = "用户登录",
                        font = ("楷体",40),
                        )
        labeltxt.pack()
        labeltxt.place(x = 240,y = 50)

        labelt1 = tk.Label(self,
                        text = "账户:",
                        font = ("楷体",25)
                        )
        labelt1.pack(padx=5, pady=10, side=tk.LEFT)
        labelt1.place(x = 210,y = 200)

        var1 = StringVar()
        e1 = Entry(self,
                  textvariable = var1,
                  )
        e1.pack()
        e1.place(x = 300,y = 215)

        # 登录密码
        labelt2 = tk.Label(self,
                            text = "密码:",
                            font = ("楷体",25)
                            )
        labelt2.pack(padx=5, pady=10, side=tk.LEFT)
        labelt2.place(x = 210,y = 320)

        var2 = StringVar()
        e2 = Entry(self,
                  textvariable = var2,
                   show = "*"
                  )
        e2.pack()
        e2.place(x = 300,y = 335)

        # 按钮设计
        btnkaishi = tk.Button(self,
                              text="直接登录",
                              width = 20,
                              height = 4,
                              activeforeground = "red",
                            #  command=lambda:

                              )
        btnkaishi.pack(padx = 5, pady = 10, side = tk.LEFT)
        btnkaishi.place(x = 50,y = 470)

        btnkaishi = tk.Button(self,
                              text="立即注册",
                              width = 20,
                              height = 4,
                              activeforeground = "red",
                              command=lambda: root.show_frame(PageOne)
                              )
        btnkaishi.pack(padx = 5, pady = 10, side = tk.LEFT)
        btnkaishi.place(x = 500,y = 470)

#注册账号信息、
class PageOne(tk.Frame):



    # root = tk.Tk()
    # root.iconbitmap(".//school_logo.ico")
    # root.title('Employee-managerment')
    # root.geometry('450x300')
    # view = PageOne(root)
    # view.pack(side="top", fill="both", expand=True)
    # root.mainloop()

    def __init__(self, *args, **kwargs):

        tk.Frame.__init__(self, *args, **kwargs)


        b = tk.Button(self, text="Open new window", command=self.new_window1)
        b.pack(side="bottom")

        # welcome image
        canvas = tk.Canvas(self, height=200, width=500)  # 画布
        image_file = tk.PhotoImage(file='welcome.gif')  # 加载图片文件
        image = canvas.create_image(0, 0, anchor='nw', image=image_file)  # 将图片置于画布上
        canvas.pack(side='top')  # 放置画布（为上端）

        # user information
        tk.Label(self, text='User name: ').place(x=50, y=150)
        tk.Label(self, text='Password: ').place(x=50, y=190)

        var_usr_name = tk.StringVar()  # 定义变量
        var_usr_name.set('example@python.com')
        entry_usr_name = tk.Entry(self, textvariable=var_usr_name)
        entry_usr_name.place(x=160, y=150)
        var_usr_pwd = tk.StringVar()
        entry_usr_pwd = tk.Entry(self, textvariable=var_usr_pwd, show='*')
        entry_usr_pwd.place(x=160, y=190)

        def enter_mainwindows():
            # 实例化Application
            app = Application()
            app.iconbitmap(".//school_logo.ico")
            # 主循环:
            app.mainloop()
        def usr_login():
            usr_name = var_usr_name.get()
            usr_pwd = var_usr_pwd.get()

            ##这里设置异常捕获，当我们第一次访问用户信息文件时是不存在的，所以这里设置异常捕获。
            ##中间的两行就是我们的匹配，即程序将输入的信息和文件中的信息匹配。
            try:
                with open('usrs_info.pickle', 'rb') as usr_file:
                    usrs_info = pickle.load(usr_file)
            except FileNotFoundError:
                ##这里就是我们在没有读取到`usr_file`的时候，程序会创建一个`usr_file`这个文件，并将管理员
                ##的用户和密码写入，即用户名为`admin`密码为`admin`。
                with open('usrs_info.pickle', 'wb') as usr_file:
                    usrs_info = {'admin': 'admin'}
                    pickle.dump(usrs_info, usr_file)

            if usr_name in usrs_info:
                if usr_pwd == usrs_info[usr_name]:
                    tk.messagebox.showinfo(title='Welcome', message='How are you? ' + usr_name)
                    root.destroy()
                    enter_mainwindows()
                else:
                    tk.messagebox.showerror(message='Error, your password is wrong, try again.')
            else:
                is_sign_up = tk.messagebox.askyesno('Welcome',
                                                    'You have not signed up yet. Sign up today?')
                if is_sign_up:
                    self.new_window1()


        # login and sign up button
        btn_login = tk.Button(self, text='Login', command=usr_login)
        btn_login.place(x=170, y=230)
        btn_sign_up = tk.Button(self, text='Sign up', command=self.new_window1)
        btn_sign_up.place(x=270, y=230)

    def new_window1(self):

        window = tk.Toplevel(self)
        window.title("人才管理系统")
        window.geometry("700x600")
        label = tk.Label(window, text=id)
        label.pack(side="top", fill="both", padx=10, pady=10)

        labeltxt = tk.Label(window,
                            text="账号注册",
                            font=("楷体", 40),
                            )
        labeltxt.pack()
        labeltxt.place(x=240, y=50)

        # 登录账号
        labelt1 = tk.Label(window,
                           text="账户:",
                           font=("楷体", 25)
                           )
        labelt1.pack(padx=5, pady=10, side=tk.LEFT)
        labelt1.place(x=200, y=140)

        var1 = StringVar()
        e1 = Entry(window,
                   textvariable=var1,
                   )
        e1.pack()
        e1.place(x=305, y=150)

        # 登录密码
        labelt2 = tk.Label(window,
                           text="密码:",
                           font=("楷体", 25)
                           )
        labelt2.pack(padx=5, pady=10, side=tk.LEFT)
        labelt2.place(x=200, y=240)

        var2 = StringVar()
        e2 = Entry(window,
                   textvariable=var2,
                   show="*"
                   )
        e2.pack()
        e2.place(x=305, y=250)

        # 确认密码
        labelt3 = tk.Label(window,
                           text="确认密码:",
                           font=("楷体", 25)
                           )
        labelt3.pack(padx=5, pady=10, side=tk.LEFT)
        labelt3.place(x=150, y=350)

        var3 = StringVar()
        e3 = Entry(window,
                   textvariable=var3,
                   show="*"
                   )
        e3.pack()
        e3.place(x=305, y=365)

        labelp = tk.Label(window,
                          text=" ",
                          font=("楷体", 20)
                          )
        labelp.pack(padx=5, pady=10, side=tk.LEFT)
        labelp.place(x=200, y=400)

        def show1():
            basedata = {
                'host': '103.248.223.58',
                'port': 3306,
                'user': 'root',
                'passwd': '123',
                'db': 'test',
                'charset': 'utf8'
            }
            # 打开数据库连接
            conn = pymysql.connect(**basedata)

            try:
                User = str(e1.get())
                Passwd = str(e2.get())

                # 使用 cursor() 方法创建一个游标对象 cursor
                cursor = conn.cursor()
                print()

                sql = "INSERT INTO test1(id,name ) \
                              VALUES ('%s', '%s' )" % \
                      (User, Passwd)

                cursor.execute(sql)

                # commit 修改
                conn.commit()

                # 关闭游标
                cursor.close()

                # 关闭链接
                conn.close()
                print("添加成功")

                labelp.configure(text="注册成功")

            except:
                print("添加记录失败")
                labelp.configure(text="注册失败")
                # 发生错误时回滚
                conn.rollback()

        # 按钮设计
        btnkaishi = tk.Button(window,
                              text="立即注册",
                              width=20,
                              height=4,
                              activeforeground="red",
                              command=show1
                              )
        btnkaishi.pack(padx=5, pady=10, side=tk.LEFT)
        btnkaishi.place(x=50, y=470)

        btnkaishi = tk.Button(window,
                              text="返回登录",
                              width=20,
                              height=4,
                              activeforeground="red",
                              command=lambda: window.show_frame(StartPage)
                              )
        btnkaishi.pack(padx=5, pady=10, side=tk.LEFT)
        btnkaishi.place(x=500, y=470)







            # window = tk.Toplevel()
            # label = tk.Label(window, text=id)
            # label.pack(side="top", fill="both", padx=10, pady=10)


# 注册个人信息页面
class PageTwo(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)

        labeltxt = tk.Label(self,
                        text = "用户注册",
                        font = ("楷体",40),
                        )
        labeltxt.pack()
        labeltxt.place(x = 230,y = 10)


        # 姓名
        labelt1 = tk.Label(self,
                            text = "姓名:",
                            font = ("楷体",17)
                            )
        labelt1.pack(padx=5, pady=10, side=tk.LEFT)
        labelt1.place(x = 100,y = 70)

        var1 = StringVar()
        e1 = Entry(self,
                  textvariable = var1,
                  )
        e1.pack()
        e1.place(x = 170,y = 80)

        # 年龄
        labelt2 = tk.Label(self,
                            text = "ID:",
                            font = ("楷体",17)
                            )
        labelt2.pack(padx=5, pady=10, side=tk.LEFT)
        labelt2.place(x = 350,y = 70)
        var2 = StringVar()
        e2 = Entry(self,
                  textvariable = var2,
                  )
        e2.pack()
        e2.place(x = 420,y = 80)

        # 性别
        labelt3 = tk.Label(self,
                            text = "性别:",
                            font = ("楷体",17)
                            )
        labelt3.pack(padx=5, pady=10, side=tk.LEFT)
        labelt3.place(x = 100,y = 150)
        var3 = StringVar()
        e3 = Entry(self,
                  textvariable = var3,
                  )
        e3.pack()
        e3.place(x = 170,y = 160)

        # 生日
        labelt4 = tk.Label(self,
                            text = "生日:",
                            font = ("楷体",17)
                            )
        labelt4.pack(padx=5, pady=10, side=tk.LEFT)
        labelt4.place(x = 350,y = 150)
        var4 = StringVar()
        e4 = Entry(self,
                  textvariable = var4,
                  )
        e4.pack()
        e4.place(x = 420,y = 160)

        # 学历
        labelt5 = tk.Label(self,
                            text = "学历:",
                            font = ("楷体",17)
                            )
        labelt5.pack(padx=5, pady=10, side=tk.LEFT)
        labelt5.place(x = 100,y = 230)
        var5 = StringVar()
        e5 = Entry(self,
                  textvariable = var5,
                  )
        e5.pack()
        e5.place(x = 170,y = 240)

        # 专业
        labelt6 = tk.Label(self,
                            text = "专业:",
                            font = ("楷体",17)
                            )
        labelt6.pack(padx=5, pady=10, side=tk.LEFT)
        labelt6.place(x = 350,y = 230)
        var6 = StringVar()
        e6 = Entry(self,
                  textvariable = var6,
                  )
        e6.pack()
        e6.place(x = 420,y = 240)

        # 学校
        labelt7 = tk.Label(self,
                            text = "毕业学校:",
                            font = ("楷体",17)
                            )
        labelt7.pack(padx=5, pady=10, side=tk.LEFT)
        labelt7.place(x = 50,y = 285)
        var7 = StringVar()
        e7= Entry(self,
                  textvariable = var7,
                  )
        e7.pack()
        e7.place(x = 170,y = 295)

        # 手机号码
        labelt8 = tk.Label(self,
                            text = "手机号码:",
                            font = ("楷体",17)
                            )
        labelt8.pack(padx=5, pady=10, side=tk.LEFT)
        labelt8.place(x =50,y = 335)
        var8 = StringVar()
        e8= Entry(self,
                  textvariable = var8,
                  )
        e8.pack()
        e8.place(x = 170,y = 345)

        # # QQ邮箱
        # labelt9 = tk.Label(self,
        #                     text = "QQ邮箱:",
        #                     font = ("楷体",17)
        #                     )
        # labelt9.pack(padx=5, pady=10, side=tk.LEFT)
        # labelt9.place(x = 50,y = 385)
        # var9 = StringVar()
        # e9= Entry(self,
        #           textvariable = var9,
        #           )
        # e9.pack()
        # e9.place(x = 170,y = 395)

         # 工作部门
        labelt10 = tk.Label(self,
                            text = "工作部门:",
                            font = ("楷体",17)
                            )
        labelt10.pack(padx=5, pady=10, side=tk.LEFT)
        labelt10.place(x = 50,y = 435)
        var10 = StringVar()
        e10= Entry(self,
                  textvariable = var10,
                  )
        e10.pack()
        e10.place(x =170,y = 445)

        # 姓名
        labelt11 = tk.Label(self,
                           text="QQ/Wechat:",
                           font=("楷体", 17)
                           )
        labelt11.pack(padx=5, pady=10, side=tk.LEFT)
        labelt11.place(x=350, y=285)

        var11 = StringVar()
        e11 = Entry(self,
                   textvariable=var11,
                   )
        e11.pack()
        e11.place(x=500, y=285)

        # 年龄
        labelt12 = tk.Label(self,
                           text="入职时间:",
                           font=("楷体", 17)
                           )
        labelt12.pack(padx=5, pady=10, side=tk.LEFT)
        labelt12.place(x=350, y=335)
        var12 = StringVar()
        e12 = Entry(self,
                   textvariable=var12,
                   )
        e12.pack()
        e12.place(x=500, y=335)

        # 性别
        labelt13 = tk.Label(self,
                           text="等级:",
                           font=("楷体", 17)
                           )
        labelt13.pack(padx=5, pady=10, side=tk.LEFT)
        labelt13.place(x=350, y=385)
        var13 = StringVar()
        e13 = Entry(self,
                   textvariable=var13,
                   )
        e13.pack()
        e13.place(x=500, y=395)

        # 生日
        labelt14 = tk.Label(self,
                           text="密码:",
                           font=("楷体", 17)
                           )
        labelt14.pack(padx=5, pady=10, side=tk.LEFT)
        labelt14.place(x=350, y=435)
        var14 = StringVar()
        e14 = Entry(self,
                   textvariable=var14,

                   )
        e14.pack()
        e14.place(x=500, y=435)

        def show():
            basedata = {
                        'host':'103.248.223.58',
                        'port':3306,
                        'user':'root',
                        'passwd':'123',
                        'db':'test',
                        'charset':'utf8'
                        }
            # 打开数据库连接
            conn = pymysql.connect(**basedata)

            try:

                Name = str(e1.get())
                Id = str(e2.get())
                Sex = str(e3.get())
                Birthday = str(e4.get())
                Edb = str(e5.get())
                Major = str(e6.get())
                Graduate = str(e7.get())
                phone = str(e8.get())
                # #Emile = str(e9.get())
                Department = str(e10.get())
                wechat = str(e11.get())
                Entry_time = str(e12.get())
                # Level = str(e13.get())
                Password = str(e14.get())

                # 使用 cursor() 方法创建一个游标对象 cursor
                cursor = conn.cursor()
                # print(Id,Name, Sex ,Birthday ,Edb,Graduate ,Major,phone,wechat,Entray_time,Department,Level,Password)

                # sql = "INSERT INTO member(id,name, sex , birthday ,EDB , graduate ,major ,Phone ,QQ/Wechat,entray_time,department,level,password) \
                #                  VALUES ('%s','%s ','%s','%s','%s' ,'%s','%s' , '%s' ,'%s' ,'%s','%d' , '%s')" % \
                #     (Id,Name, Sex ,Birthday ,Edb,Graduate ,Major,phone,wechat,Entray_time,Department,Level,Password)

                sql = "INSERT INTO member(id,name, sex , birthday ,EDB , graduate ,major,Phone ,department,password,entry_time,Wechat) \
                                                                   VALUES ('%s','%s ','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                      (Id, Name, Sex, Birthday, Edb, Graduate, Major, phone,Department,Password,Entry_time,wechat)

                #
				#
                # sql = "INSERT INTO member(id,name, sex , birthday ,EDB , graduate ,major,Phone ) \
                #                    VALUES ('%s','%s ','%s','%s','%s','%s','%s','%s')" % \
                #       (Id ,Name, Sex ,Birthday,Edb, Graduate ,Major,phone)


                cursor.execute(sql)


                # commit 修改
                conn.commit()

                # 关闭游标
                cursor.close()

                # 关闭链接
                conn.close()
                print("添加成功")

            except:
                print("添加记录失败")

                # 发生错误时回滚
                conn.rollback()

        # 按钮设计
        btnkaishi = tk.Button(self,
                              text="立即注册",
                              width = 20,
                              height = 4,
                              activeforeground = "red",
                              command = show
                              )
        btnkaishi.pack(padx = 5, pady = 10, side = tk.LEFT)
        btnkaishi.place(x = 50,y = 470)

        btnkaishi = tk.Button(self,
                              text="返回查询",
                              width = 20,
                              height = 4,
                              activeforeground = "red",
                              command=lambda: root.show_frame(PageThree)
                              )
        btnkaishi.pack(padx = 5, pady = 10, side = tk.LEFT)
        btnkaishi.place(x = 500,y = 470)

# 个人信息查询
class PageThree(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        labeltxt = tk.Label(self,
                        text = "个人信息",
                        font = ("楷体",40),
                        )
        labeltxt.pack()
        labeltxt.place(x = 230,y = 10)
        # 姓名
        labelt1 = tk.Label(self,
                            text = "姓名:",
                            font = ("楷体",17)
                            )
        labelt1.pack(padx=5, pady=10, side=tk.LEFT)
        labelt1.place(x = 100,y = 70)
        var1 = StringVar()
        e1 = Entry(self,
                  textvariable = var1,
                  )
        e1.pack()
        e1.place(x = 170,y = 80)

        # 年龄
        labelt2 = tk.Label(self,
                            text = "年龄:",
                            font = ("楷体",17)
                            )
        labelt2.pack(padx=5, pady=10, side=tk.LEFT)
        labelt2.place(x = 350,y = 70)
        var2 = StringVar()
        e2 = Entry(self,
                  textvariable = var2,
                  )
        e2.pack()
        e2.place(x = 420,y = 80)

        # 性别
        labelt3 = tk.Label(self,
                            text = "性别:",
                            font = ("楷体",17)
                            )
        labelt3.pack(padx=5, pady=10, side=tk.LEFT)
        labelt3.place(x = 100,y = 150)
        var3 = StringVar()
        e3 = Entry(self,
                  textvariable = var3,
                  )
        e3.pack()
        e3.place(x = 170,y = 160)

        # 生日
        labelt4 = tk.Label(self,
                            text = "生日:",
                            font = ("楷体",17)
                            )
        labelt4.pack(padx=5, pady=10, side=tk.LEFT)
        labelt4.place(x = 350,y = 150)
        var4 = StringVar()
        e4 = Entry(self,
                  textvariable = var4,
                  )
        e4.pack()
        e4.place(x = 420,y = 160)

        # 学历
        labelt5 = tk.Label(self,
                            text = "学历:",
                            font = ("楷体",17)
                            )
        labelt5.pack(padx=5, pady=10, side=tk.LEFT)
        labelt5.place(x = 100,y = 230)
        var5 = StringVar()
        e5 = Entry(self,
                  textvariable = var5,
                  )
        e5.pack()
        e5.place(x = 170,y = 240)

        # 专业
        labelt6 = tk.Label(self,
                            text = "专业:",
                            font = ("楷体",17)
                            )
        labelt6.pack(padx=5, pady=10, side=tk.LEFT)
        labelt6.place(x = 350,y = 230)
        var6 = StringVar()
        e6 = Entry(self,
                  textvariable = var6,
                  )
        e6.pack()
        e6.place(x = 420,y = 240)

        # 固定电话
        labelt7 = tk.Label(self,
                            text = "毕业学校:",
                            font = ("楷体",17)
                            )
        labelt7.pack(padx=5, pady=10, side=tk.LEFT)
        labelt7.place(x = 180,y = 290)
        var7 = StringVar()
        e7= Entry(self,
                  textvariable = var7,
                  )
        e7.pack()
        e7.place(x = 300,y = 300)

        # 手机号码
        labelt8 = tk.Label(self,
                            text = "手机号码:",
                            font = ("楷体",17)
                            )
        labelt8.pack(padx=5, pady=10, side=tk.LEFT)
        labelt8.place(x = 180,y = 350)
        var8 = StringVar()
        e8= Entry(self,
                  textvariable = var8,
                  )
        e8.pack()
        e8.place(x = 300,y = 360)

        # QQ邮箱
        labelt9 = tk.Label(self,
                            text = "QQ邮箱:",
                            font = ("楷体",17)
                            )
        labelt9.pack(padx=5, pady=10, side=tk.LEFT)
        labelt9.place(x = 180,y = 410)
        var9 = StringVar()
        e9= Entry(self,
                  textvariable = var9,
                  )
        e9.pack()
        e9.place(x = 300,y = 420)

        # 按钮设计
        btnkaishi = tk.Button(self,
                              text="立即查询",
                              width = 20,
                              height = 4,
                              activeforeground = "red",
                              )
        btnkaishi.pack(padx = 5, pady = 10, side = tk.LEFT)
        btnkaishi.place(x = 50,y = 470)

        btnkaishi = tk.Button(self,
                              text="查询其他",
                              width = 20,
                              height = 4,
                              activeforeground = "red",
                              )
        btnkaishi.pack(padx = 5, pady = 10, side = tk.LEFT)
        btnkaishi.place(x = 500,y = 470)

#部门人员查询
class PageFore(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)

        labeltxt = tk.Label(self,
                        text = "部门人员查询",
                        font = ("楷体",40),
                        )
        labeltxt.pack()
        labeltxt.place(x = 180,y = 10)

        labelt1 = tk.Label(self,
                            text = "请输入所要查询的部门:",
                            font = ("楷体",20)
                            )
        labelt1.pack(padx=5, pady=10, side=tk.LEFT)
        labelt1.place(x = 100,y = 100)
        var1 = StringVar()
        e1 = Entry(self,
                  textvariable = var1,
                  )
        e1.pack()
        e1.place(x = 170,y = 140)

        # global Ret,row,vol

        def show1():

            basedata = {"103.248.223.58", "root", "h1613401", "test"}
            # basedata = {
            #     'host': 'localhost',
            #     'port': 3306,
            #     'user': 'root',
            #     'passwd': ' ',
            #     'db': 'test',
            #     'charset': 'utf8'
            # }
            # 打开数据库连接
            conn = pymysql.connect(**basedata)
            try:
            # 获取一个光标
                cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 返回字典数据类型

            # 定义将要执行的sql语句
                sql = 'select user,passwd from userr where user=%s;'%e1.get()
            # 拼接并执行sql语句
                cursor.execute(sql)

            # 取到查询结果
                ret1 = cursor.fetchall()  # 取所有
                #ret1 = cursor.fetchone()  # 取一条
                #ret2 = cursor.fetchmany(3)  # 取三条

                row = cursor.rowcount  # 取得记录个数，用于设置表格的行数
                vol = len(ret1[0])  # 取得字段数，用于设置表格的列数
                Ret=ret1


                cursor.close()
                conn.close()

                def get_tree():
                    # # # 删除原节点
                    # for _ in map(tree.delete, tree.get_children("")):
                    #     pass
                    # 更新插入新节点
                    for i in range(0, row):
                        tree.insert("", "end", values=(i + 1, Ret[i]["user"],
                                                       Ret[i]["passwd"]))
                    # tree.after(500, get_tree)

                get_tree()

                print(ret1)
                print(e1.get())

                print("查询成功")
                # l.insert(END, ret1)

            except:
                print("查询失败")

                # 发生错误时回滚
                conn.rollback()

            # 表格内容插入






        labelt2 = tk.Label(self,
                            text = "查询部门的结果:",
                            font = ("楷体",20),
                            fg = "red"
                            )
        labelt2.pack(padx=5, pady=10, side=tk.LEFT)
        labelt2.place(x = 10,y = 200)

        scrolly = Scrollbar(self)    #滚动条
        scrolly.pack(side=RIGHT, fill=Y)

        l=tk.Listbox(self,width = 70,height = 17,exportselection = False,yscrollcommand=scrolly.set)
        l.pack()
        l.place(x=10,y = 260)









        tree = ttk.Treeview(l)  # 表格
        tree["columns"] = ("num","user", "passwd")

        # # 定义树形结构与滚动条
        # vbar = ttk.Scrollbar(l, orient=VERTICAL, command=tree.yview)
        # tree.configure(yscrollcommand=vbar.set)

        tree.column("num", width=100)
        tree.column("user", width=100)  # 表示列,不显示
        tree.column("passwd", width=100)
        # tree.column("身高", width=100)

        tree.heading("num", text="num-id")
        tree.heading("user", text="user-name")  # 显示表头
        tree.heading("passwd", text="passwd-age")
        # tree.heading("身高", text="身高-tall")

        # tree.insert("", 0, text="line1", values=("1", "2", "3"))  # 插入数据，
        # tree.insert("", 1, text="line1", values=("1", "2", "3"))
        # tree.insert("", 2, text="line1", values=("1", "2", "3"))
        # tree.insert("", 3, text="line1", values=("1", "2", "3"))



        # 调用方法获取表格内容插入
        # get_tree()
        # tree.grid(row=0, column=0, sticky=NSEW)
        # vbar.grid(row=0, column=1, sticky=NS)


        b1 = tk.Button(self, text='查询', width=15, height=3, activeforeground="red", command=show1)
        b1.pack(padx=5, pady=10)
        b1.place(x=500, y=110)

        tree.pack()

#专业配置
class PageFive(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        labeltxt = tk.Label(self,
                        text = "专业配置",
                        font = ("楷体",40),
                        )
        labeltxt.pack()
        labeltxt.place(x = 200,y = 10)

        labelt1 = tk.Label(self,
                            text = "请输入所要查询的专业:",
                            font = ("楷体",20)
                            )
        labelt1.pack(padx=5, pady=10, side=tk.LEFT)
        labelt1.place(x = 100,y = 100)
        var1 = StringVar()
        e1 = Entry(self,
                  textvariable = var1,
                  )
        e1.pack()
        e1.place(x = 170,y = 140)

        b1=tk.Button(self,text='查询',width = 15,height = 3,activeforeground = "red")
        b1.pack(padx = 5, pady = 10)
        b1.place(x=500,y=110)

        labelt2 = tk.Label(self,
                            text = "查询专业的结果:",
                            font = ("楷体",20),
                            fg = "red"
                            )
        labelt2.pack(padx=5, pady=10, side=tk.LEFT)
        labelt2.place(x = 10,y = 200)

        scrolly = Scrollbar(self)
        scrolly.pack(side=RIGHT, fill=Y)

        l = tk.Listbox(self, width=70, height=17, exportselection=False, yscrollcommand=scrolly.set)
        l.pack()
        l.place(x=10, y=260)


        tree = ttk.Treeview(l)  # 表格
        tree["columns"] = ("姓名", "年龄", "身高")
        tree.column("姓名", width=100)  # 表示列,不显示
        tree.column("年龄", width=100)
        tree.column("身高", width=100)
        tree.heading("姓名", text="姓名-name")  # 显示表头
        tree.heading("年龄", text="年龄-age")
        tree.heading("身高", text="身高-tall")
        tree.insert("", 0, text="line1", values=("1", "2", "3"))  # 插入数据，
        tree.insert("", 1, text="line1", values=("1", "2", "3"))
        tree.insert("", 2, text="line1", values=("1", "2", "3"))
        tree.insert("", 3, text="line1", values=("1", "2", "3"))
        tree.pack()

#工资查询
class PageSix(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        labeltxt = tk.Label(self,text = "工资查询",font = ("楷体",40),)
        labeltxt.pack()
        labeltxt.place(x = 200,y = 10)

        f = Figure(figsize=(5, 4), dpi=100)
        f_plot = f.add_subplot(111)

        canvas = FigureCanvasTkAgg(f, self)
        # canvas.get_tk_widget().pack(anchor = E ,expand=1)
        canvas.get_tk_widget().place(x =0,y =200)

        def other_picture_alg():  # 数据相关的算法应该与plot分离开
            x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            y = [3, 6, 9, 12, 15, 18, 15, 12, 15, 18]
            return x, y

        def draw_picture():
            f_plot.clear()
            x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 关于数据的部分可以提取出来
            y = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
            print(x)
            f_plot.plot(x, y)
            canvas.draw()

        def draw_picture2():
            f_plot.clear()
            x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 关于数据的部分可以提取出来
            y = [2, 4, 6, 8, 10, 8, 6, 4, 2, 0]
            f_plot.plot(x, y)
            canvas.draw()

        def draw_picture3():
            f_plot.clear()
            x, y = other_picture_alg()  # 使用由算法生成的数据，可以避免重复的运算过程
            f_plot.plot(x, y)
            canvas.draw()

        Button(self, text='pic', command=draw_picture).place(x =500,y =250)
        Button(self, text='pic2', command=draw_picture2).place(x =500,y =350)
        Button(self, text='pic3', command=draw_picture3).place(x =500,y =450)




        labelt1 = tk.Label(self,text = "请输入所要查询的工号:",font = ("楷体",20))
        labelt1.pack(padx=5, pady=10, side=tk.LEFT)
        labelt1.place(x = 100,y = 100)

        var1 = StringVar()
        e1 = Entry(self,textvariable = var1,)
        e1.pack()
        e1.place(x = 170,y = 140)

        def show1():
            # basedata = {'host': '103.248.223.58', 'port': 3306, 'user': 'root', 'passwd': '123', 'db': 'test',
            #             'charset': 'utf8'}
            basedata = {
                'host': 'localhost',
                'port': 3306,
                'user': 'root',
                'passwd': '000',
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
                sql = 'select * from salary where id=%s;' % e1.get()
                # 拼接并执行sql语句
                cursor.execute(sql)

                # 取到查询结果
                ret1 = cursor.fetchone()  # 取一条
                # ret1 = cursor.fetchall()

                cursor.close()
                conn.close()

                # print(ret1)
                # print(e1.get())
                l.insert(END, "查询成功")
                l.insert(END, ret1)

            except:
                print("下载失败")
                # 发生错误时回滚
                conn.rollback()

        def download():
            # basedata = {'host': '103.248.223.58', 'port': 3306, 'user': 'root', 'passwd': '123', 'db': 'test',
            #             'charset': 'utf8'}
            basedata = {
                'host': 'localhost',
                'port': 3306,
                'user': 'root',
                'passwd': '000',
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
                sql = 'select * from salary where id=%s;' % e1.get()
                # 拼接并执行sql语句
                cursor.execute(sql)

                # 取到查询结果
                ret1 = cursor.fetchone()  # 取一条
                # ret1 = cursor.fetchall()

                cursor.close()
                conn.close()

                print("已下载")
                # l.insert(END, "已下载")

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
                    # "name":"饼形图",
                    # "categories": "=Sheet1!$A$2:$A$4",
                    # "values": "=Sheet1!$B$2:$B$4",
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
            # basedata = {'host': '103.248.223.58', 'port': 3306, 'user': 'root', 'passwd': '123', 'db': 'test',
            #             'charset': 'utf8'}
            basedata = {
                'host': 'localhost',
                'port': 3306,
                'user': 'root',
                'passwd': '000',
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
                sql = 'select * from history where id=%s;' % e1.get()
                # 拼接并执行sql语句
                cursor.execute(sql)

                # 取到查询结果
                ret1 = cursor.fetchone()  # 取一条
                # ret1 = cursor.fetchall()
                ret2 = cursor.description  # 获取表字段名

                cursor.close()
                conn.close()

                print("已查询")
                l.insert(END, "已查询")
                # print(ret2)
                # print("表头:", ",".join([item[0] for item in ret2]))
                # l.insert(END, ",".join([item[0] for item in ret2]))
                l.insert(END, ret1)
                # print("数据:", ",".join([item[0] for item in ret1]))

                # 新建一个excel文件，起名为expense01.xlsx
                workbook = xlsxwriter.Workbook(ret1[1]+"每月薪水情况.xlsx")
                # 添加一个Sheet页，不添写名字，默认为Sheet1
                worksheet = workbook.add_worksheet()

                # 准备数据
                headings = [item[0] for item in ret2]
                data = [[ret1[0],ret1[1],ret1[2],ret1[3],ret1[4],ret1[5], ret1[6],ret1[7], ret1[8],ret1[9], ret1[10],ret1[11], ret1[12]]]


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

            except:
                print("下载失败")
                # 发生错误时回滚
                conn.rollback()


        #label设计
        b1=tk.Button(self,text='查询',width = 8,height = 2,activeforeground = "red",command=show1)
        b1.pack(padx = 5, pady = 10)
        b1.place(x=350,y=140)

        b2=tk.Button(self,text='下载',width = 8,height = 2,activeforeground = "red",command=download)
        b2.pack(padx = 5, pady = 20)
        b2.place(x=450,y=140)
        #
        # b3=tk.Button(self,text='查看历史',width = 8,height = 2,activeforeground = "red",command=history)
        # b3.pack(padx = 5, pady = 20)
        # b3.place(x=550,y=140)

        # labelt2 = tk.Label(self,text = "查询工资的结果:",font = ("楷体",20),fg = "red")
        # labelt2.pack(padx=5, pady=10, side=tk.LEFT)
        # labelt2.place(x = 10,y = 200)
        #
        # scrolly = Scrollbar(self)
        # scrolly.pack(side=RIGHT, fill=Y)
        #
        # l=tk.Listbox(self,width = 70,height = 17,exportselection = False,yscrollcommand=scrolly.set)
        # l.pack()
        # l.place(x=10,y = 260)


#签到情况查询、
class PageSeven(tk.Frame):
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
        var1 = StringVar()

        e1 = Entry(self,
                  textvariable = var1,
                  )
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

            plt.yticks(range(32))  # 设置y1刻度
            plt.bar(x1, y1, width=0.5)
            plt.title(name + "本月的考勤情况")
            plt.xlabel("考勤情况")
            plt.ylabel("天数")
            plt.show()
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


 # 调动员工信息
class PageEight(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)

        label = tk.Label(self, text="人员调动", font=("楷体", 40), )
        label.pack()
        label.place(x=200, y=10)

        labelt1 = tk.Label(self,
                           text="部门调动人员工号：",
                           font=("楷体", 20)
                           )
        labelt1.pack(padx=5, pady=10, side=tk.LEFT)
        labelt1.place(x=100, y=100)

        labelt1 = tk.Label(self,
                           text="调入部门：",
                           font=("楷体", 20)
                           )
        labelt1.pack(padx=5, pady=10, side=tk.LEFT)
        labelt1.place(x=50, y=200)

        labelt2 = tk.Label(self,
                           text="调入等级：",
                           font=("楷体", 20)
                           )
        labelt2.pack(padx=5, pady=10, side=tk.LEFT)
        labelt2.place(x=50, y=290)


        var1 = StringVar()
        e1 = Entry(self,
                   textvariable=var1,
                   )
        e1.pack()
        e1.place(x=370, y=100)

        var2 = StringVar()
        e2 = Entry(self,
                   textvariable=var2,
                   )
        e2.pack()
        e2.place(x=200, y=210)

        var3 = StringVar()
        e3 = Entry(self,
                   textvariable=var3,
                   )
        e3.pack()
        e3.place(x=200, y=300)

        # 建立对象
        def tran():
            wangwu = Trans(e1.get())
            wangwu.department_trans(e1.get(), e2.get())

        def d_trans():
            wangwu = Trans(e1.get())
            wangwu.rank_trans(e1.get(), e3.get())


        b1=tk.Button(self, text="部门调动", width=8, font=("楷体",20), command=tran)
        b1.pack(padx=2, pady=20)
        b1.place(x=400, y=200)

        b1 = tk.Button(self, text="等级调动", width=8, font=("楷体", 20), command=d_trans)
        b1.pack(padx=2, pady=20)
        b1.place(x=400, y=290)

        b2=tk.Button(self, text="返回首页", width=8, font=("楷体",20), command=lambda: root.show_frame(PageTwo))
        b2.pack(padx=5, pady=40)
        b2.place(x=500, y=410)

# 创建部门调动与级别调动类
class Trans():
    def __init__(self, id):
        self.id = id
    def department_trans(self, id, cur_department):
        db = pymysql.connect("103.248.223.58", "root", "h1613401", "test")
        cursor = db.cursor()
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_0 = "insert into trans set trans_date='%s'"%(now)
        sql_1 = "update trans set id=%s where trans_date='%s'"%(id,now)
        sql_2 = """ update trans, member
                    set trans.name=member.name, trans.entry_time=member.entry_time, 
                    trans.ori_department=member.department, trans.ori_rank=member.rank, 
                    trans.cur_department=%s, trans.cur_rank=member.rank
                    where trans.id=%s and member.id=%s and trans.trans_date='%s'
                """%(cur_department, id, id, now)
        sql_3 = """ update member, clock, salary
                    set member.department=%s, clock.department=%s, salary.department=%s
                    where member.id=%s and clock.id=%s and salary.id=%s
                """%(cur_department, cur_department, cur_department, id, id, id)
        try:
            cursor.execute(sql_0)
            cursor.execute(sql_1)
            cursor.execute(sql_2)
            cursor.execute(sql_3)
            db.commit()
            tk.messagebox.showinfo(title='ok', message='部门调动完成！')
            print('部门调动完成')
        except Exception as e:
            tk.messagebox.showinfo(title='no', message='error')
            print('error:'+str(e))
            db.rollback()
        cursor.close()
        db.close()
    def rank_trans(self, id, cur_rank):
        db = pymysql.connect("103.248.223.58", "root", "h1613401", "test")
        cursor = db.cursor()
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_4 = "insert into trans set trans_date='%s'"%(now)
        sql_5 = "update trans set id = %s where trans_date='%s'"%(id,now)
        sql_6 = """ update trans, member 
                    set trans.name = member.name, trans.entry_time = member.entry_time, 
                    trans.ori_department = member.department, trans.ori_rank = member.rank, 
                    trans.cur_department = member.department, trans.cur_rank = %s
                    where trans.id = %s and member.id = %s and trans.trans_date='%s'
                """%(cur_rank, id, id, now)
        sql_7 = """ update member, clock, salary
                    set member.rank = %s, clock.rank = %s, salary.rank = %s
                    where member.id = %s and clock.id = %s and salary.id = %s
                """%(cur_rank, cur_rank, cur_rank, id, id, id)
        try:
            cursor.execute(sql_4)
            cursor.execute(sql_5)
            cursor.execute(sql_6)
            cursor.execute(sql_7)
            db.commit()
            tk.messagebox.showinfo(title='ok', message='等级调动完成！')
            print('等级调动完成')
        except Exception as e:
            tk.messagebox.showinfo(title='no', message='error')
            print('error:'+str(e))
            db.rollback()
        cursor.close()
        db.close()

#考勤信息
class PageNine(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)

        labeltxt = tk.Label(self,
                            text="考勤",
                            font=("楷体", 40),
                            )
        labeltxt.pack()
        labeltxt.place(x=200, y=10)

        labelt1 = tk.Label(self,
                           text="考勤id:",
                           font=("楷体", 20)
                           )
        labelt1.pack(padx=5, pady=10, side=tk.LEFT)
        labelt1.place(x=100, y=100)

        var1 = StringVar()
        e1 = Entry(self,
                   textvariable=var1,
                   )
        e1.pack()
        e1.place(x=170, y=140)

        # 建立对象
        def qiandao():
            wangwu = Clock(e1.get())
            wangwu.clock_in(e1.get())
            # wangwu.clock_out(e1.get())

        def qiantui():
            wangwu = Clock(e1.get())
            # wangwu.clock_in(e1.get())
            wangwu.clock_out(e1.get())

        b1 = tk.Button(self, text='签到', width=15, height=3, activeforeground="red", command=qiandao)
        b1.pack(padx=5, pady=10)
        b1.place(x=500, y=110)

        b2 = tk.Button(self, text='签退', width=15, height=3, activeforeground="red", command=qiantui)
        b2.pack(padx=5, pady=10)
        b2.place(x=500, y=210)

# 创建考勤类
class Clock():
    def __init__(self, id):
        self.id = id
    def clock_in(self, id):
        db = pymysql.connect("103.248.223.58", "root", "h1613401", "test")
        cursor = db.cursor()
        # 考勤表中clock_in字段清零
        try:
            sql_0 = """ update clock, member 
                        set clock_in='0000-00-00 00:00:00'
                        where clock.id=%s
                    """%(id)
            cursor.execute(sql_0)
            db.commit()
        except Exception as e:
            print('error:'+str(e))
            db.rollback()
        # 签到
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_1 = "update clock set clock_in='%s' where clock.id=%s"%(now, id)
        if now[-8:]<='08:00:00':
            sql_2 = "update history set clock_history=concat(clock_history,'未迟到 ') where history.id=%s"%(id)
            try:
                cursor.execute(sql_1)
                cursor.execute(sql_2)
                db.commit()
                print("签到完成")
            except Exception as e:
                print('error:'+str(e))
                db.rollback()
            cursor.close()
            db.close()
        else:
            sql_3 = "update history set clock_history=concat(clock_history,'迟到 ') where history.id=%s"%(id)
            try:
                cursor.execute(sql_1)
                cursor.execute(sql_3)
                db.commit()
                print('签到完成，已迟到')
            except Exception as e:
                print('error:'+str(e))
                db.rollback()
            cursor.close()
            db.close()
    def clock_out(self, id):
        db = pymysql.connect("103.248.223.58", "root", "h1613401", "test")
        cursor = db.cursor()
        # 考勤表中clock_out字段清零
        try:
            sql_0 = """ update clock, member 
                        set clock_out='0000-00-00 00:00:00'
                        where clock.id=%s
                    """%(id)
            cursor.execute(sql_0)
            db.commit()
        except Exception as e:
            print('error:'+str(e))
            db.rollback()
        # 签到
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_1 = "update clock set clock_out='%s' where clock.id=%s"%(now, id)
        if now[-8:]>='18:00:00':
#             sql_1 = "update history set clock_history = left(clock_history,LENGTH(clock_history) - 1) where history.id=%s"%(id)
            sql_2 = "update history set clock_history=concat(clock_history,'未早退；') where history.id=%s"%(id)
            try:
                cursor.execute(sql_1)
                cursor.execute(sql_2)
                db.commit()
                print("签退完成")
            except Exception as e:
                print('error:'+str(e))
                db.rollback()
            cursor.close()
            db.close()
        else:
#             sql_3 = "update history set clock_history = left(clock_history,LENGTH(clock_history) - 1) where history.id=%s"%(id)
            sql_4 = "update history set clock_history=concat(clock_history,'早退；') where history.id=%s"%(id)
            try:
                cursor.execute(sql_3)
                cursor.execute(sql_4)
                db.commit()
                print('签退完成，已早退')
            except Exception as e:
                print('error:'+str(e))
                db.rollback()
            cursor.close()
            db.close()

if __name__ == '__main__':


    StartPage0()


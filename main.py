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
import salary as sal
import check as che

id1=0

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
mpl.rcParams['axes.unicode_minus'] = False  # 负号显示
# print(StartPage0.var_usr_name.get())
#登陆后界面
class Application(tk.Tk):

    def __init__(self):
        super().__init__()   #super() 函数是用于调用父类(超类)的一个方法。

        self.wm_title("人才管理系统")
        self.geometry("930x600")
        self.resizable(width = 0,height = False)

        print(id1)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)  #fill 填充整个分配给它的空间
        container.grid_rowconfigure(0, weight=1)#grid 网格
        container.grid_columnconfigure(0, weight=1)

        # 创建一个菜单项，类似于导航栏
        menubar=Menu(self)
        # 创建菜单项
        # menubar.add_cascade(label="登录",command=lambda: self.show_frame(StartPage))
        menubar.add_cascade(label="考勤",command=lambda: self.show_frame(PageNine))
        menubar.add_cascade(label="用户信息添加",command=lambda: self.show_frame(PageTwo))
        # menubar.add_cascade(label="个人信息查询",command=lambda: self.show_frame(PageThree))
        menubar.add_cascade(label="部门人员查询",command=lambda: self.show_frame(PageFore))
        # menubar.add_cascade(label="专业配置",command=lambda: self.show_frame(PageFive))
        menubar.add_cascade(label="工资查询",command=lambda: self.show_frame(sal.salary))
        menubar.add_cascade(label="签到情况查询",command=lambda: self.show_frame(che.check))
        menubar.add_cascade(label="人员调动", command=lambda: self.show_frame(PageEight))
        self['menu']=menubar

        self.frames = {}

        for F in (PageNine,PageTwo,PageFore,sal.salary,che.check,PageEight):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")  # 四个页面的位置都是 grid(row=0, column=0), 位置重叠，只有最上面的可见！！


        self.show_frame(PageNine)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() # 切换，提升当前 tk.Frame z轴顺序

#欢迎页
class StartPage0(object):
    idd=10
    def __init__(self):
        # super().__init__()  # super() 函数是用于调用父类(超类)的一个方法。

        window = tk.Tk()
        window.iconbitmap("./school_logo.ico")
        window.title('Employee-managerment')
        window.geometry('450x300')

        # welcome image
        canvas = tk.Canvas(window, height=200, width=500)  # 画布
        image_file = tk.PhotoImage(file='welcome.gif')  # 加载图片文件
        image = canvas.create_image(0, 0, anchor='nw', image=image_file)  # 将图片置于画布上
        canvas.pack(side='top')  # 放置画布（为上端）

        # user information
        tk.Label(window, text='User name: ').place(x=50, y=150)
        tk.Label(window, text='Password: ').place(x=50, y=190)

        var_usr_name = tk.StringVar()  # 定义变量
        var_usr_name.set('')
        entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
        entry_usr_name.place(x=160, y=150)
        var_usr_pwd = tk.StringVar()
        entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
        entry_usr_pwd.place(x=160, y=190)



        def enter_mainwindows():
            # 实例化Application
            # self.idd
            app = Application()
            app.iconbitmap("./school_logo.ico")
            # 主循环:
            app.mainloop()

        def usr_sign_up():

            def sign_to():
                np = new_pwd.get()
                npf = new_pwd_confirm.get()
                nn = new_name.get()
                with open('usrs_info.pickle', 'rb') as usr_file:
                    exist_usr_info = pickle.load(usr_file)
                if np != npf:
                    tk.messagebox.showerror('Error', 'Password and confirm password must be the same!')
                elif nn in exist_usr_info:
                    tk.messagebox.showerror('Error', 'The user has already signed up!')
                else:
                    exist_usr_info[nn] = np
                    with open('usrs_info.pickle', 'wb') as usr_file:
                        pickle.dump(exist_usr_info, usr_file)
                    tk.messagebox.showinfo('Welcome', 'You have successfully signed up!')
                    window_sign_up.destroy()

            window_sign_up = tk.Toplevel(window)  # 在主体窗口的window上创建一个Sign up window窗口。
            window_sign_up.geometry('350x200')
            window_sign_up.iconbitmap(".//school_logo.ico")
            window_sign_up.title('Sign up window')

            new_name = tk.StringVar()
            new_name.set('')
            tk.Label(window_sign_up, text='User name: ').place(x=10, y=10)
            entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
            entry_new_name.place(x=150, y=10)

            new_pwd = tk.StringVar()
            tk.Label(window_sign_up, text='Password: ').place(x=10, y=50)
            entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
            entry_usr_pwd.place(x=150, y=50)

            new_pwd_confirm = tk.StringVar()
            tk.Label(window_sign_up, text='Confirm password: ').place(x=10, y=90)
            entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
            entry_usr_pwd_confirm.place(x=150, y=90)

            btn_comfirm_sign_up = tk.Button(window_sign_up, text='Sign up', command=sign_to)
            btn_comfirm_sign_up.place(x=150, y=130)

        def usr_login():
            usr_name = var_usr_name.get()
            global id1
            id1 = usr_name
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
                    # a=tk.messagebox.showinfo(title='Welcome', message='Welcome to Employee-managerment ' + usr_name)

                    print(datetime.datetime.now())

                    time.sleep(1)


                    # a.destroy()
                    window.destroy()
                    enter_mainwindows()
                else:
                    tk.messagebox.showerror(message='Error, your password is wrong, try again.')
            else:
                is_sign_up = tk.messagebox.askyesno('Welcome',
                                                    'You have not signed up yet. Sign up today?')
                if is_sign_up:
                    usr_sign_up()

        # login and sign up button
        btn_login = tk.Button(window, text='Login', command=usr_login)
        btn_login.place(x=170, y=230)
        btn_sign_up = tk.Button(window, text='Sign up', command=usr_sign_up)
        btn_sign_up.place(x=270, y=230)



        window.mainloop()

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

# 用户信息添加页面
class PageTwo(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)

        labeltxt = tk.Label(self,
                        text = "用户信息添加",
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
        var2.set(id1)
        e2 = Entry(self,
                  textvariable = var2,state=DISABLED
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
                            text = "等级:",
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

                Name = str(e1.get())
                Id = str(e2.get())
                Sex = str(e3.get())
                Birthday = str(e4.get())
                Level = str(e5.get())
                Major = str(e6.get())
                Graduate = str(e7.get())
                phone = str(e8.get())
                # #Emile = str(e9.get())
                Department = str(e10.get())
                Mail = str(e11.get())
                Entry_time = str(e12.get())
                # Level = str(e13.get())
                Password = str(e14.get())

                # 使用 cursor() 方法创建一个游标对象 cursor
                cursor = conn.cursor()
                print(Id,Name, Sex ,Birthday ,Graduate ,Major,phone,Mail,Department,Level,Password)

                sql = """INSERT INTO member(id,name, sex, birthday ,rank, edu,major,phone_number ,department,entry_time,mail) \
                                                                   VALUES ('%s','%s ','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % \
                      (Id, Name, Sex, Birthday, Level, Graduate,Major, phone,Department,Entry_time,Mail)

                # sql = """INSERT INTO member(id,name, sex , birthday ,level , edu ,major,phone_number ,department,password,entry_time,mail) \
                #                                                    VALUES ('%s','%s ','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % \
                #       (Id, Name, Sex, Birthday, Level, Graduate, Major, phone,Department,Password,Entry_time,wechat)

                cursor.execute(sql)

                # commit 修改
                conn.commit()

                # 关闭游标
                cursor.close()

                # 关闭链接
                conn.close()
                tk.messagebox.showinfo('ok', '添加成功')
                print("添加成功")

            except:
                print("添加记录失败")
                tk.messagebox.showerror('error', '添加失败')
                # 发生错误时回滚
                conn.rollback()

        # 按钮设计
        btnkaishi = tk.Button(self,
                              text="立即添加",
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

            # basedata = {"103.248.223.58", "root", "h1613401", "test"}
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
                cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 返回字典数据类型

            # 定义将要执行的sql语句
                sql = """select id,name,phone_number,mail,major from member where department=%s;"""%(e1.get())
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
                        tree.insert("", "end", values=(i + 1, Ret[i]["id"],
													   Ret[i]["name"],
													   Ret[i]["phone_number"],
													   Ret[i]["mail"],
                                                       Ret[i]["major"]))
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

        l = tk.Listbox(self,width = 10,height = 17,exportselection = False,yscrollcommand=scrolly.set)
        l.pack()
        l.place(x=0,y = 260)


        tree = ttk.Treeview(l)  # 表格
        tree["columns"] = ("num","id","name", "phone_number","mail","major")

        # # 定义树形结构与滚动条
        # vbar = ttk.Scrollbar(l, orient=VERTICAL, command=tree.yview)
        # tree.configure(yscrollcommand=vbar.set)


        tree.column("num", width=100)
        tree.column("id", width=100)
        tree.column("name", width=100)
        tree.column("phone_number", width=100)
        tree.column("mail", width=120)
        tree.column("major", width=100)  # 表示列,不显示

        tree.heading("num", text="num")
        tree.heading("id", text="id")
        tree.heading("name", text="name")  # 显示表头
        tree.heading("phone_number", text="phone_number")
        tree.heading("mail", text="mail")
        tree.heading("major", text="major")  # 显示表头


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
        var1.set(id1)
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
        var1.set(id1)
        e1 = Entry(self,
                   textvariable=var1,state=DISABLED
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

            sql_3 = "update history set clock_history=concat(clock_history,'早退；') where history.id=%s"%(id)
            try:
                cursor.execute(sql_1)
                cursor.execute(sql_3)
                db.commit()
                print('签退完成，已早退')
            except Exception as e:
                print('error:'+str(e))
                db.rollback()
            cursor.close()
            db.close()

if __name__ == '__main__':


    a=StartPage0()

    print(id1)

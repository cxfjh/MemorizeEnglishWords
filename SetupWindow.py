import os  # 导入操作系统相关的模块
import sys  # 导入用于退出应用程序的模块
import tkinter as tk  # 导入用于创建图形用户界面的模块
from tkinter import filedialog  # 导入文件对话框模块，用于打开和保存文件

info = []  # 存储设置信息的列表
filePath = "默认词汇.txt"  # 默认词汇文件路径
default = ["中英文均可", "允许重复"]

# 创建设置窗口类
class SetupWindow(tk.Frame):
    def __init__(self):
        super().__init__()
        
        self.optionVar = tk.StringVar(value=default[0])  # 初始化随机模式变量
        self.repeatVar = tk.StringVar(value=default[1])  # 初始化重复模式变量
        self.vocabFilevar = tk.StringVar(value=os.path.basename(filePath))  # 初始化词汇文件路径变量

        # 设置行列权重
        for i in range(4): self.grid_rowconfigure(i, weight=1)
        for j in range(4): self.grid_columnconfigure(j, weight=1)

        dropdownMenu = [["只随机中文", "只随机英文", "中英文均可"], ["允许重复", "不允许重复"]]
        size = ("Helvetica", 10)
        padXY = 10

        # 创建选择中英下拉菜单
        tk.Label(self, text="选择随机模式:", font=size, anchor="center").grid(row=0, column=0, sticky="NSEW", padx=padXY, pady=padXY)
        optionMenu = tk.OptionMenu(self, self.optionVar, *dropdownMenu[0])
        optionMenu.config(font=size, width=padXY)
        optionMenu.grid(row=0, column=1, sticky="NSEW", padx=padXY, pady=padXY)

        # 创建选择重复下拉菜单
        tk.Label(self, text="是否允许重复:", font=size, anchor="center").grid(row=1, column=0, sticky="NSEW", padx=padXY, pady=padXY)
        repeatoptionMenu = tk.OptionMenu(self, self.repeatVar, *dropdownMenu[1])  
        repeatoptionMenu.config(font=size, width=padXY)
        repeatoptionMenu.grid(row=1, column=1, sticky="NSEW", padx=padXY, pady=padXY)

        # 创建用户选择词汇按钮
        tk.Label(self, text="词汇文件:", font=size, anchor="center").grid(row=2, column=0, sticky="NSEW", padx=padXY, pady=padXY)
        tk.Button(self, text="选择文件", font=size, command=self.chooseFile).grid(row=2, column=1, sticky="NSEW", padx=padXY, pady=padXY)
        tk.Label(self, textvariable=self.vocabFilevar, font=size, anchor="center",).grid(row=2, column=2, sticky="NSEW", padx=padXY, pady=padXY)

        # 开始按钮
        tk.Button(self, text="开始", font=size, command=self.start).grid(row=3, column=0, sticky="NSEW", padx=padXY, pady=padXY)

    # 关闭窗口时退出应用程序
    def onClosing(self):
        sys.exit()

    # 选择词汇文件
    def chooseFile(self):
        if getattr(sys, "frozen", False): basePath = sys.executable
        else: basePath = os.path.abspath(".")
        filename = filedialog.askopenfilename(initialdir=basePath, title="选择词汇文件", filetypes=(("文本文件", "*.txt"), ("所有文件", "*.*")))
        if filename:
            global filePath
            filePath = filename
            self.vocabFilevar.set(os.path.basename(filename))  # 更新词汇文件路径显示

    # 开始按钮点击事件
    def start(self):
        global info, filePath, default
        info = [self.optionVar.get(), self.repeatVar.get(), filePath]  # 获取设置信息
        default = [self.optionVar.get(), self.repeatVar.get()]
        self.master.destroy()  # 销毁设置窗口
        try: createGUI()
        except:
            from WordApplication import createGUI
            createGUI()


# 创建设置界面
def settingsInterface():
    root = SetupWindow()
    root.master.title("设置")  # 设置窗口标题
    root.master.geometry("320x200")  # 设置窗口大小
    root.master.attributes("-topmost", True)  # 窗口置顶显示
    root.pack()  # 将SetupWindow添加到主窗口上
    root.mainloop()


# 导出信息
def SetupWindowInfo():
    SetupWindowInfo = {"info": info, "filePath": filePath}  # 将设置信息封装为字典
    return SetupWindowInfo  # 返回设置信息字典


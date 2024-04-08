import os  # 导入操作系统相关的模块
import sys  # 导入系统模块
import random  # 导入用于生成随机数的模块
import pyttsx3  # 导入用于文本转语音的模块
import threading  # 导入线程模块，用于执行多个任务
import tkinter as tk  # 导入用于创建图形用户界面的模块
from tkinter import filedialog  # 导入文件对话框模块，用于打开和保存文件
from datetime import datetime  # 导入日期时间模块，用于处理日期和时间
from tkinter import messagebox  # 导入消息框模块，用于显示消息框
from processingModule import extractVocab, getresourcePath, resize # 从processingModule模块中导入所需函数
from SetupWindow import SetupWindowInfo, settingsInterface # 从SetupWindow模块中导入SetupWindowInfo类

usedWordDict = {}
misspelledWordsArr = []
randomWords = ""
SetupWindowModule = ""
info = ""
filePath = ""
wordDict = ""

# 初始化信息
def initialInformation():
    global usedWordDict, misspelledWordsArr, randomWords, info, filePath, wordDict, SetupWindowModule
    usedWordDict = {}
    misspelledWordsArr = []
    randomWords = ""
    SetupWindowModule = SetupWindowInfo()
    info = SetupWindowModule["info"]
    filePath = SetupWindowModule["filePath"]
    wordDict = extractVocab(getresourcePath(info[2]))


# 初始化文本到语音引擎
pronunciation = pyttsx3.init()
pronunciation.setProperty("rate", 100)

# 创建单词应用程序窗口类
class WordApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.createWidgets()

        # 设置行列权重
        for i in range(4): self.grid_rowconfigure(i, weight=1)
        for i in range(2): self.grid_columnconfigure(i, weight=1)

    # 创建窗口部件
    def createWidgets(self):
        # 显示剩余单词数量
        self.resulCount = tk.Label(self, text="")
        self.resulCount.grid(row=0, column=1, pady=0, sticky=tk.N+tk.E)

        # 显示单词
        self.wordLabel = tk.Label(self)
        self.wordLabel.grid(row=1, column=0, columnspan=4, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

        # 输入框
        self.entryField = tk.Entry(self)
        self.entryField.bind("<Return>", self.checkAnswerWithoutSolution)
        self.entryField.grid(row=2, column=0, columnspan=4, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

        # 显示答案结果
        self.resultLabel = tk.Label(self, text="")
        self.resultLabel.grid(row=3, column=0, pady=10, columnspan=4, sticky=tk.W + tk.E)

        # 读音按钮
        self.readButton = tk.Button(self)
        self.readButton["text"] = "读音"
        self.readButton["command"] = self.readWord
        self.readButton.grid(row=4, column=0, padx=10, sticky=tk.N + tk.S + tk.E + tk.W)

        # 下一个按钮
        self.nextButton = tk.Button(self)
        self.nextButton["text"] = "下一个"
        self.nextButton["command"] = self.nextWord
        self.nextButton.grid(row=4, column=1, padx=10, sticky=tk.N + tk.S + tk.E + tk.W)

        # 检查答案按钮
        self.checkButton = tk.Button(self)
        self.checkButton["text"] = "查看答案"
        self.checkButton["command"] = self.checkAnswerWithSolution
        self.checkButton.grid(row=5, column=0, padx=10, pady=25, sticky=tk.N + tk.S + tk.E + tk.W)

        # 导出易错词汇按钮
        self.exportButton = tk.Button(self)
        self.exportButton["text"] = "导出易错词汇"
        self.exportButton["command"] = self.exportWords
        self.exportButton.grid(row=5, column=1, padx=10, pady=25, sticky=tk.N + tk.S + tk.E + tk.W)
        
        # 载入下一个单词
        self.nextWord()

    # 载入下一个单词
    def nextWord(self):
        if wordDict == {}:
            self.resultLabel["text"] = "结束"
            return

        # 根据设置重复或不重复
        if info[1] == "不允许重复":
            self.word, self.translations = random.choice(list(wordDict.items()))
            usedWordDict[self.word] = wordDict.pop(self.word)
            self.resulCount["text"] = f"剩余：{len(wordDict)}"
        else: self.word, self.translations = random.choice(list(wordDict.items()))

        # 根据设置随机显示中文或英文
        if info[0] == "只随机中文": self.isWord = False
        elif info[0] == "只随机英文": self.isWord = True
        else: self.isWord = random.random() < 0.5

        global randomWords
        randomWords = self.word
        if self.isWord: self.wordLabel["text"] = f"请输入 '{self.word}' 的中文翻译: "
        else:
            self.translation = random.choice(self.translations)
            self.wordLabel["text"] = f"请输入 '{self.translation}' 的英文原词: "

        self.entryField.delete(0, "end")
        self.resultLabel["text"] = ""

    # 检查答案
    def checkAnswerWithoutSolution(self, event=None):
        userInput = self.entryField.get()
        if (self.isWord and userInput in self.translations or not self.isWord and userInput == self.word):
            self.resultLabel["text"] = f"答对了！正确答案是： '{userInput}'"
            # self.after(2000, self.nextWord)
            self.nextWord()
        else:
            self.resultLabel["text"] = "抱歉，答错了。"
            wordTxt = "; ".join(self.translations)
            wrongWords = f"{self.word} {wordTxt}"
            if wrongWords not in misspelledWordsArr: misspelledWordsArr.append(wrongWords)

    # 查看答案
    def checkAnswerWithSolution(self):
        correctAnswer = " /  ".join(self.translations) if self.isWord else self.word
        self.resultLabel["text"] = f"正确答案是： '{correctAnswer}'"

    # 读音按钮
    def readWord(self):
        t = threading.Thread(target=self.speak, args=(randomWords,))
        t.start()

    # 导出易错词汇
    def exportWords(self):
        if not misspelledWordsArr: return messagebox.showinfo("提示", "暂无易错词汇")
        time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        if getattr(sys, "frozen", False): currentDir = sys.executable
        else: currentDir = os.path.abspath(".")
        # 选择文件保存路径
        filename = filedialog.asksaveasfilename(initialdir=currentDir, defaultextension=".txt", initialfile=f"{time}-易错词汇.txt", filetypes=[("文本文件", "*.txt")])
        if not filename: return
        # 写入易错词汇到文件
        with open(filename, "w", encoding="utf-8") as file:
            for index, item in enumerate(misspelledWordsArr, start=1):
                file.write(f"{index}.{item}\n")
        messagebox.showinfo("导出文件成功", f"路径：{filename}")
        os.startfile(os.path.dirname(os.path.abspath(filename)))

    # 朗读单词
    def speak(self, text):
        pronunciation.say(text)
        pronunciation.runAndWait()


# 创建GUI界面
def createGUI():
    initialInformation()
    root = tk.Tk()
    root.title("背单词")
    root.geometry("525x400")
    root.attributes("-topmost", True)
    frame = WordApplication(master=root)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    components = [frame.wordLabel, frame.entryField, frame.checkButton, frame.nextButton, frame.readButton, frame.resultLabel, frame.exportButton]
    root.bind("<Configure>", lambda event: resize(components, root, event)) # 窗口大小变化时，调整组件大小
    root.mainloop()
    settingsInterface()

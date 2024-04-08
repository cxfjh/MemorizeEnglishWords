import re  # 导入正则表达式模块
import os  # 导入操作系统模块
import sys  # 导入系统模块

# 从文件中提取词汇及其解释
def extractVocab(filePath):
    with open(filePath, "r", encoding="utf-8") as vocabFile:  # 打开文件并指定编码为utf-8
        rawText = vocabFile.read()  # 读取文件内容

    processedText = re.sub("[^a-zA-Z\u4e00-\u9fa5;,/；，。]", "", rawText)  # 使用正则表达式处理文本
    wordAndExplanationPairs = re.findall(r"([a-zA-Z]+)([\u4e00-\u9fa5;,/；，。]+)", processedText)  # 查找词汇及其解释
    vocabDict = {}  # 创建空字典用于存储词汇及其解释

    for word, explanation in wordAndExplanationPairs:  # 遍历词汇及解释
        explanationList = re.split(r"[^a-zA-Z\u4e00-\u9fa5]+", explanation)  # 利用正则表达式分割解释
        explanationList = [exp for exp in explanationList if len(exp) > 0]  # 去除空字符串
        vocabDict[word] = explanationList  # 将词汇及其解释存入字典

    return vocabDict  # 返回词汇字典


# 调整组件大小
def resize(components, root, event):
    fontSize = min(int(root.winfo_width() / 25), int(root.winfo_height() / 20))  # 计算字体大小
    fontName = ("Helvetica", fontSize)  # 设置字体名称和大小
    for component in components:  # 遍历所有组件
        component.config(font=fontName)  # 配置组件的字体


# 获取资源文件路径
def getresourcePath(relativePath):
    if getattr(sys, "frozen", False):  # 检查是否为打包后的可执行文件
        basePath = sys._MEIPASS  # 获取打包后的资源路径
    else:
        basePath = os.path.abspath(".")  # 获取当前工作目录的绝对路径
    return os.path.join(basePath, relativePath)  # 返回资源文件的绝对路径

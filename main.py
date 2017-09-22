#!/usr/bin/python
# -*- coding:utf8 -*
import json
from Tkinter import *
import requests

# 从文本中获取链接
def getUrls(text):
    return re.findall("(?isu)(https?\://[a-zA-Z0-9\.\?/&\=\:{#_%}]+)", text)

# 从一条url中获取参数值
argDict = dict()
def getArgDict(url):

    # 链接取值
    if len(url.split("?")) > 1 :
        arg_array = url.split("?")[1].split("&")
        for arg in arg_array:
            argDict[arg.split("=")[0]] = arg.split("=")[1]
        return url.split("?")[0], argDict

    return url.split("?")[0], argDict

# 将参数字典拼接成字符串
def apendArg(arg_dict):

    new_string = ""

    for key in arg_dict:
        new_string = new_string + "&" + key+"="+arg_dict[key]

    return new_string[1:]

# 给一个链接,修改成最终链接
def makeUrl(url):
    # 1.获取映射表

    dataU = requests.get('https://raw.githubusercontent.com/lch872/UrlParametersTool/master/list.json')
    arg_list = dataU.json()

    # 2.遍历映射表
    for item in arg_list:

        # 3.匹配上广告主
        if item["key"] in url.split("?")[0]:
            # 获取 主路径 和 参数字典
            (domain_url, arg_dict) = getArgDict(url)

            # 修改链接参数
            for ss in item["arg"]:

                if item["arg"][ss].startswith('+'):
                    arg_dict[ss] = arg_dict[ss].split("{")[0] + item["arg"][ss].split("+")[1]
                    continue

                arg_dict[ss] = item["arg"][ss]

            return domain_url + "?" + apendArg(arg_dict)

# 修改文本中的链接
def replaceUrl(text):
    urls = getUrls(text)

    # 生成新连接
    for url in urls:
        new_url = makeUrl(url)
        text = text.replace(url, new_url.encode("utf-8")+"\n")
    return text

root = Tk(className='auto replace tool v1.0')

power = Label(root, text='Power by Da.Lan', font = 'Helvetica -9', anchor = 'e',width=115).pack()

inputText = Text(root, background='lightcyan', width=100, height=10)
inputText.pack()

outputText = Text(root, background='honeydew', width=100, height=10)
outputText.pack()

def buttonDidClick():
    input_text = inputText.get('1.0', END)

    try:
        output_text = replaceUrl(input_text)
    except Exception,msg:
        output_text = "Error :" + msg.message

    # 清空并替换文本
    outputText.delete("1.0", END)
    outputText.insert(INSERT, output_text)

button = Button(root, text='Make URL', command=buttonDidClick).pack(fill=BOTH)


mainloop()

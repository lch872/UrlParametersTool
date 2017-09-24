#!/usr/bin/python
# -*- coding:utf8 -*
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from Tkinter import *
import requests



# 从文本中获取链接
def getUrls(text):
    return re.findall("(?isu)(https?\://[a-zA-Z0-9\-\.\?/&\=\:{!@#$_^*(+)%}]+)", text)

# 从一条url中获取参数值
def getArgDict(url):
    argDict = {}

    # 链接取值
    if len(url.split("?")) > 1 :
        arg_array = url.split("?")[1].split("&")
        for arg in arg_array:
            argDict[arg.split("=")[0]] = arg.split("=")[1]

    return url.split("?")[0], argDict

# 将参数字典拼接成字符串
def apendArg(arg_dict):

    new_string = ""

    for key,value in arg_dict.iteritems():
        new_string = new_string + "&" + key + "=" + value

    return new_string[1:]

# 给一个链接,修改成最终链接
json_list = {}
def makeUrl(url):

    # 1.遍历映射表
    for item in json_list["data"]:

        # 2.匹配上广告主
        if item["key"] in url.split("?")[0]:
            # 获取 主路径 和 参数字典
            (domain_url, arg_dict) = getArgDict(url)

            # 修改链接参数
            for key,value in item["arg"].iteritems():

                if value.startswith('+'):
                    arg_dict[key] = arg_dict[key].split("{")[0] + value.split("+")[1]
                    continue

                arg_dict[key] = value

            return domain_url + "?" + apendArg(arg_dict)


# 修改文本中的链接
def replaceUrl(text):

    urls = getUrls(text)

    # 生成新连接
    for url in urls:
        new_url = makeUrl(url)

        if new_url is None:
            raise NameError('Cannot find advertiser')

        text = text.replace(url, new_url.encode("utf-8")+"\n")
        
    return text

# 版本升级
def checkUpdata(current):
    ver = json_list["source"]
    
    if float(ver['version']) > float(current):

        return "最新版本: %s ,当前版本: %s ,请升级!\nfeature: %s \n下载链接: %s"\
               %(ver['version'],currentVersion,ver['feature'],ver['url'])

    return "当前已经是最新版本"

currentVersion = "1.0"
root = Tk(className='preferences replace v%s'%currentVersion)

power = Label(root, text='Power by Da.Lan', font = 'Helvetica -10', anchor = 'e',width=115).pack()

inputText = Text(root, background='lightcyan', width=100, height=10)
inputText.pack()

outputText = Text(root, background='honeydew', width=100, height=10)
outputText.pack()

def buttonDidClick():
    input_text = inputText.get('1.0', END)

    try:
        output_text = replaceUrl(input_text)
    except Exception,ex:
        output_text = "Error :" + ex.message

    # 清空并替换文本
    outputText.delete("1.0", END)
    outputText.insert(INSERT, output_text)

button = Button(root, text='Make URL', command=buttonDidClick).pack(fill=BOTH)

dataU = requests.get('http://git.oway.mobi/chenhao/TrackingTool/raw/master/list.json')
json_list = dataU.json()
outputText.insert(INSERT, checkUpdata(currentVersion))

mainloop()

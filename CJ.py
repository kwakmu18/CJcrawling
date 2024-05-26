from bs4 import BeautifulSoup
from urllib.request import urlopen
from html_table_parser import parser_functions as parser
import pandas as pd
import json
import time
import collections
import requests
import tkinter as tk
import ttkbootstrap as ttk
from datetime import datetime

if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

CODE = 572334569856 # 송장번호

def func():
    payload = {"wblNo":CODE}
    url = "https://trace.cjlogistics.com/next/rest/selectTrackingDetailList.do"
    
    try:
        resp = requests.post(url, data=payload)
        resp.encode = "UTF-8"
        data = []
        for row in json.loads(resp.text)["data"]["svcOutList"]:
            data.append([row["branNm"], row["procBranTelNo"], row["workDt"], row["workHms"], row["crgStDnm"], row["crgStDcdVal"],row["patnBranNm"]])
        return data
    except KeyboardInterrupt:
        return None
    except Exception as e:
        return None

window = ttk.Window()
window.geometry("1500x600")

label1 = tk.Label(window, text="갱신 시간 : %s"%(datetime.now()))
label1.place(x=0, y=10)

label2 = tk.Label(window, text="송장번호 : %d"%(CODE))
label2.place(x=400, y=10)
tree = ttk.Treeview(window, columns = ["A","B","C","D","E","F","G"], displaycolumns=["A","B","C","D","E","F","G"])
tree.place(x=0,y=40,width=1500, height=560)

url = "https://trace.cjlogistics.com/next/tracking.html?wblNo=%d"%CODE

result = urlopen(url)
html = result.read()
soup = BeautifulSoup(html, "html.parser")

temp = soup.find_all("table")

p = parser.make2d(temp[1])
w = [100, 100, 100, 100, 100, 300, 100]
for i in range(len(p[0])):
    tree.column("#%d"%i, width=w[i], anchor="center")
    tree.heading("#%d"%i, text=p[0][i])

def thread():
    while True:
        label1["text"] = "갱신 시간 : %s"%(datetime.now())
        datas = func()
        if datas==None:continue
        tree.delete(*tree.get_children())
        for data in datas:
            tree.insert("", "end", text=data[0], values=data[1:])
        time.sleep(60)

import threading
t = threading.Thread(target=thread)
t.start()
window.mainloop()
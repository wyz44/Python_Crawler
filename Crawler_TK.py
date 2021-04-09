import tkinter as tk
import urllib.request as req
import bs4
import pandas as pd
import re

url="http://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_data"
request=req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
})
with req.urlopen(request) as response:
    data=response.read().decode("utf-8")
root=bs4.BeautifulSoup(data, "html.parser")
#
root=str(root)
root=re.split(",|\r\n", root)
roots=[]
for i in range(len(root)):
    roots.append(root[i].strip('"'))

# 建立證券代號列表
num=[]
for i in range(1,len(roots)-1):
    if i % 10 == 0:
        num.append(roots[i])

# 建立證券名稱列表
name=[]
for i in range(1,len(roots)-1): #原本的len是11251,[i]就是11250,不-1就沒辦法印[i+1](會超出範圍),要印[i-9]
    if i % 10 == 0:
        name.append(roots[i+1])

# 建立成交量列表
volume=[]
for i in range(1,len(roots)-1):
    if i % 10 == 0:
        if roots[i+2] != "":
            roots[i+2]=int(roots[i+2])
        volume.append(roots[i+2])

# 建立開盤價列表
opening_price=[]
for i in range(1,len(roots)-1):
    if i % 10 == 0:
        if roots[i+4] != "":
            roots[i+4]=float(roots[i+4])
        opening_price.append(roots[i+4])

# 建立收盤價列表
closing_price=[]
for i in range(1,len(roots)-1):
    if i % 10 == 0:
        if roots[i+7] != "":
            roots[i+7]=float(roots[i+7])
        closing_price.append(roots[i+7])

# 建立漲跌幅列表
rise=[]
for i in range(1,len(roots)-1):
    if i % 10 == 0:
        if roots[i+8] != "":
            roots[i+8]=float(roots[i+8])
        rise.append(roots[i+8])

pddict={
    "證券代號":num,
    "證券名稱":name,
    "成交量":volume,
    "開盤價":opening_price,
    "收盤價":closing_price,
    "漲跌價差":rise
    }
df=pd.DataFrame(pddict)
df=df[~df["收盤價"].str.contains("", na=False)]  #刪除沒有數值的行(無法進行數值篩選),na=False


pd.set_option('display.max_rows', None)  #顯示全部的列
pd.set_option('display.max_column', None)  #顯示全部的欄

#------------------tkinter------------------
window = tk.Tk()
window.title("STOCK")
window.geometry("500x250+500+150")  #.geometry("window width x window height + position right + position down")
window.resizable(width=0, height=0)  #不可調整

#--------------輸入篩選條件---------------
input_start_1 = tk.Entry()
input_start_1.config(bg="#BEBEBE", fg="#000")
input_start_1.grid(row=0, column=1)

input_start_2 = tk.Entry()
input_start_2.config(bg="#BEBEBE", fg="#000")
input_start_2.grid(row=0, column=3)

input_end_1 = tk.Entry()
input_end_1.config(bg="#BEBEBE", fg="#000")
input_end_1.grid(row=1, column=1)

input_end_2 = tk.Entry()
input_end_2.config(bg="#BEBEBE", fg="#000")
input_end_2.grid(row=1, column=3)

input_rise_1 = tk.Entry()
input_rise_1.config(bg="#BEBEBE", fg="#000")
input_rise_1.grid(row=2, column=1)

input_rise_2 = tk.Entry()
input_rise_2.config(bg="#BEBEBE", fg="#000")
input_rise_2.grid(row=2, column=3)

input_vol_1 = tk.Entry()
input_vol_1.config(bg="#BEBEBE", fg="#000")
input_vol_1.grid(row=3, column=1)

input_vol_2 = tk.Entry()
input_vol_2.config(bg="#BEBEBE", fg="#000")
input_vol_2.grid(row=3, column=3)

#------------輸入提示文字-------------------
label_start_1 = tk.Label(text="開盤價>= :")
label_start_1.grid(row=0, column=0)

label_start_2 = tk.Label(text="開盤價<= :")
label_start_2.grid(row=0, column=2)

label_end_1 = tk.Label(text="收盤價>= :")
label_end_1.grid(row=1, column=0)

label_end_2 = tk.Label(text="收盤價<= :")
label_end_2.grid(row=1, column=2)

label_rise_1 = tk.Label(text="漲跌幅>= :")
label_rise_1.grid(row=2, column=0)

label_rise_2 = tk.Label(text="漲跌幅<= :")
label_rise_2.grid(row=2, column=2)

label_vol_1 = tk.Label(text="成交量>= :")
label_vol_1.grid(row=3, column=0)

label_vol_2 = tk.Label(text="成交量<= :")
label_vol_2.grid(row=3, column=2)

#-----------Button Function-----------------
def get_number():
    global df
    #設定篩選默認值(包含所有股票)
    con_start_1=df["開盤價"]>=-1
    con_start_2=df["開盤價"]<=9999
    con_end_1=df["收盤價"]>=-1
    con_end_2=df["收盤價"]<=9999
    con_rise_1=df["漲跌價差"]>=-11
    con_rise_2=df["漲跌價差"]<=11
    con_vol_1=df["成交量"]>=-1
    con_vol_2=df["成交量"]<=999999999999
    #若沒有輸入則依照默認值篩選
    if input_start_1.get() != "" :
        con_start_1=df["開盤價"]>=float(input_start_1.get())
    if input_start_2.get() != "" :
        con_start_2=df["開盤價"]<=float(input_start_2.get())
    if input_end_1.get() != "" :
        con_end_1=df["收盤價"]>=float(input_end_1.get())
    if input_end_2.get() != "" :
        con_end_2=df["收盤價"]<=float(input_end_2.get())
    if input_rise_1.get() != "" :
        con_rise_1=df["漲跌價差"]>=float(input_rise_1.get())
    if input_rise_2.get() != "" :
        con_rise_2=df["漲跌價差"]<=float(input_rise_2.get())
    if input_vol_1.get() != "" :
        con_vol_1=df["成交量"]>=float(input_vol_1.get())*1000
    if input_vol_2.get() != "" :
        con_vol_2=df["成交量"]<=float(input_vol_2.get())*1000
        
    con_start = con_start_1 & con_start_2
    con_end = con_end_1 & con_end_2
    con_rise = con_rise_1 & con_rise_2
    con_vol = con_vol_1 & con_vol_2
    
    df=df[con_start & con_end & con_rise & con_vol]
    print(df)
    window.destroy()   #關閉視窗
#-----------------------------------------------

btn = tk.Button()
btn.config(bg="skyblue", text="Run", height="2", width="20", padx="-10", pady="-100", command=get_number)
btn.grid(row=4, column=1, columnspan="3")

window.mainloop() #執行





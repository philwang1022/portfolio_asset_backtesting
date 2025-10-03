import pandas as pd
import numpy as np
import json
import requests
import time
id=[]
industry_id={}
sqllll=[]
###公司資料###
# col=['有價證券代號' ,'國際證券編碼','有價證券名稱', '產業別','有價證券別']
res = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y")
df = pd.read_html(res.text)[0]        # Parse the Source Code into a Pandas DataFrame
df = df.drop([0,4,7,8,9],axis = 1)  # Drop Useless Columns
df.columns = df.iloc[0]               # Replace DataFrame Columns Title
# df=df.reset_index(drop=True)
df = df.iloc[1:]
df=df[['有價證券名稱','有價證券代號' , '國際證券編碼','產業別','有價證券別']]
print(df)
print("##############################################################")
res = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=I&industry_code=&Page=1&chklike=Y")
df1 = pd.read_html(res.text)[0]        # Parse the Source Code into a Pandas DataFrame
df1 = df1.drop([0,4,7,8,9],axis = 1)  # Drop Useless Columns
df1.columns = df1.iloc[0]               # Replace DataFrame Columns Title
# df1=df1.reset_index(drop=True)
df1 = df1.iloc[1:]
df1=df1[['有價證券名稱','有價證券代號' , '國際證券編碼','產業別','有價證券別']]
print(df1)
print("##############################################################")
print("##############################################################")
data = pd.concat([df, df1],axis=0)
data.index=range(len(data))
# data=data.reset_index()
# c={0:"水泥工業"}
print(data)
stocksymbol=[]
date=['20211231','20220131','20220228','20220331','20220430','20220531','20220630','20220731','20220831','20220930','20221031','20221130','20221231']
for a in range(len(data)):
    stocksymbol.append(data.loc[:,'有價證券代號'][a])
    id.append(a)
for k in range(9,10):
    for a in range(len(date)):
        url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+ date[a] +'&stockNo='+stocksymbol[k]
        print(url)
        data = requests.get(url).text
        time.sleep(5)
        # time.sleep(5)
        # print(data)
        json_data = json.loads(data)
        Stock_data = json_data['data']
        Stock_name= json_data['title']
        StockPrice = pd.DataFrame(Stock_data, columns = ['Date','Volume','Volume_Cash','Open','High','Low','Close','Change','Order'])
    
        StockPrice=StockPrice.drop(['Volume_Cash','Change','Order'],axis=1)
        StockPrice=StockPrice[['Date','Open','High','Low','Close','Volume']]
        print(Stock_name[8:21])
        for b in range(len(StockPrice)):
            StockPrice['Volume'][b]=StockPrice['Volume'][b].replace(',','')
        # print(StockPrice)

        # sql = "INSERT INTO price(product_id, date, open_price, high_price, low_price, close_price, volume) VALUES "
        str_ = ''
        
        for i in range(len(StockPrice)):
            str2_ = str(id[k+1]) + ','
            for j in range(6): #欄位長度
                if j != 0:
                    str2_ = str2_ + str(StockPrice.loc[i][j]) + ','
                else:
                    str2_ = str2_ + "'" + str(StockPrice.loc[i][j]) + "',"


            str_ = str_ + f"""({str2_[:-1]}),"""

        str_ =  str_[:-1] + ';'
        sqllll.append(str_)
        # print(str_)

print(sqllll)
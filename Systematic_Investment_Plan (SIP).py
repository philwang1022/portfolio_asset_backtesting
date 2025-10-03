#!/usr/bin/env python
# coding: utf-8

# In[2]:


import yfinance as yf
import pandas as pd


# In[12]:


stock1=yf.download("2330.TW",start="2010-1-1",end='2012-1-1')
stock2=yf.download("1103.TW",start="2010-1-1",end='2012-1-1')
stock3=yf.download("1104.TW",start="2010-1-1",end='2012-1-1')
stock_list=[stock1,stock2,stock3]
print(stock1)


# In[13]:


for i in stock_list:
    i.drop(["Open"],axis=1,inplace=True)
    i.drop(["High"],axis=1,inplace=True)
    i.drop(["Low"],axis=1,inplace=True)
    i.drop(["Adj Close"],axis=1,inplace=True)
    i.drop(["Volume"],axis=1,inplace=True)


# In[14]:


data=pd.merge(stock1,stock2,left_index=True,right_index=True,how='inner')
data.rename(columns={'Close_x':'2330','Close_y':'1103'},inplace=True)
data=pd.merge(data,stock3,left_index=True,right_index=True,how='inner')
data.rename(columns={'Close':'1104'},inplace=True)
data


# In[15]:


PMT=10000
start='2010-1-1'
end='2012-1-1'
ratio=[0.5,0.25,0.25]


# In[16]:


df=data.copy()
dfm=df.resample('BM').last()
dfm=dfm.loc[start:end]
dfm


# In[17]:



TotalCost_list=[]
for i in range(1,len(dfm)+1):
    TotalCost=PMT*i
    TotalCost_list.append(TotalCost)
dfm['total_cost']=TotalCost_list


# In[18]:


bb=[]
for k in range(len(dfm.columns[0:len(stock_list)])):
    unit_list=[]
    bb.append("unit"+str(k+1))
    unit_list=[PMT*ratio[k]/dfm[dfm.columns[k]].iloc[0]]
    for i in dfm[dfm.columns[k]].iloc[1:]:
        unit=unit_list[-1]+PMT*ratio[k]/i
        unit_list.append(unit)
    dfm[bb[k]]=unit_list

dfm.head()


# In[19]:


aa=[]
for k in range(len(dfm.columns[0:len(stock_list)])):
    preNAV_list=[0]
    aa.append("preNAV"+str(k+1))
    for i,j in enumerate(dfm[dfm.columns[k]].iloc[1:]):
        preNAV=dfm[bb[k]].iloc[i]*j
        preNAV_list.append(preNAV)
    dfm[aa[k]]=preNAV_list

dfm.head()


# In[21]:


cc=[]
for k in range(len(dfm.columns[0:len(stock_list)])):
    cc.append("return"+str(k+1)+'(%)')
    dfm[cc[k]]=(dfm[aa[k]]/(dfm['total_cost']*ratio[k]-PMT*ratio[k])-1)*100
dfm.head()


# In[ ]:





# In[ ]:





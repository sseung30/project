#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import pandas as pd
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')


# In[2]:


# 한국어 표시를 위해 나눔스퀘어 사용
# matplotlib 폰트설정
plt.rc('font', family='NanumSquareOTF') # For MacOS


# In[3]:


data = pd.read_csv('busan.csv', encoding = 'CP949')
data.head()


# In[4]:


dinfo= pd.read_csv('busan_station.csv',encoding = 'CP949')  #한글파일 csv인 경우 engine옵션 필요
dinfo.head()


# In[5]:


##역명의 양쪽공백 문자 제거 
data['역명'] = data['역명'].str.strip()
##역명의 중간 공백 문자 제거
data['역명'] = data['역명'].str.replace(" ","")


# In[14]:


#컬럼 일괄 변경 
data.columns = ['역번호', '역명', '년월일','구분', '합계','1시', '2시', '3시', '4시', '5시','6시', '7시', '8시', '9시', '10시', '11시', '12시','13시', '14시', '15시', '16시', '17시', '18시','19시', '20시', '21시', '22시', '23시', '24시']
data.columns


# In[15]:


#datatype변경 년월일:to_datetime  역번호: astype('str')
data['년월일']=data['년월일'].astype('str')  # int -> str변환후 날짜 변환
data['년월일']=pd.to_datetime(data['년월일'])
data['역번호']=data['역번호'].astype('str')


# In[16]:


#결측데이터 확인
data.isnull().sum()


# In[17]:


#데이터 검증 역별로 데이터건수가 동일한지 체크해보자
#df.groupby(['년월일','역번호','역명'])['합계'].mean()
d_check =pd.DataFrame(data.groupby(['역번호','역명','구분'])['년월일'].count())
d_check=d_check.reset_index()
d_check.head()


# In[19]:


#년월일 갯수가 365가 아닌 역 체크해보자 :아래 목록에 나온건은 정제 대상
d_check[d_check['년월일']<213]


# In[20]:


#정제된 데이터 파일로 저장, 한글encoding
data.to_csv('busan_pre.csv',encoding='CP949',index=False)


# In[22]:


#시간대별 분석이 아니므로 일합계만 처리
df = data[['년월일', '역번호', '역명', '구분', '합계']]
df.head()


# In[24]:


#일자로 groupby 승하차 합계의 평균을 1일 이용객수로 산정
dfg = df.groupby(['년월일', '역번호', '역명'])['합계'].mean()


# In[25]:


dfg.head(10)


# In[26]:


#seriese를 데이터프레임으로 재처리
dfg2=pd.DataFrame(dfg)
dfg2.head()


# In[27]:


#index reset
dfg2 = dfg2.reset_index()
dfg2.head()


# In[32]:


#컬럼명 변경 합계 ->이용객수
dfg2.columns
dfg2.columns = ['년월일', '역번호', '역명', '이용객수']
dfg2


# In[34]:


dfg3 = pd.DataFrame(round(dfg2.groupby(['역번호', '역명'])['이용객수'].mean()))
dfg3


# In[35]:


#이용객수로 정렬
dfg3 = dfg3.sort_values(by='이용객수', ascending = False)
dfg3.head(20)


# In[ ]:





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


station = pd.read_csv('daegu_station.csv', encoding = 'CP949')
station.head()


# In[4]:


station2 = station[['역번호','역사명','역사도로명주소']]
station2.columns = ['역번호', '역명', '역주소']
adress_split = station2['역주소'].str.split(" ")
station2["구"] = adress_split.str.get(1)
station2['구']
station2


# In[5]:


station2 = station2[['역명','구']]

#공백 제거
station2['역명'] = station2['역명'].str.replace(" ","")
station2


# In[17]:


#역명 추가 수정 딕셔너리
di = {'대구':'대구역', '동대구':'동대구역'}


#역명수정
station2["역명"].replace(di, inplace=True)

station2


# In[18]:


#승하차데이터 읽어오기
daegu_pre = pd.read_csv('daegu_pre.csv', encoding = 'CP949', lineterminator='\n', thousands = ',')
daegu_pre['합계'] = daegu_pre.sum(axis=1)

#월만 남기기
date_split = daegu_pre['년월일'].str.split("-")
daegu_pre["년월"] = date_split.str.get(0) + "-" + date_split.str.get(1)
daegu_pre


# In[19]:


#승하차 정보에 구 정보 추가
merge_df = pd.merge(station2, daegu_pre, how='right')
merge_df


# In[20]:


#구NaN인 데이터 확인
merge_df_nan = merge_df[merge_df['구'].isnull()]
merge_df_nan['역명'].unique()


# In[21]:


#구 NaN데이터 역명 보기 (dic 만들기 위해 station2 역명 찾기용)
station2.loc[station2['역명'].str.contains('반월당')]


# In[23]:


#구NaN 채우기: 
merge_df.loc[merge_df['역명'] == '서부정류장', '구'] = '남구'
merge_df.loc[merge_df['역명'] == '명덕1', '구'] = '중구'
merge_df.loc[merge_df['역명'] == '반월당1', '구'] = '중구'
merge_df.loc[merge_df['역명'] == '청라언덕2', '구'] = '중구'
merge_df.loc[merge_df['역명'] == '반월당2', '구'] = '중구'
merge_df.loc[merge_df['역명'] == '청라언덕3', '구'] = '중구'
merge_df.loc[merge_df['역명'] == '명덕3', '구'] = '남구'


# In[26]:


#구NaN인 데이터 확인 :0으로 확인
merge_df_nan = merge_df[merge_df['구'].isnull()]
merge_df_nan['역명'].unique()

merge_df


# In[27]:


#필요데이터만 남기기
merge_df = merge_df.filter(['역명', '구', '년월', '합계' ])
merge_df


# In[36]:


#구별, 년월 합계
gu_sum = merge_df.groupby(['년월','구']).sum()
gu_sum = pd.DataFrame(gu_sum).reset_index()
gu_sum = gu_sum.rename({'합계':'구별-월-승하차인원'}, axis=1)
gu_sum


# In[37]:


#구별, 년월, 최대승하차역
gu_max = merge_df.groupby(['년월','구']).max()
gu_max = pd.DataFrame(gu_max).reset_index()
gu_max = gu_max.rename({'합계':'최대역-승하차인원','역명':'최대승하차역'}, axis=1)
gu_max


# In[38]:


#표 하나로 합치기
result = pd.merge(gu_sum, gu_max, how='outer')
result


# In[39]:


#저장
result.to_csv("daegu_result", encoding = 'utf-8-sig')


# In[ ]:





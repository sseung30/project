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


station = pd.read_csv('busan_tube_station.csv', encoding = 'CP949')
station.head()


# In[4]:


station2 = station[['역코드','역명','역주소']]
station2 = station2.rename(columns = {'역코드':'역번호'})
adress_split = station2['역주소'].str.split(" ")
station2["구"] = adress_split.str.get(1)
station2['구']


# In[5]:


station2 = station2[['역번호', '역명','구']]
station2


# In[6]:


#역이름 통일 : 뒷글자'역'제거

station2['역명'] = station2['역명'].str.replace('역','')


# In[7]:


#역명 추가 수정 딕셔너리
di = {'부산':'부산역', '서면(1)':'1서면','연산(1)':'1연산','동래(1)':'1동래',
      '시립미술관':'벡스코','수영':'수영','경성대·부경대':'경성대부경대',
      '국제금융센터·부산은행':'국제금융센터','서면(2)':'2서면','덕천(2)':'2덕천',
      '부산대 양산캠퍼스':'부산대양산', '연산(3)':'3연산', '미남(3)':'미남', '미남(4)':'미남',
      '덕천(3)':'3덕천', '동래(4)':'4동래', '반여농산물시장':'반여농산물','동부산대학':'동부산대',
      '수영':'수영', '수영(2)':'수영', '사상(2)':'사상'}

#역명수정
station2["역명"].replace(di, inplace=True)

station2


# In[8]:


busan_pre = pd.read_csv('busan_pre.csv', encoding = 'CP949', lineterminator='\n', thousands = ',')
busan_pre['합계'] = busan_pre.sum(axis=1)

#월만 남기기
date_split = busan_pre['년월일'].str.split("-")
busan_pre["년월"] = date_split.str.get(0) + "-" + date_split.str.get(1)
busan_pre


# In[9]:


#승하차 정보에 구 정보 추가
merge_df = pd.merge(station2, busan_pre, how='right')
merge_df


# In[10]:


#구NaN인 데이터 확인
merge_df_nan = merge_df[merge_df['구'].isnull()]
merge_df_nan['역명'].unique()


# In[11]:


#구 NaN데이터 역명 보기 (dic 만들기 위해 station2 역명 찾기용)
station2.loc[station2['역명'].str.contains('사상')]


# In[12]:


#필요데이터만 남기기
merge_df = merge_df.filter(['역명', '구', '년월', '합계' ])
merge_df


# In[13]:


#구별, 년월 합계
gu_sum = merge_df.groupby(['년월','구']).sum()
gu_sum = pd.DataFrame(gu_sum).reset_index()
gu_sum = gu_sum.rename({'합계':'구별-월-승하차인원'}, axis=1)
gu_sum


# In[16]:


#구별, 년월, 최대승하차역
gu_max = merge_df.groupby(['년월','구']).max()
gu_max = pd.DataFrame(gu_max).reset_index()
gu_max = gu_max.rename({'합계':'최대역-승하차인원','역명':'최대승하차역'}, axis=1)
gu_max


# In[17]:


#표 하나로 합치기
result = pd.merge(gu_sum, gu_max)
result


# In[18]:


#저장
result.to_csv("busan_result", encoding = 'utf-8-sig')


# In[ ]:





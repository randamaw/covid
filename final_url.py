#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd 
import numpy as np
from bs4 import BeautifulSoup


############ MONTHS ##############
page = requests.get("https://coronavirus.dc.gov/page/coronavirus-data")
soup = BeautifulSoup(page.content, 'html.parser')

ct = 0 
ray = np.array([])



for path in soup.find_all('p'):
    
    phrase = path.get_text() ## stores phrase and checks if keyword is in phrase
    
#     if (phrase.find('April') != -1) or (phrase.find('March') != -1): # raw months outpout
#         print (phrase)

    year = phrase.find('2020') +4 #clean months output
    if (phrase.find('April') != -1):
        pos = phrase.find('April')
#         print (phrase[pos : year])

        date = phrase[pos : year]
        if (date != ''):
            ray = np.append(ray, date)
        ct += 1

    elif (phrase.find('March') != -1):
        pos = phrase.find('March')
        date = phrase[pos : year]
        if (year != 3):
            if (date != ''):
                date = phrase[pos : year]
                ray = np.append(ray, date)
#             print (phrase[pos : year])
            ct += 1
        else:
            date = phrase[pos:len(phrase)-1]+", 2020"
            if (date != ''):
                ray = np.append(ray, date)
            if (phrase.find('March 11')):
                break

# print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~', ct)

#     if (phrase.find('Number') != -1): # ALL STATISTICS 
#         print (stat.get_text())



def overall (phrase,key): 
   
    colon = phrase.find(':')
    if (phrase.find(key) != -1) or (phrase.find(key.capitalize()) != -1):
       
        if (colon != -1):
#             print (phrase[colon+2:len(phrase)])
            return (phrase[colon+2:len(phrase)])

        else: 
#             print (phrase[:len(phrase)])
            return (phrase)
            
    
def positive (phrase,key, ct2):
    colon = phrase.find(':')
    if (phrase.find(key) != -1) or (phrase.find(key.capitalize()) != -1):
        
        if (phrase.find('PHL') != -1):
            ct2 +=1
#             print (ct2, phrase[colon+2:len(phrase)], end = ' ')
            x = phrase[colon+2:len(phrase)]
            return x,ct2
        
        elif (phrase.find(';') != -1):
#             print ('')
            x = ''
            return x, ct2
        
        else:        
            if (phrase.find('commercial lab') != -1):
                ct2 = 2
#             print (phrase[colon+2:len(phrase)])
            x = phrase[colon+2:len(phrase)]
            return x, ct2






ct2 = 0 

nums = np.array([])
deaths = np.array([])
recover = np.array([])
pos = np.array([])


for stat in soup.find_all('li'):
    
    total = None
    phrase = stat.get_text()
    phrase = phrase.replace(',', '')
    phrase = phrase.replace('*','')
    
    key = "overall"
    total = overall(phrase,key)
    if (total != None):
        total = total.replace(' ','')
        total = int(total)
        nums = np.append(nums, total)
    
    
    key = 'lost' 
    total = overall(phrase,key)  
    if (total != None):
        deaths = np.append(deaths, total)
    key = 'deaths' 
    total = overall(phrase,key)  
    if (total != None):
        deaths = np.append(deaths, total)
        
        
    key = 'recovered'
    total = overall(phrase,key)  
    if (total != None):
        recover = np.append(recover, total)
        
        
    key = "positives"
    total = positive(phrase,key,ct2) 

    if (total != None):
        if (total[1] == 2):
            x = len(pos) - 1
            pos[x] = int(pos[x])
#             y = int(total[0])
            pos[x]= pos[x] + ' ' + total[0]
#             print('hi')
        elif (total[0] != ''):
            pos = np.append(pos, total[0])
        

allz = np.array([])
for x in pos:
    finder = x.find(' ')
    if(finder != -1):
        first = int(x[0:finder])
        second = int (x[finder+1:len(x)])     
        total = first + second 
#         print (total)
        allz = np.append(allz, total)

    else:
        total = int(x)
        allz = np.append(allz, total)
#         print(x)

if (len(allz) != len(nums)):
    allz = np.delete(allz,len(allz)-1)
    ray = np.delete(ray,len(ray)-1)

ct = 0
for x in ray:
    comma = x.find(',')
    if (x.find('March') != -1):
        x = '3/'+ x[6:comma]
        ray[ct] = x
    else:
        x = '4/'+ x[6:comma]
        ray[ct] = x
    ct +=1
    
ray = ray[::-1]   #INVERTS ALL THE COLUMNS
allz = allz[::-1]
nums = nums[::-1]



# In[2]:


redo = np.array([])  ### FILLS DATAFRAME
rate = np.array([])

ct = 0
for x in nums:
    first = x
    if(ct == 8):
        first = int(first)
        first = first + 1000
    redo = np.append(redo,first)
    ct +=1 

    
ct = 0
for x in redo:
    x = int(x)
    net = (allz[ct]/x)*100
    rate = np.append(rate, net)
    ct +=1

df = pd.DataFrame({
    "Dates":ray,
    "Positives":allz,
    "Overall":redo
#     "Rate":rate
    
})


df['\u0394 +'] = df['Positives'].diff(1) # DELTA POSITIVES!!!!!!!!
df['\u0394 total'] = df['Overall'].diff(1)
df['Rate'] = round((df['\u0394 +'] / df['\u0394 total'])* 100,2)
df = df[7:]
# print(df)


# In[4]:


from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from plotly import tools
import os

fig = make_subplots(rows=3, cols=1, 
                    shared_xaxes=True, 
                    subplot_titles=("Positives","Rate", "\u0394 +"),
                    vertical_spacing=0.07)

fig.add_trace(go.Scatter(x = df['Dates'], y = df['Positives'], name = 'Total Positives'),row=1, col=1)

fig.add_trace(
    go.Scatter(x=df['Dates'],y = df['Rate'],
    mode='lines',
    name='Rate'),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(x=df['Dates'], y=df['\u0394 +'],
    mode='markers',
    name='\u0394 +'), row=3, col=1)

fig.update_layout(height=700, width=950)
fig.update_xaxes(tickangle= 60)
fig.write_html("/home/roh/covid/_includes/graphs.html")
# fig.show()

#####DATAFRAME
df = df.iloc[::-1]

fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df['Dates'], df['Positives'], df['Overall'],df['\u0394 +'], df['\u0394 total'],df['Rate']],
               fill_color='lavender',
               align='left'))
])

fig.write_html("/home/roh/covid/_includes/data.html")
# fig.show()




# In[ ]:





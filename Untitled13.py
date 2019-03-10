
# coding: utf-8

# In[18]:


import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer
from collections import OrderedDict
import pandas as pd


url = "https://www.ox.ac.uk/admissions/undergraduate/courses/course-listing?wssl=1"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
links=[]

for link in soup.findAll('a', attrs={'href': re.compile("^//www.ox.ac.uk/admissions/undergraduate/courses-listing")}):
    links.append(link.get('href') )
#courses list
courses = [x[56:] for x in links]

final = pd.DataFrame()

for t in range(len(links)):
    print(courses[t])
    soup = BeautifulSoup( urlopen("https:"+links[t]), 'lxml')
    table = soup.findAll("div" , id = re.compile("content-tab--3") )
    table[0].findAll("tbody")
    keys = ["A-levels:" , "Advanced Highers:", "IB:" , "Helpful:" , "Description:" ,
             
            "Submission deadline:" ,"Recommended:" , "Essential:" ,"Test:",
            "Test date:" , "Registration deadline:"]
    #d = {key : None for key in keys}
    #for mytable in table :
    d = OrderedDict()
    
    #oddlist = []
    table_body = table[0].findAll('tbody')
    length = len(table_body)
    for i in range(length):
        try:
            rows = table_body[i].find_all('tr')
            #print(rows)
            for tr in rows:
                cols = tr.find_all('td')
                #if length of cols is odd (assume = 1)then create other list for storing that values
                if len(cols)%2==0:
                    d[cols[0].text] = cols[1].text
                
                    
        except:
            print("no tbody")
    print(d)
    keyslist = list(d.keys())
    
    values = [d[key] for key in keyslist]
    
    #s = pd.DataFrame(keyslist , columns= ["head"])
    #t = pd.DataFrame(values , columns = ["values"])
    #v = pd.concat([s,t] ,axis = 1)
    
    #now entering values in list
    index = pd.MultiIndex.from_product([ [courses[t] ], keyslist] , names = ["courses" , "attributes"])
    da = pd.DataFrame(values , index = index , columns = ["valuie"])
    final = pd.concat([final , da] , axis =0)
    
    
    
    
    


# In[19]:


final


# In[20]:


save = final.to_csv(r"C:\Users\Vivek Kushwaha\Downloads\collegeentry.csv")


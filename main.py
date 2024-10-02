import requests
import pandas as pd
from bs4 import BeautifulSoup
url ="http://ufcstats.com/statistics/events/completed"
r= requests.get(url)
with open("data/competitions.html", "w") as f:
    f.write(r.text)
with open("data/competitions.html","r") as f:
    html_doc = f.read()
dx = {'S.No.': [] , "Fight Name":[], "Date":[], "Location":[]}

soup = BeautifulSoup(html_doc,"html.parser")
span = soup.select("a.b-link.b-link_style_black")
i=1
for s in span:
    dx['S.No.'].append(i)
    name=s.string.strip()
    dx["Fight Name"].append(name)
    lx = s.get("href")
    r= requests.get(lx)
    with open (f"data/playerdata/fight{i}.html","w") as f1:
        f1.write(r.text)
    i=i+1
span = soup.select("span.b-statistics__date")
a= 1
b=1
for s in span:
    name = s.string.strip()
    if(name=="September 28, 2024"):
        continue
    dx["Date"].append(name)
    a=a+1
span = soup.select("td.b-statistics__table-col.b-statistics__table-col_style_big-top-padding")
for s in span:
    name =s.string.strip()
    if(name =="Paris, Ile-de-France, France"):
        continue
    dx["Location"].append(name)
    b=b+1
df = pd.DataFrame.from_dict(dx)
df.to_csv("data/competitions.csv",index=False)

# <---------------------------- now making fights csv files ---------------------------------------------------->


li =[]
h=1
data = {"S.No.":[],"Fighters":[],"Fight Name":[],"Weight Class":[],"Method":[],"Round":[],"Time":[],"Winner":[]}
for i in range(1,25,1):
        with open(f"data/playerdata/fight{i}.html","r") as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc,"html.parser")
        data1 = {"S.No.":[],"Fighters":[],"Fight Name":[],"Weight Class":[],"Method":[],"Round":[],"Time":[],"Winner":[]}
        span = soup.select("td.b-fight-details__table-col")
        j=0
        
        for x in span:
              if j%10==1:
                st=""
                for a in x.select("a.b-link.b-link_style_black"):
                        name = a.string.strip()
                        if(name not in li):
                              li.append(name)
                              link = a.get("href")
                              url1 = requests.get(link)
                              with open(f"data/playerinfo/{h}.html","w") as hf:
                                    hf.write(url1.text)
                              print("player",h," done")
                              h=h+1
                              
                        if(len(st)==0):
                            st=name
                            data1["Winner"].append(name)
                        else:
                            st= st+", "+name
                data1["Fighters"].append(st)       
                               
              if j%10 ==6:
                    name= x.find("p").text.strip()
                    data1["Weight Class"].append(name)
              if j%10 ==7:
                    data1["Method"].append(x.find("p").text.strip())
              if j%10 ==8:
                    data1["Round"].append(x.find("p").text.strip())
              if j%10 ==9:
                    data1["Time"].append(x.find("p").text.strip())
              j=j+1
        nx = soup.find("span").text.strip()
        for kx in range(1,len(data1["Winner"])+1,1):
              data1["S.No."].append(kx)
              data1["Fight Name"].append(nx)
        df = pd.DataFrame.from_dict(data1)
        df.to_csv(f"data/playerdata/fight{i}.csv",index=False)
        data1 = data 

# <----------------------------------  Now making player infot=rmation table csv file -------------------------------------------->


data = {"S.No.":[],"Fighter Name":[],"Height":[],"Weight":[],"Reach":[],"Stance":[],"DOB":[]}
for i in range (1,360,1) :
    with open(f"data/playerinfo/{i}.html","r") as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc,"html.parser")
    span = soup.find("ul")
    # span = soup.select("ul.b-list__box-list")
    data["Fighter Name"].append(soup.find("span").text.strip())
    k=0
    for a in span.find_all("li"):
        
        if k%5==0:
            str1 = a.text.strip()[10:].strip()
            ht = float(str1[0:1])+0.01*(float(str1[2:4]))
            data["Height"].append(ht)
        if k%5==1:
            data["Weight"].append(a.text.strip()[10:].strip())
        if k%5==2:
            data["Reach"].append(a.text.strip()[9:].strip())
        if k%5==3:
            data["Stance"].append(a.text.strip()[10:].strip())
        if k%5==4:
            data["DOB"].append(a.text.strip()[7:].strip())
        k=k+1    

for i in range(1,len(data["DOB"])+1,1):
    data["S.No."].append(i)
df = pd.DataFrame.from_dict(data)
df.to_csv(f"data/player_information.csv",index=False)


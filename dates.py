from bs4 import BeautifulSoup
from simple_get import simple_get


def dates(code):
    raw_html = simple_get("https://finance.yahoo.com/calendar/earnings?symbol="+code)
    html = BeautifulSoup(raw_html, "html.parser")
    data = [p.text for p in html.select('span')]
    i=0
    datesList =[]
    for x in data:
        #print(i,x)
        if (i==53 or i==56 or i==59):
            datesList.append(x)
        i+=1
    return datesList

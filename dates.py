from bs4 import BeautifulSoup
from simple_get import simple_get


def dates(code):
	raw_html = simple_get("https://finance.yahoo.com/calendar/earnings?symbol="+code)
	html = BeautifulSoup(raw_html, "html.parser")

	data = [p.text for p in html.select('span')]
	i=0
	datesList =[]
	for x in data:
		if (i==51 or i==54 or i==57):
			datesList.append(x)
		i+=1
	return datesList
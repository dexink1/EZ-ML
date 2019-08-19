from bs4 import BeautifulSoup
from simple_get import simple_get

def company(link):
	raw_html = simple_get(link)
	html = BeautifulSoup(raw_html, "html.parser")

	data = [p.text for p in html.select('a.Fw(b)')]
	return data


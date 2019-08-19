from bs4 import BeautifulSoup
from simple_get import simple_get
from collections import OrderedDict

def pastPrices(code):
	raw_html = simple_get("https://finance.yahoo.com/quote/"+code+"/history")
	html = BeautifulSoup(raw_html, "html.parser")

	data = [p.text for p in html.select('span')][34:724]

	data_dict = OrderedDict()
	i = 0
	skip=False

	for item in data:
		#print(i,item)
		if not skip:
			if i==0:
				try: 
					data_dict[item]
				except:
					data_dict[item] = [0,0]
					temp_date = item
				else:
					skip = True
					i=-1
			elif i==1:
				data_dict[temp_date][0] = item.replace(',','')
			elif i==4:
				data_dict[temp_date][1] = item.replace(',','')
			elif i==6:
				i=-1
			
			i+=1
		else:
			skip = False	

	return data_dict	

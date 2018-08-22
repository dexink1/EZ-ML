from pastPrices import pastPrices
from dates import dates
from statistics import mean
import statistics
from company import company

def summarize(code):

	releaseDates = [date[:12] for date in dates(code)]
	prices = pastPrices(code)
	filteredDates = []
	finalDiff = []

	for date  in releaseDates:
		try:
			prices[date]
		except KeyError:
			pass
		else:
			filteredDates.append(date)
	after = False
	previous=0
	for date in prices:
		try:
			#print(date,prices[date],finalDiff,after)
			if date in filteredDates:
				after=True
				finalDiff.insert(0,previous)
			elif after:
				after=False
				finalDiff[0] = ((float(finalDiff[0])-float(prices[date][1]))/float(prices[date][1]))
			else:
				previous=prices[date][0]
		except Exception as e:
			#print(e)
			pass

	if after:
		finalDiff = finalDiff[1:]

	return finalDiff

link = "https://finance.yahoo.com/calendar/earnings?day=2018-08-21"

total = []
i = 0
length = len(company(link))
#print(length)


for item in company(link):
	try:
		c = (item,mean(summarize(item)))
		total.append(c)
	except statistics.StatisticsError:
		pass
	i+=1
	print(str(round((i/length)*100,2)) + "% completed")

total.sort(key=lambda value:-value[1])
j=0
for item in total:
	j+=1;
	print(j,item)


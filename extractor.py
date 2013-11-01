from bs4 import BeautifulSoup

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

def getDay(entry):
	parent = entry.find_parent(attrs={'class' : 'SSSWEEKLYBACKGROUND'})
	index = -1
	for _ in parent.previous_siblings:
		index += 1
	return DAYS[index]

def getClasses(soup):
	soup.prettify()
	for entry in soup.find_all(attrs={'class': 'SSSTEXTWEEKLY'}):
		print(getDay(entry))
		print('\t'.join([s for s in entry.strings]))

soup = BeautifulSoup(open('test.html', 'r').read())
getClasses(soup)

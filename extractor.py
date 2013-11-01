from bs4 import BeautifulSoup
import datetime

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
SEMESTER_START = datetime.datetime(2013, 8, 26)

class Class:
	__slots__=('number', 'name', 'start', 'end')
	def __init__(self):
		pass

	def __str__(self):
		return "Number: %s\nStart: %s\nEnd: %s" % (self.number, self.start, self.end)

def getDay(entry):
	parent = entry.find_parent(attrs={'class' : 'SSSWEEKLYBACKGROUND'})
	index = -1
	for _ in parent.previous_siblings:
		index += 1
	return index

def makeClass(entry):
	day = getDay(entry)

	arr = [s for s in entry.strings]

	c = Class()

	c.number = arr[0]

	starthour = int(arr[2].split(" - ")[0].split(":")[0])
	startmin = int(arr[2].split(" - ")[0].split(":")[1])
	c.start = SEMESTER_START + datetime.timedelta(days=day, hours=starthour, minutes=startmin)

	endhour = int(arr[2].split(" - ")[1].split(":")[0])
	endmin = int(arr[2].split(" - ")[1].split(":")[1])
	c.end = SEMESTER_START + datetime.timedelta(days=day, hours=endhour, minutes=endmin)
	
	return c

def getClasses(soup):
	soup.prettify()
	for entry in soup.find_all(attrs={'class': 'SSSTEXTWEEKLY'}):
		c = makeClass(entry)
		print(c)
		print()

soup = BeautifulSoup(open('test.html', 'r').read())
getClasses(soup)

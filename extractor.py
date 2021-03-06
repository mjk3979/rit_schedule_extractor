from bs4 import BeautifulSoup
from icalendar import Calendar, Event
import datetime
import hashlib
import sys

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
SEMESTER_START = datetime.datetime(2013, 8, 26)
SEMESTER_END = datetime.date(2013, 12, 13)

class Class:
	__slots__=('number', 'name', 'start', 'end')
	def __init__(self):
		pass
	
	def toEvent(self):
		event = Event()
		event.add('summary', self.number)
		event.add('dtstart', self.start)
		event.add('dtend', self.end)
		
		repeat = {}
		repeat['FREQ'] = 'WEEKLY'
		repeat['UNTIL'] = SEMESTER_END
		event.add('rrule', repeat)

		event['uid']=hashlib.sha224(self.__str__()).hexdigest()

		return event

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
	return [makeClass(entry) for entry in soup.find_all(attrs={'class': 'SSSTEXTWEEKLY'})]

soup = BeautifulSoup(open(sys.argv[1], 'r').read())
soup.prettify()

classes = getClasses(soup)

cal = Calendar()
cal.add('prodid', '-//RIT Class Schedule//mxm.dk//')
cal.add('version', '2.0')

for c in classes:
	cal.add_component(c.toEvent())
print cal.to_ical()

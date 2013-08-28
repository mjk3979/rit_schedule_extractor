from bs4 import BeautifulSoup

soup = BeautifulSoup(open('test.html', 'r').read())
soup.prettify()
for entry in soup.find_all(attrs={'class': 'SSSTEXTWEEKLY'}):
	print('\t'.join([s for s in entry.strings]))

#Python Scraper for Jefferson County Health Dept. website
#Goes thru each letter and scrapes health inspection reports and links
#Uses BeautifulSoup and writes to a txt file

import requests
from bs4 import BeautifulSoup
from string import ascii_uppercase
import addtodb
import asyncio

url = "http://www.jcdh.org/EH/FnL/FnL03.aspx"

def scrape_and_add():
	for letters in ascii_uppercase:

		#error handling for requests to jcdh website
		try:
			response = requests.get(url+"?Letter="+letters)
		except requests.exceptions.Timeout:
			#timeout on letter - skip letter in loop
			continue
		except requests.exceptions.RequestException:
			sys.exit(1)


		html = response.content

		soup = BeautifulSoup(html, "html5lib")
		table = soup.find('table', id='ctl00_BodyContent_gvFoodScores')
		#print ("Processing " + letters)

		#error checking in case letters don't exist
		if table is not None and table.findAll('tr')[1:] is not None:

			for row in table.findAll('tr')[1:]: #skip header
				row_list = []
				for cell in row.findAll('td'): #skip smoke free y/n
					#extract name, type, address, score, date checked
					text = cell.text.replace('\n', '') 
					row_list.append(text) 
				for cell in row.findAll('a'):
					#extract links for past scores and link to reports
					links = cell.get('href')
					#add the prefix of the url
					row_list.append("http://www.jcdh.org/EH/FnL/"+links)
				
				addtodb.add_row([row_list])

			#cmmdline display of status

			print("Finished " + letters)
json_data = addtodb.json_formatter()
#scrape_and_add(); uncomment to update db and run in cmd prompt
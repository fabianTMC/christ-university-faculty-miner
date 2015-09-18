from pyquery import PyQuery as pq
from lxml import etree
import urlparse
import urllib
import re
import operator


class Miner:
	def facultyMiner(self, url):
		print url

	'''
		This takes the url of a department and extracts the name of the department and passes the url of the faculty to the faculty miner
	'''
	def departementMiner(self, url):
		# load the html document
		d = pq(url=url)

		# get the department name
		name = d('.civilmtext').eq(0).text()

		# get the links so that we can find the link to the faculty profile
		target = None
		links = d('.civilmenu')('a')

		# loop through the links until we find the faculty profile
		for i in range(0, links.length):
			text = links.eq(i).text().strip()

			if text.lower() == 'faculty profile':
				target = i
				break

		# check if we found the target url
		if target is None:
			print "Unable to find faculty profile for "+name+" at url "+url
		else:
			facultyUrl = links.eq(target).attr('href')
			if facultyUrl is not None:
				self.facultyMiner(facultyUrl)
			else:
				print "Faculty profile url is empty for "+name+" at url "+url

	'''
	Constructor that takes a parameter of the academics page url and extracts the url of each department and passes it to the departementMiner
	'''
	def __init__(self, depturl):
		self.depturl = depturl

		# load the html document
		d = pq(url=self.depturl)

		# find all the department details
		links = d("#departmentDetails")

		debug = 0

		# loop through the links and find the divs in each
		for i in range(0, links.length):
			# load the span content and find all the divs
			span = pq(links[i])
			divs = span('div')

			for j in range(0, divs.length):
				# load the current div and extract the text
				# NOTE: currently there is no text; only an image
				current = pq(divs.eq(j))
				href = current('a').attr("href")

				# check if we found a url
				if href is not None:
					debug = debug + 1
					self.departementMiner(href)

					if debug == 1:
						break
				else:
					print "Department url not found for element at"+current


# start the miner
Miner('http://localhost/fabian/cached/faculty/academics')
from pyquery import PyQuery as pq
from lxml import etree
import urlparse
import urllib
import re
import operator


class Miner:
	'''
	Constructor that takes a parameter of the academics page url and extracts the url of each department and passes it to the departementMiner
	'''
	def __init__(self, depturl):
		self.depturl = depturl

		# load the html document
		d = pq(url=self.depturl)

		# find all the department details
		links = d("#departmentDetails")

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

				if href is not None:
					print href


# start the miner
Miner('http://localhost/fabian/cached/faculty/academics')
from pyquery import PyQuery as pq
import re

class Miner:
	# variables needed for the miner to work correctly
	teacherTypes = ['professor', 'associate professor', 'assistant professor', 'teaching associate', ' research director']

	'''
		This takes the url of the faculty profile for a department and extracts the name, degrees,position and profile details of each professor
	'''
	def facultyMiner(self, url):
		teachers = []

		# load the html document
		d = pq(url=url)

		# get the container for the faculty
		container = d('.sylfull')

		# there are two containers but we only want to loop through one

		professors = container.eq(0)('.col-md-3')

		# loop through all the professors
		for j in range(0, professors.length):
			professor = professors.eq(j)

			# extract the data of the professor
			name = professor('strong').text()
			picture = professor('img').attr('src')

			# we have to do some parsing of the text to get what type of professor they are
			text = professor.text()
			# strip the name of the professor
			text = text[len(name):].strip()

			distance = 0
			start = None
			end = None

			# loop through the professor types and find them in the text
			for k in self.teacherTypes:
				pattern = re.compile(k, re.IGNORECASE)
				match = re.search(pattern, text.lower())

				# did we find anything
				if match:
					currentDistance = match.end() - match.start()

					# check if this was a closer match that the others
					if currentDistance > distance:
						distance = currentDistance
						start = match.start()
						end = match.end()

			# did we find the professor type?
			if start is not None and end is not None:
				# extract the data
				position = text[start:end]
				degress = text[:start]

				# get the url of the profile details of the professor
				link = professor('.probut03').attr('onclick')
				if link is not None:
					pattern = re.compile("document.location.href='", re.IGNORECASE)
					linkSearch = re.search(pattern, link)

					# check if we found the url
					if linkSearch is not None:
						link = link[linkSearch.end():-1]
					else:
						print "None link found for professor details on url "+url
				else:
					print "Could not detect professor details link on url "+url

				# strip extra spaces
				name = re.sub('(\s)+', ' ', name)

				print name
				print position
				print degress
				print link
				print
			else:
				print "Could not detect professor type on url "+url+" with text `"+text+"`"

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
				print "Department of "+name
				print "-------------------------------------"
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

					# if debug == 1:
					# 	break


# start the miner
Miner('http://www.christuniversity.in/academics')
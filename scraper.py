# Developed by Gyu Lim.  Jan 2017


def Data_Scraper_Per_WebPage(sURL):	
# Function Overview: "Data_Scraper_Per_WebPage"
#   a) Feature : This function scrapes information about the threads that are posted on the 'F150 Ecoboost' web forum. 
# 	b) Input   : URL for the webpage (It is observed that each page contains as many as 20 threads)
#   c) Output  : Column vector for {Thread Title}, {Thread Link}, {# of Views}, {# of Replies}, {Last post date}, {Last post time}

	# 1. Importing necessary libraries
	import bs4 as bs   #import "BeautifulSoup4" for HTML text parsing
	import urllib2     #import "urllib2" for importing data from html 
	from datetime import date, datetime, timedelta
	
	# 2. Web HTML source into BeautifulSoup
	sauce = urllib2.urlopen(sURL).read()  #loading the html.
	soup = bs.BeautifulSoup(sauce, "lxml") # converting the loaded html to be beautifulsoup-friendly.
	
	# 3. Declaration of the variable who will contain scraped data. 
	#    (They will be exported at the end of the function.)
	sThreadLink = []
	sTitle = []
	iNumViews = []
	sLastPostTime = []
	sLastPostDate = []
	
	# 4. Data Scraping (This section performs various text mining techniques provided by BeautifulSoup4)

	# 4.1 [Link to Thread] & [Name of Thread]
	for a in soup.find_all("a", {"class" : "title"}):
		sTitle.append(a.text)             # Thread Title
		sThreadLink.append(a.get("href")) # Thread Link
		
	# 4.2 [Number of Views]
	for li in soup.find_all("li"):
		if li.text[0:6] == "Views:":               # If first 6 characters are "Views:" out of "Views: XXXXX", it performs scraping
			sNumViews = li.text[7:len(li.text)]    # Extract the strings that indicates the number of views
			sNumViews = sNumViews.replace(",", "") # take out the commas and turn into integer
			iNumViews.append(int(sNumViews))       # String into Integer
	

	# 4.3 [Last Post Date] and [Last Post Time]
	for dd in soup.find_all("dd"):
		if "AM" in dd.text or "PM" in dd.text:
			[sDate, sTime] = dd.text.rstrip().split(",")
			sLastPostTime.append(sTime)
			if sDate == "Today":
				sDateYesterday = date.today().strftime('%m-%d-%Y') # The web has its date with the M-D-Y format, therefore, I set that to be the format throughout the codes.
				sLastPostDate.append(sDateYesterday)
			elif sDate == "Yesterday":
				sDateYesterday = (date.today() - timedelta(days=1)).strftime('%m-%d-%Y') 
				sLastPostDate.append(sDateYesterday)
			else:
				sLastPostDate.append(sDate)
	
	# 4.4 Function returns the sc
	return 	(sTitle, sThreadLink, iNumViews, sLastPostDate, sLastPostTime)




def run_scraper():
	iNumThreadPerPage = 20 # hard-coded, knowing that each page will have 20 posting therefore 100 threads.
	iNumWebPage = 5 # hard-coded, knowing that scraping from 5 pages yields 100 threads. (5 pages X 20 threads)
	sURL_List = []
	for i in range(0, iNumWebPage):  
		if i == 0:
			# I observed that as I click "sort by Number of Views", the following URL showed up on the first page.
			sURL = "http://www.f150ecoboost.net/forum/42-2015-ford-f150-ecoboost-chat?pp=20&daysprune=-1&sort=views&order=desc"
			sURL_List.append(sURL)
		else:
			# I observed that as I click "sort by Number of Views", the URL for the subsequent pages (after the first page) had the following pattern.  
			sURL = "http://www.f150ecoboost.net/forum/42-2015-ford-f150-ecoboost-chat/index" + str(i+1) + ".html?sort=views&order=desc&daysprune=-1"
			sURL_List.append(sURL)
	
	# 2. Data-scraping
	# 2.1 Delcaring the empty array (where the scraped data will be stored for future export to CSV)
	sExport_Title = []
	sExport_ThreadLink = []
	sExport_NumViews = []
	sExport_LastPostDate = []
	sExport_LastPostTime = []
	# 2.2 Looping the data scraping and data-stroing. 
	#from beautifulsoup_example import Data_Scraper_Per_WebPage

	for i in range(0, iNumWebPage):	
		#2.2.1 Looping the data scarping.
		(sTitle, sThreadLink, iNumViews, sLastPostDate, sLastPostTime) = Data_Scraper_Per_WebPage(sURL_List[i])


		#2.2.2 Looping the data-storing.
		for j in range(0, iNumThreadPerPage):
			sExport_Title.append(sTitle[j])
			sExport_ThreadLink.append(sThreadLink[j])
			sExport_NumViews.append(str(iNumViews[j]))
			sExport_LastPostDate.append(sLastPostDate[j])
			sExport_LastPostTime.append(sLastPostTime[j])
	
	return (sExport_Title, sExport_ThreadLink, sExport_NumViews, sExport_LastPostDate, sExport_LastPostTime)
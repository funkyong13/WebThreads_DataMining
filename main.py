# Developed by Gyu Lim.  Jan 2017

# Overview
# This program is develeped to perform data mining from a web-forum.
#   For the purpose of demonstration of python-web-data-mining, the following 
#   particular web-forum is used.
#   http://www.f150ecoboost.net/forum/42-2015-ford-f150-ecoboost-chat

# Output: Web-scraoed data is exported as a csv file.
#         It describes the attiributes of the 100 most viewed threads. 



# STEP1. Read data from the scraper function
from scraper import run_scraper
(sTitle, sThreadLink, sNumViews, sLastPostDate, sLastPostTime) = run_scraper()



# STEP2. Save the imported data into Pasdas DATA FRAME
import pandas as pd
threads = pd.DataFrame(
	{"Title": sTitle,
	 "Thread Link": sThreadLink,
	 "Number of Views": sNumViews,
	 "Last Pot Date": sLastPostDate,
	 "LastPostTime": sLastPostTime
	})



# STEP3. Export the pandas data frame as a csv file. ("threads.scarped.csv")
# print(threads.to_string())
csv_title = "threads_scraped"
threads.to_csv(csv_title, index = True, encoding = "utf-8")
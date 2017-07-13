#Tonaton Webscraping script for house rentals

import urllib2
import bs4
import math

## Returns the html text of a url
def openUrl(url, hdr = {'User-Agent' : "Magic Browser"}):

 	req = urllib2.Request(url, headers= hdr)
 	source = urllib2.urlopen(req).read()
 	return source

## Takes a source and makes a Beautiful Soup object
def makeSoup(source, type = "html.parser"):

	soup = bs4.BeautifulSoup(source, type)
	return soup



source = openUrl("https://tonaton.com/en/ads/ghana/houses?type=for_rent&page=")

soup = makeSoup(source)



search_num_results = soup.find_all("div", {"class": "ui-panel-content ui-panel-block"})

#Determines the total number of pages that contain all the property listing information
pages = 0

for item in search_num_results:

	t = item.find("span", {"class" : "t-small summary-count"})

	if t is not None:
		pages = t.text.split(" ")
		number_per_page = int(pages[1].replace("-", " ").split(" ")[-1])
		pages = math.ceil(float(pages[-2].replace(",", ""))/number_per_page)
		break



##Make a list of all the url extensions to the description pages
House_links = []

for i in range(int(pages)):

	i += 1

	url = "https://tonaton.com/en/ads/ghana/houses?type=for_rent&page=" + str(i)

	source = openUrl(url)

	soup = makeSoup(source)

	House = soup.find_all("div", {"class": "item-content"})

	[House_links.append(item.a.get("href")) for item in House]


#Open a new csv file with appropriate name
f = open("Houses_Ghana.csv", "w")

headers = "Name, Landmark, City, Town, Bed, Bath, Size, Currency, Rent, Owner,\
Listing_Date, Type, Description\n"
f.write(headers)

#Lets loop through the code to the data
for item in House_links:

	url = "https://tonaton.com" + item

	source = openUrl(url)

	soup = makeSoup(source)

	data = soup.find("div", {"class": "ui-panel-content ui-panel-block"})
	

	temp_holder = data.find("div", {"class": "item-top col-12 lg-8"})

	if temp_holder is not None:

		name = temp_holder.h1.text.encode("utf-8")
		Owner = temp_holder.p.span.text.replace("For rent by ", "").encode("utf-8")

		if "MEMBER" in Owner:
			Owner = Owner.replace("MEMBER", "").encode("utf-8")

		Date = temp_holder.p.find("span", {"class": "date"}).text.encode("utf-8")
		Location = temp_holder.p.find("span", {"class": "location"}).text

		City = Location.split(", ")[0].encode("utf-8")
		Region = Location.split(", ")[1].encode("utf-8")


	details = data.find("div", {"class": "col-12 lg-8 item-body"})

	#Extracts currency and rent
	if details is not None:
		money = details.find("div", {"class": "ui-price-tag"}).text.split(" ")
		Currency = "Ghana cedis"
		Amount = money[1].replace(",", "").encode("utf-8")


	describe = data.find("div", {"itemprop": "description"})

	#Extracts the blurb about the house..
	if describe is not None:
		Description = describe.get_text(separator = " ").encode("utf-8")


	Property_details = data.find("div", {"class": "item-properties"})

	if Property_details is not None:

			#Extracts the data about the house..
			t = Property_details.get_text(separator='\n').split("\n")

			if 'Street / Landmark:' in t:
				Landmark = t[1].encode("utf-8")

				#checks whether the unit of measurement is sqft or sq m
				if "sqft" in t[3]:
					Size = t[3].encode("utf-8")
				else:
					num = t[3].split(" ")[0]
					Size = " ".join((num, "sqm")).encode("utf-8")
				Beds = t[5].encode("utf-8") #stores number of beds
				Baths = t[7].encode("utf-8") #stores number of baths
			else:
				Landmark = ""

				#checks whether the unit of measurement is sqft or sq m
				if "sqft" in t[1]:
					Size = t[1].encode("utf-8")
				else:
					num = t[1].split(" ")[0]
					Size = " ".join((num, "sqm")).encode("utf-8")

				Beds = t[3].encode("utf-8")	#stores number of beds
				Baths = t[5].encode("utf-8") #stores number of baths



	Type = "House" #type of building


	#Write the variables to a csv file to store
	f.write(name.replace(",", " ") + "," + Landmark.replace(",", " ") + "," + City.replace(",", " ") + \
		","+ Region.replace(",", " ") + "," + Beds + "," + Baths + "," + Size + "," + Currency + "," + \
		Amount + "," + Owner.replace(",", " ")+ "," + Date +  "," + Type + "," + Description.replace(",", " ") + "\n")


f.close()




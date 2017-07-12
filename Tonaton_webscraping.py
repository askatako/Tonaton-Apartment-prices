import urllib2
import bs4

url = "https://tonaton.com/en/ads/ghana/houses?type=for_rent&page="

hdr = {'User-Agent' : "Magic Browser"}

req = urllib2.Request(url, headers=hdr)

source = urllib2.urlopen(req).read()


soup = bs4.BeautifulSoup(source, "html.parser")

num_range = 47

f = open("Apartments in Ghana.csv", "w")

headers = "Property name, Bed, Bath, Rent, Area, Posting date\n"
f.write(headers)

for i in range(num_range):

	i += 1

	url = "https://tonaton.com/en/ads/ghana/houses?type=for_rent&page=" + str(i)
	hdr = {'User-Agent' : "Magic Browser"}

	req = urllib2.Request(url, headers=hdr)

	source = urllib2.urlopen(req).read()

	soup = bs4.BeautifulSoup(source, "html.parser")

	Apartment = soup.find_all("div", {"class": "ui-item"})

	Apartment = Apartment[2:]

	#Lets get the data 
	for item in Apartment:

	#name of the property
		names = item.find("a", {"class" : "item-title h4"}).text

	#Bed_bath combination
		temp_holder = item.find("p", {"class": "item-meta"})
		bed_bath = ""
		if temp_holder is not None:
			bed_bath = temp_holder.text
		else:
			bed_bath = "NA"

		splitlist = bed_bath.split(",")
		Beds = splitlist[0].replace("Beds:", "")
		Baths = splitlist[-1].replace("Baths:", "")

		Rent = item.find("p", {"class": "item-info"}).text
		if "/month" in Rent:
			Rent = Rent[:-6]

		Rent = Rent[4:].replace(",", "")

		Area = item.find("span", {"class": "item-area"}).text

		Time = item.find("p", {"class": "item-location"})

		if "MEMBER" in Time.contents[0]:
			Time = Time.contents[1].text
		else:
			Time = Time.contents[0].text

		f.write(names + "," + Beds + "," + Baths + "," + Rent + "," + Area + "," + Time + "\n")

f.close()

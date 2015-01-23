import json
import folium
import time
from geopy import geocoders
g = geocoders.GeoNames(username='kmsahai')
google = geocoders.GoogleV3()
import unicodedata
import sys
j = json.load(open('C:\\Users\Chirag\Desktop\PROJECT\data\scraper.json'))
f = j.keys()
print f[0]
if raw_input("Cont?")=='n':
	sys.exit()
parsed = j[f[0]]
##print json.dumps(j['1190201723'],indent=4,sort_keys=True)
##raw_input()
Out = open('Latitute_Longitude.json','w')

a = {}
error_log = open("Error_Log.dat",'a')
skipped_log = open("Skipped_Projects.dat",'a')
counter = 0
for i in f:

	counter = counter + 1

	if(counter==150):
		Out.write(json.dumps(a))
		counter = 0

	try:
		city = j[i]["location"]["short_name"]

	except KeyError:
		error_log.write("KeyError (location) in key = " + i)
		error_log.write(json.dumps(j[i],indent=4,sort_keys=True))
		error_log.write("******************************************")
		error_log.write("******************************************")
		error_log.write("")

	else:
	
		try:
			place,(lat,lng) = g.geocode(city)
	
		except Exception as e:
	
			print "Exception is"
			print e.message
			print i

			if (e.message == 'Service timed out'):
				print "Service Timed Out"
				#Out.write(json.dumps(a))
				
				while (1):
					time.sleep(5)
					try:
						place,(lat,lng) = g.geocode(city)
					except Exception:
						print "Waiting because of Service Timeout....."
					else:
						print "(", place , "(", lat, lng,")",")"
						a[unicodedata.normalize('NFKD',i).encode('ascii','ignore')] =  {"location":place,"lat":lat,"lng":lng}
						break

						
			else:
					##The Error message on hourly/daily time outs mentions that "the hourly limit for ...."
					##so i have used that if the second character in the error message is "h" (the), the code pauses
				if (e.message[1] == 'h'):
					

					print e.message
					Out.write(json.dumps(a))
					print "Hourly Limit"
					

					while (1):
						time.sleep(300)
						try:
							place,(lat,lng) = g.geocode(city)
						except Exception:
							print "Waiting because of Max Entry Exceeded....."
						else:
							print "(", place , "(", lat, lng,")",")"
							a[unicodedata.normalize('NFKD',i).encode('ascii','ignore')] =  {"location":place,"lat":lat,"lng":lng}
							break
				else:	

					a[unicodedata.normalize('NFKD',i).encode('ascii','ignore')] =  {"location":"N/A","lat":000.0,"lng":000.0}
			
		else:
			
			try:
				print "(", place , "(", lat, lng,")",")"
			
			except Exception:

				try:

					a[unicodedata.normalize('NFKD',i).encode('ascii','ignore')] =  {"location":place,"lat":lat,"lng":lng}
	
				except Exception:

					a[unicodedata.normalize('NFKD',i).encode('ascii','ignore')] =  {"location":"N/A","lat":000.0,"lng":000.0}

			else:	

				try:

					a[unicodedata.normalize('NFKD',i).encode('ascii','ignore')] =  {"location":place,"lat":lat,"lng":lng}
	
				except Exception:

					a[unicodedata.normalize('NFKD',i).encode('ascii','ignore')] =  {"location":"N/A","lat":000.0,"lng":000.0}

	
	
#print a

print "Now Printing Final to File..."
Out.write(json.dumps(a))
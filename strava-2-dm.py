from datetime import datetime, timedelta
import os
import json
import string

d=datetime.today()-timedelta(days=1)
yest_epoch=d.strftime('%s')
print yest_epoch

#retrieve activies from strave in the last 1 day and store in file
stravacmd = "curl -G https://www.strava.com/api/v3/activities -H \"Authorization: Bearer de1c39931a3c0e7292649c576d65e1090cde9566\" -d per_page=4 -d after="+yest_epoch+" | python -m json.tool > strava-output.json"
os.system(stravacmd);

jsondata = json.loads(open('strava-output.json').read())
activity=jsondata[0]

distance_miles = str(activity["distance"]/1000/1.6)
wtype = activity["type"]
wtitle = activity["name"]
timemins=str(activity["elapsed_time"]/60.0)

description ="workout"
if "description" in activity.keys():
	description = activity["description"]

if(wtype=="Run"):
	wtype="running"
if(wtitle=="Ride"):
	wtype="cycling"

print("Distance:"+distance_miles)
print("Type:"+wtype)
print("Title:"+wtitle)
print("Time (mins):"+timemins)
print("Description:"+description)


#upload previous day activies to dailymile
dailymilecmd="curl -d \'{\"message\":\""+description+"\",\"workout\":{\"distance\":{\"value\":"+distance_miles+",\"units\":\"miles\"},\"duration\":"+timemins+",\"activity_type\":\""+wtype+"\",\"title\":\""+wtitle+"\"}}\' -H \'Content-Type: application/json\' https://api.dailymile.com/entries.json?oauth_token=6ywXQMhKWhPn2QihhbS3NdOoVnIJ59euy2vbyRwe"
os.system(dailymilecmd);

print dailymilecmd



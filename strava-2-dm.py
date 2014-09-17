from datetime import datetime, timedelta
import os
import json
import string

d=datetime.today()-timedelta(days=1)
yest_epoch=d.strftime('%s')
print yest_epoch

#retrieve activies from strave in the last 1 day and store in file
stravacmd = "curl -G https://www.strava.com/api/v3/activities -H \"Authorization: Bearer de1c39931a3c0e7292649c576d65e1090cde9566\" -d per_page=4 -d after="+yest_epoch+" | python -m json.tool > output.json"
os.system(stravacmd);

jsondata = json.loads(open('output.json').read())

for i in range(len(jsondata)):
	activity=jsondata[i]

	distance_miles = str(activity["distance"]/1000/1.6)
	wtype = activity["type"]
	wtitle = activity["name"]
	timesecs=str((activity["elapsed_time"]/60.0)*60)
	activityid=activity["id"]

	if(wtype=="Run"):
		wtype="running"
	if(wtype=="Ride"):
		wtype="cycling"

	#upload previous day activies to dailymile
	#dailymilecmd="curl -d \'{\"message\":\""+description+"\",\"workout\":{\"distance\":{\"value\":"+distance_miles+",\"units\":\"miles\"},\"duration\":"+timesecs+",\"activity_type\":\""+wtype+"\",\"title\":\""+wtitle+"\"}}\' -H \'Content-Type: application/json\' https://api.dailymile.com/entries.json?oauth_token=6ywXQMhKWhPn2QihhbS3NdOoVnIJ59euy2vbyRwe"

	stravaactivitycmd = "curl -G https://www.strava.com/api/v3/activities/"+str(activityid)+" -H \"Authorization: Bearer de1c39931a3c0e7292649c576d65e1090cde9566\" | python -m json.tool > activity_output.json"
	os.system(stravaactivitycmd);

	activity_jsondata = json.loads(open('activity_output.json').read())

	description = str("http://www.strava.com/activities/")+str(activityid)+". ";
	if activity_jsondata["description"] is not None:
		description += activity_jsondata["description"];
	

	print("Distance:"+distance_miles)
	print("Type:"+wtype)
	print("Title:"+wtitle)
	print("Time (secs):"+timesecs)
	print("Description:"+description)

	dailymilecmd="curl -d \'{\"message\":\""+description+"\",\"workout\":{\"distance\":{\"value\":"+distance_miles+",\"units\":\"miles\"},\"duration\":"+timesecs+",\"activity_type\":\""+wtype+"\",\"title\":\""+wtitle+"\"}}\' -H \'Content-Type: application/json\' https://api.dailymile.com/entries.json?oauth_token=xJB5Ztj5wMx61Nv87bhoT9J7RBzuKZRhDHn4kF75"

	os.system(dailymilecmd);
	print dailymilecmd



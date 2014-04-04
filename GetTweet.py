import urllib
import httplib
import base64
import json
import ast
import pprint as pp

CONSUMER_KEY='uGv1JwnszyrXEbvamVTXVdmff'
CONSUMER_SECRET='0Ayg2bZsLrSAWBcgXuDlAVz84PHYHYJWjN5V1v9V3s9F5zQCEH'

enc_str= base64.b64encode(CONSUMER_KEY+":"+CONSUMER_SECRET)

conn = httplib.HTTPSConnection("api.twitter.com")

#Acquiring the access token
param = urllib.urlencode({'grant_type':'client_credentials'})
headers = {"Authorization":"Basic "+enc_str,"Content-type": "application/x-www-form-urlencoded;charset=UTF-8"}
        

conn.request("POST","/oauth2/token/",param,headers)
response=conn.getresponse()
payload = response.read()

##Converting the payload string to a dictionary
dic = ast.literal_eval(payload)
#print dic

access_token = dic.get("access_token")

get_headers={"Authorization":"Bearer "+access_token}
        

#Replace ScreenName with  screen name of person to see their tweets
#Count represents the no. of tweets to retrieve
       
conn.request("GET","/1.1/statuses/user_timeline.json?screen_name=ScreenName&count=5","",get_headers)  

get_resp = conn.getresponse()
sample = get_resp.read()
#print sample

##converting the received string in JSON form 
data = json.loads(str(sample))
#print data

#Displaying Tweets

for i in range(len(data)):
    print pp.pprint(data[i]['text'])
    

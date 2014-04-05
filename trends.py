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
        
##Getting WorldWide Trends 
conn.request("GET","/1.1/trends/place.json?id=1","",get_headers)  
get_resp = conn.getresponse()
sample = get_resp.read()
        
##converting the received string in JSON form 
data = json.loads(str(sample))
names = data[0]['trends']

#Getting Tweets for Trends
conn.request("GET","/1.1/search/tweets.json?q="+str(names[0]['query']),"",get_headers)

tweets_resp = conn.getresponse()
tweets = tweets_resp.read()
tweets_json = json.loads(str(tweets))
tweet=tweets_json['statuses']

#print Tweets
for i in range(len(tweet)):
    print pp.pprint(tweet[i]['text'])
        
        

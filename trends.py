import urllib
import httplib
import base64
import json
import ast
import pprint as pp
from pymongo import MongoClient 

def insert_into_database(trendname,screenname,tweet,loc=None):
    try:       
       client = MongoClient('localhost', 27017)
       db = client.test_database
       
       screen_name = db.trends.find_one({"trend":trendname,"screenname":screenname,"tweet":tweet})
       print "%s"%screen_name
       if not(screen_name):
            if loc:
                db.trends.insert({"trend":trendname,"screenname":screenname,"tweet":tweet,"location":loc})
                print "********Gone into the database********\n\n"

       else:
            print "************Already present****************\n\n"

    except:
        print "Database Error"


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

for x in names:
    print "**********%s trending**********"%x['name']
    print "query-%s"%(x['query'])
    conn.request("GET","/1.1/search/tweets.json?q="+(x['query'])+"&count=1","",get_headers)    
    tweets_resp = conn.getresponse()
    tweets = tweets_resp.read()
    tweets_json = json.loads(str(tweets))    
    #tweet=tweets_json['statuses']        
    
    #Check if location=='None'
    for tweet in tweets_json['statuses']:
        location = str(tweet['user']['time_zone']).encode('utf-8')
        if(location=='None'):
            location=str(tweet['user']['location']).encode('utf-8')
        if(location=='None'):
            location=str(tweet['place']).encode('utf-8')

        print "**********%s tweets**********"%(tweet['user']['screen_name'])
        print "%s"%(tweet['text'])

        if(location != 'None'):
            insert_into_database(x['name'],tweet['user']['screen_name'],tweet['text'],location)




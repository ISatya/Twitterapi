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
                #print "********Gone into the database********\n"

       #else:
            #print "************Already present****************\n"

    except:
        print "Database Error"


CONSUMER_KEY='YOUR_CONSUMER_KEY'
CONSUMER_SECRET='YOUR_CONSUMER_SECRET'

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
    print "\033[95m**********%s trending**********\033[0m"%x['name']
    conn.request("GET","/1.1/search/tweets.json?q="+(x['query'])+"&count=10","",get_headers)    
    tweets_resp = conn.getresponse()
    tweets = tweets_resp.read()
    tweets_json = json.loads(str(tweets))    
    
    #Check if location=='None'
    for tweet in tweets_json['statuses']:
        location = str(tweet['user']['time_zone']).encode('utf-8')
        if(location=='None'):
            location=str(tweet['user']['location']).encode('utf-8')
        if(location=='None'):
            location=str(tweet['place']).encode('utf-8')

        print "**********%s Tweets**********"%(tweet['user']['screen_name'])
        print "\033[92m%s\033[0m"%(tweet['text'])

        if(location != 'None'):
            insert_into_database(x['name'],tweet['user']['screen_name'],tweet['text'],location)

    client = MongoClient('localhost', 27017)
    db = client.test_database
    newlist=sorted(list(db.trends.find({"trend":x['name']})),key=lambda k: k['location'])
    
    tz=''
    trend=''
    count=0;
    trending_loc=''

##Find Location with most Tweets
    for each in newlist:
        if (tz != each['location']):
            tz=each['location']
            cnt=db.trends.find({"trend":x['name'],"location":tz}).count()
            if(count<cnt):
                count=cnt
                trending_loc=tz
                             
            #print "\n\033[92mNo of users talking about %s from %s=%d\033[0m\n"%(x['name'],tz,cnt)
    
    print "\033[93m*******Most Tweets about %s from %s*******\n\033[0m"%(x['name'],trending_loc)


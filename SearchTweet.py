import urllib
import httplib
import base64
import json
import ast
import pprint as pp
from sys import argv

#Taking query from user
script,query = argv

CONSUMER_KEY='Your_Consumer_key'
CONSUMER_SECRET='Your_Consumer_Secret'

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
        
#Search Query
#query='#michael schumacher'

#URL encoded Query
enc_query=urllib.quote_plus(query)

conn.request("GET","/1.1/search/tweets.json?q="+enc_query+"&result_type=recent&count=5","",get_headers)  

get_resp = conn.getresponse()
sample = get_resp.read()
#print sample

#converting the received string in JSON form 
data = json.loads(str(sample))

#print pp.pprint(data['statuses'])

#Displaying Tweets
for i in range(len(data['statuses'])):
    print pp.pprint(data['statuses'][i]['text'])


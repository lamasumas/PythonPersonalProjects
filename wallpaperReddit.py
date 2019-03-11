import praw
import requests 
import urllib3
import pickle 
from requests.packages.urllib3.exceptions import InsecureRequestWarning



##This will download a picture from a url##
def download(theUrls):
    
    urlSplitted = theUrls.split(".")
    formatFile = urlSplitted[len(urlSplitted)-1] 
    name = urlSplitted[2].split("/")[1]
    f = open("Wallpaper/"+name+'.'+formatFile, 'w')

    f.write(requests.get(theUrls).content)
    f.close()

##This will parse the html searching for the valid url##
def parseInfo(element):
    t = []
    urls = []
    x = str(element)
    y = x.split('href="')
    for z in y:
        img = z.split('"')
        t.append(img[0])
    for i in t:
        if i.startswith("https://i.redd."):
            return i 

##........................MAIN_FUNCTION............................##
##This is form not downloading all the pictures again, persistance ##
try:
    listOfFiles = pickle.load(open("url.p","r"))
except :
    listOfFiles = []

print len(listOfFiles)
##For downloading the html file, initializiate the basic libraries##
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

## This part is for downloading the saved post with the Reddit api ##
Reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                     client_secret='YOUR_CLIENT_SECRE',
                     password='YOUR_USER_PASSWORD',
                     user_agent='YOUR_USER_AGENT',
                     username='YOUR_USER_NAME')
savedPost = Reddit.redditor('YOUR_USER_NAME').saved(limit=100)

##Download the html of each saved post ##
for x in savedPost:
    savedPostUrl = "https://www.reddit.com/"+str(x)
    if savedPostUrl in listOfFiles:
        ## This means that is allready up-to-date##
        break
    else:
        ## New post ##
        listOfFiles.append(savedPostUrl)    
        theData = http.request('GET',savedPostUrl).data 
    
        if theData not in listOfFiles:
            url = parseInfo(theData)
            ## This for skipping the error if it appear ##
            if type(url) is str :
                print url
                download(url)

## Serialization of the url list, for next download ##
pickle.dump(listOfFiles, open("url.p","w"))


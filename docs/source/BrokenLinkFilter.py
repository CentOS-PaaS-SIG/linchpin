import re
import glob, os
import requests
files=[]
texts= []
urls= []
print("We are scanning all the links! Please wait...")
os.chdir("./")
for file in glob.glob("*.rst"):
    files.append(open(file, "r+"))

for file in files:
    texts.append(file.read())

for text in texts:
    url= re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    urls=urls + url

brokenLinks=[]

count = 0
total = len(urls)
for url in urls:
    count+=1
    ret=0
    # url=url[0:len(url)-1]
    url = url.replace(">","")
    finish = float(count)/float(total)*100
    print("finished:"+" "+str(finish)[0:4]+"%")
    try:
        request = requests.get(url,timeout=3)
    except:
        ret = 999
    if ret != 999:
        ret = request.status_code
    if ret != 200:
        brokenLinks.append(url)

for link in brokenLinks:
    open("Deprecated_Link.txt","a").write(link+"\n")

print("Finished scanning! The deprecated links are in Deprecated_Link.txt")
import json
import requests
from tabulate import tabulate

url = "https://communities.win/api/v2/post/newv2.json?community=technology"
global sheet
sheet = [["uuid", "title", "author", "comments", "lastcomment", "lca"]]

def appendsheet(items,status):
    if status != "first":
        itemlist = items
    else:
        itemlist = items[1:]
    for x in itemlist:
        #print(x['title'])
        uuid = x['uuid']
        title = x['title']
        author = x['author']
        comments = x['comments']
        lastcomment = x['last_comment_created']
        lca = x['last_comment_author']
        sheet.append([uuid, title, author, comments, lastcomment, lca])

def uuid_iteration(uposts):
    fpost = uposts[0]['uuid']
    lpost = uposts[-1]['uuid']
    print(lpost)
    while lpost != fpost:
        iurl = f"{url}&from={lpost}"
        print(iurl)
        irequest = requests.get(iurl)
        idata = irequest.json()
        iposts = idata["posts"]
        print(iposts[-1]['uuid'])
        fpost = iposts[0]['uuid']
        lpost = iposts[-1]['uuid']
        if fpost == lpost:
            break
        appendsheet(iposts,"i")
    return posts

request = requests.get(url)
data = request.json()
posts = data["posts"]
appendsheet(posts,"f")
 
uuid_iteration(posts)

print(tabulate(sheet))
print(len(sheet))

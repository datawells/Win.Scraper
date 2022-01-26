import json
import requests
from tabulate import tabulate
import numpy as np

url = "https://communities.win/api/v2/post/newv2.json?community=technology"
global file
file = "D:\stuff2.txt"
sheet = [["id", "title", "author", "comments", "lastcomment", "lca"]]

def appenddict(aposts,items):
    itemlist = items[1:]
    for x in itemlist:
        posts.append(x)

def formsheet(postlist):
    a_file = open(file, "w")
    json.dump(postlist,a_file)
    a_file.close()
    for x in postlist:
        print(x['title'])
        id = x['id']
        title = x['title']
        author = x['author']
        comments = x['comments']
        lastcomment = x['last_comment_created']
        lca = x['last_comment_author']
        sheet.append([id, title, author, comments, lastcomment, lca])
    return sheet        

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
        appenddict(posts,iposts)

request = requests.get(url)
data = request.json()
global posts
posts = data["posts"]
 
uuid_iteration(posts)

formsheet(posts)
print(tabulate(sheet))
print(len(sheet))

import json
import requests
import mysql.connector
from tabulate import tabulate
import numpy as np

mydb = mysql.connector.connect(
  host="127.0.0.1",
  port="3306",
  user="test",
  password="test_pass",
  database="test_db",
  auth_plugin="mysql_native_password")

cursor = mydb.cursor(buffered=True)

#values for community lookup
community = "technology"
phase1 = f"https://communities.win/api/v2/post/newv2.json?community={community}"

#populate community / retrieve community ID
cursor.execute("SELECT id FROM communities WHERE community = %s", (community,))
cids = cursor.fetchone()

if cids==None:
    try:
        insert = "INSERT INTO communities (id, community) VALUES (%s, %s)"
        ival = ("0", community)
        cursor.execute(insert, ival)
        mydb.commit()
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    cursor.execute("SELECT id FROM communities WHERE community = %s", (community,))
    cids = cursor.fetchone()
for cid in cids:
    print(cid)
    cid = cid

global file
file = "D:\stuff2.txt"
sheet = [["id", "title", "author", "comments", "lastcomment", "lca"]]

#append posts - aposts not used
def appenddict(aposts,items):
    itemlist = items[1:]
    for x in itemlist:
        posts.append(x)

#inserts posts into DB
def insertposts(postlist):
    a_file = open(file, "w")
    json.dump(postlist,a_file)
    a_file.close()
    for x in postlist:
        #print(x['title'])

        x['author'] = useridlookup(x['author'])
        if x['last_comment_author']:
            x['last_comment_author'] = useridlookup(x['last_comment_author'])
        else:
            #TO DO seed null user on table creation
            x['last_comment_author'] = "26"
        try:
            c = len(x)
            s = "%s, " * c
            s = s.rstrip(', ')
            for v in x:
                if x[v]==None:
                    x[v] = "NULL"
            insert = f"INSERT INTO posts (id, uuid, preview, is_locked, is_twitter, tweet_id, sticky_comment, link, domain, author_flair_class, is_video_mp4, is_removed, title, type, content, score_up, score_down, score, author_flair_text, is_admin, suggested_sort, is_stickied, is_nsfw, post_flair_class, is_deleted, is_image, comments, author, created, is_edited, community, is_moderator, last_comment_author, last_comment_created, is_video, video_link, is_new_user, vote_state, post_flair_text, is_crosspost) VALUES ({s})"
            ival = (x['id'], x['uuid'], x['preview'], int(x['is_locked']), x['is_twitter'], x['tweet_id'], x['sticky_comment'], x['link'], x['domain'], x['author_flair_class'], int(x['is_video_mp4']), int(x['is_removed']), x['title'], x['type'], x['content'], x['score_up'], x['score_down'], x['score'], x['author_flair_text'], int(x['is_admin']), x['suggested_sort'], int(x['is_stickied']), int(x['is_nsfw']), x['post_flair_class'], int(x['is_deleted']), int(x['is_image']), x['comments'], x['author'], x['created'], int(x['is_edited']), cid, int(x['is_moderator']), x['last_comment_author'], x['last_comment_created'], int(x['is_video']), x['video_link'], int(x['is_new_user']), x['vote_state'], x['post_flair_text'], x['is_crosspost'])
            cursor.execute(insert, ival)
            mydb.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
    # return sheet        

#aggregates posts by loading json files and removing the duplicate
def uuid_iteration(uposts):
    fpost = uposts[0]['uuid']
    lpost = uposts[-1]['uuid']
    print(lpost)
    while lpost != fpost:
        iurl = f"{phase1}&from={lpost}"
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

#populate user / search lookup ID
def useridlookup(user):
    cursor.execute("SELECT id FROM users WHERE user = %s", (user,))
    r = cursor.fetchone()
    if r==None:
        try:
            insert = "INSERT INTO users (id, user, community) VALUES (%s, %s, %s)"
            ival = ("0", user, cid)
            cursor.execute(insert, ival)
            mydb.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        cursor.execute("SELECT id FROM users WHERE user = %s", (user,))
        r = cursor.fetchone()
    for f in r:
        id = f
    return id

request = requests.get(phase1)
data = request.json()
global posts
posts = data["posts"]

#Disable for testing. 
#uuid_iteration(posts)

insertposts(posts)
#print(tabulate(sheet))
print(len(sheet))

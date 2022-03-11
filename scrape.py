import json
from types import ClassMethodDescriptorType
import requests
import configparser
import mysql.connector
import os

def main():
    """Initiates variables and MySQL connection."""
    global config
    config = configparser.ConfigParser()
    dir = os.path.dirname(os.path.realpath(__file__))
    global CONFIGFILE
    CONFIGFILE = os.path.join(dir, 'config.ini')
    config.read(CONFIGFILE)
    global MYDB
    try:
        MYDB = mysql.connector.connect(
        host=config['Database']['host'],
        port=config['Database']['port'],
        user=config['Database']['user'],
        password=config['Database']['password'],
        database=config['Database']['db'],
        auth_plugin=config['Database']['auth_plugin'])
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
        quit()
    global cursor
    cursor = MYDB.cursor(buffered=True)

    #values for community lookup
    global COMMUNITY
    COMMUNITY = config['Community']['community1']
    global phase1
    phase1 = f"https://communities.win/api/v2/post/newv2.json?community={COMMUNITY}"

    #populate community / retrieve community ID
    cursor.execute("SELECT id FROM communities WHERE community = %s", (COMMUNITY,))
    CIDS = cursor.fetchone()
    if CIDS is None:
        try:
            insert = "INSERT INTO communities (id, community) VALUES (%s, %s)"
            ival = ("0", COMMUNITY)
            cursor.execute(insert, ival)
            MYDB.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        cursor.execute("SELECT id FROM communities WHERE community = %s", (COMMUNITY,))
        CIDS = cursor.fetchone()
    global cid
    cid = (CIDS[0])
    print(cid)

class Posts:
    """Generates a list of posts from the selected community using pull_list or pull_missing.
    The list can then be used to populate MySQL server using insertposts."""
    def __init__(self, plist, title):
        request = requests.get(plist)
        data = request.json()
        self.posts = data["posts"]
        fpost = self.posts[0]['uuid']
        lpost = self.posts[-1]['uuid']
        print(lpost)
        while lpost != fpost:
            #stops iteration on duplicate, but could be changed out for updating records
            cursor.execute("SELECT uuid FROM posts WHERE uuid = %s", (lpost,))
            pid = cursor.fetchone()
            if pid==None:
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
                self.posts.extend(iposts[1:])
            else:
                break
        if title != False:
            self.posts[0]['title'] = title

    
    @classmethod
    def pull_list(cls, plist, title):
        return cls(plist, False)

    @classmethod
    def pull_missing(cls, plist, title):
        return cls(plist, title)    

    #inserts posts into DB
    def insertposts(self):
        if self.posts!=None:
            for x in self.posts:
                #print(x['title'])
                cursor.execute("SELECT id FROM posts WHERE id = %s", (x['id'],))
                pid = cursor.fetchone()
                if pid is None:
                    x['author'] = useridlookup(x['author'])
                    try:
                        #length changes if crosspost
                        #c = len(x)
                        c = int('39')
                        s = "%s, " * c
                        s = s.rstrip(', ')
                        if "crosspost_uuid" in x.keys():
                            xpid = x['crosspost_uuid']
                        else:
                            xpid = ""
                        insert = f"INSERT INTO posts (id, uuid, preview, is_locked, is_twitter, tweet_id, sticky_comment, link, domain, author_flair_class, is_video_mp4, is_removed, title, type, content, score_up, score_down, score, author_flair_text, is_admin, suggested_sort, is_stickied, is_nsfw, post_flair_class, is_deleted, is_image, comments, author, created, is_edited, community, is_moderator, is_video, video_link, is_new_user, vote_state, post_flair_text, crosspost_uuid, is_crosspost) VALUES ({s})"
                        ival = (x['id'], x['uuid'], x['preview'], int(x['is_locked']), int(x['is_twitter']), x['tweet_id'], x['sticky_comment'], x['link'], x['domain'], x['author_flair_class'], int(x['is_video_mp4']), int(x['is_removed']), x['title'], x['type'], x['content'], x['score_up'], x['score_down'], x['score'], x['author_flair_text'], int(x['is_admin']), x['suggested_sort'], int(x['is_stickied']), int(x['is_nsfw']), x['post_flair_class'], int(x['is_deleted']), int(x['is_image']), x['comments'], x['author'], x['created'], int(x['is_edited']), cid, int(x['is_moderator']), int(x['is_video']), x['video_link'], int(x['is_new_user']), x['vote_state'], x['post_flair_text'], xpid, int(x['is_crosspost']))
                        cursor.execute(insert, ival)
                        MYDB.commit()
                    except mysql.connector.Error as error:
                        print(x)
                        print("Failed to insert into MySQL table {}".format(error))
                        break
   

class Comments:
    """Generates a list of comments from the selected community.
    The list can then be used to populate MySQL server using insertcomms.
    
    The first run will pull all comments from all posts. This can be forced using the comment flat in config.ini"""
    def __init__ (self):
        if config['Flags']['comments']=="false":
                cursor.execute("SELECT id,comments FROM posts")
                pid = cursor.fetchall()
                i = True
                for p in (y for y in pid if y[1] > 0):
                    
                    phase2 = f"https://communities.win/api/v2/post/post.json?id={p[0]}&commentSort=top&comments=true"
                    print(phase2)
                    crequest = requests.get(phase2)
                    cdata = crequest.json()
                    if i == True:
                        self.clist = cdata["comments"]
                    else: 
                        self.clist.extend(cdata["comments"])
                    i = False
                config.set('Flags','comments','true')
                config.write(open(CONFIGFILE, "w"))    
        else:    
            p = 1
            phase2 = f"https://communities.win/api/v2/comment/community.json?community={COMMUNITY}&page={p}"
            print(phase2)
            crequest = requests.get(phase2)
            cdata = crequest.json()
            
            comms = cdata["comments"]
            lcom = comms[-1]['id']
            while p < 100:
                print(lcom)
                cursor.execute("SELECT id FROM comments WHERE id = %s", (lcom,))
                comid = cursor.fetchone()
                if comid is None:
                    p += 1
                    phase2 = f"https://communities.win/api/v2/comment/community.json?community={COMMUNITY}&page={p}"
                    print(phase2)
                    crequest = requests.get(phase2)
                    cdata = crequest.json()
                    icomms = cdata["comments"]
                    comms.extend(icomms[1:])
                    lcom = icomms[-1]['id']
                else:
                    break
            self.clist = comms
    def insertcomms(self):        
        def commsearch(var):
            cursor.execute("SELECT id FROM comments WHERE id = %s", (var['id'],))
            pid = cursor.fetchone()
            return pid
        #list comprehension to recreate list without duplicate entries
        cproclist = [c for c in self.clist if commsearch(c) == None]
        print('writing comments to db')
        for x in reversed(cproclist):
            x['author'] = useridlookup(x['author'])
            for _ in range(2):
                try:
                    #length changes if crosspost
                    #c = len(x)
                    clen = int('19')
                    s = "%s, " * clen
                    s = s.rstrip(', ')
                    insert = f"INSERT INTO comments (id, uuid, parent_id, is_removed, content, score_up, score_down, score, is_admin, is_stickied, is_deleted, author, created, comment_parent_id, is_edited, community, is_moderator, is_new_user, vote_state) VALUES ({s})"
                    ival = (x['id'], x['uuid'], x['parent_id'], int(x['is_removed']), x['content'], x['score_up'], x['score_down'], x['score'], int(x['is_admin']), int(x['is_stickied']), int(x['is_deleted']), x['author'], x['created'], x['comment_parent_id'], int(x['is_edited']), cid, int(x['is_moderator']), int(x['is_new_user']), x['vote_state'])
                    cursor.execute(insert, ival)
                    MYDB.commit()
                except mysql.connector.Error as error:
                    print(x)
                    print("Failed to insert into MySQL table {}".format(error))
                    if error.errno == 1452:
                        mp = f"https://communities.win/api/v2/post/post.json?id={x['parent_id']}"
                        print(mp)
                        missingp = Posts.pull_missing(mp, x['post_title'])
                        missingp.insertposts()
                        continue
                    else:
                        break
                break
#populate user / search lookup ID
def useridlookup(user):
    cursor.execute("SELECT id FROM users WHERE user = %s", (user,))
    r = cursor.fetchone()
    if r is None:
        try:
            insert = "INSERT INTO users (id, user, community) VALUES (%s, %s, %s)"
            ival = ("0", user, cid)
            cursor.execute(insert, ival)
            MYDB.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        cursor.execute("SELECT id FROM users WHERE user = %s", (user,))
        r = cursor.fetchone()
    return r[0]

if __name__ == '__main__':
    main()

    plist = Posts.pull_list(phase1, False)
    plist.insertposts()
    
    clist = Comments()
    clist.insertcomms()

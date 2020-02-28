import requests
import praw
import time

gfycat_api = 'https://api.gfycat.com/v1/gfycats/'

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     password='',
                     user_agent='gfycat by /u/DevouringOne and /u/jadenx2',
                     username='NBA_MOD')

subreddit = reddit.subreddit('nba_mods')

for submission in subreddit.stream.submissions(skip_existing=True):
    if 'streamable' in submission.url:
        title = submission.title

        data = {'fetchUrl': submission.url, 'title': title}
        response = requests.post(gfycat_api, data=str(data).encode('utf-8'))  # This line is where the gfycat is created

        gfyname = response.json()['gfyname']

        is_ready = requests.get(gfycat_api + gfyname)

        while is_ready.status_code is not 200:
            time.sleep(15)
            is_ready = requests.get(gfycat_api + gfyname)
            print("Trying again... response code: {}".format(is_ready.status_code))

        print("Response code: {} - gfycat mirror is ready".format(is_ready.status_code))

        reply = "Here is a [Gfycat mirror of this Streamable link](https://gfycat.com/{0})".format(gfyname)

        for comment in submission.comments:
            if comment.stickied and comment.author == 'NBA_MOD':
                mirror = comment.reply(reply)
                mirror.mod.distinguish()
                print("Mirror posted")

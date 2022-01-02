from discord.ext import tasks

import config
import discord
import requests


subreddit = 'gamedeals'
limit = 5
timeframe = 'month'         # hour, day, week, month, year, all
listing = 'hot'             # controversial, best, hot, new, random, rising, top


def get_listings(subreddit, listing, limit, timeframe):
    try:
        base_url = f'http://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers={'User-agent': 'yourbot'})
    except:
        print('An error occurred fetching listings.')
    return request.json()


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.posts = []
        self.fetch_posts.start()

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(client))

    @tasks.loop(seconds=10)
    async def fetch_posts(self):
        await self.wait_until_ready()
        channel = self.get_channel(797616940390154294)
        self.posts = []
        r = get_listings(subreddit, listing, limit, timeframe)
        for post in r['data']['children']:
            x = post['data']['title']
            self.posts.append(x)
        await channel.send(self.posts)

client = MyClient()
client.run('bot-token')

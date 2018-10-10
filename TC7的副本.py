#https://dev.to/rodolfoferro/sentiment-analysis-on-trumpss-tweets-using-python-
 #不报错。抓粉丝数和粉丝列表，数据存下来，可视化
#General:2.7
import tweepy           # To consume Twitter's API
import pandas as pd     # To handle data
import numpy as np      # For number computing

from IPython.display import display
#% matplotlib inline

#import matplotlib.pyplot as plt
#import seaborn as sns


CONSUMER_KEY    = '4RRwA0SjreJc2Hcjfywyt46se'
CONSUMER_SECRET = 'eYbSNu71fCBQtSW7yY1U1SLoJ5kIWG8CR0hXTQ5HQpLBCQOtqg'

ACCESS_TOKEN  = '840983112297279488-p2NH5UsN3lD9TGwxaPQsK9brZpXztUV'
ACCESS_SECRET = 'wanV0J02UxKn0xgoqBzQKuv4I1TmHmb4Xdx7GTq0zeyiB'

from credentials import *    # This will allow us to use the keys as variables

def twitter_setup():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

extractor = twitter_setup()

tweets = extractor.user_timeline(screen_name="realDonaldTrump", count=200)
print("Number of tweets extracted: {}.\n".format(len(tweets)))

print("5 recent tweets:\n")
for tweet in tweets[:5]:
    print(tweet.text)
    print()

data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

display(data.head(10))

print(dir(tweets[0]))

print(tweets[0].id)
print(tweets[0].created_at)
print(tweets[0].source)
print(tweets[0].favorite_count)
print(tweets[0].retweet_count)
print(tweets[0].geo)
print(tweets[0].coordinates)
print(tweets[0].entities)
#print(tweets[0].followers)

data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
#data['followers'] = np.array([tweets.followers for tweet in tweets])
display(data.head(10))

mean = np.mean(data['len'])

print("The lenght's average in tweets: {}".format(mean))


fav_max = np.max(data['Likes'])
rt_max  = np.max(data['RTs'])

fav = data[data.Likes == fav_max].index[0]
rt  = data[data.RTs == rt_max].index[0]


print("The tweet with more likes is: \n{}".format(data['Tweets'][fav]))
print("Number of likes: {}".format(fav_max))
print("{} characters.\n".format(data['len'][fav]))

print("The tweet with more retweets is: \n{}".format(data['Tweets'][rt]))
print("Number of retweets: {}".format(rt_max))
print("{} characters.\n".format(data['len'][rt]))


tlen = pd.Series(data=data['len'].values, index=data['Date'])
tfav = pd.Series(data=data['Likes'].values, index=data['Date'])
tret = pd.Series(data=data['RTs'].values, index=data['Date'])

#fig = plt.plot()
#tlen.plot(figsize=(16,4), color='r');

#h = tlen.plot(figsize=(16,4), color='r');
#h.savefig('picture', dpi=200)

tfav.plot(figsize=(16,4), label="Likes", legend=True)
tret.plot(figsize=(16,4), label="Retweets", legend=True);
#h = tfav.plot(figsize=(16,4), label="Likes", legend=True)
#i = tret.plot(figsize=(16,4), label="Retweets", legend=True);
#h.savefig('avd')



sources = []
for source in data['Source']:
    if source not in sources:
        sources.append(source)

print("Creation of content sources:")
for source in sources:
    print("* {}".format(source))


percent = np.zeros(len(sources))

for source in data['Source']:
    for index in range(len(sources)):
        if source == sources[index]:
            percent[index] += 1
            pass

percent /= 100

pie_chart = pd.Series(percent, index=sources, name='Sources')
pie_chart.plot.pie(fontsize=11, autopct='%.2f', figsize=(6, 6));




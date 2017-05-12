import config
import tweepy
import csv
import time

auth = tweepy.OAuthHandler(config.twitterConfig.twitterConsKey, config.twitterConfig.twitterConsSec)
auth.set_access_token(config.twitterConfig.twitterToken, config.twitterConfig.twitterTokenSec)

api = tweepy.API(auth)

csvFile = open('output.csv', 'a', encoding='utf8')
csvWriter = csv.writer(csvFile)

cursor = tweepy.Cursor(api.search,
                       q=config.query,
                       count=100,
                       result_type="recent",
                       lang="en")

for page in cursor.pages(100):
    for tweet in page:
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            csvWriter.writerow(["https://twitter.com/" + tweet.user.screen_name,
                                tweet.text])
            csvFile.flush()
            time.sleep(1)

csvFile.close()

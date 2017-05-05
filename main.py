import config
import tweepy
import csv
import time

auth = tweepy.OAuthHandler(config.twitterConsKey, config.twitterConsSec)
auth.set_access_token(config.twitterToken, config.twitterTokenSec)

api = tweepy.API(auth)

csvFile = open('output.csv', 'a')
csvWriter = csv.writer(csvFile)

cursor = tweepy.Cursor(api.search,
                       q=config.startKeyword,
                       count=100,
                       result_type="recent",
                       lang="en")


for page in cursor.pages(1):
    for tweet in page:
        userTweetsCursor = tweepy.Cursor(api.search,
                               q="from:" + tweet.user.name,
                               count=100,
                               result_type="recent",
                               lang="en")

        score = 0
        words = ""
        print(tweet.user.name)
        for userPage in userTweetsCursor.pages(1):
            for userTweet in userPage:
                if not userTweet.retweeted and 'RT @' not in userTweet.text:
                    for keyword in config.keywords:
                        count = tweet.text.lower().count(keyword)
                        if (count > 0):
                            words += ", " + keyword
                        score += tweet.text.lower().count(keyword)

        csvWriter.writerow([tweet.user.screen_name.encode('utf8'), "score: " + str(score), "words: " + words])
        time.sleep(10)

csvFile.close()
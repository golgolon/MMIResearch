import config
import tweepy
import csv

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


for page in cursor.pages(1000):
    for tweet in page:
        userTweetsCursor = tweepy.Cursor(api.search,
                               q="from:" + tweet.user.name,
                               count=100,
                               result_type="recent",
                               lang="en")

        score = 0
        print(tweet.user.name)

        for userPage in userTweetsCursor.pages(1000):
            for userTweet in userPage:
                for keyword in config.keywords:
                    score += tweet.text.lower().count(keyword)

        csvWriter.writerow([tweet.user.name.encode('utf8'), "score: " + str(score)])

csvFile.close()
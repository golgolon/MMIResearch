import config
import tweepy
import csv

auth = tweepy.OAuthHandler(config.twitterConsKey, config.twitterConsSec)
auth.set_access_token(config.twitterToken, config.twitterTokenSec)

api = tweepy.API(auth)

csvFile = open('output.csv', 'a')
csvWriter = csv.writer(csvFile)

cursor = tweepy.Cursor(api.search,
                       q=" OR ".join(config.keywords),
                       count=100,
                       result_type="recent",
                       lang="en")

for page in cursor.pages():
    for tweet in page:
        csvWriter.writerow([tweet.created_at, tweet.user.screen_name.encode('utf8'), tweet.text.encode('utf-8')])

csvFile.close()
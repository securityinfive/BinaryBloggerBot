import tweepy
import csv
import requests
import datetime
import logging
from time import sleep
from datetime import date, time
from creds import *

# Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Text Message Via Email
def send_email_textmessage(date_now, quote, author):
    #print("text")
    return requests.post("<your mailgun sandbox URL>",
                      auth=("api", "<mailgun API token>"),
                      data={"from": "<some email address>",
                            "to": "<email address>",
                            "subject": "Tweeted",
                            "text": date_now + ": " + quote + " - " + author})

csvfile = ""
# Enter path to CSV file of quotes
with open('<CSV location>') as csvfile:
    time_now = datetime.datetime.now()
    quote_getter = csv.DictReader(csvfile)
    posts = []
    date_today = date.today()
    date_today = date_today.strftime("%m/%d/%Y")
    for row in quote_getter:
        if row['POSTDATE'] == date_today:
            posts.append(row)
    
    csvfile.close()

for post in posts:
    tweet = post['QUOTE'] + " - " + post['AUTHOR'] + " #QuoteOfTheDay"
    if int(len(tweet)) <= 240:
        try:
            api.update_status(tweet) # post the tweet
            send_email_textmessage(str(time_now), post['QUOTE'], post['AUTHOR'])
        except:
            send_email_textmessage(str(time_now), "Bot ran, no tweet.", "Exception.")
            pass
    else:
        send_email_textmessage(str(time_now), "Tweet was too long, not updated.", " - ")
    
    sleep(3600) #If multiple quotes, wait an hour between posts

exit()

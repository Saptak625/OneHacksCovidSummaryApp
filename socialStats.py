import tweepy
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from wordcloud import WordCloud, STOPWORDS
matplotlib.use('Agg')

def getSocialStats():
    plt.style.use('fivethirtyeight')

    consumer_key = "q9ZAAGzvkOwhBwCCwj95EjV6p"
    consumer_secret = "45hffFWt9cPEHN3QWEPOzh4Kc3KKm3lazYMgRXPFYVRlPr1Bmt"
    access_token = "1378411001218002950-Lpz0TWyrx0vt5s3hx3CdgJAkYayCDH"
    access_token_secret = "692hLljgmLOEJwNV3fCQ1xrYzoWxg7cd3gmB3XMXnmb3L"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    user = api.me()
    print(user.name)

    tweets = []

    for page in range(1,5):
        tweets.extend(api.user_timeline(screen_name="V2019N", count=200, page=page))

    print("Number of tweets extracted: {}. \n".format(len(tweets)))

    for tweet in tweets[:5]:
        print(tweet.text)

    own_tweets = [tweet for tweet in tweets if tweet.retweeted == False and "RT @" not in tweet.text]

    df = pd.DataFrame(data=[[tweet.created_at, tweet.text, len(tweet.text), tweet.id, tweet.favorite_count, tweet.retweet_count] for tweet in own_tweets], columns=['Date', 'Tweet', 'Length', 'ID', 'Likes', 'Retweets'])

    nltk.download('vader_lexicon')
    vader = SentimentIntensityAnalyzer()
    f = lambda tweet: vader.polarity_scores(tweet)['compound']
    df['Sentiment'] = df['Tweet'].apply(f)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df.head()

    df['Sentiment'].plot(kind='hist', bins=20, figsize=(5,5), ec='black')
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    plt.title('Sentiment of Tweets by Covid-19')
    #plt.savefig('static/SentimentOfTweets.png')

    date_df = df.groupby(['Date']).mean().reset_index()

    date_df.plot(kind='line', x='Date', y='Sentiment', figsize=(15,15), ylim=[-1,1])
    plt.axhline(y=0, color='black')
    plt.ylabel('Average Sentiment')
    plt.title('Daily Average Sentiment of Tweets')
    plt.savefig('static/AverageSentiment.png')

    text = " ".join(text for text in df.Tweet)

    stopwords = set(STOPWORDS)
    stopwords.update(["HTTPS", "CO"])

    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    #plt.savefig('static/wordcloud.png')

    return [i.text for i in own_tweets if len(i.text.split(' ')) > 15][:5]
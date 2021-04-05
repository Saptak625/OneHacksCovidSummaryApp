from flask import Flask, redirect, request, url_for, render_template, abort, session, flash
from socialStats import getSocialStats
from covidStats import getCovidVisualization, getMLPrediction
from covidNewsWebScrapers import getBBCLink, getCNNLink, bbcExtractor, cnnExtractor
import codecs
import requests
from bs4 import BeautifulSoup
import lxml

# Flask app setup
app = Flask(__name__)
# app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'

@app.route("/")
@app.route("/homepage")
def home():
    cnnNews = cnnExtractor()
    current_news = bbcExtractor()[:3] + [i for i in cnnNews if i[-1] != None][:3]
    cdcData = [['TOTAL CASES TODAY:', 67989], ['7-DAY CASE RATE PER 100,000:', 134.9], ['TOTAL DEATHS:', 789]]
    return render_template('homepage.html', current_news=current_news, trends=cdcData)

@app.route("/news")
def news():
    return render_template('news.html', bbcNews=bbcExtractor(), cnnNews=cnnExtractor(), bbcLink=getBBCLink(),
                           cnnLink=getCNNLink())

@app.route("/covidstats")
def covidStats():
    getCovidVisualization()
    getMLPrediction()
    return render_template('covidstats.html')

@app.route("/socialstats")
def socialStats():
    tweets = getSocialStats()
    print(tweets)
    return render_template('socialstats.html', tweets=tweets)

if __name__ == "__main__":
    #Development only
    app.run(debug=True)
    #Production only
    # app.run(host = '0.0.0.0', ssl_context="adhoc")
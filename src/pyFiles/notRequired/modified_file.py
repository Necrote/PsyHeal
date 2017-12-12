import webbrowser
import os
from os.path import join, dirname,abspath
import json
import sys
import codecs
import csv

from bs4 import BeautifulSoup
from selenium import webdriver
import tweepy
from watson_developer_cloud import PersonalityInsightsV2


personality_insights = PersonalityInsightsV2(
    username='',
    password='',url='https://gateway-fra.watsonplatform.net/personality-insights/api')

if __name__ == '__main__':
   

    filepath=join('./sunburst-chart-master/examples/profiles','personality_analysis.json')
    chartpath=join('./sunburst-chart-master/examples','example_v2.html')
    #print(filepath)
    f=open(filepath,'w+')
    with open(join(dirname(__file__), './my_tweets.csv.txt')) as \
    personality_text:
     json.dump(personality_insights.profile(text=personality_text.read()), f)
    driver = webdriver.Chrome() #I actually used the chromedriver and did not test firefox, but it should work.
    firefox_path="C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
    webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path),1)
    webbrowser.get('firefox').open_new_tab(chartpath)
    #summary=soup.find('section', { "id" : "experience" })
    #print(summary.getText().encode('utf-8'))
    f.close();
    
    #get tweets for username passed at command line
   

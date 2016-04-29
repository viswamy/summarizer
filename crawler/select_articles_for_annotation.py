__author__ = 'swvenu'
#This program selects articles to be used for manual annotation of summaries
#The current plan is to consider articles with number of paragraphs >= 8 and limit to 100 articles

import json
import math
import os.path
import sys

def processArticles(fileName):
    articles = json.load(open(fileName, 'r'))
    res = []
    articleLength = 7
    numberOfArticles = 100
    i = 0
    j = 0
    while i < numberOfArticles and j < len(articles):
        if len(articles[j]["content"]) >= articleLength:
            res.append(articles[j])
            i += 1
        j += 1
    with open("../annotator/"+fileName, 'w') as outfile:
        json.dump(res, outfile)

processArticles("udayavani_cinema_news.json")
#processArticles("udayavani_sports_news.json")
#processArticles("udayavani_state_news.json")
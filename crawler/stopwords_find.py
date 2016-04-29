__author__ = 'swvenu'
#This program tries to find stopwaords in kannada

import json

def processArticles(fileNames):
    res = {}
    for fileName in fileNames:
        articles = json.load(open(fileName, 'r'))

        i = 0
        while i < len(articles):
            for sentence in articles[i]['content']:
                words = sentence.split()
                for word in words:
                    if word in res:
                        res[word] += 1
                    else:
                        res[word] = 1
            i += 1

    out = sorted(res, key=res.get, reverse=True);
    with open("stopword.json", 'w') as outfile:
        json.dump(out[1:300], outfile)

processArticles(["udayavani_cinema_news.json","udayavani_sports_news.json", "udayavani_state_news.json"])


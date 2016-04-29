from __future__ import division, unicode_literals
from textblob import TextBlob as tb
import json
import sys
import os
import math
reload(sys)
sys.setdefaultencoding('utf-8')
import pickle


# class gss:
def findValue(state,cinema,sports):
    stateNews = json.load(open(state,'r'))
    cinemaNews = json.load(open(cinema, 'r'))
    sportsNews = json.load(open(sports, 'r'))
    results = "output.txt"
    allDicts = "allDicts.txt"
    if not os.path.exists(results):
        os.makedirs(results)
    cinemaWordDict = createDict(cinemaNews)
    stateWordDict = createDict(stateNews)
    sportsWordsDict = createDict(sportsNews)
    lenDict = {}
    lenDict["lengthCinema"] = len(cinemaNews)
    lenDict["lengthState"] = len(stateNews)
    lenDict["lengthSports"] = len(sportsNews)
    setAllWords = buildCorpus(cinemaWordDict,stateWordDict,sportsWordsDict)
    gssDict = gss(setAllWords , cinemaWordDict ,len(cinemaNews), stateWordDict ,len(stateNews),sportsWordsDict,len(sportsNews))

    pickle.dump(gssDict , open(results,'w+'))

    finalDict = []
    finalDict.append(cinemaWordDict)
    finalDict.append(stateWordDict)
    finalDict.append(sportsWordsDict)
    finalDict.append(lenDict)

    pickle.dump(finalDict, open(allDicts, 'w+'))
    


def gss(setAllWords , cinemaWordDict ,lenCinema,stateWordDict ,lenState,sportsWordsDict,lenSports) :

    p1Dict = {}
    for eachWord in setAllWords :
        p1 = []
        if eachWord in cinemaWordDict :
            val1 = cinemaWordDict[eachWord]
            x = (1/3) * val1/lenCinema
            p = (1/3) * (lenCinema - val1 )/lenCinema
        else :
            x = 1/lenCinema
            p = (1/3) * (lenCinema - x)/lenCinema

        if eachWord in stateWordDict and eachWord in sportsWordsDict:
            val2 = stateWordDict[eachWord]
            val3 = sportsWordsDict[eachWord]
            y = (2/3) * ((lenState + lenSports)-(val2 + val3))/(lenState + lenSports)
            q = (2/3) * (val2 + val3)/(lenState + lenSports)
        else :
            if eachWord in stateWordDict :
                val2 = stateWordDict[eachWord]
                y = (2 / 3) * ((lenState + lenSports) - (val2 + 1/lenSports)) / (lenState + lenSports)
                z = (2/3) * ((val2 + 1/lenSports)) / (lenState + lenSports)
            else :
                val3 = sportsWordsDict[eachWord]
                y = (2 / 3) * ((lenState + lenSports) - (val3 + 1 / lenState)) / (lenState + lenSports)
                z = (2 / 3) * ((val3 + 1 / lenState)) / (lenState + lenSports)

        gssValue =x*y - p*q
        p1[0] = gssValue

        if eachWord in stateWordDict:
            val1 = stateWordDict[eachWord]
            x = (1 / 3) * val1 / lenState
            p = (1 / 3) * (lenState - val1) / lenState
        else:
            x = 1 / lenState
            p = (1 / 3) * (lenState - x) / lenState

        if eachWord in cinemaWordDict and eachWord in sportsWordsDict:
            val2 = cinemaWordDict[eachWord]
            val3 = sportsWordsDict[eachWord]
            y = (2 / 3) * ((lenCinema + lenSports) - (val2 + val3)) / (lenCinema + lenSports)
            q = (2 / 3) * (val2 + val3) / (lenCinema + lenSports)
        else:
            if eachWord in cinemaWordDict:
                val2 = cinemaWordDict[eachWord]
                y = (2 / 3) * ((lenCinema + lenSports) - (val2 + 1 / lenSports)) / (lenCinema + lenSports)
                z = (2 / 3) * ((val2 + 1 / lenSports)) / (lenCinema + lenSports)
            else:
                val3 = sportsWordsDict[eachWord]
                y = (2 / 3) * ((lenCinema + lenSports) - (val3 + 1 / lenCinema)) / (lenCinema + lenSports)
                z = (2 / 3) * ((val3 + 1 / lenCinema)) / (lenCinema + lenSports)

        gssValue = x * y - p * q
        p1[1] = gssValue

        if eachWord in sportsWordsDict:
            val1 = sportsWordsDict[eachWord]
            x = (1 / 3) * val1 / lenSports
            p = (1 / 3) * (lenSports - val1) / lenSports
        else:
            x = 1 / lenSports
            p = (1 / 3) * (lenSports - x) / lenSports

        if eachWord in cinemaWordDict and eachWord in stateWordDict:
            val2 = cinemaWordDict[eachWord]
            val3 = stateWordDict[eachWord]
            y = (2 / 3) * ((lenCinema + lenState) - (val2 + val3)) / (lenCinema + lenState)
            q = (2 / 3) * (val2 + val3) / (lenCinema + lenState)
        else:
            if eachWord in cinemaWordDict:
                val2 = cinemaWordDict[eachWord]
                y = (2 / 3) * ((lenCinema + lenState) - (val2 + 1 / lenState)) / (lenCinema + lenState)
                z = (2 / 3) * ((val2 + 1 / lenState)) / (lenCinema + lenState)
            else:
                val3 = stateWordDict[eachWord]
                y = (2 / 3) * ((lenCinema + lenState) - (val3 + 1 / lenCinema)) / (lenCinema + lenState)
                z = (2 / 3) * ((val3 + 1 / lenCinema)) / (lenCinema + lenState)

        gssValue = x * y - p * q
        p1[2] = gssValue
        p1Dict[eachWord] = p1
    return p1Dict



def buildCorpus(cinemaDict, stateDict, sportsDict):
    s = set()
    for key in cinemaDict:
        s.add(cinemaDict[key])
    for key in stateDict:
        s.add(stateDict[key])
    for key in sportsDict:
        s.add(sportsDict[key])

    return s


def createDict(jsonData):
    Dict = {}
    Blob = []
    for i in range(0, len(jsonData)):
        content = ''.join(jsonData[i]['content'])
        Blob.append(tb(content))

    for i, blob in enumerate(Blob):
        for word in set(blob.words):
            if word not in Dict:
                Dict[word] = 0
            Dict[word] += 1
    return Dict



state = "crawler/udayavani_state_news.json"
cinema = "crawler/udayavani_cinema_news.json"
sports = "crawler/udayavani_sports_news.json"

findValue(state,cinema,sports)

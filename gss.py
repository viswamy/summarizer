from textblob import TextBlob as tb
import json
import os
import pickle

def gssDictfunc(jsonData):
    Dict = {}
    Blob = []
    for i in range(0, 2000):
        content = ''.join(jsonData[i]['content'])
        Blob.append(tb(content))
    total = 0
    for i, blob in enumerate(Blob):
        total += len(blob.words)
        for word in blob.words:
            if word not in Dict:
                Dict[word] = 1
            Dict[word] += 1.0
    Dict["total_words_category"] = total
    return Dict


def findValue(state,cinema,sports):
    stateNews = json.load(open(state,'r'))
    cinemaNews = json.load(open(cinema, 'r'))
    sportsNews = json.load(open(sports, 'r'))
    results = "gss.pickle"
    allDicts = "allDicts.pickle"
    # if not os.path.exists(results):
    #     os.makedirs(results)
    cinemaWordDict = createDict(cinemaNews)
    stateWordDict = createDict(stateNews)
    sportsWordsDict = createDict(sportsNews)

    cinemaGssDict = gssDictfunc(cinemaNews)
    stateGssDict = gssDictfunc(stateNews)
    sportsGssDict = gssDictfunc(sportsNews)


    lenDict = []
    lenDict.append(len(cinemaNews))
    lenDict.append(len(stateNews))
    lenDict.append(len(sportsNews))
    setAllWords = buildCorpus(cinemaWordDict,stateWordDict,sportsWordsDict)
    gssDict = gss(setAllWords , cinemaWordDict ,len(cinemaNews), stateWordDict ,len(stateNews),sportsWordsDict,len(sportsNews))

    index = {}
    index["cinema"] = 0
    index["state"] = 1
    index["sports"] = 2

    finalDict = []
    finalDict.append(cinemaGssDict)
    finalDict.append(stateGssDict)
    finalDict.append(sportsGssDict)
    finalDict.append(lenDict)
    finalDict.append(index)



    with open(results, 'wb') as handle:
        pickle.dump(gssDict, handle)

    with open(allDicts, 'wb') as handle1:
        pickle.dump(finalDict, handle1)
    


def gss(setAllWords , cinemaWordDict ,lenCinema,stateWordDict ,lenState,sportsWordsDict,lenSports) :

    p1Dict = {}
    for eachWord in setAllWords :
        p1 = [1.0,1.0,1.0]
        # print eachWord
        if eachWord in cinemaWordDict :
            val1 = cinemaWordDict[eachWord]
            x = (1.0/3.0) * val1/lenCinema
            p = (1.0/3.0) * (lenCinema - val1 )/lenCinema
        else :
            x = 1.0/lenCinema
            p = (1.0/3.0) * (lenCinema - x)/lenCinema

        if eachWord in stateWordDict and eachWord in sportsWordsDict:
            val2 = stateWordDict[eachWord]
            val3 = sportsWordsDict[eachWord]
            y = (2.0/3.0) * ((lenState + lenSports)-(val2 + val3))/(lenState + lenSports)
            q = (2.0/3.0) * (val2 + val3)/(lenState + lenSports)
        else :
            if eachWord in stateWordDict :
                val2 = stateWordDict[eachWord]
                y = (2.0 / 3.0) * ((lenState + lenSports) - (val2 + 1.0/lenSports)) / (lenState + lenSports)
                z = (2.0 / 3.0) * ((val2 + 1.0/lenSports)) / (lenState + lenSports)

            if eachWord in sportsWordsDict:
                val3 = sportsWordsDict[eachWord]
                y = (2.0 / 3.0) * ((lenState + lenSports) - (val3 + 1.0 / lenState)) / (lenState + lenSports)
                z = (2.0 / 3.0) * ((val3 + 1.0 / lenState)) / (lenState + lenSports)
            else :
                y = (2.0 / 3.0) * ((lenState + lenSports) - (1.0/lenSports + 1.0 / lenState)) / (lenState + lenSports)
                z = (2.0 / 3.0) * ((1.0/lenSports + 1.0 / lenState)) / (lenState + lenSports)
            q = (2.0/3.0) * ((1.0/lenSports + 1.0 / lenState))/(lenState + lenSports)

        gssValue1 =x*y - p*q
        p1[0] = gssValue1

        if eachWord in stateWordDict:
            val1 = stateWordDict[eachWord]
            x = (1.0 / 3.0) * val1 / lenState
            p = (1.0 / 3.0) * (lenState - val1) / lenState
        else:
            x = 1.0 / lenState
            p = (1.0 / 3.0) * (lenState - x) / lenState

        if eachWord in cinemaWordDict and eachWord in sportsWordsDict:
            val2 = cinemaWordDict[eachWord]
            val3 = sportsWordsDict[eachWord]
            y = (2.0 / 3.0) * ((lenCinema + lenSports) - (val2 + val3)) / (lenCinema + lenSports)
            q = (2.0 / 3.0) * (val2 + val3) / (lenCinema + lenSports)
        else:
            if eachWord in cinemaWordDict:
                val2 = cinemaWordDict[eachWord]
                y = (2.0 / 3.0) * ((lenCinema + lenSports) - (val2 + 1.0 / lenSports)) / (lenCinema + lenSports)
                z = (2.0 / 3.0) * ((val2 + 1.0 / lenSports)) / (lenCinema + lenSports)
            if eachWord in sportsWordsDict:
                val3 = sportsWordsDict[eachWord]
                y = (2.0 / 3.0) * ((lenCinema + lenSports) - (val3 + 1.0 / lenCinema)) / (lenCinema + lenSports)
                z = (2.0 / 3.0) * ((val3 + 1.0 / lenCinema)) / (lenCinema + lenSports)
            else :
                y = (2.0 / 3.0) * ((lenCinema + lenSports) - (1.0/lenSports + 1.0 / lenCinema)) / (lenCinema + lenSports)
                z = (2.0 / 3.0) * ((1.0/lenSports + 1.0 / lenCinema)) / (lenCinema + lenSports)

        q = (2.0 / 3.0) * ((1.0 / lenSports + 1.0 / lenCinema)) / (lenCinema + lenSports)
        gssValue2 = x * y - p * q
        p1[1] = gssValue2

        if eachWord in sportsWordsDict:
            val1 = sportsWordsDict[eachWord]
            x = (1.0 / 3.0) * val1 / lenSports
            p = (1.0 / 3.0) * (lenSports - val1) / lenSports
        else:
            x = 1.0 / lenSports
            p = (1.0 / 3.0) * (lenSports - x) / lenSports

        if eachWord in cinemaWordDict and eachWord in stateWordDict:
            val2 = cinemaWordDict[eachWord]
            val3 = stateWordDict[eachWord]
            y = (2.0 / 3.0) * ((lenCinema + lenState) - (val2 + val3)) / (lenCinema + lenState)
            q = (2.0 / 3.0) * (val2 + val3) / (lenCinema + lenState)
        else:
            if eachWord in cinemaWordDict:
                val2 = cinemaWordDict[eachWord]
                y = (2.0 / 3.0) * ((lenCinema + lenState) - (val2 + 1.0 / lenState)) / (lenCinema + lenState)
                z = (2.0 / 3.0) * ((val2 + 1.0 / lenState)) / (lenCinema + lenState)

            if eachWord in stateWordDict:
                val3 = stateWordDict[eachWord]
                y = (2.0 / 3.0) * ((lenCinema + lenState) - (val3 + 1.0 / lenCinema)) / (lenCinema + lenState)
                z = (2.0 / 3.0) * ((val3 + 1.0 / lenCinema)) / (lenCinema + lenState)
            else :
                y = (2.0 / 3.0) * ((lenCinema + lenState) - (1.0/lenState + 1.0 / lenCinema)) / (lenCinema + lenState)
                z = (2.0 / 3.0) * ((1.0/lenState + 1.0 / lenCinema)) / (lenCinema + lenState)
        q = (2.0 / 3.0) * ((1.0 / lenState + 1.0 / lenCinema)) / (lenState + lenCinema)
        gssValue3 = x * y - p * q
        p1[2] = gssValue3
        p1Dict[eachWord] = p1
    return p1Dict



def buildCorpus(cinemaDict, stateDict, sportsDict):
    s = set()
    for key in cinemaDict:
        s.add(key)
    for key in stateDict:
        s.add(key)
    for key in sportsDict:
        s.add(key)

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
            Dict[word] += 1.0
    return Dict



state = "crawler/udayavani_state_news.json"
cinema = "crawler/udayavani_cinema_news.json"
sports = "crawler/udayavani_sports_news.json"

findValue(state,cinema,sports)

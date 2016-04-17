# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import operator
from textblob import TextBlob as tb
import json
import math
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TfIdf:

    def __init__(self, corpusPath, topWords="all"):
        self.corpusPath = corpusPath
        self.corpusRead = open(self.corpusPath, 'r')
        self.corpus = json.load(self.corpusRead)
        self.outFileDir = "results"
        self.topWords = topWords
        self.bloblist = []
        self.extractContent()
        self.computeTfIdf()

    def tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)

    def n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob)

    def idf(self, word, bloblist):
        return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))

    def tfidf(self, word, blob, bloblist):
        return self.tf(word, blob) * self.idf(word, bloblist)

    def extractContent(self):
        for i in range(0,len(self.corpus)-1):
            content = ''.join(self.corpus[i]['content'])
            self.bloblist.append(tb(content))

    def computeTfIdf(self):
        if not os.path.exists(self.outFileDir):
            os.makedirs(self.outFileDir)
        for i, blob in enumerate(self.bloblist):
            sentenceList = []
            for sentence in blob.sentences:
                sentenceList.append(sentence)

            scores = {word: self.tfidf(word, blob, self.bloblist) for word in blob.words}
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            topWordsDict = {}
            if self.topWords == "all":
                for word, score in sorted_words:
                    topWordsDict[word] = score
            else:
                for word, score in sorted_words[:self.topWords - 1]:
                    topWordsDict[word] = score

            articleNumber = i + 1
            self.sentenceRank(sentenceList, topWordsDict, articleNumber)

    def sentenceRank(self, sentenceList, topWordsDict, articleNumber):
        sentenceRankDict = {}
        for i, blob in enumerate(sentenceList):
            sentenceRank = None
            for word in blob.words:
                if topWordsDict.has_key(word):
                    if sentenceRank is None:
                        sentenceRank = 1
                    sentenceRank *= topWordsDict[word]

            if sentenceRank is not None:
                sentenceNumber = i
                sentenceRankDict[sentenceList[sentenceNumber]] = sentenceRank

        topSentences = sorted(sentenceRankDict.items(), key=lambda x: x[1], reverse=True)
        # TODO: Decide on the number of important top sentences
        topSentencesToFile = ""
        for sentence, sentenceNumber in topSentences[:3]:
            topSentencesToFile += format(sentence)
            topSentencesToFile += '\n'
        outfileName = os.path.join(self.outFileDir, format(articleNumber) + ".txt")
        outFile = open(outfileName, 'w')
        sentencesToFile = ""
        for sen in sentenceList:
            sentencesToFile += format(sen)
            sentencesToFile += '\n'

        outFile.write(sentencesToFile)
        outFile.write('\n')
        outFile.write("--------------------- Summary -----------------------------")
        outFile.write('\n')
        outFile.write(topSentencesToFile)


corpusPath = 'udayavani_test.json'
#TfIdf(corpusPath, 50)
TfIdf(corpusPath)
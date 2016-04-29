
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

#import stemmer_test
<<<<<<< HEAD
=======
import re
>>>>>>> efee6a2cd816c3d07407f64528ccb71bb54a68e8
from textblob import TextBlob as tb
import json
import math
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TfIdf:

    def __init__(self, corpusPath, devPath, outDir):
        self.corpus = json.load(open(corpusPath[0], 'r'))
        self.dev = json.load(open(devPath, 'r'))
        self.outFileDir = outDir

        if not os.path.exists(self.outFileDir):
            os.makedirs(self.outFileDir)
<<<<<<< HEAD

=======
        self.reg = re.compile('\. |\.\xa0')
>>>>>>> efee6a2cd816c3d07407f64528ccb71bb54a68e8
        self.wordDfDict = {}
        self.trainBloblist = []
        self.testBloblist = []
        self.trainBloblistLength = 0
        self.testBloblistLength = 0
        self.buildCorpus()
        self.calculateDf()
        self.buildTestData()
        self.extractSummary()

    def tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)

    def computeIdf(self, df):
        return math.log(self.trainBloblistLength + 1 / (1 + df))

    def buildCorpus(self):
        for i in range(0,len(self.corpus)):
            content = '. '.join(self.corpus[i]['content'])
            content.replace('..','.')
            self.trainBloblist.append(tb(content))
        self.trainBloblistLength = len(self.trainBloblist)

    def buildTestData(self):
        for i in range(0, len(self.dev)):
            content = '. '.join(self.dev[i]['content'])
            content.replace('..','.')
            self.testBloblist.append(tb(content))
        self.testBloblistLength = len(self.testBloblist)

    def calculateDf(self):
        for i, blob in enumerate(self.trainBloblist):
            #print i
            for word in set(blob.words):
                if word not in self.wordDfDict:
                    self.wordDfDict[word] = 0
                self.wordDfDict[word] += 1

    def extractSummary(self):
        for i, blob in enumerate(self.testBloblist):
            sentenceList = self.reg.split(unicode(blob))
            sentenceRankDict = {}
            for sentence in sentenceList:
                sentenceRank = 0
                wordsInSentence = sentence.split()
                for word in wordsInSentence:
<<<<<<< HEAD
                    if self.wordDfDict.has_key(word):
=======
                    if word in self.wordDfDict:
>>>>>>> efee6a2cd816c3d07407f64528ccb71bb54a68e8
                        tf = self.tf(word, blob)
                        df = self.wordDfDict[word]
                        #sentenceRank += self.bagOfWords[word]
                        tfIdf = tf * self.computeIdf(df+1)
                        sentenceRank += tfIdf

                if sentenceRank != 0:
                    sentenceRankDict[sentence] = sentenceRank

            topSentences = sorted(sentenceRankDict.items(), key=lambda x: x[1], reverse=True)
            #deciding
            topSentencesToFile = ""
            numberOfSentence = int(math.floor(0.2*len(sentenceList)))
            if  numberOfSentence > 6:
                numberOfSentence = 6
            elif numberOfSentence < 4:
                numberOfSentence = 4

            for sentence, sentenceNumber in topSentences[:numberOfSentence+1]:
                topSentencesToFile += format(sentence)+". \n"

            articleNumber = i
            sentencesToFile = ""
            for sentence in sentenceList:
                sentencesToFile += format(sentence)+". \n"

            self.writeToFile(articleNumber, sentencesToFile, topSentencesToFile)

    def writeToFile(self, articleNumber, sentencesToFile, topSentencesToFile):
        outfileName = os.path.join(self.outFileDir, format(articleNumber) + ".txt")
        outFile = open(outfileName, 'w')
        outFile.write(sentencesToFile)
        outFile.write('\n')
        outFile.write("--------------------- Summary -----------------------------")
        outFile.write('\n')
        outFile.write(topSentencesToFile)

<<<<<<< HEAD
corpusPath = ["crawler/udayavani_cinema_news.json"]
devPath = 'annotator/udayavani_cinema_news.json'
#TfIdf(corpusPath, 50)
=======
corpusPath = ["annotator/udayavani_cinema_news.json"]
devPath = 'annotator/udayavani_cinema_news.json'
>>>>>>> efee6a2cd816c3d07407f64528ccb71bb54a68e8
TfIdf(corpusPath, devPath, 'resultsWithoutStemmer')


# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

#import stemmer_test
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
            content = ''.join(self.corpus[i]['content'])
            self.trainBloblist.append(tb(content))
        self.trainBloblistLength = len(self.trainBloblist)

    def buildTestData(self):
        for i in range(0, len(self.dev)):
            content = ''.join(self.dev[i]['content'])
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
            sentenceList = blob.sentences
            sentenceRankDict = {}
            for sentence in sentenceList:
                sentenceRank = 0
                wordsInSentence = sentence.split()
                for word in wordsInSentence:
                    if self.wordDfDict.has_key(word):
                        tf = self.tf(word, blob)
                        df = self.wordDfDict[word]
                        #sentenceRank += self.bagOfWords[word]
                        tfIdf = tf * self.computeIdf(df+1)
                        sentenceRank += tfIdf

                if sentenceRank != 0:
                    sentenceRankDict[sentence] = sentenceRank

            topSentences = sorted(sentenceRankDict.items(), key=lambda x: x[1], reverse=True)
            # TODO: Decide on the number of important top sentences
            topSentencesToFile = ""
            for sentence, sentenceNumber in topSentences[:4]:
                topSentencesToFile += format(sentence)
                topSentencesToFile += '\n'

            articleNumber = i + 1
            sentencesToFile = ""
            for sentence in sentenceList:
                sentencesToFile += format(sentence)
                sentencesToFile += '\n'
            self.writeToFile(articleNumber, sentencesToFile, topSentencesToFile)

    def writeToFile(self, articleNumber, sentencesToFile, topSentencesToFile):
        outfileName = os.path.join(self.outFileDir, format(articleNumber) + ".txt")
        outFile = open(outfileName, 'w')
        outFile.write(sentencesToFile)
        outFile.write('\n')
        outFile.write("--------------------- Summary -----------------------------")
        outFile.write('\n')
        outFile.write(topSentencesToFile)

corpusPath = ["crawler/udayavani_cinema_news.json"]
devPath = 'annotator/udayavani_cinema_news.json'
#TfIdf(corpusPath, 50)
TfIdf(corpusPath, devPath, 'resultsWithoutStemmer')

# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import stemmer_test
from textblob import TextBlob as tb
import json
import math
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TfIdf:

    def __init__(self, corpusPath, devPath):
        self.corpus = json.load(open(corpusPath, 'r'))
        self.dev = json.load(open(devPath, 'r'))

        model_file = open('prefix_suffix.json', 'r')
        self.model = json.loads(model_file.read())


        self.outFileDir = "results"
        if not os.path.exists(self.outFileDir):
            os.makedirs(self.outFileDir)

        self.wordDfcDict = {}
        self.trainBloblist = []
        self.testBloblist = []
        self.trainBloblistLength = 0
        self.testBloblistLength = 0
        self.buildCorpus()
        self.storeDfc()
        self.buildTestData()
        self.extractSummary()

    def tf(self, word, blob):
        return blob.words.count(word) / len(blob.words)

    def n_containing(self, word, bloblist):
        return sum(1 for blob in bloblist if word in blob)

    def computeIdf(self, df):
        return math.log(self.trainBloblistLength + 1 / (1 + df))

    def dfc(self, word):
        return self.n_containing(word, self.trainBloblist)

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

    def storeDfc(self):
        for i, blob in enumerate(self.trainBloblist):
            print i
            dfs = {word: self.dfc(word) for word in blob.words}
            #sortedDfs = sorted(dfs.items(), key=lambda x: x[1], reverse=True)
            for word, score in dfs.items():
                self.wordDfcDict[word] = score

    def extractSummary(self):
        for i, blob in enumerate(self.testBloblist):
            sentenceList = blob.sentences
            sentenceRankDict = {}
            for sentence in sentenceList:
                sentenceRank = 0
                wordsInSentence = sentence.split()
                for word in wordsInSentence:
                    if self.wordDfcDict.has_key(word):
                        tf = self.tf(word, blob)
                        dfc = self.wordDfcDict[word]
                        #sentenceRank += self.bagOfWords[word]
                        tfIdf = tf * self.computeIdf(dfc+1)
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

corpusPath = 'udayavani.json'
devPath = 'prajavani.json'
#TfIdf(corpusPath, 50)
TfIdf(corpusPath, devPath)

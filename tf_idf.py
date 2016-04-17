# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
from textblob import TextBlob as tb
import json
import math
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TfIdf:

    def __init__(self, corpusPath, outFileDir, topWords):
        self.corpusPath = corpusPath
        self.corpusRead = open(self.corpusPath, 'r')
        self.corpus = json.load(self.corpusRead)
        self.outFileDir = outFileDir
        self.topWords = topWords
        self.bloblist = []
        self.extractContent()
        self.computeTfIdfAndWrite()

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

    def computeTfIdfAndWrite(self):
        if not os.path.exists(self.outFileDir):
            os.makedirs(self.outFileDir)
        for i, blob in enumerate(self.bloblist):
            scores = {word: self.tfidf(word, blob, self.bloblist) for word in blob.words}
            fileName = i+1
            self.WriteTopScores(scores, fileName)

    def WriteTopScores(self, scores, fileName):
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        outfileName = os.path.join(self.outFileDir, format(fileName) + ".txt")
        outFile = open(outfileName, 'w')
        for word, score in sorted_words[:self.topWords-1]:
            outFile.write("Word: {}, TF-IDF: {}".format(word, score))
            outFile.write('\n')


corpusPath = 'crawler/udayavani.json'
TfIdf(corpusPath, "results", 20)

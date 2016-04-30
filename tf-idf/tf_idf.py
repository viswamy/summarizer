# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

#import stemmer_test
import re
from textblob import TextBlob as tb
import json
import math
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pickle


class TfIdf:

    def __init__(self, corpusPath, outDir ):
        self.cps = corpusPath
        self.corpus = ""#json.load(open(corpusPath[0], 'r'))
        self.outFileDir = outDir

        if not os.path.exists(self.outFileDir):
            os.makedirs(self.outFileDir)
        self.reg = re.compile('\. |\.\xa0')
        self.wordDfDict = {}
        self.trainBloblist = []
        self.testBloblist = []
        self.trainBloblistLength = 0
        self.testBloblistLength = 0
        #gss
        with open('../gss.pickle','r') as f:
            self.gss = pickle.load(f)
        with open('../allDicts.pickle','r') as f:
            l = pickle.load(f)
            self.categoryWordDict = []
            self.categoryWordDict.append(l[0])
            self.categoryWordDict.append(l[1])
            self.categoryWordDict.append(l[2])
            self.categoryDictLength = l[3]
            self.cindex = l[4]


    def setup(self):
        self.buildCorpus()
        for cp in self.cps:
            self.corpus = json.load(open(cp, 'r'))
            self.calculateDf()

    def tf(self,blob):
        out = {}
        for word in blob.words:
            if word not in out:
                out[word] = 0
            out[word] += 1
        for key,value in out.iteritems():
            out[key] = value/len(blob.words)
        return out

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

    def extractSummary(self, devPath, outFileName):
        self.dev = json.load(open(devPath, 'r'))
        self.buildTestData()
        out = {}
        c = {0:0,1:0,2:0}
        for i, blob in enumerate(self.testBloblist):
            cn = self.getCategoryNumber(blob)
            c[cn] += 1
            sentenceList = self.reg.split(unicode(blob))
            sentenceRankDict = {}
            tfw = self.tf(blob)
            for j in range(0,len(sentenceList)):
                sentence = tb(sentenceList[j])
                sentenceRank = 0
                for word in sentence.words:
                    if word in self.wordDfDict:
                        tf = tfw[word]
                        df = self.wordDfDict[word]
                        tfIdf = tf * self.computeIdf(df+1)
                        gss = 0
                        if word in self.gss:
                            gss = tf*self.gss[word][cn]
                        sentenceRank += (tfIdf + gss)

                if sentenceRank != 0:
                    sentenceRankDict[sentence] = [sentenceRank, j]

            topSentences = sorted(sentenceRankDict.items(), key=lambda x: x[1][0], reverse=True)
            #deciding
            topSentencesToFile = ""
            #select 20% of article, with min = 4 , max = 6 sentences
            numberOfSentence = int(math.floor(0.2*len(sentenceList)))
            if  numberOfSentence > 6:
                numberOfSentence = 6
            elif numberOfSentence < 4:
                numberOfSentence = 4

            topSentences = sorted(topSentences[:numberOfSentence], key=lambda x: x[1][1])
            for sentence, sentenceNumber in topSentences:
                topSentencesToFile += format(sentence)+". \n"
            out[i] = {"text" : topSentencesToFile}
            articleNumber = i
            sentencesToFile = ""
            for sentence in sentenceList:
                sentencesToFile += format(sentence)+". \n"

        #    self.writeToFile(articleNumber, sentencesToFile, topSentencesToFile)
        print c
        outfileName = "system_"+outFileName
        with open(self.outFileDir+"/"+outfileName, 'w') as outfile:
            json.dump(out, outfile)

    def getCategoryNumber(self, blob):
        #naive bayes to determine category
        out = [1.0, 1.0, 1.0]
        #cinema     #state        #sports
        for i in range(0, len(self.cindex)):
            #out[i] *= self.categoryDictLength[i]/ (sum(self.categoryDictLength)- self.categoryDictLength[i]) # prior
            for word in blob.words:
                if word in self.categoryWordDict[i]:
                    out[i] = out[i]*math.log( self.categoryWordDict[i][word]/self.categoryWordDict[i]["total_words_category"])
        return out.index(max(out))


    def writeToFile(self, articleNumber, sentencesToFile, topSentencesToFile):
        outfileName = os.path.join(self.outFileDir, format(articleNumber) + ".txt")
        outFile = open(outfileName, 'w')
        outFile.write(sentencesToFile)
        outFile.write('\n')
        outFile.write("--------------------- Summary -----------------------------")
        outFile.write('\n')
        outFile.write(topSentencesToFile)
        outFile.close()

corpusPath = ["../crawler/udayavani_cinema_news.json", "../crawler/udayavani_sports_news.json", "../crawler/udayavani_state_news.json"]
t = TfIdf(corpusPath, 'tf_idf_results' )
t.setup()
t.extractSummary('cinema_test.json', 'cinema.json')
t.extractSummary('state_test.json', 'state.json')
t.extractSummary('sports_test.json', 'sports.json')

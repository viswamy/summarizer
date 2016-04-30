# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import json
import os.path

def gen(path,fileName):
    if not os.path.exists(path):
            os.makedirs(path)
    j = json.load(open(fileName, 'r'))
    fs = fileName.split("/")
    fs = fs[0].split("_")
    category = fs[1].split(".")[0]
    annotator = fs[0]
    for key,value in j.iteritems():
        fname = category+key+"_"+annotator+".txt"
        outFile = open(path+fname, 'w')
        outFile.write(value["text"].encode("utf-8"))
        outFile.close()

#'''
#human_af = ["annotated_complete/achyut_cinema.json"]
system_af = ["systemStemmer_cinema.json","systemStemmer_state.json"]

#for file in human_af:
#    gen("rouge/reference/", file)

for file in system_af:
    gen("rouge/system/", file)
#'''
'''
human_af = ["annotated_complete/achyut_state.json"]
system_af = ["annotated_complete/nitish_state.json"]

for file in human_af:
    gen("inter_annotator_agreement_state/reference/", file)

for file in system_af:
    gen("inter_annotator_agreement_state/system/", file)
'''
'''
human_af = ["annotated_complete/swaroop_sports.json"]
system_af = ["annotated_complete/vswamy_sports.json"]

for file in human_af:
    gen("inter_annotator_agreement_sports/reference/", file)

for file in system_af:
    gen("inter_annotator_agreement_sports/system/", file)
'''
'''
human_af = ["annotated_complete/achyut_cinema.json"]
system_af = ["annotated_complete/vswamy_cinema.json"]

for file in human_af:
    gen("inter_annotator_agreement_cinema/reference/", file)

for file in system_af:
    gen("inter_annotator_agreement_cinema/system/", file)
'''
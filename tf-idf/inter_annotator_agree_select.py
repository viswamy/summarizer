import glob

__author__ = 'swvenu'
import numpy as np
import json
from shutil import copy

category = "sports"
file = "../rouge_package/results_inter_"+category+".csv"
ann_dir = "inter_annotator_agreement_"+category+"/"
rouge_eval_dir = "rouge/reference/"
corpus_path = ["../annotator/udayavani_","_news.json"]
data = np.genfromtxt(file, dtype=None, delimiter=',', names=True)
agree_percentage = 0.6
rouge_f1_col = 5
file_name_col = 1
fileNames = []
test_data = {}
json_data = json.load(open(corpus_path[0]+category+corpus_path[1], 'r'))


for i in range(0,len(data)):
    if data[i][rouge_f1_col] >= 0.5:
        l = [int(s) for s in data[i][file_name_col] if s.isdigit()]
        l = int(''.join([ "%d"%x for x in l]))
        fileNames.append( category+str(l)+"_*")
        test_data[l] = json_data[l]

#take all those files put into rouge_eval_dir
for file in fileNames:
    l = glob.glob(ann_dir+"**/"+file)
    for f in l:
        copy(f.replace("\\\\","\\"),rouge_eval_dir)

with open(category+"_test.json", 'w') as outfile:
    json.dump(test_data, outfile)
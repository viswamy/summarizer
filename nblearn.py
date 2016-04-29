import os
import json
from operator import add
from collections import defaultdict
# from collections import Counter

import string
import fileinput
import sys
directory = sys.argv[1]

# remove the Readme directory from their system or handle readme.txt file

STOPWORDS = ['a','able','about','across','after','all','almost','also','am','among',
             'an','and','any','are','as','at','be','because','been','but','by','can',
             'could','dear','did','do','does','either','else','ever','every',
             'for','from','get','got','had','has','have','he','her','hers','him','his',
             'how','however','i','if','in','into','is','it','its','just','least','let',
             'like','likely','may','me','might','most','must','my',
             'of','off','often','on','only','or','other','our','own','rather','said',
             'say','says','she','should','since','so','some','than','that','the','their',
             'them','then','there','these','they','this','tis','to','too','twas','us',
             'wants','was','we','were','what','when','where','which','while','who',
             'whom','why','will','with','would','yet','you','your']


STOPWORDS1 = ['a','able','about','across','after','all','almost','also','am','among',
             'an','and','any','are','as','at','be','because','been','but','by','can',
             'could','dear','did','do','does','either','else','ever','every',
             'for','from','get','got','had','has','have','he','her','hers','him','his',
             'how','however','i','if','in','into','is','it','its','just','least','let',
             'like','likely','may','me','might','most','must','my','not' , 'never' ,'nor',
             'of','off','often','on','only','or','other','our','own','rather','said',
             'say','says','she','should','since','so','some','than','that','the','their',
             'them','then','there','these','they','this','tis','to','too','twas','us',
             'wants','was','we','were','what','when','where','which','while','who',
             'whom','why','will','with','would','yet','you','your']



def get_immediate_subdirectories(a_dir):
    return [os.path.join(a_dir, name) for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


get_immediate_subdirectories(directory)
negative_class_path = get_immediate_subdirectories(directory)[0]
positive_class_path =  get_immediate_subdirectories(directory)[1]

get_immediate_subdirectories(negative_class_path)
negative_deceptive_class_path = get_immediate_subdirectories(negative_class_path)[1]
negative_truthful_class_path = get_immediate_subdirectories(negative_class_path)[0]

get_immediate_subdirectories(positive_class_path)
positive_deceptive_class_path = get_immediate_subdirectories(positive_class_path)[1]
positive_truthful_class_path = get_immediate_subdirectories(positive_class_path)[0]

#print " "+ negative_class_path + "\n " +positive_class_path +"\n " + negative_deceptive_class_path + "\n " +negative_truthful_class_path + "\n " +positive_deceptive_class_path +"\n " + positive_truthful_class_path


def allfiles_dir(path) :
    f =[]
    count=0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                f.append(os.path.join(root, file))
                count+=1
    # print count
    return f


def allfiles_dir_append(path , array_of_files) :
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                array_of_files.append(os.path.join(root, file))
                # count+=1
    # print count
    return array_of_files



negative_class_all_files = allfiles_dir(negative_class_path)
positive_class_all_files = allfiles_dir(positive_class_path)

deceptive_class_all_files = allfiles_dir(negative_deceptive_class_path)
deceptive_class_all_files = allfiles_dir_append(positive_deceptive_class_path , deceptive_class_all_files)


truthful_class_all_files =  allfiles_dir(negative_truthful_class_path)
truthful_class_all_files = allfiles_dir_append(positive_truthful_class_path , truthful_class_all_files)

def remove_stopwords(line,stopwords=STOPWORDS) :
    line1=""
    words = line.split()
    for word in words :
        if word not in stopwords :
            line1 =line1 + word + " "
    # print line1
    return line1


def trim_line(line) :
        line = line.lower()
        line = line.replace(",", "")
        line = (line.replace(".", ""))
        line = line.replace("-", " ")
        line = line.replace("/", "")
        line = line.replace("(", "")
        line = line.replace(")", "")
        line = line.replace("!" , "")
        # line = line.replace("\'","")
        line = line.replace("\\", "")
        line = line.replace("*", "")
        line = line.replace("#", "")
        line = line.replace("?", "")
        line = line.replace("[", "")
        line = line.replace("]", "")
        line = line.replace("{", "")
        line = line.replace("}", "")
        line = line.replace("\"", "")
        line = line.replace(">", " ")
        line = line.replace("<", " ")
        line = line.replace("~", "")
        line = line.replace("$", "")
        line = line.replace("+", "")
        # line = line.replace("-", " ")
        line = line.replace("&", "and")
        line = line.replace(":", "")
        line = line.replace(";", "")
        return line


def large_class_file_neg(path,all_files_array) :
    large_file =  "neg.txt"
    with open(large_file, 'w+') as outfile:
        for fname in all_files_array:
            with open(fname) as infile:
                for line in infile:
                    line = trim_line(line)
                    line = remove_stopwords(line)
                    outfile.write(line)
    #print large_file
    return large_file

def large_class_file_pos(path,all_files_array) :
    large_file =  "pos.txt"
    with open(large_file, 'w+') as outfile:
        for fname in all_files_array:
            with open(fname) as infile:
                for line in infile:
                    line = trim_line(line)
                    line = remove_stopwords(line)
                    outfile.write(line)
    #print large_file
    return large_file


def large_class_file_dec_tru(fname , all_files_array) :
    large_file = fname
    with open(large_file, 'w+') as outfile:
        for fname in all_files_array:
            with open(fname) as infile:
                for line in infile:
                    line = trim_line(line)
                    line = remove_stopwords(line)
                    outfile.write(line)
    #print large_file
    return large_file



class_file_negative = large_class_file_neg(negative_class_path, negative_class_all_files)
class_file_positive = large_class_file_pos(positive_class_path,positive_class_all_files)

class_file_deceptive = large_class_file_dec_tru("deceptive.txt",deceptive_class_all_files)
class_file_truthful = large_class_file_dec_tru("truthful.txt" , truthful_class_all_files)

def wordcount() :
    wordcount={}
    file = open(class_file_negative , "r+")
    file1 = open(class_file_positive , "r+")
    file2 = open(class_file_deceptive , "r+")
    file3 = open(class_file_truthful,"r+")
    count1 = count2 = count3 = count4 = 0

    for word in file.read().split():
        count1+=1
        wordcount[word] = map(add, wordcount.get(word, [1,1,1,1]), [1,0,0,0])
    wordcount["negative_wc"] =  count1
    #print wordcount
    #print wordcount["negative_wc"]

    for word in file1.read().split():
        count2+=1
        wordcount[word] = map(add, wordcount.get(word, [1,1,1,1]), [0,1,0,0])
    #print count2
    wordcount["positive_wc"] =  count2
    #print wordcount
    #print wordcount["positive_wc"]


    for word in file2.read().split():
         count3+=1
         wordcount[word] = map(add, wordcount.get(word, [1,1,1,1]), [0,0,1,0])
    #print count3
    wordcount["deceptive_wc"] =  count3
    #print wordcount
    #print wordcount["deceptive_wc"]

    for word in file3.read().split():
        count4+=1
        wordcount[word] = map(add, wordcount.get(word, [1,1,1,1]), [0,0,0,1])
    #print count4
    wordcount["truthful_wc"] =  count4
    #print wordcount
    #print wordcount["truthful_wc"]
    return wordcount

#
word_count_dictionary = wordcount()
# print word_count_dictionary["negative_wc"]
# outputfile = sys.argv[1] + "/nbmodel.txt"
outputfile = "nbmodel.txt"
json.dump(word_count_dictionary , open(outputfile,'w+'), indent=4)

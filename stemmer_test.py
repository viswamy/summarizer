import sys
import os
import time
import json
import math

model_file = open('prefix_suffix.json','r')
model = json.loads(model_file.read())


def get_stem(model, word):
    MAX_P = 0
    STEM = word
    prefix_dictionary = model['prefix']
    suffix_dictionary = model['suffix']
    for i in range(3, len(word)):
        prefix_str = word[0:i]
        suffix_str = word[i:len(word)]
        prefix_frequency = 1
        suffix_frequency = 1
        if(prefix_str in prefix_dictionary):
            prefix_frequency = prefix_dictionary[prefix_str]
        if(suffix_str in suffix_dictionary):
            suffix_frequency = suffix_dictionary[suffix_str]
        P = len(prefix_str) * math.log(prefix_frequency) + len(suffix_str) * math.log(suffix_frequency)
        if(MAX_P < P):
            MAX_P = P
            STEM = prefix_str
    return STEM
    
    
'''
while(True):
    word = input('Enter the word here$$ ')
    print(get_stem(model, word))

'''



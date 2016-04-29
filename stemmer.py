import sys
import os
import time
import json
import math

class Process:
    def __init__(self, path):
        self.path = path
        self.items_file = open(path,'r')
        self.items = json.loads(self.items_file.read())
        self.prefix = {}
        self.suffix = {}  
        self.process()
        return

    def process(self):
        for i in range(0, len(self.items)):
            article = self.items[i]
            url = article['url']
            title = article['title']
            content = article['content']
            
            for paragraph in content:
                self.process_pragraph(paragraph)
        
        return
        
    def process_word(self, word):
        for i in range(3, len(word)):
            prefix_str = word[0:i]
            suffix_str = word[i: len(word)]
            
            if(prefix_str in self.prefix):
                self.prefix[prefix_str] += 1
            else:
                self.prefix[prefix_str] = 1
            
            if(suffix_str in self.suffix):
                self.suffix[suffix_str] += 1
            else:
                self.suffix[suffix_str] = 1
                    
    def process_pragraph(self, paragraph):
        words = paragraph.split(' ')
        for word in words:
            self.process_word(word)
        return
        
    def to_JSON(self):
        out = {}
        out['prefix'] = self.prefix
        out['suffix'] = self.suffix
        return json.dumps(out, indent = 4)
    
    def get_stem(self, word):
        MAX_P = 0
        STEM = ''
        for i in range(3, len(word)):
            prefix_str = word[0:i]
            suffix_str = word[i:len(word)]
            prefix_frequency = 1
            suffix_frequency = 1
            if(prefix_str in self.prefix):
                prefix_frequency = self.prefix[prefix_str]
            if(suffix_str in self.suffix):
                suffix_frequency = self.suffix[suffix_str]
            P = len(prefix_str) * math.log(prefix_frequency) + len(suffix_str) * math.log(suffix_frequency)
            if(MAX_P < P):
                MAX_P = P
                STEM = prefix_str
        return STEM

def get_json(process_list):
    out_prefix = {}
    out_suffix = {}
    
    for process_item in process_list:
        process_item_prefix = process_item.prefix
        for item in process_item_prefix:
            if item in out_prefix:
                out_prefix[item] += process_item_prefix[item]
            else:
                out_prefix[item] = process_item_prefix[item]
                        
        process_item_suffix = process_item.suffix
        for item in process_item_suffix:
            if item in out_suffix:
                out_suffix[item] += process_item_suffix[item]
            else:
                out_suffix[item] = process_item_suffix[item]
                
    out = {}
    out['prefix'] = out_prefix
    out['suffix'] = out_suffix
    return json.dumps(out, indent = 4)        
        
    


#main    
#path = 'udayavani_sample.json'
path_cinema = 'crawler/udayavani_cinema_news.json'
path_sports = 'crawler/udayavani_sports_news.json'
path_state = 'crawler/udayavani_state_news.json'

process_cinemas = Process(path_cinema)
process_sports = Process(path_sports)
process_state = Process(path_state)
process_list = [process_cinemas, process_sports, process_state]

output_path = 'prefix_suffix.json'
output_file = open(output_path, 'w')

output_file.write(get_json(process_list))

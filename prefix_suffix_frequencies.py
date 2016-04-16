import sys
import os
import time
import json


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
            #print('prefix = ' + prefix_str)
            #print('suffix = ' + suffix_str)
            
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
    
#path = 'udayavani_sample.json'
path = 'crawler/udayavani.json'

process = Process(path)

output_path = 'prefix_suffix.json'
output_file = open(output_path, 'w')

output_file.write(process.to_JSON())
#print(process.to_JSON())
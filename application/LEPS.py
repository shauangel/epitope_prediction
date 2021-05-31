#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 10:18:27 2021

@author: shauangel
"""

#import json
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class LEPS:
    def parse_web(self,FASTA):
        FASTA_len = len(FASTA.split(']')[1].replace('\n', ''))
        
        chrome = webdriver.Chrome('./chromedriver.exe')
        chrome.get("https://leps.biolab.ml/LEPS/")
        
        seq = chrome.find_element_by_name('seq')
        seq.send_keys(FASTA)
        
        send = chrome.find_element_by_xpath('//input[@value="Submit"]')
        send.click()
        
        time.sleep(5)
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        prediction = soup.find('div', {'class' : 'peakSubSeq finalResult'})
        ranges = prediction.find_all('div', {'class' : 'range'})
        
        chrome.close()
        
        range_result = []
        for r in ranges:
            range_result.append(r.text.split('~'))
        return self.result_analyze(range_result, FASTA_len)
        
    
    def result_analyze(self, range_result, seq_len):
        result = "."*seq_len
        for r in range_result:
            start = int(r[0])-1
            end = int(r[1])-1
            E = 'E'*len(result[start:end+1])
            result = result[:start] + E + result[end:]
            
        return result
    

"""
url = input('Enter file path: ')
protein = input('Enter protein name: ')
paths = open(url)
FASTA_paths = paths.read().split('\n')

results = {}
for path in FASTA_paths:
    data = {"PREDS" : "", "tcoffee" : "", "color" : "" }
    name = path[path.find('[')+1 : path.find(']')]
    file = open(path)
    FASTA = file.read()
    data['PREDS'] = parse_web(FASTA)
    results[name] = data
    
    

with open('LEPS-' + protein + '.json', 'w', encoding='utf-8') as f:
    json.dump(results, f)


"""

















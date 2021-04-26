#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 10:18:27 2021

@author: shauangel
"""

from selenium import webdriver
from bs4 import BeautifulSoup


class ABCpred:
    def parse_web(self, FASTA):
        chrome = webdriver.Chrome('./chromedriver')
        chrome.get("https://webs.iiitd.edu.in/raghava/abcpred/ABC_submission.html")
        
        seq = chrome.find_element_by_name('SEQ')
        seq.send_keys(FASTA)
        
        send = chrome.find_element_by_xpath('//input[@type="submit"]')
        send.click()
        
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        pre = soup.find_all('pre')
        overlap_list = pre[2].get_text(separator = '\n').strip()
        
        chrome.close()
        
        seq_list = overlap_list.split('\n')
        return self.result_analyze(seq_list)
        
    
    def result_analyze(self, seq_list):
        overlap_list = []
        seq = ""
        total = int(seq_list[1])
        for i in range(3,len(seq_list)):
            seq += seq_list[i]
            if len(seq) < total:
                continue
            else:
                overlap_list.append(seq)
                seq = ""
                
        result = ""
        for i in range(total):
            test = [seq[i] != '-' for seq in overlap_list]
            #print(sum(test))
            if sum(test) > 1:
                result += "E"
            else:
                result += "."
        
        return result
        
"""
url = "/Users/shauangel/Desktop/生資專題/Enolase/FASTA/Enolase_all_path.txt"
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
    
    

with open('ABCpred-Enolase.json', 'w', encoding='utf-8') as f:
    json.dump(results, f)


"""

















#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 02:41:39 2021

@author: shauangel
"""

from selenium import webdriver
from bs4 import BeautifulSoup

class BCPREDS:
    def parse_web(self, FASTA):
        chrome = None
        try:
            chrome = webdriver.Chrome('./chromedriver')
        except:
            chrome = webdriver.Chrome('./chromedriver.exe')
        chrome.get("http://ailab-projects1.ist.psu.edu:8080/bcpred/predict.html")
        
        seq = chrome.find_element_by_name('sequence')
        seq.send_keys(FASTA.split(']')[1])
        
        send = chrome.find_element_by_xpath('//input[@type="submit"]')
        send.click()
        
        
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        fonts = soup.find_all('font', {'color' : 'red'})
        epitope = ""
        for result in fonts:
            epitope += result.text
        
        chrome.close()
        return epitope
        
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
    FASTA = file.read().split(']')[1]
    data['PREDS'] = parse_web(FASTA)
    results[name] = data
 
    

with open('BCPREDS-' + protein + '.json', 'w', encoding='utf-8') as f:
    json.dump(results, f)
    
    
"""
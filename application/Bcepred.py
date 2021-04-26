#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 03:55:15 2021

@author: shauangel
"""
from selenium import webdriver
from bs4 import BeautifulSoup


class BcePred:
    def parse_web(self, FASTA):
        chrome = webdriver.Chrome('./chromedriver')
        chrome.get("https://webs.iiitd.edu.in/raghava/bcepred/bcepred_submission.html")
        
        seq = chrome.find_element_by_name('SEQ')
        seq.send_keys(FASTA)
        
        send = chrome.find_element_by_xpath('//input[@type="submit"]')
        send.click()
        
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        table = soup.find_all('table')
        tds = table[0].find_all('td')
        fonts = tds[3].find_all('font')
        chrome.close()
        
        result = ""
        for font in fonts:
            if font["color"] == "black":
                result += "."
            elif font["color"] == "blue":
                result += "E"
                
        return result

"""
url = "/Users/shauangel/Downloads/OmpA/OmpA_all_path.txt"
paths = open(url)
FASTA_paths = paths.read().split('\n')


results = {}
for path in FASTA_paths:
    name = path[path.find('[')+1 : path.find(']')]
    file = open(path)
    FASTA = file.read()
    results[name] = parse_web(FASTA)
    
with open('Bcepred-OmpA.json', 'w', encoding='utf-8') as f:
    json.dump(results, f)
"""













#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:14:34 2021

@author: shauangel
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re

class tcoffee:
    def parse_web(self, file):
        chrome = None
        try:
            chrome = webdriver.Chrome('./chromedriver')
        except:
            chrome = webdriver.Chrome('./chromedriver.exe')
        chrome.get("http://tcoffee.crg.cat/apps/tcoffee/do:regular")
        
        seqs = chrome.find_element_by_name('seqs')
        seqs.send_keys(file)
        
        send = chrome.find_element_by_xpath('//button[@type="submit"]')
        send.click()
        
        rid = chrome.current_url.split('=')[1]
        
        time.sleep(10)
        while(True):
            try:
                chrome.get("http://tcoffee.crg.cat/data/" + rid + "/result.fasta_aln")
                soup = BeautifulSoup(chrome.page_source, 'html.parser')
                pre = soup.find("pre")
                result = pre.text
                break
            except:
                continue
        chrome.close()
        return self.result_analyze(result)
    
    def result_analyze(self, text):
        result = {}
        seq = re.split(r'(>)', text)
        index = [d for d, s in enumerate(seq) if s == ">" ]
        seq = [ seq[ind]+seq[ind+1] for ind in index]
        for f in seq :
            pattern = re.compile(r'[[](.*?)[]]', re.S)
            result[re.findall(pattern, f)[0]] = f.split(']')[1].replace('\n', '')
        return result
        
        
        
        
"""
file = open("/Users/shauangel/Desktop/生資專題/portein_data/Dnak/FASTA/Dnak_all.txt")
FASTA = file.read()
test = tcoffee()
result = test.parse_web(FASTA)
print(result)
"""













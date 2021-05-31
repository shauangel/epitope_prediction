#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 11:28:03 2021

@author: shauangel
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import copy


class LBtope:
    
    def parse_web(self, FASTA):
        chrome = webdriver.Chrome('./chromedriver.exe')
        chrome.get("https://webs.iiitd.edu.in/raghava/lbtope/protein.php")
        
        seq = chrome.find_element_by_name('seq')
        seq.send_keys(FASTA)
        
        send = chrome.find_element_by_xpath('//input[@type="submit"]')
        send.click()
        
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        a = soup.find('a', string='click here ')
        
        return a['href']
    
    def get_result(self, urls):
        sys_result = copy.deepcopy(urls)
        for name, url in urls.items():
            sys_result[name]['PREDS'] = self.parse_result_web(url['PREDS'])
        return sys_result
    
    def parse_result_web(self, result_url):
        chrome = webdriver.Chrome('./chromedriver.exe')
        chrome.get(result_url)
        
        while(True):
            soup = BeautifulSoup(chrome.page_source, 'html.parser')
            pre = soup.find('pre')
            if pre == None :
                time.sleep(5)
            else:
                table = pre.find('table')
                fonts = table.find_all('font')
                chrome.close()
                result = ""
                for font in fonts:
                    try:
                        color = font["color"]
                        #print(font)
                        if (color == "#000000" or color == "#ff9900"):
                            result += '.'
                        elif (color == "#00ccff" or color == "#ff0000" or color == "#009900"):
                            result += 'E'
                    except:
                        continue
                break
            
        return result

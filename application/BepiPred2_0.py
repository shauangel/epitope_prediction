
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class Bepipred2:
    
    def parse_web(self, FASTA):
        chrome = None
        try:
            chrome = webdriver.Chrome('./chromedriver')
        except:
            chrome = webdriver.Chrome('./chromedriver.exe')
        chrome.get("http://www.cbs.dtu.dk/services/BepiPred/")
        
        seq = chrome.find_element_by_name('fasta')
        seq.send_keys(FASTA)
        
        send = chrome.find_element_by_xpath('//input[@type="submit"]')
        send.click()
        
        waiting = True
        while(waiting):
            soup = BeautifulSoup(chrome.page_source, 'html.parser')
            progress = soup.find(id="progress")
            if progress == None:
                epitope = soup.find('epitope-highlight')
                break
            else:
                time.sleep(5)
        
        chrome.close()
        seq = epitope.find_all('b')
        result = [word.text for word in seq]
        
        return "".join(result)
            
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
    
    

with open('BepiPred2.0-' + protein + '.json', 'w', encoding='utf-8') as f:
    json.dump(results, f)

"""

















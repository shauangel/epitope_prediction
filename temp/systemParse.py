#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 00:04:42 2021

@author: shauangel
"""
from bs4 import BeautifulSoup
import time
import requests

import db_connection as DB
#-----------------------------------------------------------------------------#
class ABCpred:
    def parse_web(self, FASTA):
        #直接向網頁發出request
        url = "https://webs.iiitd.edu.in/cgibin/abcpred/test1_main.pl"
        mydata = { "SEQNAME" : "test",
                   "SEQ" : FASTA.split('\n')[1],
                   "seqfile" : b"",
                   "Threshold" : 0.51,
                   "window" : 16,
                   "filter" : "on" }
        result = requests.post(url, data = mydata)   
        #bs4解析網頁內容，取得預測結果
        soup = BeautifulSoup(result.text, 'html.parser')
        pre = soup.find_all('pre')
        overlap_list = pre[2].get_text(separator = '\n').strip()        
        seq_list = overlap_list.split('\n')
        
        #轉換網頁結果至所需格式
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
            result += "E" if sum(test) > 1 else "."
        return result

#-----------------------------------------------------------------------------#
class BcePred:
    def parse_web(self, FASTA):
        #透過api取得response
        url = "https://webs.iiitd.edu.in/cgibin/bcepred/bcepred.pl"
        mydata = { "SEQNAME" : "",
                 "SEQ" : FASTA.split('\n')[1],
                 "seqfile" : b"",
                 "Threshold" : [2, 1.9, 2, 1.9, 2.4, 2.3, 1.8, 1.9],
                 "propno" : ["hydro", "flexi", "access", "turns", "surface", "polar", "antipro"]}
        web_result = requests.post(url, data = mydata)  
        
        #解析網頁資訊
        soup = BeautifulSoup(web_result.text, 'html.parser')
        
        try:
            table = soup.find_all('table')
            tds = table[0].find_all('td')
            fonts = tds[3].find_all('font')
        except:
            print(web_result.text)
            return "err"
            
        #轉換成所需格式
        result = ""
        for font in fonts:
            if font["color"] == "black":
                result += "."
            elif font["color"] == "blue":
                result += "E"
        return result
    
    
#-----------------------------------------------------------------------------#
class BCPREDS:
    def parse_web(self, FASTA):
        url = "http://ailab-projects1.ist.psu.edu:8080/bcpred/SimpleServlet"
        mydata = {"sequence" : FASTA.split('\n')[1],
                  "pmethod" : "bcpred",
                  "length" : 20,
                  "specificity" : 75,
                  "overlap" : "yes",
                  "submit" : "Submit query"}
        web_result = requests.post(url, data = mydata)        
        soup = BeautifulSoup(web_result.text, 'html.parser')
        try:
            fonts = soup.find_all('font', {'color' : 'red'})
        except:
            print(web_result.text)
            return "err"
        epitope = ""
        for result in fonts:
            epitope += result.text
        return epitope


#-----------------------------------------------------------------------------#
class Bepipred2:
    
    def parse_web(self, FASTA):
        url = "http://www.cbs.dtu.dk/cgi-bin/webface2.fcgi"
        mydata = {"configfile" : "/usr/opt/www/pub/CBS/services/BepiPred-2.0/lyra.cf",
                  "fasta" : FASTA.split('\n')[1],
                  "uploadfile" : b""}
        web_result = requests.post(url, data = mydata)
        soup = BeautifulSoup(web_result.text, 'html.parser')
        resultPageUrl = soup.find('noscript').find('a')['href']
        process_id = resultPageUrl.split('=')[1]
        
        while(1):
            result_web = requests.get(resultPageUrl)
            soup = BeautifulSoup(result_web.text, 'html.parser')
            progress = soup.find(id="progress")
            if progress == None:
                
                try:
                    result_json = "http://www.cbs.dtu.dk/services/BepiPred-2.0/tmp/" + process_id + "/results.json"
                    myjson = requests.get(result_json).json()
                    result = ["." if i < 0.5 else "E" for i in myjson["antigens"]['Sequence']['PRED']]
                    break
                except:
                    return "err"
            else:
                print(">>>still running")
                time.sleep(10)
        return "".join(result)
    

#-----------------------------------------------------------------------------#
class LBtope:
    ####需要header, 否則系統資訊會出錯
    def parse_web(self, FASTA):
        #送出序列資料
        url = "https://webs.iiitd.edu.in/raghava/lbtope/submitpro.php"
        mydata = {"seq" : FASTA,
                  "MAX_FILE_SIZE" : "",
                  "file" : b"",
                  "for" : "flx",
                  "expect" : 15,
                  "email" : "",
                  "val" : 60,
                  "send" : "Submit antigen for prediction"}
        web_result = requests.post(url, data = mydata)
        soup = BeautifulSoup(web_result.text, 'html.parser')
        #取得process id
        a = soup.find('a', string='click here ')['href'].split('=')[1]
        
        while(True):
            #結果目標api
            web_result = requests.get("https://webs.iiitd.edu.in/raghava/lbtope/vrindex/lbtope.php?ran=" + a)
            soup = BeautifulSoup(web_result.text, 'html.parser')
            #預測結果表格
            result_table = soup.find('pre').find('table')
            #檢查表格是否已出現（系統已完成預測）
            if result_table == None :
                print(">>>still running")
                time.sleep(20)
            else:
                try:
                    fonts = result_table.find_all('font')
                except:
                    return "err"
            
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


#-----------------------------------------------------------------------------#
class LEPS:
    def parse_web(self, FASTA):
        url = "https://leps.biolab.studio/LEPS/"
        mydata = {"secstru" : "on",
                  "secstruScale" : "betaturn_D_R",
                  "length5" : 7, "ws5" : 11, "ps5" : 11, "we5" : 0.4,
                  "hydrophi" : "on",
                  "hydrophiScale" : "hydropath_K_D",
                  "length1" : 7, "ws1" : 11, "ps1" : 11, "we1" : 0.3,
                  "surfacc" : "on",
                  "surfaccScale" : "surface_E_A",
                  "length3" : 7, "ws3" : 11, "ps3" : 11, "we3" : 0.15,
                  "flexi" : "on",
                  "flexiScale" : "flexi_K_S",
                  "length7" : 7, "ws7" : 11, "ps7" : 11, "we7" : 0.15,
                  "polarity" : "on",
                  "polarityScale" : "polarity_Z_E_S",
                  "length4" : 7, "ws4" : 11, "ps4" : 11, "we4" : 0,
                  "other" : "on",
                  "otherScale" : "mw",
                  "length6" : 3, "ws6" : 11, "ps6" : 11, "we6" : 0,
                  "wsAG" : 9, "psAG" : 9,
                  "entered" : True,
                  "thresh" : "avg",
                  "seq" : FASTA }
        web_result = requests.post(url, data = mydata)
        soup = BeautifulSoup(web_result.text, 'html.parser')
        
        try:
            prediction = soup.find('div', {'class' : 'peakSubSeq finalResult'})
            ranges = prediction.find_all('div', {'class' : 'range'})
        except:
            print(web_result.text)
            return "err"
            
        FASTA_len = len(FASTA.split('\n')[1])
        range_result = [r.text.split('~') for r in ranges]
        result = "."*FASTA_len
        for r in range_result:
            start = int(r[0])-1
            end = int(r[1])
            E = 'E'*len(result[start:end])
            result = result[:start] + E + result[end:]
        return result



if __name__ == "__main__":
    
    data = DB.SEQ_COLLECTION.find_one({"seq_id" : "P15252"})
    FASTA = "\n".join([data['FASTA'].split('\n')[0],"".join(data['FASTA'].split('\n')[1:])])
    print(FASTA.split('\n')[1])
    print(len(FASTA.split('\n')[1]))
    
    """
    sys = ABCpred()
    result = sys.parse_web(FASTA.replace(" ", ""))
    print(len(result))
    
    """
    
    test = "MWRSLGLALALCLLPSGGTESQDQSSLCKQPPAWSIRDQDPMLNSNGSVTVVALLQASYLCILQASKLEDLRVKLKKEGYSNISYIVVNHQGISSRLKYTHLKNKVSEHIPVYQQEENQTDVWTLLNGSKDDFLIYDRCGRLVYHLGLPFSFLTFPYVEEAIKIAYCEKKCGNCSLTTLKDEDFCKRVSLATVDKTVETPSPHYHHEHHHNHGHQHLGSSELSENQQPGAPNAPTHPAPPGLHHHHKHKGQHRQGHPENRDMPASEDLQDLQKKLCRKRCINQLLCKLPTDSELAPRSCCHCRHLIFEKTGSAITQCKENLPSLCSQGLRAEENITESCQRLPPAAQISQQLIPTEASASRKNQAKKEPSN"
    print(test)
    print(len(test))












    
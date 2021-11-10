import json
import csv

#change here
sys="w9"

dic={}
with open("epitope_data.json", 'r') as obj:
    tmp = json.load(obj)

for i in tmp:
    try:
        dic[i["seq_id"]]+=[i["epitope"]]
    except:
        dic[i["seq_id"]]=[i["epitope"]]


with open("json/"+sys+"_result.json", 'r') as obj:
    tmp = json.load(obj)

ans={}
data={}
for i in tmp:
    data[i["id"]]={}
    data[i["id"]]["result"]=i["result"]
    data[i["id"]]["seq"]=i["seq"]

#print(data)

for i in dic:
    if i in data:
        ans[i] = "." * len(data[i]["seq"])
        for s in dic[i]:
            if ',' not in s:
                pos = data[i]["seq"].find(s)
                if pos==-1:
                    print(i+"->"+s+" ERROR")
                    continue
                ans[i] = ans[i][:pos] + ("E" * len(s))+ ans[i][pos+len(s):]
            else:
                bcell=s.split(", ")
                for b in bcell:
                    pos=int(b[1:])
                    ans[i]= ans[i][:pos] + 'E' + ans[i][pos+1:]



amino=["A","F","C","D","N","E","Q","G","H","L","I","K","M","P","R","S","T","V","W","Y"]
ptotal = {}
ntotal = {}
pcorrect = {}
ncorrect = {}
for i in amino:
    ptotal[i]=0
    pcorrect[i]=0
    ntotal[i]=0
    ncorrect[i]=0
for i in amino:
    for j in amino:
        ptotal[i+j]=0
        pcorrect[i+j]=0
        ntotal[i+j]=0
        ncorrect[i+j]=0


for i in ans:
    #print(i)
    #print(ans[i])
    for j in range(len(ans[i])):
        try:
            if ans[i][j]=='E':
                ptotal[data[i]["seq"][j]]+=1
                if data[i]["result"][j]=='E':
                    pcorrect[data[i]["seq"][j]]+=1
                if (j+1)<len(ans[i]):
                    if ans[i][j+1]=='E':
                        ptotal[data[i]["seq"][j:j+2]]+=1
                        if data[i]["result"][j:j+2]=='EE':
                            pcorrect[data[i]["seq"][j:j+2]]+=1
        except:
            pass

#neg
for i in ans:
    for j in range(len(ans[i])):
        try:
            if ans[i][j]=='.':
                ntotal[data[i]["seq"][j]]+=1
                if data[i]["result"][j]=='.':
                    ncorrect[data[i]["seq"][j]]+=1
                if (j+1)<len(ans[i]):
                    if ans[i][j+1]=='.':
                        ntotal[data[i]["seq"][j:j+2]]+=1
                        if data[i]["result"][j:j+2]=='..':
                            ncorrect[data[i]["seq"][j:j+2]]+=1
        except:
            pass


with open('pn/'+sys+'_pn.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    #all F1_score
    pt=pc=nt=nc=TP=FN=FP=TN=precision=recall=F1score=0
    for i in amino:
        pt+=ptotal[i]
        nt+=ntotal[i]
        pc+=pcorrect[i]
        nc+=ncorrect[i]
    TP=pc/pt
    FP=1-TP
    TN=nc/nt
    FN=1-TN
    precision = TP/(TP+FP)
    recall = TP/(TP+FN)
    F1score = 2 * ((precision*recall) / (precision+recall))
    writer.writerow([sys+" F1_score", F1score])


    writer.writerow(['amino', 'TP', 'tp_correct', 'tp_total', 'TN', 'tn_correct', 'tn_total','F1_score'])
    for i in ptotal:
        TP=FN=FP=TN=precision=recall=F1score=0
        if ptotal[i]!=0:
            TP=pcorrect[i]/ptotal[i]
            FP=1-TP
        if ntotal[i]!=0:
            TN=ncorrect[i]/ntotal[i]
            FN=1-TN
        try:
            precision = TP/(TP+FP)
        except:
            pass
        try:
            recall = TP/(TP+FN)
        except:
            pass
        try:
            F1score = 2 * ((precision*recall) / (precision+recall))
        except:
            pass
        writer.writerow([i, TP, pcorrect[i], ptotal[i], TN, ncorrect[i], ntotal[i],F1score])


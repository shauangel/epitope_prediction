import csv

sys=["ABCpred","BcePred","BCPREDS","Bepipred2_0","LBtope","LEPS"]
amino=["A","F","C","D","N","E","Q","G","H","L","I","K","M","P","R","S","T","V","W","Y"]

fscore={}
for sysname in sys:
    with open("pn/"+sysname+'_pn.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        tmp = list(rows)
        dict_tmp = {}
        for i in tmp:
            if len(i[0])<3:
                dict_tmp[i[0]]=float(i[7])
        fscore[sysname]=dict_tmp

#print(fscore)

with open('weighting.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["amino"]+sys)
    for i in amino:
        ABC=fscore["ABCpred"][i]
        Bce=fscore["BcePred"][i]
        BCP=fscore["BCPREDS"][i]
        Bep=fscore["Bepipred2_0"][i]
        LBt=fscore["LBtope"][i]
        LEP=fscore["LEPS"][i]
        deno=ABC+Bce+BCP+Bep+LBt+LEP
        try:
            writer.writerow([i,ABC/deno,Bce/deno,BCP/deno,Bep/deno,LBt/deno,LEP/deno])
        except:
            writer.writerow([i,0,0,0,0,0,0])
    for i in amino:
        for j in amino:
            ABC=fscore["ABCpred"][i+j]
            Bce=fscore["BcePred"][i+j]
            BCP=fscore["BCPREDS"][i+j]
            Bep=fscore["Bepipred2_0"][i+j]
            LBt=fscore["LBtope"][i+j]
            LEP=fscore["LEPS"][i+j]
            deno=ABC+Bce+BCP+Bep+LBt+LEP
            try:
                writer.writerow([i+j,ABC/deno,Bce/deno,BCP/deno,Bep/deno,LBt/deno,LEP/deno])
            except:
                writer.writerow([i+j,0,0,0,0,0,0])
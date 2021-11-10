import csv

def vote_func(data): #傳入字典
    tc=""
    each=[]
    sys=[]
    perc = data["range"]
    minnum = data["min lenth"]
    vote_6sys = {}
    for e in data["sys"]:
        sys+=[e]
        name=[]
        PREDS=[]
        tcoffee=[]
        n=[]
        #open json
        for i in data["sys"][e]["data"]:
            name+=[i]
            PREDS+=[data["sys"][e]["data"][i]["PREDS"]]
            if PREDS == "":
                PREDS = "." * len(data["sys"][e]["data"][i]["t-coffee"])
            tcoffee+=[data["sys"][e]["data"][i]["t-coffee"]]
            f=data["sys"][e]["f"]
            n+=[0]

        #去換行
        for i in range(len(tcoffee)):
            tcoffee[i]=tcoffee[i].replace("\n","")

        #系統內投票
        for i in range(len(name)):
            for j in range(len(tcoffee[i])):
                if tcoffee[i][j]=='-':
                    PREDS[i]=PREDS[i][:j]+'-'+PREDS[i][j:]

        tc=tcoffee[0]
        tmp=""
        vote_tmp=[]
        for i in range(len(tcoffee[0])):
            c=0
            c1=len(name)
            for j in range(len(name)):
                if PREDS[j][i]=='E':
                    c+=1
            vote_tmp += [c]
            if c/c1>=f:
                tmp=tmp+"E"
            elif c/c1<f:
                tmp=tmp+"."
        each+=[tmp]
        vote_6sys[e] = vote_tmp

    #去掉"-"
    for i in range(len(tc)-1,-1,-1):
        if tc[i]=='-':
            tc = tc[:i] + tc[i+1:]
            for j in range(len(each)):
                each[j] = each[j][:i] + each[j][i+1:]

    #整合投票
    fscore={"ABCpred":{},"BcePred":{},"BCPREDS":{},"Bepipred2_0":{},"LBtope":{},"LEPS":{}}
    with open('weighting.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        tmp = list(rows)
        for i in tmp:
            if len(i[0])<3:
                fscore["ABCpred"][i[0]] = float(i[1])
                fscore["BcePred"][i[0]] = float(i[2])
                fscore["BCPREDS"][i[0]] = float(i[3])
                fscore["Bepipred2_0"][i[0]] = float(i[4])
                fscore["LBtope"][i[0]] = float(i[5])
                fscore["LEPS"][i[0]] = float(i[6])


    start=-1
    result = tc
    vote = []
    epitope = []
    sclist = []
    EEEE = "." * len(tc)
    for i in range(len(tc)):
        c = score = 0
        for j in range(len(each)):
            if each[j][i]=='E':
                c += 1
                try:
                    if i==0:
                        score += ( fscore[sys[j]][tc[i]] + fscore[sys[j]][tc[i:i+2]] )/2
                    elif i == len(tc)-1:
                        score += ( fscore[sys[j]][tc[i]] + fscore[sys[j]][tc[i-1:i+1]] )/2
                    else:
                        score += ( fscore[sys[j]][tc[i]] + fscore[sys[j]][tc[i-1:i+1]] + fscore[sys[j]][tc[i:i+2]] )/3

                except:
                    score = 0
        vote += [c]
        sclist += [score]
        if score>=perc and start<=0:
            start=i
        elif score<perc and start>0:
            if (i-start)>=minnum:
                dict_tmp = {"range" : str(start) + "-" + str(i-1), "seq" : tc[start:i]}
                epitope += [dict_tmp]
                EEEE = EEEE[:start] + "E"*(i-start) + EEEE[i:]
            start=-1

    rtn = {
            "result" : result,
            "EEEE" : EEEE,
            "vote" : vote,
            "score" : sclist,
            "vote_6sys" : vote_6sys,
            "epitope" : epitope
        }
    return rtn


if __name__ == "__main__":
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#test
"""
a={
    "sys":{
        "ABCpred":{
            "data":{
                "Vibrio brasiliensis": {
                    "PREDS":"..........................................................................................EEE.....EEEEEE..EEEEEEEE..E.........................................................................................................E.E..E........................................................................................................................",
                    "t-coffee":"MN\nKTLIALAVSAAA\nVATGANAAEIYSQDGNSIEMGGRAEAR\n\nLSLK---------------DGKAEDNSRVRLNFLGKAQITDGLYGVGFYEGEFTTADNGGETDSNSDSLTNRYAYAGLGG-AFGEITYGKNDGALGVITDFTDIMAYHGNS-AAMKINVADRADNMISYKGQFADLGVKASYRFADRTELNAAGNVATGNEAVASYGDNDADGYSLSAIYAIGDTGVKLGGGYASQYSGA-------QEQNEYMLAASYAISDFYFAGTFTDGQLAE------ENADYTGYEFATAYTLDKTVFTATYNNAETDS-------ETSADNVAIDATYYFKPNFRGYVSYNFNLISEGDAYGKVGANGTATKADAEDEIALGLRYDF",
                }
            },
            "f":0.3
        },
        "BcePred":{
            "data":{
                "Vibrio brasiliensis": {
                    "PREDS":".............EEEEEEE.EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE..EEEE..EEEEEEEEEE..EEEE..........EE.......EEEEEEE..EEEEEEE...EEEEEE.EEEEEEEEEEEEEEEEEEEEEE..EEEE..EEEEEEEEEE..EEEE......EEEEEE.......EEE......EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE.......EEE.....EEEEEEEE....EEEE.......EEEEE.....EEEEEE.EEEEEEEEE.EEEEEE.........E.........EEEEEEEEEEEEEEEE.EEEEE....EEEEEEEEEEEEEEEE...........",
                    "t-coffee":"MNKTLIALAVSAAAVATGANAAEIYSQDGNSIEMGGRAEARLSLK---------------DGKAEDNSRVRLNFLGKAQITDGLYGVGFYEGEFTTADNGGETDSNSDSLTNRYAYAGLGG-AFGEITYGKNDGALGVITDFTDIMAYHGNS-AAMKINVADRADNMISYKGQFADLGVKASYRFADRTELNAAGNVATGNEAVASYGDNDADGYSLSAIYAIGDTGVKLGGGYASQYSGA-------QEQNEYMLAASYAISDFYFAGTFTDGQLAE------ENADYTGYEFATAYTLDKTVFTATYNNAETDS-------ETSADNVAIDATYYFKPNFRGYVSYNFNLISEGDAYGKVGANGTATKADAEDEIALGLRYDF"
                }
            },
            "f":0.3
        },
        "BCPREDS":{
            "data":{
                "Vibrio brasiliensis": {
                    "PREDS":"..........................................................................................EEE.....EEEEEE..EEEEEEEE..E.........................................................................................................E.E..E........................................................................................................................",
                    "t-coffee":"MN\nKTLIALAVSAAA\nVATGANAAEIYSQDGNSIEMGGRAEAR\n\nLSLK---------------DGKAEDNSRVRLNFLGKAQITDGLYGVGFYEGEFTTADNGGETDSNSDSLTNRYAYAGLGG-AFGEITYGKNDGALGVITDFTDIMAYHGNS-AAMKINVADRADNMISYKGQFADLGVKASYRFADRTELNAAGNVATGNEAVASYGDNDADGYSLSAIYAIGDTGVKLGGGYASQYSGA-------QEQNEYMLAASYAISDFYFAGTFTDGQLAE------ENADYTGYEFATAYTLDKTVFTATYNNAETDS-------ETSADNVAIDATYYFKPNFRGYVSYNFNLISEGDAYGKVGANGTATKADAEDEIALGLRYDF",
                }
            },
            "f":0.3
        },
        "Bepipred2_0":{
            "data":{
                "Vibrio brasiliensis": {
                    "PREDS":"..........................................................................................EEE.....EEEEEE..EEEEEEEE..E.........................................................................................................E.E..E........................................................................................................................",
                    "t-coffee":"MN\nKTLIALAVSAAA\nVATGANAAEIYSQDGNSIEMGGRAEAR\n\nLSLK---------------DGKAEDNSRVRLNFLGKAQITDGLYGVGFYEGEFTTADNGGETDSNSDSLTNRYAYAGLGG-AFGEITYGKNDGALGVITDFTDIMAYHGNS-AAMKINVADRADNMISYKGQFADLGVKASYRFADRTELNAAGNVATGNEAVASYGDNDADGYSLSAIYAIGDTGVKLGGGYASQYSGA-------QEQNEYMLAASYAISDFYFAGTFTDGQLAE------ENADYTGYEFATAYTLDKTVFTATYNNAETDS-------ETSADNVAIDATYYFKPNFRGYVSYNFNLISEGDAYGKVGANGTATKADAEDEIALGLRYDF",
                }
            },
            "f":0.3
        },
        "LBtope":{
            "data":{
                "Vibrio brasiliensis": {
                    "PREDS":"..........................................................................................EEE.....EEEEEE..EEEEEEEE..E.........................................................................................................E.E..E........................................................................................................................",
                    "t-coffee":"MN\nKTLIALAVSAAA\nVATGANAAEIYSQDGNSIEMGGRAEAR\n\nLSLK---------------DGKAEDNSRVRLNFLGKAQITDGLYGVGFYEGEFTTADNGGETDSNSDSLTNRYAYAGLGG-AFGEITYGKNDGALGVITDFTDIMAYHGNS-AAMKINVADRADNMISYKGQFADLGVKASYRFADRTELNAAGNVATGNEAVASYGDNDADGYSLSAIYAIGDTGVKLGGGYASQYSGA-------QEQNEYMLAASYAISDFYFAGTFTDGQLAE------ENADYTGYEFATAYTLDKTVFTATYNNAETDS-------ETSADNVAIDATYYFKPNFRGYVSYNFNLISEGDAYGKVGANGTATKADAEDEIALGLRYDF",
                }
            },
            "f":0.3
        },
        "LEPS":{
            "data":{
                "Vibrio brasiliensis": {
                    "PREDS":"..........................................................................................EEE.....EEEEEE..EEEEEEEE..E.........................................................................................................E.E..E........................................................................................................................",
                    "t-coffee":"MN\nKTLIALAVSAAA\nVATGANAAEIYSQDGNSIEMGGRAEAR\n\nLSLK---------------DGKAEDNSRVRLNFLGKAQITDGLYGVGFYEGEFTTADNGGETDSNSDSLTNRYAYAGLGG-AFGEITYGKNDGALGVITDFTDIMAYHGNS-AAMKINVADRADNMISYKGQFADLGVKASYRFADRTELNAAGNVATGNEAVASYGDNDADGYSLSAIYAIGDTGVKLGGGYASQYSGA-------QEQNEYMLAASYAISDFYFAGTFTDGQLAE------ENADYTGYEFATAYTLDKTVFTATYNNAETDS-------ETSADNVAIDATYYFKPNFRGYVSYNFNLISEGDAYGKVGANGTATKADAEDEIALGLRYDF",
                }
            },
            "f":0.3
        },
    },
    "min lenth": 5,
    "range": 0.5
}

#print(vote_func(a))
#vote_func(a)
"""
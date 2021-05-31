
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
            for j in range(len(tcoffee[i])-1,-1,-1):
                if tcoffee[i][j]=="\n":
                    tcoffee[i] = tcoffee[i][:j] + tcoffee[i][j+1:]

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
    start=-1
    result = tc
    vote = []
    epitope = []
    for i in range(len(tc)):
        c=0
        c1=len(each)
        for j in range(len(each)):
            if each[j][i]=='E':
                c+=1
        vote += [c]
        if c/c1>=perc and start<=0:
            start=i
        elif c/c1<perc and start>0:
            if (i-start)>=minnum:
                #print( str(start-2) + "-" + str(i-3) )
                #print( tc[start:i] )
                dict_tmp = {"range" : str(start) + "-" + str(i-1), "seq" : tc[start:i]}
                epitope += [dict_tmp]
            start=-1

    rtn = {
            "result" : result,
            "vote" : vote,
            "vote_6sys" : vote_6sys,
            "epitope" : epitope
        }
    return rtn


#test
a={
    "sys":{
        "LBtope":{
            "data":{
                "Vibrio brasiliensis": {
                    "PREDS":"..........................................................................................EEE.....EEEEEE..EEEEEEEE..E.........................................................................................................E.E..E........................................................................................................................",
                    "t-coffee":"MN\nKTLIALAVSAAA\nVATGANAAEIYSQDGNSIEMGGRAEAR\n\nLSLK---------------DGKAEDNSRVRLNFLGKAQITDGLYGVGFYEGEFTTADNGGETDSNSDSLTNRYAYAGLGG-AFGEITYGKNDGALGVITDFTDIMAYHGNS-AAMKINVADRADNMISYKGQFADLGVKASYRFADRTELNAAGNVATGNEAVASYGDNDADGYSLSAIYAIGDTGVKLGGGYASQYSGA-------QEQNEYMLAASYAISDFYFAGTFTDGQLAE------ENADYTGYEFATAYTLDKTVFTATYNNAETDS-------ETSADNVAIDATYYFKPNFRGYVSYNFNLISEGDAYGKVGANGTATKADAEDEIALGLRYDF",
                }, 
                "Aliivibrio fischeri": {
                    "PREDS":".........................E.E..E..................................E.............EEEEEE.E........................................................................E.........................................................EE.................................E.............................................EE..EEE.EEEEEE.........",
                    "t-coffee":"MNKKVLALAVAAITSAGAVNAAELYKDEAQ\nSIEMGGRAEARLAMK---------------DGDAADNTRIRLNFKGTTQISDGLYGVGFWEGEFTTNDAV----NPNGNLENRYTYAGIGG-NFGEVTYGKNDGALGVITDFTDIMAYHGNS-AAYKLAVADREDNAIAYKGQFGDFAFKANYRFDDAAA-----------------NQESNDGFSTSGIYAFGDSGFKLGAGYADQG-----------TDNEAMVAGSMTMGDFYFAGTFTTGEVV--------DLDYTGFEVAGAYTMGKTVFTATYNNADHDTNALTVANNENADNFAVDATYFFNANFRTYISYNLNLLDDDAL-K------GITKAMTEDEVALGMRYDF",
                    }, 
                "Enterovibrio norvegicus": {
                    "PREDS":"..................EEEEEEEEEEEEEEE...............................E.............E.............E.....EEEE......E........................EE........EEEE.................................................EEEEEEE......E...............EEE.E.E...E...E.....................................................EEEE............",
                    "t-coffee":"MNKTFIALAVAALA-STSVSAA\n\nEIFNDGTSSMAIGGRAEARASIK---------------DGDMNDASRVRINVLGTTQISEEAYGVGFFEREFKSNK---------DSDENRYLFAGIGT-EYGLVTYGKNDGSLGMITDFTDIMSYHGAA-ASSKITVADRTDNNIAYKGEFGGLTVKANYVGNN---------------------ETIDKGYSLGAVYAM-ENGLAMGLGYADQDNLT------KTTESQIEAAVSYTMGDIYVAALYKDGESNV----SGSDKDLTGYELAAAYTMGQTKFTTTYGKAETES-------DDTADSIAIDATHYFNGNFRTYASYNFNLLDADK----------VGKAKAEDELVFGLRYDF",
                }, 
                "Grimontia hollisae": {
                    "PREDS":".................EEEEEEEEEE...E.....E.................................EEEEEEEEEEEEEEEEEEE..............EEEEE.................................EEEEEEEEEEEEEE........................................................................E...............E..............................................................E...E..EEEE............",
                    "t-coffee":"MNKKLIALAVAAVA-STSVSAAEIFNDG\nTSSLAIGGRAEARAAIK---------------DGDVNDNSRVRLNVMGTTQIAEGAYGIGFFEQEFTTNDAV----PDGEKDETRYLFAGIGS-DYGLVTYGKNDGSLGVITDFTDIMAYHGNG-AGAKIAVADRTDNNLGYMGEFGGLTVKANYVFDTVSEGINN-----------TVRTDRVGGYSASAIYNF-DFGLALGLGYADQGKND------IDAESQAMAAASYTVGDFYFAGLFADGEFGQ----GVYHTETAGFELAAAYTMNQTKFTATYNYQEAEMAG---IKYDTVDQIAIDATHFFNDNFRAYASYNFNLLDEKDV---------AHKLDAEDELVFGLRYDF",
                }, 
                "Photobacterium phosphoreum": {
                    "PREDS":"...........................................................................................................E...................EE...........................EEEEE.EEEEEE.........EE....E.E.....EEEEE...................E...EEE........................EE.................E.EE..................EEEE.......................................E......................",
                    "t-coffee":"MNKNLIA\nLAVAAATFSGAASAATVYSDDTSSLAIGGRVEARALLSENAKNENAPLLTQQTSNDVTDISRVRVNIDAKTQIADGVQGIGYFEREFKSDN---------ANDENRYMYAGVNSDKYGQIVYGKADGSLGMITDFTDIMAYAGSVVGGSKLAVSDRTSNNLAYSGTFNNLTFKANYVFDGAAYN-DT-----------TGQKTNQNGFSTAAKYTVGDTGLALGVGYAQQKDQTAANNSVNQTSKQTFAVASYTIGDLYFGGLYKYGHRDATNLVTNDLTDSQGYEFAAAYTMGKAVFTTTYGFMKDERNT-SGAYDELANAVSVDGTYYFNSNFRTYASYTYNMLDKNK----------VGKVAASDQVVLGARYDF",
                }
            },
            "f":0.3
        },
        "ABCpred":{
            "data":{
                "Vibrio brasiliensis": {
                    "PREDS":".............EEEEEEE.EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE..EEEE..EEEEEEEEEE..EEEE..........EE.......EEEEEEE..EEEEEEE...EEEEEE.EEEEEEEEEEEEEEEEEEEEEE..EEEE..EEEEEEEEEE..EEEE......EEEEEE.......EEE......EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE.......EEE.....EEEEEEEE....EEEE.......EEEEE.....EEEEEE.EEEEEEEEE.EEEEEE.........E.........EEEEEEEEEEEEEEEE.EEEEE....EEEEEEEEEEEEEEEE...........",
                    "t-coffee":"MNKTLIALAVSAAAVATGANAAEIYSQDGNSIEMGGRAEARLSLK---------------DGKAEDNSRVRLNFLGKAQITDGLYGVGFYEGEFTTADNGGETDSNSDSLTNRYAYAGLGG-AFGEITYGKNDGALGVITDFTDIMAYHGNS-AAMKINVADRADNMISYKGQFADLGVKASYRFADRTELNAAGNVATGNEAVASYGDNDADGYSLSAIYAIGDTGVKLGGGYASQYSGA-------QEQNEYMLAASYAISDFYFAGTFTDGQLAE------ENADYTGYEFATAYTLDKTVFTATYNNAETDS-------ETSADNVAIDATYYFKPNFRGYVSYNFNLISEGDAYGKVGANGTATKADAEDEIALGLRYDF"
                }, 
                "Aliivibrio fischeri": {
                    "PREDS":".............EEEEEEE......EEE......................EEEEEEEEEE..EEEE..EEEEEEEEEEEEEEEE...................EEEEEEEEEEEEEEEE...EEE......EEEEEEEEEEEEEEEE..EEEE..EEEEEEEEEEEEEEEEEEEEEEEEEEEEE................EEEEEEEEE...EEEE...........E.............EE.........EEEEE...EEEEEEEE....EEEE......EEEEEE..EEEEEEEEEEEEEEEEEEEEEE......EEE......EEEEEEEEEEEEEEEE............",
                    "t-coffee":"MNKKVLALAVAAITSAGAVNAAELYKDEAQSIEMGGRAEARLAMK---------------DGDAADNTRIRLNFKGTTQISDGLYGVGFWEGEFTTNDAV----NPNGNLENRYTYAGIGG-NFGEVTYGKNDGALGVITDFTDIMAYHGNS-AAYKLAVADREDNAIAYKGQFGDFAFKANYRFDDAAA-----------------NQESNDGFSTSGIYAFGDSGFKLGAGYADQG-----------TDNEAMVAGSMTMGDFYFAGTFTTGEVV--------DLDYTGFEVAGAYTMGKTVFTATYNNADHDTNALTVANNENADNFAVDATYFFNANFRTYISYNLNLLDDDAL-K------GITKAMTEDEVALGMRYDF",
                }, 
                "Enterovibrio norvegicus": {
                    "PREDS":"..........EEEEEEE.EEEEEEEE......................EEEEE...................EEEEEEEEE................EEEEEEEEEE..................EEEEEEEEEEEEEEEE.........................................EEEE..EEEEEEEEEEEEEEEEEEEEEEEEE.....E.....EEEEEEEEEE.EEEEE....EEEEEEE...EEEEEE...EEEEEEEEEEEEEEEEEEEEEEEEEEEEE.....EEEE.....EEEEEEE...EEEEEE..........",
                    "t-coffee":"MNKTFIALAVAALA-STSVSAAEIFNDGTSSMAIGGRAEARASIK---------------DGDMNDASRVRINVLGTTQISEEAYGVGFFEREFKSNK---------DSDENRYLFAGIGT-EYGLVTYGKNDGSLGMITDFTDIMSYHGAA-ASSKITVADRTDNNIAYKGEFGGLTVKANYVGNN---------------------ETIDKGYSLGAVYAM-ENGLAMGLGYADQDNLT------KTTESQIEAAVSYTMGDIYVAALYKDGESNV----SGSDKDLTGYELAAAYTMGQTKFTTTYGKAETES-------DDTADSIAIDATHYFNGNFRTYASYNFNLLDADK----------VGKAKAEDELVFGLRYDF",
                }, 
                "Grimontia hollisae": {
                    "PREDS":"............EEEEEEEEE.............................E......EEEEEEEEEEEEEEEE................EEEEEEE.EEEEEEEE.EEEEEEE....EEEEE.EEEEEEEEEE..EEEE..EEEEEEEEEEEEEEEEEEEEEEE....EE.........EEEEE.......EEEE......EEEEEE.....EEEEE..EEEEEEEEE...EEEE..EEEEEEEEEEEEEEEE....EEEEEE....EEEEEE.EEEEEEEEEEEEEEEEEEEEEE.....EEE..........EEE......EEEEEEE....EEEEE...........",
                    "t-coffee":"MNKKLIALAVAAVA-STSVSAAEIFNDGTSSLAIGGRAEARAAIK---------------DGDVNDNSRVRLNVMGTTQIAEGAYGIGFFEQEFTTNDAV----PDGEKDETRYLFAGIGS-DYGLVTYGKNDGSLGVITDFTDIMAYHGNG-AGAKIAVADRTDNNLGYMGEFGGLTVKANYVFDTVSEGINN-----------TVRTDRVGGYSASAIYNF-DFGLALGLGYADQGKND------IDAESQAMAAASYTVGDFYFAGLFADGEFGQ----GVYHTETAGFELAAAYTMNQTKFTATYNYQEAEMAG---IKYDTVDQIAIDATHFFNDNFRAYASYNFNLLDEKDV---------AHKLDAEDELVFGLRYDF",
                }, 
                "Photobacterium phosphoreum": {
                    "PREDS":"...........EEEEEE..EEEEEEEE...EEEEE....EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE....EEEEEE.......EEE......EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE.EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE.EEEEE..........................EEEE.......EEEEE.....EEEEEEEEEEEEEEEE..EEEE..EEEEEEEEEEEEEEEE......EEE...EEEEEEEEEEEEEEEE......EEE.....EEEEEEEE..EEEEEE..........",
                    "t-coffee":"MNKNLIALAVAAATFSGAASAATVYSDDTSSLAIGGRVEARALLSENAKNENAPLLTQQTSNDVTDISRVRVNIDAKTQIADGVQGIGYFEREFKSDN---------ANDENRYMYAGVNSDKYGQIVYGKADGSLGMITDFTDIMAYAGSVVGGSKLAVSDRTSNNLAYSGTFNNLTFKANYVFDGAAYN-DT-----------TGQKTNQNGFSTAAKYTVGDTGLALGVGYAQQKDQTAANNSVNQTSKQTFAVASYTIGDLYFGGLYKYGHRDATNLVTNDLTDSQGYEFAAAYTMGKAVFTTTYGFMKDERNT-SGAYDELANAVSVDGTYYFNSNFRTYASYTYNMLDKNK----------VGKVAASDQVVLGARYDF",
                }
            },
            "f":0.3
        }
    },
    "min lenth": 5,
    "range": 0.5
}

print(vote_func(a))
# -*- coding: utf-8 -*-
'''
大考中心字表計數(請叫Vex.Count(...))
輸入：檔案(open(...))，是否轉換成原形(預設False)，是否改以頻率作為特徵(預設False)
輸出：特徵串列
同一個子目錄裡要有vex.txt和anc.txt
'''
import nltk

def clean(s, oth = ''):
    fomart = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\'- '
    for c in s:
        if not c in fomart:   
            s = s.replace(c,'')   
    s = s.lower()
    return s

TSL = dict()
def Count(fl, trans = None, fqc = None):
    if trans == None:
        trans = False
    if fqc == None:
        fqc =False
    level = 0

    #用anc建 變化型-原形 字典TSL
    for line in open("C:/Users/user/Documents/web/paragraph/background/anc.txt",'r',encoding='latin1'):
        t = line.split('\t')
        if t[0] not in TSL:
            #Np            print(t[0])
            if trans == True:
                #np                print("True")
                TSL[t[0]] = t[1]
            else:
                TSL[t[0]] = t[0]

    #大考中心字表         
    nbr = dict()    #numbering；編號
    cnt = [ 0, 0, 0, 0, 0, 0, 0 ]    #count；出現次數。cnt[0~6]
    for line in open("C:/Users/user/Documents/web/paragraph/background/vex.txt", 'r',encoding='latin1'):
        if line.startswith("LEVEL"):
            line = line.split(' ')
            level = int(line[1])
            #Np            print(str(level))
            continue
        if line not in nbr:
            line = line.split("\n")
            line = line[0]
            #            print(line)
            if line in TSL:
                ######                print(line)
                nbr[ TSL[line] ] = level
             
    lenth = 0.0
    for line in fl:
        #No problem.        print(line)
        line = clean(line)       #這個轉換有把重要訊息去掉的風險，但值得嘗試
        #No problem.        print(line)
        tkn = nltk.word_tokenize(line)
        #No problem.        print(tkn)
        for item in tkn:
            #Np            print(item)
            if item in TSL:
                #Np                print(item)
                item = TSL[item]
                #Np                print(item)
                if item in nbr:
                    ########                    print(item)
                    cnt[ nbr[item] ] += 1
                    #######                    print(cnt[nbr[item]])
                    lenth += 1.0
    #    print(str(lenth))
                    
    feature = []
    for num in range(6):
        item = cnt[ num + 1 ]
        if fqc == True:
            feature.append(100*(float(item)/lenth))
        else:
            feature.append(item)
    #    print feature
    return feature

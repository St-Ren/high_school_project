# -*- coding: utf-8 -*-
'''
單字計數(請叫Word.Count(...))
輸入：檔案(open(...))，幾個單字一組(預設1，即不分組)，
     是否轉換成原形(預設False)，是否改以頻率作為特徵（預設False）
輸出：特徵串列
同一個子目錄裡要有anc.txt
'''
import nltk

def clean(s,oth=''):
    fomart = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\'- '
    for c in s:
        if not c in fomart:   
            s = s.replace(c,'')   
    s = s.lower()
    return s

TSL = dict()
def AncBuild(T):
    opt = []
    for line in open("C:/Users/user/Documents/web/paragraph/background/anc.txt",'r',encoding='latin1'):
        t = line.split('\t')
        if t[0] not in TSL:
            if T == True:
                TSL[t[0]] = t[1]
                opt.append(t[1].lower())#
            else:
                opt.append(t[0].lower())#
    return opt

def Count(fl, g = None, trans = None, fqc = None):
    if g == None:
        g = 1
    if trans == None:
        trans = False
    if fqc == None:
        fqc = False
    nbr = dict()    #numbering；編號
    cnt = list()    #count；出現次數
    dic = AncBuild(trans)
    i = 0
    for item in dic:
        if item not in nbr:
            nbr[item] = i
            cnt.append(0)
            i += 1          
    lenth = 0.0
    for line in fl:
        line = clean(line)       #這個轉換有把重要訊息去掉的風險，但值得嘗試
        tkn = nltk.word_tokenize(line)
        if trans == True:
            tmp = tkn
            tkn = []
            for item in tmp:
                if item in TSL:
                    tkn.append(TSL[item])
        for item in tkn:
            if item in nbr:
                cnt[nbr[item]] += 1
                lenth += 1.0
    i = 0
    s = 0
    feature = []
    for item in cnt:
        s += item
        i += 1
        if i == g:
            if fqc == True:
                feature.append(float(s)*1000/lenth)
            else:
                feature.append(s)
            i = 0
            s = 0
            continue
    return feature

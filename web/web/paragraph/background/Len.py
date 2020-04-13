# -*- coding: utf-8 -*-
'''
平均句長(請叫Len.tkn(...))
輸入：檔案(open(...),是否要平均句長(預設True)，是否要字數(預設True), 是否要句數(預設是True))
輸出：特徵串列

各句長句比例(請叫Len.Count(...))
輸入：檔案(open(...))
輸出：特徵串列
'''
import nltk
import re
def clean(s,oth=''):
    fomart = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\'- '
    for c in s:
        if not c in fomart:   
            s = s.replace(c,'')   
    s = s.lower()
    return s

def tkn(fl, f = None , w = None, s = None):
    if f == None:
        f = True
    if w == None:
        w = True
    if s == None:
        s = True
    word = 0.0
    sntc = 0.0
    for line in fl:
        line = clean(line)
        line = nltk.word_tokenize(line)
        word += len(line)
        sntc += 1.0
    feature = []
    feature.append(word/sntc)
    if w == True:
        feature.append(int(word))
    if s == True:
        feature.append(int(sntc))
    return feature

def Test(fl,g):
    cnt = list()    #count：各個長度的句子各有幾個
    for num in range(41):
        cnt.append(0)    #40字以上的句子歸為超長句@cnt[40]
    scnt = 0.0

    for line in fl:
        scnt += 1.0
        line = clean(line)       #這個轉換有把重要訊息去掉的風險，但值得嘗試
        #tkn = nltk.word_tokenize(line)
        tkn= re.sub('[^\w]',' ',line).split()
        if len(tkn)<40:
            cnt[len(tkn)] += 1
        else:
            cnt[40] += 1
        
    feature = list()
    count = 0
    s = 0
    for i in g:
        for item in cnt:
            count += 1
            s += item
            if count == i:
                feature.append(s)
                s = 0
                count = 0
            
    '''for item in cnt:
        count += 1
        s += item
        if count == 4:
            feature.append(10*float(s)/scnt)
            s = 0
            count = 0

    for item in cnt:
        count += 1
        s += item
        if count == 5:
            feature.append(10*float(s)/scnt)
            s = 0
            count = 0'''
    return feature

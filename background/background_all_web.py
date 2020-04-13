from sklearn import svm
from sklearn.externals import joblib
import re
import json
import pickle
import nltk
from .Word import Count as wCount
from .Len import tkn

from .Vex import Count as vCount
import os
dp_dic=json.load(open('path/to/web/paragraph/background/dic.json','r'))
def dependency(text,grade=None,sent=None):
	stanfordp='path/to/stanford-parser-full-2015-12-09/lexparser.bat temp.txt'
	text=text.replace('\n',' ')
	f1=open('temp.txt','w')
	f1.write(text.strip())
	f1.close()
	rt=[]
	rd=os.popen(stanfordp).read()
	if grade != None:
		fw=open('paragraph/%d/%d.parse'%(grade,num),'w')
		fw.write(rd)
		fw.close()
	par=rd.split('\n')
	k=False
	sl=[]
	rt=[]
	for i,t in enumerate(par):
		if k:
			rt.append(t.split('(')[0])
		if len(t)==0:
			if len(rt)!=0:
				sl.append(rt)
				rt=[]
			k=k^True
	return sl
def sent_make(ts):

	for test in [ts]:
		sx=[]
		sy=[]
		for grade in range(1,4):
			#print('grade'+str(grade))
			for num in range(1,128):
				pl=[]
				if num%10 ==test:
					continue
				
				try:
					f=open('paragraph/%d/%d.sent'%(grade,num),'r')				
					sentences=json.load(f)
					f.close()
				except:
					break
				for s in sentences:
					if len(s)>5:
						l=[0]*len(dp_dic)
						for mark in s:
							if mark in dp_dic:
								l[dp_dic[mark]]+=1
						sx.append(l)
						sy.append(grade-1)
						s.append(l)
						pl.append(s)

		clf_s=svm.SVC(C=1,gamma=0.125)
		clf_s.fit(sx,sy)
		f=open('clf_s.p','wb')
		pickle.dump(clf_s,f)
		f.close()
	
def clf_make(test):
	print(test)
	x=[]
	y=[]
	for grade in range(1,4):
		for num in range(1,127):
			if num%10 ==test:
				continue
			try:
				f=open('paragraph/%d/%d.prdl'%(grade,num),'r')
				sentences=json.load(f)
				f.close()
			except:
				break
			
			f=open('paragraph/%d/%d.t'%(grade,num),'r')
			lines=f.readlines()
			a=[]
			a.extend(sentences)			
			a.extend(Word.Count(lines))
			k=Len.tkn(lines)
			a.extend(k)
			v=Vex.Count([text],fqc=True)
			a.extend(v)
				
			f1=open('paragraph/%d/%d.list'%(grade,num),'w')
			json.dump(a,f1)
			x.append(a)
			y.append(grade-1)

	clf_p=svm.SVC()
	clf_p.fit(x,y)
	f=open('clf_p.p','wb')
	pickle.dump(clf_p,f)
	f.close()


def judge(text,grade=None,num=None):
	
	dl=[0,0,0]
	sl=[]
	sent=dependency(text,grade,num)
	
	for rt in sent:
		l=[0]*len(dp_dic)
		for tag in rt:
			if tag in dp_dic:
				l[dp_dic[tag]]+=1
		sl.append(l)
	if grade != None:
		fw=open('path/to/web/paragraph/background/%d/%d.sl'%(grade,num),'w')
		json.dump(sl,fw)
		fw.close()

	clf_s=pickle.load(open('path/to/web/paragraph/background/clf_s.p','rb'))
	pr=clf_s.predict(sl)
	for ans in pr:
		dl[ans]+=1
	if grade != None:
		fw=open('path/to/web/paragraph/background/paragraph/%d/%d.prdl'%(grade,num),'w')
		json.dump(dl,fw)
		fw.close()
	a=[]
	lt=[]
	a.extend(dl)
	lt.append(len(a))
	a.extend(wCount([text],fqc=False))
	lt.append(len(a))
	sents=nltk.sent_tokenize(text)
	k=tkn(sents)
	v=vCount([text],fqc=True)
	a.extend(k)
	lt.append(len(a))
	a.extend(v)
	lt.append(len(a))
	with open('path/to/web/paragraph/background/list.json','w') as f:
		json.dump(lt,f)
	if grade != None:		
		fw=open('path/to/web/paragraph/background/paragraph/%d/%d.judge'%(grade,num),'w')
		json.dump(a,fw)
		fw.close()
	clf_p=joblib.load('path/to/web/paragraph/background/clf/clf_p.p')
	pr=clf_p.predict([a])
	f=open('path/to/web/paragraph/background/a.j','w')
	json.dump(a,f)
	f.close()
	return pr[0],v,k,dl

if __name__=='__main__':
	table=[[0,0,0],[0,0,0],[0,0,0]]
	
	for test in range(10):
		clf_make(test)
		sent_make(test)
		for grade in range(1,4):
			for num in range(1,127):
				if num%10==test:
					
					try:
						f=open('paragraph/%d/%d.t'%(grade,num),'r')
					except:
						break	
					text=f.read()
					f.close()
					text=text.replace('\n',' ')
					#ans,v,k=judge(text,grade,num)
					ans=judge(text)
					table[grade-1][ans]+=1											
	print(table)





from sklearn import svm
import re
import json
import pickle
import nltk
import Word
import Len
import os
dp_dic=json.load(open('dic.json','r'))
def dependency(text,grade=None,sent=None):
	stanfordp='/home/tfg2016/stanford-parser-full-2015-12-09/lexparser.sh temp.txt'
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

		clf_s=svm.SVC(C=1,gamma=0.125,probability=True)
		clf_s.fit(sx,sy)
		f=open('clf_s.p','wb')
		pickle.dump(clf_s,f)
		f.close()
	
def clf_make(test,c=1):
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
			
			
			a=[]
			a.extend(sentences)
			f=open('paragraph/%d/%d.prb'%(grade,num),'r')
			prb=json.load(f)
			for l in prb:
				avg=sum(l)/float(len(l))
				a.append(avg*100)
			'''except:
				continue'''				
			'''a.extend(Word.Count(lines,fqc=True))
			k=Len.tkn(lines)
			a.extend(k)'''
				
			f1=open('paragraph/%d/%d.list'%(grade,num),'w')
			json.dump(a,f1)
			x.append(a)
			y.append(grade-1)

	clf_p=svm.SVC(gamma=c)
	clf_p.fit(x,y)
	f=open('clf_p_pb.p','wb')
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
		'''fw=open('paragraph/%d/%d.sent'%(grade,num),'w')
		json.dump(sent,fw)
		fw.close()'''
		fw=open('paragraph/%d/%d.sl'%(grade,num),'w')
		json.dump(sl,fw)
		fw.close()

	clf_s=pickle.load(open('clf_s.p','rb'))
	pr=clf_s.predict(sl)
	for ans in pr:
		dl[ans]+=1
	if grade != None:
		fw=open('paragraph/%d/%d.prdl'%(grade,num),'w')
		json.dump(dl,fw)
		fw.close()
	a=[]
	a.extend(dl)
	'''a.extend(Word.Count([text],fqc=True))
	k=Len.tkn([text])
	a.extend(k)'''
	if grade != None:		
		fw=open('paragraph/%d/%d.judge'%(grade,num),'w')
		json.dump(a,fw)
		fw.close()
	clf_p=pickle.load(open('clf_p_9.p','rb'))
	pr=clf_p.predict([a])
	return pr[0]
if __name__=='__main__':
	for c_pow in range(-9,-3):
		c=2**c_pow 	
		table=[[0,0,0],[0,0,0],[0,0,0]]
		ac=0.0
		al=0.0
		for test in range(10):
			clf_make(test,c)
			f=open('clf_p_pb.p','rb')
			clf=pickle.load(f)
			f.close()
			for grade in range(1,4):
				for num in range(1,127):

					if num%10==test:
						try:
							f=open('paragraph/%d/%d.prdl'%(grade,num),'r')
							sentences=json.load(f)
							f.close()
						except:
							break
						
						
						a=[]
						a.extend(sentences)
						f=open('paragraph/%d/%d.prb'%(grade,num),'r')
						prb=json.load(f)
						for l in prb:
							avg=sum(l)/float(len(l))
							a.append(avg*100)
						ans=clf.predict([a])
						ans=ans[0]
						table[grade-1][ans]+=1
						if grade-1 ==ans:
							ac+=1
						al+=1
		print(c)											
		print(table)
		print(ac/al)

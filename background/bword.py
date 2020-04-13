from sklearn import svm
import re
import json
import pickle
from .Word import Count as wCount
from .Len import tkn
dp_dic=json.load(open('/home/tfg2016/web/paragraph/background/dic.json','r'))
def dependency(sent):
	stanfordp='/nfs/cache/hhhuang/stanford-parser-full-2015-12-09/lexparser.sh temp.txt'
	
	f1=open('temp1.txt','w')
	f1.write(sent.strip())
	f1.close()
	rt=[]
	par=os.popen(stanfordp).readlines()
	k=False
	for i,t in enumerate(par):
		if k:
			rt.append(t.split('(')[0])
		if len(t)!=1:
			k=k^True
	return rt
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
					f=open('/home/tfg2016/web/paragraph/background/paragraph/%d/%d.j'%(grade,num),'r')				
					sentences=json.load(f)
					f.close()
				except:
					break
				for s in sentences:
					if len(s[0])>5 and len(s[1])>50:
						l=[0]*len(dp_dic)
						for mark in s[0]:
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
				'''f=open('paragraph/%d/%d.dj'%(grade,num),'r')
				sentences=json.load(f)
				f.close()'''
				a=[]
				'''a.extend(sentences)'''
				f=open('/home/tfg2016/web/paragraph/background/paragraph/%d/%d.t'%(grade,num),'r')
				lines=f.readlines()
				a.extend(wCount(lines,fqc=True))
				k=tkn(lines)
				a.extend(k)
				
				f1=open('/home/tfg2016/web/paragraph/background/paragraph/%d/%d.list'%(grade,num),'w')
				json.dump(a,f1)
				x.append(a)
				y.append(grade-1)
			except:
				continue
	clf_p=svm.SVC()
	clf_p.fit(x,y)
	f=open('/home/tfg2016/web/paragraph/background/clf_p.p','wb')
	pickle.dump(clf_p,f)
	f.close()


def judge(text,grade=0,num=0):
	

	dl=[0,0,0]
	sl=[]
	
	a=[]
	a.extend(wCount([text],fqc=True))
	k=tkn([text])
	a.extend(k)

	clf_p=pickle.load(open('/home/tfg2016/web/paragraph/background/clf_p.p','rb'),encoding='latin1')
	pr=clf_p.predict([a])
	return pr[0],k
if __name__=='__main__':
	table=[[0,0,0],[0,0,0],[0,0,0]]
	
	for test in range(10):
		clf_make(test)
		sent_make(test)
		for grade in range(1,4):
			for num in range(1,127):
				if num%10==test:
					

					try:
						f= open('/home/tfg2016/web/paragraph/background/paragraph/%d/%d.t'%(grade,num),'r')
					except:
						print("%d %d "%(grade,num))
						continue
					text=f.read()
					f.close()
					text=text.replace('\n',' ')
					ans=judge(text,grade,num)
					table[grade-1][ans]+=1
							

	print(table)





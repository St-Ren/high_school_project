from sklearn import svm
import re
import json
import pickle
import nltk
from .Word import Count as wCount
from .Len import tkn
from .Len import Test
from .Vex import Count as vCount
dp_dic=json.load(open('/home/tfg2016/web/paragraph/background/dic.json','r'))	
def clf_make(test):
	print(test)
	x=[]
	y=[]
	for grade in range(1,4):
		for num in range(1,127):
			if num%10 ==test:
				continue
			try:
	
				a=[]
				f=open('/home/tfg2016/web/paragraph/background/paragraph/%d/%d.t'%(grade,num),'r')
			except:
				continue

			text=f.read()
			text=text.replace('\n',' ')
			a.extend(wCount([text]))
			a.extend(vCount([text],fqc=True))
			k=tkn([text])
			a.extend(k)
			a.extend(Len.Test([text],range(2,4)))
			
			f1=open('/home/tfg2016/web/paragraph/background/paragraph/%d/%d.list'%(grade,num),'w')
			json.dump(a,f1)
			f1.close()
			x.append(a)
			y.append(grade-1)
			
	clf_p=svm.SVC()
	clf_p.fit(x,y)
	f=open('/home/tfg2016/web/paragraph/background/clf_p_v.p','wb')
	pickle.dump(clf_p,f)
	f.close()


def judge(text,grade=0,num=0):
	

	dl=[0,0,0]
	sl=[]
	
	a=[]
	text=text.replace('\n',' ')
	a.extend(wCount([text]))
	v=vCount([text],fqc=True)
	a.extend(v)
	sents=nltk.sent_tokenize(text)
	k=tkn(sents)
	a.extend(k)
	a.extend(Test(sents,range(2,4)))

	clf_p=pickle.load(open('/home/tfg2016/web/paragraph/background/clf_p_v.p','rb'))
	pr=clf_p.predict([a])
	return pr[0],v,k
if __name__=='__main__':
	table=[[0,0,0],[0,0,0],[0,0,0]]
	wrong=[[],[],[]]
	for test in range(10):
		clf_make(test)
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
					ans,k=judge(text,grade,num)
					table[grade-1][ans]+=1
					if grade-1 !=ans:
						wrong[grade-1].append(num)
							

	print(table)
	print(wrong)
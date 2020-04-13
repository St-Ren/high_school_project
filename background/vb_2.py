from sklearn import svm
import nltk
import re
import json
import pickle
import Word
import Len
import Vex
dp_dic=json.load(open('dic.json','r'))	
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
				f=open('paragraph/%d/%d.t'%(grade,num),'r')
			except:
				continue

			text=f.read()
			text=text.replace('\n',' ')
			a.extend(Word.Count([text]))
			a.extend(Vex.Count([text],fqc=True))
			sents=nltk.sent_tokenize(text)
			k=Len.tkn(sents)
			a.extend(k)
			a.extend(Len.Test(sents,range(2,4)))
			
			f1=open('paragraph/%d/%d.list'%(grade,num),'w')
			json.dump(a,f1)
			x.append(a)
			y.append(grade-1)
			
	clf_p=svm.SVC()
	clf_p.fit(x,y)
	f=open('clf_p_v.p','wb')
	pickle.dump(clf_p,f)
	f.close()


def judge(text,grade=0,num=0):
	

	dl=[0,0,0]
	sl=[]
	
	a=[]
	text=text.replace('\n',' ')
	a.extend(Word.Count([text]))
	a.extend(Vex.Count([text],fqc=True))
	sents=nltk.sent_tokenize(text)
	k=Len.tkn(sents)
	a.extend(k)
	a.extend(Len.Test(sents,range(2,4)))

	clf_p=pickle.load(open('clf_p_v.p','rb'))
	pr=clf_p.predict([a])
	return pr[0]
if __name__=='__main__':
	table=[[0,0,0],[0,0,0],[0,0,0]]
	wrong=[[],[],[]]
	for test in range(10):
		clf_make(test)
		for grade in range(1,4):
			for num in range(1,127):
				if num%10==test:
					try:
						f= open('paragraph/%d/%d.t'%(grade,num),'r')
					except:
						print("%d %d "%(grade,num))
						continue
					text=f.read()
					f.close()
					text=text.replace('\n',' ')
					ans=judge(text,grade,num)
					table[grade-1][ans]+=1
					if grade-1 !=ans:
						wrong[grade-1].append(num)
							

	print(table)
	print(wrong)
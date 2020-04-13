from sklearn import svm
import nltk
import os
import json
import pickle
dp_dic=json.load(open('dic.json'))
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
		clf_s=svm.SVC(C=1,gamma=0.125)
		clf_s.fit(sx,sy)
		f=open('clf_s.p','wb')
		pickle.dump(clf_s,f)
		f.close()
if __name__=="__main__":
	table=[[0,0,0],[0,0,0],[0,0,0]]
	for test in range(10):
		sent_make(test)
		clf=pickle.load(open('clf_s.p','rb'))
		for grade in range(1,4):	
			for num in range(1,126):
				if num%10 ==test:
					sl=[]				
					try:
						f=open('paragraph/%d/%d.sent'%(grade,num),'r')				
						sentences=json.load(f)
						f.close()
					except:
						print('%d %d'%(grade,num))
						break
					for s in sentences:
						print('s')
						if len(s)>5:
							l=[0]*len(dp_dic)
							for mark in s[0]:
								if mark in dp_dic:
									l[dp_dic[mark]]+=1
						sl.append(l)
					print(len(sl))
					ans=clf.predict(sl)
					for a in ans:
						table[grade-1][a]+=1
	print(table)


						

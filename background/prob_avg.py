from sklearn import svm
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
						s.append(l)
						pl.append(s)

		clf_s=svm.SVC(C=1,gamma=0.125,probability=True)
		clf_s.fit(sx,sy)
		f=open('clf_s.p','wb')
		pickle.dump(clf_s,f)
		f.close()
if __name__=='__main__':
	for test in range(10):
		sent_make(test)
		for grade in range(1,4):
			for num in range(1,127):
				if num%10==test:					
					try:
						f=open('paragraph/%d/%d.sl'%(grade,num),'r')
					except:
						break
					sl=json.load(f)
					clf=pickle.load(open('clf_s.p','rb'))
					a=clf.predict_proba(sl)
					l=[[],[],[]]
					for s in a:
						for i in range(3):
							l[i].append(s[i])
					fw=open('paragraph/%d/%d.prb'%(grade,num),'w')
					json.dump(l,fw)
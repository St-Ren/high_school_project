from sklearn import svm
import Len
import Word
if __name__=='__main__':
	tabel=[[0,0,0],[0,0,0],[0,0,0]]
	for test in range(10):
		x=[]
		y=[]
		for grade in range(1,4):
			for num in range(1,126):
				if num%10==test:
					continue
				try:
					f=open('paragraph/%d/%d.t'%(grade,num),'r')
				except:
					print('%d %d'%(grade,num))
					break
				text=f.readlines()
				a=[]
				a.extend(Word.Count(text,fqc=True))
				a.extend(Len.tkn(text))
				x.append(a)
				y.append(grade-1)
		clf=svm.SVC()
		clf.fit(x,y)
		for grade in range(1,4):
			for num in range(1,126):
				if num%10!=test:
					continue
				try:
					f=open('paragraph/%d/%d.t'%(grade,num),'r')
				except:
					print('%d %d'%(grade,num))
					break
				text=f.readlines()
				a=[]
				a.extend(Word.Count(text,fqc=True))
				a.extend(Len.tkn(text))
				ans=clf.predict([a])
				table[grade-1][ans]+=1
	print(table)


				

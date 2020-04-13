import background
table=[[0,0,0],[0,0,0],[0,0,0]]
test=10
for grade in range(1,4):
	for num in range(1,126):
		if num%10==test:
			continue
		try:
			f=open('paragraph/%d/%d.t'%(grade,num))
		except:
			break

		text=f.read()
		text=text.replace('\n',' ')
		ans=background.judge(text)
		table[grade-1][ans]+=1
print(table)


for num in range(1,127):
	f=open('%d.t'%num,'r',encoding='latin1')
	print(f)
	text = f.read()
	l=list(text)
	x=1
	n=0
	while x==1:
		x=0
		for f_num in range(11):
			p=text.find(str(f_num))
			while p>0:
				if p>0:
					o=ord(text[p-1])
					if o>64 and o<91:
						l.pop(p)
						x=1
						n+=1
						text="".join(l)
						break
					else:
						if o>96 and o<123:
							l.pop(p)
							x=1
							n+=1
							text="".join(l)
							break
						else:
							p=text.find(str(f_num),p+1)
	print(n)


	f.close()
	f=open('%d.t'%num,'w',encoding='latin1')
	f.write(text)
	f.close




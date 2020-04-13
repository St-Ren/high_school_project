s='Many students procrastinate, or put off, doing an assignment until the very last minute.'
for num in range(1,113):
	f=open('%d.t'%num,'r')
	text=f.read()
	if text.find(s)>=0:
		print(num)
	f.close()
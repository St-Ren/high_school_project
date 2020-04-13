for num in range(1,127):
	f=open('%d.t'%num,'r',encoding='latin1')
	lines=f.readlines()
	f.close()
	f=open('%d.t'%num,'w',encoding='latin1')
	for line in lines:
		line=line.replace('*','')
		line=line.replace('　',' ')
		line=line.replace('??','')
		
		s=line.strip()
		if len(s)<10:
			try:
				print(f)
				print(line)
			except:
				print('false')
		else:
			
			f.write(s+'\n')



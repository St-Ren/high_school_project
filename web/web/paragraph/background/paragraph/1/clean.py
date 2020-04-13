for grade in [1]:
	for num in range(1,133):
		with open('%d.t'%num,'r',encoding='latin1') as fw:
			print(fw)
			rt=fw.read()
			rt=rt.replace('”','"')
			rt=rt.replace('“','"')
			rt=rt.replace("’","'")
			rt=rt.replace("　",' ')
			text=""
			for c in rt:
				if(ord(c)<128):
					text=text+c
			text=text.replace('	','')
			text=text.replace('*','')
			text=text.replace('??','')
			text=text.replace('? ',' ')
			text=text.replace('','')
			text=text.replace('@','')
		with open('%d.t'%num,'w',encoding='latin1') as fw:
			fw.write(text)
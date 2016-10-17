def popular_words():
	words_file = open('/usr/share/dict/american-english')
	
	temp = words_file.readlines()
	words = []
	for x in temp:
		x = x.upper().replace('\n', '').replace('\'', '')
		if len(x) > 1:
			words.append(x)
	to_return = list(set(words))
	return to_return

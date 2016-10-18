#!/usr/bin/python

# This script reads a system dictionary list, formats it appropriately to be used in word frequency check later on
#
# If you want to use a different new line delimited dictionary list, simply replace /usr/share/dict/words with an
# absolute path to the dictionary list you wish to use.


def popular_words():
	words_file = open('/usr/share/dict/words')
	
	temp = words_file.readlines()
	words = []
	for x in temp:
		x = x.upper().replace('\n', '').replace('\'', '').replace('-', '')
		if len(x) > 1:
			words.append(x)
	to_return = list(set(words))
	return to_return

#!/usr/bin/python

# This file is the main workhorse for the entire program. It receives an encrypted message and some user provided
# restraints that are then used to analyze the potentially decrypted messages.

from ColumnKeys import get_column_swap_key
from timeit import default_timer as timer
from popular_words import popular_words
from multiprocessing import Pool
from psutil import cpu_count

popular_words = popular_words()


# This method receives the potentially decrypted message and then searches the message for words from the dictionary
# list. It counts the number of words, stores the words that matched, then returns formatted output to be printed to
# the raw output file.
def analyze(key, string, x):
	number_of_words = 0
	word_list = ''
	for word in popular_words:
		if word in string:
			word_list += "{} ".format(word)
			number_of_words += 1
	
	to_print = string + " -- {}".format(number_of_words)
	to_print += "\n{0}, Caesar Key:{1}, Column Key:{2}\n".format(word_list, key, x)
	if number_of_words < 0:
		to_print = -1
	return to_print


# Returns a list containing the position indices of characters from the key. The first position in the returned list
# will correspond to the index in the key of the letter or number with the lowest value
#
# ex: keyword_index('car')
#       returns [1, 0, 2]
# ex: keyword_index('35214')
#       returns [3, 2, 0, 4, 1]
def keyword_index(word):
	keyword = list(word)
	temp_word = []
	for i in range(len(keyword)):
		temp_word.append([keyword[i], i])
	to_return = []
	for x in sorted(temp_word):
		to_return.append(x[1])
	return to_return


# This method uses the original message and the keyword_index results to populate the decrypter message string.
# Influence for the design of this method came from pycipher: https://goo.gl/yYyKS3
# I mainly wanted to write my own implementation to better understand how it works.
def new_matrix((shift_key, columns, mssg, col_key)):
	msg = list(mssg)
	empty_string = ['-'] * len(msg)
	message_length = len(msg)
	column_key = col_key
	column_key = keyword_index(column_key)
	where_am_i = 0
	for i in range(len(column_key)):
		column_pos = int(message_length / columns)
		if column_key[i] < message_length % columns:
			column_pos += 1
		empty_string[column_key[i]::columns] = msg[where_am_i:where_am_i + column_pos]
		where_am_i += column_pos
		decrypted_string = ''.join(empty_string)
		decrypted_string = analyze(shift_key, decrypted_string, col_key)
	return decrypted_string


class DecryptionObject:
	# Simple python constructor method
	def __init__(self, min_col, min_key, max_col, max_key, msg):
		self.min_column_length = min_col
		self.min_cipher_key = min_key
		self.max_column_length = max_col + 1
		self.max_cipher_key = max_key + 1
		self.message = msg
		self.column_permutations = get_column_swap_key()
		self.column_permutations
		assert self.min_column_length > 1
		self.run()

	# This contains the control logic that allows the program to run through all possible permutations of the provided
	# string under the user provided constraints. Initiates multiprocessing, and writes results to the raw output file
	def run(self):
		__file = open('./results_raw.txt', 'a+')
		__file.truncate()
		for x in range(self.min_cipher_key, self.max_cipher_key):
			deciphered_msg = self.return_ascii_ciphered_list(x, self.message)
			start = timer()
			
			for y in range(self.min_column_length, self.max_column_length):
				queue = []
				for z in self.column_permutations['{}'.format(y)]:
					queue.append([x, y, deciphered_msg, z])
				n_cpus = cpu_count()  # Counts the cores on your processor
				pool = Pool(n_cpus)
				results = pool.map(new_matrix, queue)
				pool.close()
			
				for line in results:
					__file.write(line)
			end = timer()
			print "Caesar Key {0}: {1}".format(x, (end - start))
	
	# This method is responsible for caesar shifting the letters of the message. The letters are shifted via subtraction
	@staticmethod
	def return_ascii_ciphered_list(key, message):
		to_return = []
		message_list = list(message)
		for x in message_list:
			x = ord(x)
			if not x == 35:
				x -= key
				if x < 65:
					x += 26
				x = chr(x)
				to_return.append(x)
		return ''.join(to_return)

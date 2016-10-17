from ColumnKeys import get_column_swap_key
from timeit import default_timer as timer
from popular_words import popular_words
from multiprocessing import Pool
from psutil import cpu_count

popular_words = popular_words()


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


def keyword_index(word):
	keyword = list(word)
	thing = []
	for i in range(len(keyword)):
		thing.append([keyword[i], i])
	to_return = []
	for x in sorted(thing):
		to_return.append(x[1])
	return to_return


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
				n_cpus = cpu_count()
				pool = Pool(n_cpus)
				results = pool.map(new_matrix, queue)
				pool.close()
			
				for line in results:
					__file.write(line)
			end = timer()
			print "Caesar Key {0}: {1}".format(x, (end - start))
	
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

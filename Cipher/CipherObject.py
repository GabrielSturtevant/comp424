from sympy import Matrix
from math import ceil
from popular_words import popular_words
from ColumnKeys import get_column_swap_key
from threading import Thread, Lock
import Queue

info_queue = Queue.Queue()
printer = open('results.txt', 'w+')


class DecryptionObject:
	def __init__(self, message):
		self.original_message = message
		self.original_message_list = list(self.original_message)
		self.column_key_permutations = get_column_swap_key()
		self.original_message_ascii_list = []
		for x in self.original_message_list:
			self.original_message_ascii_list.append(ord(x))
		self.caesar_list = []
		
	def re_init(self, message):
		self.original_message = message
		self.original_message_list = list(self.original_message)
		self.original_message_ascii_list = []
		for x in self.original_message_list:
			self.original_message_ascii_list.append(ord(x))
	
	def return_queue_list(self):
		lst = []
		while not info_queue.empty():
			lst.append(info_queue.get(0))
		return lst
		
	def return_ascii_ciphered_list(self, key):
		to_return = []
		for x in self.original_message_ascii_list:
			x -= key
			if x < 65 and not x == 35:
				x += 26
			to_return.append(x)
		return to_return
	
	def setup_matrix(self, columns, caesar_key, mssg):
		global info_queue
		
		self.re_init(mssg)
		final_lst = []
		temp_lst = []
		# TODO - Fix the division rounding issue
		division = int(ceil(len(self.original_message_ascii_list) / float(columns)))
		self.original_message_ascii_list = self.return_ascii_ciphered_list(caesar_key)
		for x in self.original_message_ascii_list:
			flag = True
			temp_lst.append(x)
			if len(temp_lst) == division:
				final_lst.append(temp_lst)
				temp_lst = []
				flag = False
		
		if flag:
			while len(temp_lst) < len(final_lst[0]):
				temp_lst.append(35)
			final_lst.append(temp_lst)
		
		scrambled_matrix = Matrix(final_lst)
		scrambled_matrix = scrambled_matrix.transpose()
		
		for x in self.column_key_permutations['{}'.format(len((scrambled_matrix.tolist())[0]))]:
			to_put = [
				scrambled_matrix,
				x,
				caesar_key
			]
			info_queue.put(to_put)
			

class BlockingTestThread(Thread):
	
	def __init__(self):
		self.lock = Lock()
		self._running_flag = False
		Thread.__init__(self)
	
	def some_read_function(self):
		self.lock.acquire()
		global info_queue
		if not info_queue.empty():
			info = info_queue.get(0)
		else:
			info = -1
		self.lock.release()
		return info
		
	def print_func(self, to_print):
		self.lock.acquire()
		global printer
		printer.write(to_print)
		self.lock.release()

	def worker_method(self, (_scrambled_matrix, _x, _caesar_key)):
		#info_to_calculate = self.some_read_function()
		try:
			while not info_to_calculate == -1:
				scrambled_matrix = _scrambled_matrix
				x = _x
				caesar_key = _caesar_key
				matrix_copy = scrambled_matrix[:, :]
				for i in range(len(x)):
					index_val = x[i]
					matrix_copy[:, i] = scrambled_matrix[:, index_val - 1]
				
				result_lst = matrix_copy.tolist()
				result_string = ''
				for i in result_lst:
					for j in i:
						result_string += chr(j)
				
				result_string = result_string.replace('#', '')
				number_of_words = 0
				word_list = ''
				for word in popular_words:
					if word in result_string:
						word_list += "{} ".format(word)
						number_of_words += 1
				
				to_print = result_string + " -- {}".format(number_of_words)
				to_print += "\n{0}, Caesar Key:{1}, Column Key:{2}\n".format(word_list, caesar_key, x)
		finally:
				return to_print

from CipherObject import DecryptionObject, BlockingTestThread
import word_organizer
import time
import psutil
from multiprocessing import Process, Pool
from popular_words import popular_words

message = 'DRPWPWXHDRDKDUBKIHQVQRIKPGWOVOESWPKPVOBBDVVVDXSURWRLUEBKOLVHIHBKHLHBLNDQRFLOQ'
message = 'hvalfrghaaeflckplazgfvsvn'.upper()


def worker_method((_scrambled_matrix, _x, _caesar_key)):
	# info_to_calculate = self.some_read_function()
	try:
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
		if number_of_words < 1:
			to_print = -1
	finally:
		return to_print

if __name__ == "__main__":
	
	foo = DecryptionObject(message)
	
	for i in range(1):
		for j in range(8, 11):
			foo.setup_matrix(j, 3, message)
	queue_list = foo.return_queue_list()
	print "Spinning up threads"
	start = time.clock()
	threads = []

	n_cpus = psutil.cpu_count()
	pool = Pool(n_cpus)
	results = pool.map(worker_method, queue_list)
	file_open = open('./results.txt', 'w+')
	
	for x in results:
		if not x == -1:
			file_open.write(x)
	# for x in pool:
	#
	# 	foo = BlockingTestThread()
	# 	x = Process(target=foo.worker_method(),)
	# 	threads.append(x)
	#
	# for x in threads:
	# 	x.start()
	#
	# for x in threads:
	# 	x.join()
	finish = time.clock()
	
	print "Total Time: {}".format((finish-start))
	
	try:
		word_organizer.foo()
	finally:
		print "Done"

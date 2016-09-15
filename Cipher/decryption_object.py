from keys import get_column_swap
from sympy import Matrix
from popular_words import popular_words
import sys

class decryption_obejct:
	character_string = ""
	list_of_characters = []
	list_of_ascii_characters = []
	key_permutations = {}
	file_var = ""
	
	def __init__(self, message):
		self.character_string = message
		self.list_of_characters = list(self.character_string)
		self.ascii_list(self.list_of_characters)
		self.key_permutations = get_column_swap()
	
	def ascii_list(self, chars):
		for x in chars:
			self.list_of_ascii_characters.append(ord(x))
	
	def setup_matrix(self, lst, columns):
		final_lst = []
		temp_lst = []
		
		for x in lst:
			flag = True
			temp_lst.append(x)
			if len(temp_lst) % int((len(lst) / columns)) == 0:
				final_lst.append(temp_lst)
				temp_lst = []
				flag = False
		
		if flag:
			while len(temp_lst) < len(final_lst[0]):
				temp_lst.append(35)
			final_lst.append(temp_lst)
		transposed_lst = Matrix(final_lst)
		transposed_lst = transposed_lst.transpose()
		list_to_modify = transposed_lst[:,:]
		results = ''
		for x in self.key_permutations["{}".format(len((list_to_modify.tolist())[0]))]:
			columnar_transposed_list = list_to_modify[:,:]
			for i in range(len(x)):
				index_val = x[i]
				columnar_transposed_list[:, i] = list_to_modify[:, index_val - 1]
			columnar_transposed_list = columnar_transposed_list.tolist()
			results = ""
			for z in columnar_transposed_list:
				for y in z:
					results += chr(y)
			num_of_words = 0
			for word in popular_words:
				if word.upper() in results:
					num_of_words += 1
			results += " -- {}\n".format(num_of_words)
			if num_of_words > 10:
				self.file_var.write(results)
		else:
			pass
		
	
	def return_ascii_list(self):
		return self.list_of_ascii_characters
	
	def return_ascii_ciphered_list(self, key):
		to_return = []
		for x in self.list_of_ascii_characters:
			x -= key
			if x < 65 and not x == 35:
				x += 26
			to_return.append(x)
		to_return
		return to_return
	
	def open_file(self):
		self.file_var = open('./results.txt', 'w+')
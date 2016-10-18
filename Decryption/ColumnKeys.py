#!/usr/bin/python

# This script returns a dictionary containing all possible column key permutations in the range of 2-10. This is then
# used by the decryption object to check individual column keys.

from itertools import permutations


def get_column_swap_key():
	keys = []
	temp = []
	key_dict = {}
	for i in range(2, 11):
		for j in range(1, i + 1):
			temp.append(j)
		keys.append(temp)
		temp = []
	key_permutations = []
	for x in keys:
		for y in permutations(x):
			key_permutations.append(y)
		key_dict["{}".format(len(x))] = key_permutations
		key_permutations = []
	
	return key_dict

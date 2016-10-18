#!/usr/bin/python

# This is the primary entry point for the program that actually brute force decrypts the message. It uses user provided
# constraints to minimize the search time.

from word_organizer import organize_results
from timeit import default_timer as timer
import DecryptionObject


if __name__ == "__main__":
	min_cipher_keys = 3  # Minimum Caesar cipher key value. Must be >= 0
	min_column_keys = 2  # Minimum column key size. Must be >= 2.
	
	max_cipher_keys = 3  # Maximum Caesar cipher key value. Must be <= 26
	max_column_keys = 6  # Maximum column key size. Must be <= 10
	
	message = 'DRPWPWXHDRDKDUBKIHQVQRIKPGWOVOESWPKPVOBBDVVVDXSURWRLUEBKOLVHIHBKHLHBLNDQRFLOQ'
	
	print "Starting Analysis"
	start = timer()
	DecryptionObject.DecryptionObject(
		min_column_keys,
		min_cipher_keys,
		max_column_keys,
		max_cipher_keys,
		message.upper()
	)
	end = timer()
	print "Total Elapsed time: {}".format(end - start)
	organize_results()

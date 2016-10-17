from word_organizer import organize_results
from timeit import default_timer as timer
import DecryptionObject


if __name__ == "__main__":
	min_cipher_keys = 3
	min_column_keys = 2
	
	max_cipher_keys = 3
	max_column_keys = 6
	
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

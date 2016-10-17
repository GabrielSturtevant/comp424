from operator import itemgetter


def organize_results():
	file_var = open('./results_raw.txt', 'r')
	num = 1
	result_set = []
	items = {}
	for line in file_var:
		line = line.rstrip()
		if num % 2 == 0:
			some_list = line.split(", ", 2)
			items['words'] = some_list[0]
			items['caesar key'] = some_list[1]
			items['columnar key'] = some_list[2]
			items_list = [
				items['number_of_words'],
				items['string'],
				items['words'],
				items['caesar key'],
				items['columnar key']
				]
			result_set.append(items_list)
			num += 1
		else:
			some_list = line.split(" -- ")
			items['string'] = some_list[0]
			items['number_of_words'] = int(some_list[1])
			num += 1
	result_set = sorted(result_set, key=itemgetter(0), reverse=True)
	file_var.close()
	file_var = open('./results_formatted.txt', 'w')
	for x in result_set:
		var = "{1}\n{0} -- Number of words\nWords:\n".format(x[0],x[1])
		for y in x[2].split(" "):
			if not y == "" and not y == " ":
				var += "\t{}\n".format(y)
		var += "{0}\n{1}\n\n\n".format(x[3].replace(":", " : "), x[4].replace("(", " ").replace(")", ""))
		file_var.write(var)
	file_var.close()

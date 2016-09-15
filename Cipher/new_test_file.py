from sympy import Matrix
lst = []
temp_lst = []
final_lst = []
for i in range(1, 21):
	lst.append(i)

columns = 6
flag = True

for x in lst:
	flag = True
	temp_lst.append(x)
	if len(temp_lst) % int((len(lst) / columns)) == 0:
		final_lst.append(temp_lst)
		temp_lst = []
		flag = False

if flag:
	while len(temp_lst)< len(final_lst[0]):
		temp_lst.append(99)
	final_lst.append(temp_lst)

print final_lst

foo = Matrix(final_lst)
foo = foo.transpose()

print foo

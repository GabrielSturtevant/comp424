from sympy import *
order = [2,3,1]

foo = Matrix([[1,2,3],[4,5,6],[7,8,9]])
print "Foo"
print foo
print ""
bar = foo[:,:]
for i in range(len(order)):
	index_val = order[i]
	bar[:, i] = foo[:, index_val-1]

print foo
print bar
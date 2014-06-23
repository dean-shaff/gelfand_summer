def add():
	x = raw_input("give me a number ")
	try:
		print x + 2
	except TypeError:
		print "x wasn't an integer"
		print int(x) + 2
add()
import re
fl = open( "d.csv" )
out = open( "out.csv", "w" )
lines = fl.readlines()

#pattern = re.compile(".*a[uv]+to.*\.ru")
pattern = re.compile(".*avto.*\.ru")

for i in lines:
		data = i.split(';')
		if pattern.search(data[0]):
			print (data)
			out.write( str(data) )
out.close()

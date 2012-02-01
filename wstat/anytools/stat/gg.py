infile = open( "analitics2.csv", "r" )
data = infile.readlines()
outfile = open( "out.txt", "w" )

outfile.write( "data.addColumn('string', 'Марка');\n");
outfile.write( "data.addColumn('number', 'Спрос');\n");
outfile.write( "data.addRows(%s);\n" % len(data) );

index = 0
for i in data:
	line = [ j.strip() for j in i.split(';') ]
	if len(line) > 1:
		outfile.write( "data.setValue(%s, 0, '%s');\n" % (index, line[0]) );
		outfile.write( "data.setValue(%s, 1, %s);\n" % (index, line[1]) );
		index += 1
	
outfile.close()
infile.close()
	

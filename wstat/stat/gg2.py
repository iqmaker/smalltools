infile = open( "analitics2.csv", "r" )
data = infile.readlines()
outfile = open( "out.txt", "w" )

outfile.write( "data.addColumn('string', 'Модель');\n");
outfile.write( "data.addColumn('number', 'Спрос');\n");
outfile.write( "data.addRows(%s);\n" % len(data) );

index = 0
for i in data:
	line = [ j.strip() for j in i.split(';') ]
	if len(line) > 1:
		names = [ j for j in line[0].split('_') ]
		names = [ j[0].upper() + j[1:] for j in names ]
		name = ''
		for i in names:
			name += i + ' '
		print( names )
		outfile.write( "data.setValue(%s, 0, '%s');\n" % (index, name ) );
		outfile.write( "data.setValue(%s, 1, %s);\n" % (index, line[1]) );
		index += 1
	
outfile.close()
infile.close()
	

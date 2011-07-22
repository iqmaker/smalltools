infile = open( "analitics2.txt", "r" )
outfile = open( "analitics2.csv", "w" )
data = [i.strip() for i in infile.readlines()]
for i in data:
    stat = [ i.strip() for i in i.split(' ') ]
    name = stat[0]
    count = sum( [ int(i.strip()) for i in stat[1:] if len(i.strip()) > 0] )
    outfile.write( name + ';' + str(count) + '\n' )

outfile.close()
infile.close()

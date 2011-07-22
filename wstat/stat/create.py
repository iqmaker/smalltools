infile = open( "stat.txt", "r" )
outfile = open( "outstat.txt", "w" );
total = open( "sum.txt", "w" );
data = infile.readlines()

streamstatus = 1
position = 0

mader = []
models = []
outlines = 0
for i in data:
        if len(i.strip()) == 0:
                streamstatus = 1
                position = 0
                if len( mader ) > 0 :
                        for m in mader:
                                total.write( m + ' разборка\n')
                                total.write( m + ' запчасти бу\n')
                                for j in models:
                                        outfile.write( m + ' ' + j + ' разборка\n' )
                                        outfile.write( m + ' ' + j + ' запчасти бу\n' )
                                        if outlines > 0 and outlines%160 == 0 :
                                                index = outlines / 160
                                                outfile.close()
                                                outfile = open( "outstat" + str(int(index)) + ".txt", "w" )
                                        outlines+=2
                                        
                mader = []
                models = []
                continue
	
        if streamstatus == 1 and position == 0:
                mader = [j.strip() for j in i.split()]
                position += 1 
        elif streamstatus == 1:
                model = models.append( i.strip() )

print( 'done' )	
		
infile.close()
outfile.close()
total.close()

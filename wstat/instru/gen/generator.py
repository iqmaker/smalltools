# -*- utf-8 -*-
from sites import sites
import re
import codecs

pattern = re.compile( '\{%([A-Z]+)%\}' )

infile = open( 'template.html' )
template = infile.read()

result = pattern.findall( template )
for site in sites:
    body = template
    for i in result:
        body = body.replace( '{%' + i + '%}', sites[site][i] )
    outfile = codecs.open( "index_" + site + '.html', 'w', 'utf-8' )
    outfile.write( body )
    outfile.close()
    

    


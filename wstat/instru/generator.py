# -*- utf-8 -*-
from sites import sites
import re
import codecs
import ftplib
import os

def SendFile( ftp, file, new_name='' ):
        f = open( file, 'rb' )
        if new_name == '':
                ftp.storbinary('STOR '+ file, f )
        else:
                ftp.storbinary('STOR '+ new_name, f )
        f.close()

def RemoveDir( ftp, folder ):
        pwd = ftp.pwd()
        try:
                ftp.cwd( folder )
                files = []
                ftp.dir( files.append )
                for i in files:
                        ftp.delete( i );
                try:
                        ftp.rmd( folder )
                        ftp.cwd(pwd)
                        ftp.mkd( folder )
                except:
                        pass
        except:
                try:
                        ftp.mkd( folder )
                except:
                        pass

        ftp.cwd(pwd)
        
def SendFolder( ftp, folder ):
        #ftp.rmd( folder )
        #ftp.cwd( folder )
        RemoveDir(ftp, folder)
        files = os.listdir( folder )
        for i in files:
                print( 'coping ' + i )
                if len(i.split('.')) > 1:
                        SendFile( ftp, folder + '/' + i)
        
def UploadBig( SiteName ):
        s = ftplib.FTP( 'ftp.narod.ru', SiteName ,'mazdaq' )
        s.login()
        SendFile( s, "index_" + site + '.html', 'index.html' )
        SendFolder( s, 'image')
        SendFolder( s, 'css' )
        print( SiteName )
        s.quit()
       
def UploadSmall( SiteName ):
        try:
                s = ftplib.FTP( 'ftp.narod.ru', SiteName ,'mazdaq' ) # Connect
                s.login()
                SendFile( s, "index_" + site + '.html', 'index.html' )                                # Close file and FTP
                s.quit()
                print( 'Success' + SiteName )
        except:
                print( 'exception : ' + SiteName )
	
pattern = re.compile( '\{%([A-Z]+)%\}' )

infile = codecs.open( 'template.html', 'r', 'utf-8' )
template = infile.read()

result = pattern.findall( template )
for site in sites:
    body = template
    for i in result:
        body = body.replace( '{%' + i + '%}', sites[site][i] )
    outfile = codecs.open( "index_" + site + '.html', 'w', 'cp1251' )
    outfile.write( body )
    outfile.close()
    UploadSmall( site )

html = open( 'links.html', 'w' )
html.write( '<html><head></head><body>' )
for site in sites:
        html.write( '<a href="http://' + site + '.narod.ru">' + site + '</a> <br />' )
html.write( '</body></html>' )
html.close()








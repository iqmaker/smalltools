# -*- coding: utf-8 -*-

import urllib
import urllib2
import time
import gzip
import StringIO
import zlib
import winsound
from HTMLParser import HTMLParser
from urllib2 import urlopen
import codecs
from itertools import *
import random
import re
import pickle

def decode (page):
    encoding = page.info().get("Content-Encoding")    
    if encoding in ('gzip', 'x-gzip', 'deflate'):
        content = page.read()
        if encoding == 'deflate':
            data = StringIO.StringIO(zlib.decompress(content))
        else:
            data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(content))
        page = data.read()
    else:
        page = page.read()
    return page


def write_data( filename, data ):
        outfile = open( filename, "w" )
        for i, j, k in data:
                outfile.write( i )
                outfile.write( ';' )
                outfile.write( k )
                outfile.write( '\n' )

        outfile.close()        

def urldecode( url ):
    params=url.split('&')
    result={}
    for i in params:
        if  i.find( '=' ):
            pos=i.find('=')
            first = i[:pos]
            second = i[pos+1:]
            result[first]=second
    return result
    
class Spider(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		result = []
        
	def handle_starttag(self, tag, attrs):
		if tag == 'a' and attrs:
			self.result.add( attrs[0][1] )
           
status=[ 'campaign', 'table1', 'table2', 'pages', 'continue' ]
linkstatus=['tlist', 'data', 'count', 'continue' ]

class WordsExtraction(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.links_base=[]
            self.links_depend=[]
            self.pages=[]
            self.status=''
            self.linkstatus=''
            
            self.word=''
            self.href=''
            self.count=''
            self.section = 0
            self.base_count = 0
            
        def handle_starttag(self, tag, attrs):
            #print( self.status, self.linkstatus )
            if tag=='tr':
                    for name, value in attrs:
                            if name=='valign' and value=='top':
                                    self.section += 1
                    
            if tag=='table':
                    for name, value in attrs:
                            if name=='class' and value=='campaign':
                                    self.status='campaign'
                                    return

            if self.status=='campaign' and tag == 'table':
                    for name, value in attrs:
                            if name=='width' and value=='100%':
                                    self.status='table1'  
             
            elif self.status=='table1':
                    if tag=='table':
                            for name, value in attrs:
                                    if name=='width' and value=='100%':
                                            self.status='table2'
                                            
            if self.status=='table1':
                    if tag=='div':
                            for name, value in attrs:
                                    if name=='class' and value=='pages':
                                            self.status='pages'                              

            if self.status=='table1' or self.status=='table2':
                    if tag == 'tr':
                            for name, value in attrs:
                                    if name=='class' and value=='tlist':
                                            self.linkstatus='tlist'
            
            if self.status=='pages':
                    if tag=='a':
                            for name, value in attrs:
                                    if name=='href':
                                            self.pages.append( value )

            if self.linkstatus=='tlist':
                    if tag == 'a':
                            for name, value in attrs:
                                    if name=='href':
                                            self.href=value
                                            self.linkstatus='data'
            if self.linkstatus=='data':
                    if tag == 'td':
                            for name, value in attrs:
                                    if name=='class' and value=='align-right-td':
                                            self.linkstatus='count'
        def handle_endtag(self, tag):
            if self.status=='pages' and tag=='div':
                    self.status='table1'
                    
            if self.status=='table1' and self.linkstatus=='count' and tag=='td':
                    self.links_base.append( (self.word, self.href, self.count) )
                    self.linkstatus = 'continue'
                    
            if self.status=='table2' and self.linkstatus=='count' and tag=='td':
                    self.links_depend.append( (self.word, self.href, self.count) )
                    self.linkstatus = 'continue'
            
        
        def handle_data(self, data):
            if self.section == 2:
                    #print( '|' + data + '|' )
                    r = re.search( '^(\d+)$', data )
                    if r:
                            self.base_count = r.group(0)
                    
            if self.linkstatus=='data' and data.strip() != "" :
                    self.word=data.strip()
                    
            if self.linkstatus=='count' and data.strip() != "":
                    self.count=data.strip()
        
        def get_base(self):
            return self.links_base
        
        def get_depend(self):
            return self.links_depend
        
        def get_basecount(self):
            return self.base_count

         	  
class Wordstat:
    def __init__(self):
        self.base=[]
        self.depend=[]
        self.base_count=0
        self.values = { 'cmd':'words', 'ts':'1297683175', 'key':'267137b0bacaa5d9ffb6c2ef45d90810'} 
        self.referer = 'http://wordstat.yandex.ru/'
        self.base_url = 'http://wordstat.yandex.ru/?'
        self.headers = {
					'Host' : 'wordstat.yandex.ru',
					'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13',
					'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Accept-Language' : 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
					'Accept-Encoding' : 'gzip,deflate',
					'Accept-Charset' : 'windows-1251,utf-8;q=0.7,*;q=0.7',
					'Keep-Alive' : '115',
					'Connection' : 'keep-alive',
					'Referer' : 'http://wordstat.yandex.ru/',
					'Cookie' : 'yandexuid=2466623021266432176; yabs-frequency=/3/Tm805rm6F000/; fuid01=4adb671208d39176.Hwv7MO9L_HGqQtH32e8RIJGely6JfkkboT1rkrZLKeGK66wA__23E8c3i9Tqui-fI8E_zZDhLw_zpb-44Fc7F0OoaJxLqkfls0q_3hIKlIEjhRdCYL18fY8H4psMykjd; my=YyMCAQUA; L=Vg0LemFTR1JcA0RAU2FQdFEBAltlZgkEGiMhXw4Pel9JFQw4Hk0pWURFRgZ5FDkhJ0YxNAIZCwNrKh8gEz41Tw==.1291390431.8486.213251.339520e61be5fa481aee6bd4b4e8f973; yp=4294967295.cw.48677%231300105210.ygu.1; yandex_gid=10758',
		}
        
    def get_base( self ):
        return self.base
	
    def get_depend( self ):
        return self.depend
		
    def get_basecount( self ):
        return self.base_count
	
    def set_value( self, key, value ):
        self.values[key]=value
	
    def parse( self, word, deep=True, sleep=10 ):
        self.values['page']=1
        self.values['text']=word
        nextpage = True
        while nextpage:
            self.headers['Referer']=self.referer
            data = urllib.urlencode(self.values)
			
            req = urllib2.Request( self.base_url + data,  headers=self.headers ) 
            referer=self.base_url + data
			
            response = urllib2.urlopen( req )
            outdata = decode( response )

            we = WordsExtraction()
            we.feed( outdata )        
			
            self.base.extend( we.get_base() )
            self.depend.extend( we.get_depend() )
            self.base_count = we.get_basecount()
			
            print( nextpage, len( self.base ), len( self.depend ) )

            oldpage = int( self.values['page'] )
            if len(we.pages) > 0:
                for i in we.pages:
                    params = urldecode(i)
                    if  int(params['page']) > int( self.values['page']):
                        self.values['page']=params['page']
                        self.values['key']=params['key']
                        self.values['ts']=params['ts']
												
            if oldpage == int(self.values['page']):
                nextpage = False
            else:
                nextpage = True
				 
            if not deep or not nextpage:
                break;
				
            time.sleep( random.randint(sleep, sleep + sleep/2.0) )    
        return
    


def append_to_file( out, data, sep=';' ):
    for word, href, count in data:
            out.write( word )
            out.write( ',' )
            out.write( count )
            out.write( sep )
    out.write( '\n' )
            
def append_data( filename, data ):
    outfile = open( filename, "a" )
    word, base, depend = data
    outfile.write( '#' )
    outfile.write( word )
    outfile.write( '\n' )
    
    append_to_file( outfile, base )
    append_to_file( outfile, depend )
    
    outfile.close()

def roll_data( filename, data ):
    outfile = open( filename, "a" ) 
    append_to_file( outfile, data, '\n' )
    outfile.close()
        
if __name__ == '__main__':
    ws = Wordstat()
    ws.parse( "Электронная сигарета perfect smoke" )
    base = ws.get_base()
    roll_data( "tt.txt", base ) 

        
        

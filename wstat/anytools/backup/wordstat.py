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
import xml.etree.ElementTree as etree

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
            return int(self.base_count)

         	  
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
        return int(self.base_count)
	
    def set_value( self, key, value ):
        self.values[key]=value
	
    def set_headers( self, key, value):
        self.headers[key]=value
        
    def parse( self, word, deep=True, sleep=10 ):
        print( "%s" % word )
        self.values['page']=1
        self.values['text']=word
        nextpage = True
        while nextpage:
            time.sleep( random.randint(sleep, sleep + sleep/2.0) ) 
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
        return
    

class Statist:
    def __init__(self):
        self.stat = []
        
    def extract_data(self, data):  
        self.stat = []
        for atom in data:
            bases, tokens, deeps = atom
            bases  = [ x.encode("utf-8") for x in bases if len(x.strip()) > 0 ]
            tokens  = [ x.encode("utf-8") for x in tokens if len(x.strip()) > 0 ]
            deeps  = [ x.encode("utf-8") for x in deeps if len(x.strip()) > 0 ]
            count_bases = 0
            #print( bases, tokens, deeps )
            for base in bases:
                ws = Wordstat()
                ws.parse( base, False )
                count_bases += ws.get_basecount()
            
            count_tokens = 0
            for token in tokens:
                td = token
                if len( deeps ) > 0:
                    for deep in deeps:
                        td = token + ' ' + deep
                        ss = Wordstat()
                        ss.parse( td, False )
                        count_tokens += ss.get_basecount()
                else:
                    ts = Wordstat()
                    ts.parse( td, False )
                    count_tokens += ts.get_basecount()
            
            X = 0
            if count_bases != 0:
                X = float(count_tokens) / count_bases 
            else:
                X = count_tokens
                
            self.stat.append( X )
            
        return self.stat;
        
    def calculate_deep(self, data):
        """
            Dat is list of data, example:
            [ [ ['ford'], ['ford focus', 'ford mondeo'], ['repair', 'tools', 'services'] ],  ]
            selected 'ford' count as base value 
            next : 
            selected data 'ford focus repair' 'ford focus tools' 'ford focus services' counts as single value 
            selected data 'ford mondeo repair' ...  as single vale 
            returned list 
            [ X1, X2, .. ] where 
            X1 = ( 'ford focus tools' + 'ford focus tools' + 'ford focus services' ) / 'ford'
            
            if data list value as 'ford' empty then
            X1 = ( 'ford focus tools' + 'ford focus tools' + 'ford focus services' )
            
            if data list value as ['repair', 'tools', 'services' ] empty then
            X1 = ( 'ford focus'  +  'ford mondeo' )  / 'ford' 
            
            if data list value as ['ford'] and ['repair', 'tools', 'services' ] empty
            X1 = ( 'ford focus' + 'ford mondeo' )
        """
        self.stat = []
        for atom in data:
            bases, tokens, deeps = atom
            bases  = [ x.encode("utf-8") for x in bases if len(x.strip()) > 0 ]
            tokens  = [ x.encode("utf-8") for x in tokens if len(x.strip()) > 0 ]
            deeps  = [ x.encode("utf-8") for x in deeps if len(x.strip()) > 0 ]
            count_bases = 0
            #print( bases, tokens, deeps )
            for base in bases:
                ws = Wordstat()
                ws.parse( base, False )
                count_bases += ws.get_basecount()
            
            count_tokens = 0
            for token in tokens:
                td = token
                if len( deeps ) > 0:
                    for deep in deeps:
                        td = token + ' ' + deep
                        ss = Wordstat()
                        ss.parse( td, False )
                        count_tokens += ss.get_basecount()
                else:
                    ts = Wordstat()
                    ts.parse( td, False )
                    count_tokens += ts.get_basecount()
            
            X = 0
            if count_bases != 0:
                X = float(count_tokens) / count_bases 
            else:
                X = count_tokens
                
            self.stat.append( X )
            
        return self.stat;
              
            
class Report:
    def __init__(self):
        self.attrib = {}
        self.items = []
        self.calculated = False
        self.calcdata = []
    
    def load_from_node(self, node):
        self.attrib = node.attrib
        its = node.findall( 'item' )
        for i in its:
            self.items.append( i.attrib )

    def __str__(self):
        result = ( 'report : %s\n' % self.attrib )
        for i in self.items:
            result += ( 'item: %s\n' % i )
        return result     

    def calculate(self):
        if not self.calculated:
            statdata = []
            for i in self.items:
                values = [ x.strip() for x in i['value'].split(',') ]
                bases = [ x.strip() for x in i['base'].split(',') ]
                deeps = [ x.strip() for x in i['deep'].split(',') ]
                statdata.append( [bases, values, deeps ] )
            s = Statist()
            self.calcdata = s.calculate_deep(statdata)
            self.calculated = True
        #print( statdata )
        return self.calcdata
    

def repors_loader( filename ):
    if __name__ == '__main__':
        tree = etree.parse( filename )
        root = tree.getroot()
        nodes = root.findall( "report" )
        reports = []
        for i in nodes:
            r = Report()
            r.load_from_node(i)
            reports.append( r )
    return reports
    
            
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

"""
 Давайте подумаем, какого рода отчеты должны присутствовать в возможностях парсера wordstat, 
 1. это отчет количества запросов по каждому из ключевых фраз например : 
    Мазда 3 купить 
    Ford Focus купить
    ......
    на выходе : 
    [ 33000, 50000, ... ]
    
 2. это возможность в качестве экономии сил, задавать дополнительные слова, и использовать их сумму запросов в качестве одного токена, например : 
    задаем слова токена и слова с которыми оно будет запрашиваться, как пример :
    'мазда 3, mazda 3', 'разборка, запчасти', в результате задания таких параметров должно получиться единственное число которое будет
    являтся суммой количества запросов : 
    'мазда 3 разборка'
    'мазда 3 запчасти'
    'mazda 3 разборка'
    'mazda 3 запчасти'
    самих таких токено на отчет может быть любое количество к примеру 
    f1 = [ [], ['форд', 'ford'], ['разборка', 'разбор', 'запчасти б у'] ]
    f2 = [ [], ['опель', 'opel'], ['разборка', 'разбор', 'запчасти б у'] ]
    f3 = [ [], ['мазда', 'mazda'], ['разборка', 'разбор', 'запчасти б у'] ]
    f4 = [ [], ['хонда', 'honda'], ['разборка', 'разбор', 'запчасти б у'] ]
    .........
    на выходе получаем список из 4 элементов, количества запросов на каждый токен [ 60000, 50000, 30000, 20000 ], 
    из которого можем заключить больший объем рынка для запчастей  форд и т.д.
    
 3. к возможности отчета 2., добавляем относительность, т.е. выявление относительного показателя, т.е. допустим надо сделать предположение на какие автомобили
    спрашивают больше запчастей на 1 единицу, из отчета выше мы имеем только абсолютные значения запросов, воспользуемся примером выше : 
    f1 = [ [], ['форд', 'ford'], ['разборка', 'разбор', 'запчасти б у'] ]
    f2 = [ [], ['опель', 'opel'], ['разборка', 'разбор', 'запчасти б у'] ]   
    
    в результате мы получим некоторые числа допустим [60000, 50000], из этого мы можем заключить только об объеме рынка, но для того чтобы привести эти цифры к единому
    знаменателю, нам надо поделить эти числа на число запросов со словом ford + форд, или opel + опель, тогда мы приводим эти числа к некоторому относительному значению, 
    конечно же все запросы это некоторое допущение, допустим если с компанией форд случится некоторый скандал или еще что-нибудь, что привлечет большой интерес со стороны
    интернет пользователей, то результат чистого запроса 'форд' будет сильно искажен, поэтому надо внимательно относится к этой возможности и задания базы, т.е. возможно база должна быть более предсказуема, скажем быть сочетанием слов, к примеру 'форд купить", тогда база будет похожа у всех токенов
    
    f1 = [ ['форд купить', 'ford купить'], ['форд', 'ford'], ['разборка', 'разбор', 'запчасти б у'] ]
    f2 = [ ['опель купить', 'opel купить'], ['опель', 'opel'], ['разборка', 'разбор', 'запчасти б у'] ]       
    
    в результате получим список [1.5730876605248465, 1.2078706199460916]
    резульат косвенно может значить,  что относительный спрос на запчасти выше на единицу покупаемого товара у форд
 
 4. Еще один вид данных которые хотелось бы получить, это слова стоящие рядом с нашей ключевой фразой
    допустим входящие данные это просто списки вида 
    f1 = [ [], ['форд', 'ford'], ['разборка', 'разбор', 'запчасти б у'] ]
     f2 = [ [], ['опель', 'opel'], ['разборка', 'разбор', 'запчасти б у'] ]
    тогда результатом будет список списков из фраз стоящих рядом с заданными
    [ [ 'форд разборка' + 'форд разбор' ...], [ .. 'opel разбор' ..], .. ]
"""
            
if __name__ == '__main__':
    reports = repors_loader( "reports.xml" )
    print reports[0].calculate()
    
        
        

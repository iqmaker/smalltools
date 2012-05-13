# -*- coding: utf-8 -*-
import urllib
import urllib2
import time
import gzip
import StringIO
import zlib
from HTMLParser import HTMLParser
from urllib2 import urlopen
import codecs
from itertools import *
import random
import re
import pickle
import xml.etree.ElementTree as etree
import os
import sys
import math
from pygooglechart import SimpleLineChart, StackedHorizontalBarChart, StackedVerticalBarChart, \
    GroupedHorizontalBarChart, GroupedVerticalBarChart
from pygooglechart import PieChart2D
from pygooglechart import PieChart3D
from datetime import date
import datetime
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))



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
        self.values = { 'cmd':'words', 'geo':'', 'text_geo':''}
        self.referer = 'http://wordstat.yandex.ru/'
        self.base_url = 'http://wordstat.yandex.ru/?'
        self.headers = {
					'Host' : 'wordstat.yandex.ru',
					'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.151 Chrome/18.0.1025.151 Safari/535.19',
					'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Accept-Language' : 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
					'Accept-Encoding' : 'gzip,deflate,sdch',
					'Accept-Charset' : 'windows-1251,utf-8;q=0.7,*;q=0.3',
					'Connection' : 'keep-alive',
					'Referer' : 'http://wordstat.yandex.ru/',
                    'Cookie' : 'yandexuid=1355143301318790899; fuid01=4dc7ff1c1d1605b3.O6zynGckTNmwnzKRJdZvQSSOW1JDtD_q3cljDSwK0YareCg2xrCljDCDSGR--6wVhODeQMHTBuG5DJE9tV1vP0PaDHoOoO3V7yiPYVeCLTA81aG82mqIrs18mmiW137r; yandex_login=poncy.ru; my=YygBgNU2AQEA; yp=1637339331.sp.#1651651362.udn.cG9uY3kucnU=; Session_id=1336291362.2.3.100619661.2:279875870:180.8:1336291362516:1595440222:7.83997.49047.c9902847e838acbea7ab726b299814c8; L=RlQJflpFaUF4XUZJZAZ0AFd9YgZcRmpeN14GCzZpJ0IzIVdwGlFTCA5jAFdHByYwXypEM1MBZGZBfCsAIxZYaQ==.1336291362.9346.293945.a1c09cbac1e3e7cbf8fabe19c400423c; spravka=dD0xMzM2MzA3MzcwO2k9OTUuMjQuMTI0Ljk0O3U9MTMzNjMwNzM3MDE2ODg1MzYxMjtoPTA2YmZhNjg3NGEzMWIwMzJhOWMwNmE5OTBiMDgzYTgx; aw=1_teJxinMEgtFWhSWLDpGUc63WSJI6UTeLQ1FISMFFo5yhTT5JwkJjEoayiJMCx#tr5NDHUgLbO/m+AykTRbM4VDRdVKwANIzZZUEaqLncnwCim+xW8SxHEhvsFnM#tsR5I3wHSMtpKAmvmLuZYrKckkGO4h6Nc3UiiAEhf0lUS+HDvMEeCgZLADyBd#YoS7EcWbRMQ4GBob/AAAAAP//AwCfxDAf#A#; yabs-frequency=/4/cG0200uPha_H99XF/Tm805tWDFDZ603fu3IFSnW0wU0qkT7O1Gt0D9RDe0KDi3KKFSm124mry0003Wi00FGyDd0001000/; __utma=190882677.1199585786.1336909599.1336909599.1336909599.1; __utmc=190882677; __utmz=190882677.1336909599.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=190882677.|2=Account=Yes=1^3=Login=Yes=1',
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

    def parse( self, word, all_pages=True, sleep=10, page=1 ):
        print( "%s" % word.decode("utf-8") )
        self.values['page']=page
        self.values['t']=word
        nextpage = True
        while nextpage:
            time.sleep( random.randint(sleep, sleep + sleep/2.0) )
            self.headers['Referer']=self.referer
            data = urllib.urlencode(self.values)

            req = urllib2.Request( self.base_url + data,  headers=self.headers )
            referer=self.base_url + data

            try:
                we = WordsExtraction()
                response = urllib2.urlopen( req )
                outdata = decode( response )
                open( "tmpfile.html", "w" ).write( outdata )
                we.feed( outdata )
            except:
                self.parse(word, all_pages, sleep, int(self.values['page']) )

            self.base.extend( we.get_base() )
            self.depend.extend( we.get_depend() )
            self.base_count = we.get_basecount()

            print( nextpage, len( self.base ), len( self.depend ), self.values['page'] )

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

            if not all_pages or not nextpage:
                break;
        return


class Statist:
    def extract_data(self, data, all_pages=False):
        stat = []
        for atom in data:
            bases, firsts, seconds, thirds = atom
            bases  = [ x.encode("utf-8") for x in bases if len(x.strip()) > 0 ]
            firsts  = [ x.encode("utf-8") for x in firsts if len(x.strip()) > 0 ]
            seconds  = [ x.encode("utf-8") for x in seconds if len(x.strip()) > 0 ]
            thirds  = [ x.encode("utf-8") for x in thirds if len(x.strip()) > 0 ]
            curdata = []
            for first in firsts:
                td = first
                if len( seconds ) > 0:
                    for second in seconds:
                        td = first + ' ' + second
                        if len(thirds) > 0:
                            for third in thirds:
                                td = first + ' ' + second + ' ' + third
                                ss = Wordstat()
                                ss.parse( td, all_pages )
                                curdata.extend( ss.get_base() )
                        else:
                            ts = Wordstat()
                            ts.parse( td, all_pages )
                            curdata.extend( ts.get_base() )
                else:
                    ts = Wordstat()
                    ts.parse( td, all_pages )
                    curdata.extend( ts.get_base() )

            stat.append( curdata )
        return stat;

    def calculate_deep(self, data):
        """
            Data is list of data, example:
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
        stat = []
        for atom in data:
            bases, firsts, seconds, thirds = atom
            bases  = [ x.encode("utf-8") for x in bases if len(x.strip()) > 0 ]
            firsts  = [ x.encode("utf-8") for x in firsts if len(x.strip()) > 0 ]
            seconds  = [ x.encode("utf-8") for x in seconds if len(x.strip()) > 0 ]
            thirds  = [ x.encode("utf-8") for x in thirds if len(x.strip()) > 0 ]
            count_bases = 0
            #print( bases, firsts, seconds )
            for base in bases:
                ws = Wordstat()
                ws.parse( base, False )
                count_bases += ws.get_basecount()

            count_firsts = 0
            for first in firsts:
                td = first
                if len( seconds ) > 0:
                    for second in seconds:
                        td = first + ' ' + second
                        if len(thirds) > 0:
                            for third in thirds:
                                td = first + ' ' + second + ' ' + third
                                ss = Wordstat()
                                ss.parse( td, False )
                                count_firsts += ss.get_basecount()
                        else:
                            ts = Wordstat()
                            ts.parse( td, False )
                            count_firsts += ts.get_basecount()
                else:
                    ts = Wordstat()
                    ts.parse( td, False )
                    count_firsts += ts.get_basecount()

            X = 0
            if count_bases != 0:
                X = float(count_firsts) / count_bases
            else:
                X = count_firsts

            stat.append( X )

        return stat;


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

    def get_type(self):
        return self.attrib['type']

    def get_title(self):
        return self.attrib['title'].encode("utf-8")

    def get_id(self):
        return self.attrib['id']

    def is_sorted(self):
        if 'sorted' in self.attrib and self.attrib['sorted'] == 'true':
            return True
        return False

    def get_labels(self):
        labels = []
        for i in self.items:
            if 'label' in i:
                labels.append( i['label'].encode("utf-8") )
            else:
                labels.append( i['first'].encode("utf-8") )
        return labels

    def get_annotate(self):
        if 'annotate' in self.attrib:
            return self.attrib['annotate']
        if self.get_type() == 'pie':
            return 'percent'
        if self.get_type() == 'barchart':
            return 'part'

        return 'absolute'

    def calculate(self):
        if not self.calculated:
            statdata = []
            for i in self.items:
                firsts, seconds, thirds, bases = [[],[],[],[]]
                if 'first' in i:
                    firsts = [ x.strip() for x in i['first'].split(',') ]
                if 'second' in i:
                    seconds = [ x.strip() for x in i['second'].split(',') ]
                if 'third' in i:
                    thirds = [ x.strip() for x in i['third'].split(',') ]
                if 'base' in i:
                    bases = [ x.strip() for x in i['base'].split(',') ]

                statdata.append( [bases, firsts, seconds, thirds ] )
            
            s = Statist()
            if self.get_type() == 'barchart' or self.get_type() == 'pie':
                self.calcdata = s.calculate_deep(statdata)

                for index in range(len(self.calcdata)):
                    self.items[index]['count'] = self.calcdata[index]

            elif self.get_type() == 'simple_list' or self.get_type() == 'extra_list' or self.get_type() == 'html' or self.get_type() == 'extra_html':
                if self.get_type() == 'extra_list' or self.get_type() == 'extra_html': 
                    self.calcdata = s.extract_data(statdata, True )
                else:
                    self.calcdata = s.extract_data(statdata)

            self.calculated = True
        #print( self.items )

        if self.is_sorted():
            self.items = sorted(self.items, key=lambda count: count['count'])
            self.calcdata.sort()

        return self.calcdata


class RbuildItem:

    def __init__(self):
        self.id = ''
        self.interval = ''
        self.lastdate = ''
        self.nextdate = ''
        self.attrib = {}

    def load_from_node( self, node ):
        self.attrib = node.attrib
        self.id = node.attrib[ 'id' ]
        self.interval = node.attrib[ 'interval' ]
        self.lastdate = node.attrib[ 'lastdate' ]
        self.nextdate = node.attrib[ 'nextdate' ]

    def __str__(self):
        return self.id + '->' + self.interval + '->' + self.lastdate + '->' + self.nextdate

    def get_id(self):
        return self.id

def reload_rbuild( ritems, filename ):
    tree = etree.parse( filename )
    root = tree.getroot() 
    nodes = root.findall( 'rbuild/item' )
    for ri in ritems:
        for n in nodes:
            if n.attrib[ 'id' ] == ri.id:
                n.attrib = ri.attrib
    #for i in ritems: print i.attrib
    out = etree.tostring( root, encoding='UTF-8' )
    file( 'reports.xml', 'w' ).write( out )
    
def load_rbuild( filename ):
    tree = etree.parse( filename )
    root = tree.getroot()
    nodes = root.findall( "rbuild/item" )
    ritems = []
    for i in nodes:
        ri = RbuildItem()
        ri.load_from_node(i)
        ritems.append( ri )
    return ritems

def reports_loader( filename ):
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

def annotate_labels( labels, data, absolute="part" ):
    if len(labels) != len(data):
        return labels
    s = sum(data)
    m = min(data)
    nlabels=[]
    for i in range(len(labels)):
        if absolute == 'percent':
            nlabels.append( labels[i] + ' (' + str( math.floor(data[i]*10000.0/s + 0.5)/100.0 ) + '%)' )
        elif absolute == 'part':
            nlabels.append( labels[i] + ' (' + str(math.floor(data[i]/float(m)*100.0 + 0.5)/100.0) + ')' )
        elif absolute == 'absolute':
            nlabels.append( labels[i] + ' (' + str( data[i] ) + ')' )

    return nlabels

class HTMLViewer:
    def __init__(self):
        self.title = ''
        self.labels = []
        self.data = []
    def set_data(self, title, labels, data ):
        self.title = title
        self.labels = labels
        self.data=data

    def get_html(self, file_name):
        out = open( file_name, 'w' )
        out.write( codecs.BOM_UTF8 )
        out.write( '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/></head><title>%s</title><body><h1>%s</h1>' % (self.title, self.title ) )
        for lable, value in zip( self.labels, self.data ):
            out.write( '<h2>%s</h2>'% lable )
            out.write( '<ol>' )
            for item in value:
                word, link, count = item
                urlparams_yandex = { 'text': word,  }
                urlparams_google = { 'q':word, }
                """http://www.google.ru/#sclient=psy-ab&hl=ru&site=&source=hp&q=разборка+мазда+3"""
                oline = '<li><a href="%s">%s</a> - %s<a href="%s" style="font-size:1.2em; margin-left:20px;">yandex</a><a href="%s" style="font-size:1.2em; margin-left:20px;">google</a></li>' % ( ('http://wordstat.yandex.ru' + link), word.decode("utf-8"), count, "http://yandex.ru/yandsearch?%s" % urllib.urlencode(urlparams_yandex), "http://www.google.ru/#sclient=psy-ab&hl=ru&site=&source=hp&%s" % urllib.urlencode(urlparams_google) )
                #print oline
                out.write( oline.encode("utf-8") )
            out.write( '</ol>' )
        out.write( '</body></html>' ) 


    def get_flat(self, file_name):
        out = open( file_name, 'w' )
        out.write( "Отчет : " + self.title + '\n' )
        for lable, value in zip( self.labels, self.data ):
            out.write( "Позиция : " + lable + '\n' )
            for item in value:
                word, link, count = item
                out.write( '\t' + word + ', ' + count + '\n') 

from svg.charts import bar
def create_chart( report, out_name ):
    data = report.calculate()
    dstring = "%04d-%02d-%02d"%( date.today().year, date.today().month, date.today().day )

    if report.get_type() == 'extra_html':
        file_exists = os.path.exists( './reports/statistics_' + report.get_id() + '.py' )
        tout = open( './reports/statistics_' + report.get_id() + '.py', "a")
        if not file_exists:
            tout.write( 'v = {}\n' )
            
        sdata = []
        for d in data: sdata += d
        tout.write( 'v["%s"]='%dstring + str(sdata) + '\n' )
        tout.close()

    result_file = None
    if report.get_type() == 'barchart':
        result_file = out_name + '.svg'
        """
        chart = StackedHorizontalBarChart(480, 40 + 15 * len(report.get_labels()), x_range=(0, max(data) ) )
        chart.set_bar_width( 10 )
        chart.set_colours(['8159F7', ])
        chart.add_data( data )
        chart.set_title( report.get_title() )
        chart.set_legend( ['',] )

        annotatel = annotate_labels( report.get_labels(), data, report.get_annotate() )
        annotatel.reverse()
        chart.set_axis_labels('y', annotatel )
        chart.annotated_data()
        chart.download(result_file)
        """
        fields = [ x.decode("utf-8") for x in report.get_labels() ]
        g = bar.HorizontalBar(fields)
        options = dict(
        scale_integers=True,
        rotate_x_labels = True,
        rotate_y_labels = False,
    	stack='side',
    	height=400 + 30 * len(report.get_labels()),
    	width=480,
    	graph_title=report.get_title().decode( "utf-8" ),
    	show_graph_title=True,
    	no_css=False,)
        g.__dict__.update(options)
        g.add_data(dict(data=data, title='Questions'))
        open( result_file, 'w').write(g.burn())

    elif report.get_type() == 'pie':
        result_file = out_name + '.svg'
        chart = PieChart3D( 730, 300 )
        # Add some data
        chart.add_data( data )
        # Assign the labels to the pie data
        chart.set_title( report.get_title() )
        annotatel = annotate_labels( report.get_labels(), data, report.get_annotate() )
        chart.set_pie_labels( annotatel  )
        # Download the chart
        chart.download( result_file )

    elif report.get_type() == 'extra_list' or report.get_type() == 'list':
        result_file = out_name + '.txt'
        hv = HTMLViewer()
        hv.set_data( title=report.get_title(), labels=report.get_labels(), data=data )
        hv.get_flat( result_file )

    elif report.get_type() == 'extra_html' or report.get_type() == 'html':
        result_file = out_name + '.html'
        hv = HTMLViewer()
        hv.set_data( title=report.get_title(), labels=report.get_labels(), data=data )
        hv.get_html( result_file )

    return result_file




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

def create_report(reports, ritem, out_name ):
    for i in reports:
        if i.get_id() == ritem.get_id():
            return create_chart(i, out_name )
    return ''

intervals = { '3':3, '2':2, '4':4, '5':5, '6':6, 'week':7, 'day':1, 'month':30, 'year':365 }
def create_reports():
    reports_file = 'reports.xml'
    reports = reports_loader( reports_file )
    items = load_rbuild( reports_file )

    for ritem in items:
        cdate = date.today().isoformat()
        if ritem.nextdate <= cdate and cdate > ritem.lastdate:
            create_report( reports, ritem, './reports/%s_%04d-%02d-%02d'%( ritem.id, date.today().year, date.today().month, date.today().day ) )
            ritem.lastdate = cdate
            ritem.attrib['lastdate'] = ritem.lastdate
            ritem.nextdate = ( date.today() + datetime.timedelta( intervals[ ritem.interval ] ) ).isoformat()
            ritem.attrib['nextdate'] = ritem.nextdate
            print ritem.attrib
        else:
            print 'skip : ', ritem

    reload_rbuild( items, reports_file )

if __name__ == '__main__':
    create_reports()



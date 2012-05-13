# -*- coding: utf-8 -*-
import sys
import imp
import datetime
import urllib 
import wordstat

DAY, WEEK, MONTH, YEAR = 1, 7, 30, 365

def create_table_head( tup ):
    result = ['<tr>' ]

    result.append( '<td class="head">%s</td>' % 'Запрос' )
    result.append( '<td class="head">%s</td>' % 'Начало периода' )
    result.append( '<td class="head">%s</td>' % 'Конец периода' )
    result.append( '<td class="head">%s</td>' % 'Динамика роста (%)' )
    
    days = sorted( tup.keys() )
    for i in days:
        result.append( '<td class="head">%s</td>' % i )
    result.append( '</tr>' )
    return ''.join( result )

def create_table_row( tup, *vals ):
    result = ['<tr>']
    for i, v in enumerate(vals):
        if i == 0:
            result.append( '<td class="item">%s <div class="right"><a class="yandex" href="http://yandex.ru/yandsearch?%s">Y </a><a class="google" href="http://www.google.ru/#sclient=psy-ab&hl=ru&site=&source=hp&%s">G </a> <a class="wordstat" href="http://wordstat.yandex.ru/?cmd=words&page=1&geo=&text_geo=&%s">W</a></div></td>' % ( v, urllib.urlencode( {'text':v}), urllib.urlencode( {'q':v}), urllib.urlencode( {'text':v}) ) )
        elif i == 1:
            result.append( '<td class="first-value">%s</td>' % v )
        elif i == 2:
            delta = vals[2] - vals[1]
            sclass = 'equal'
            if delta > 0.0:
                sclass = 'plus'
            elif delta < 0.0:
                sclass = 'minus'
            result.append( '<td class="second-value">%s <span class="%s">(%+d)</span></td>' % (v, sclass, delta ) )
        elif i == 3:
            if v > 0.0:
                result.append( '<td class="plus">%.2f</td>' % v )
            elif v < 0.0:
                result.append( '<td class="minus">%.2f</td>' % v )
            else:
                result.append( '<td class="equal">%.2f</td>' % v )

        else:
            result.append( '<td>%s</td>' % v )

    days = sorted( tup.keys() )
    for i, day in enumerate( days ):
        class_name = 'equal'
        if tup[day] > 0.0 and i > 0 : class_name = 'plus'
        elif tup[day] < 0.0 : class_name = 'minus'
        result.append( '<td class="%s">%+d</td>' % ( class_name, tup[day] ) )

    result.append( '</tr>\n' )

    return ''.join( result )


def html_report( result_report, test_name ):
    
    reports = wordstat.reports_loader( "reports.xml" )
    for i in reports:
        if i.get_id() == test_name:
            r = i
    report_title = r.get_title()
    report_labels = r.get_labels()

    out = file( './reports/' + test_name + '.html', 'w' )
    out.write( 
    """<html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
             <style type="text/css">
             .head { 
              font-weight:bold; font-size:18px; padding:8px; color:#444;
              padding-left:15px;
              padding-right:15px;
             }
             .plus { 
                color:green;
             }
             .minus{ 
                color:red;
             }
             .equal { 
                color:gray;
             }
             .item { 
                padding-left:10px;
             }
             .item, .item > a { 
                font-size:16px; color:#666; font-weight:bold; text-decoration:none;
             }

             .item:first-letter {
               text-transform: uppercase;
             }
             .first-value, .second-value, .plus, .minus, .equal { 
                text-align:center;
             }
             .first-value { 
                color:blue;
             }
             .second-value { 
                color:magenta;
             }
             .yandex, .google, .wordstat { 
                font-size:18px !important;
             }
             .yandex { 
                /*color:#FFCF76 !important;*/
                color:orange !important;
             }
             .google { 
                /*color:#8690FF !important;*/
                color:blue !important;
             }
             .wordstat { 
                /*color:#FF8686 !important;*/
                color:red !important;
             } 
             .right { float:right; margin-right:10px; }
             h1 { color:#666; }
             .date { font-size:10px; color:#444; }
             </style>
        </head>
        <title>%s</title>
        <body>
            <h1>Отчет: «%s»</h1>
            <span class="date">Дата генерации: %s, идентификатор: %s</span>
            <table border="1" >""" % ( report_title, report_title, datetime.date.today().isoformat(), test_name ) )

    first = result_report[0]
    out.write( create_table_head( first[4] ) )

    for r in result_report:
        word = r[0]
        first = r[1]
        last = r[2]
        progress = r[3]
        vals = r[4]
        out.write( create_table_row( vals, equals[word], first, last, progress ) )
      
    out.write( '</table></body></html>' )
    out.close()
   
equals = { }  
def full_data_sorter( data ):
    for i in data:
        v = data[i]
        for num, item in enumerate( v ):
            word, link, count = item
            wl = sorted( word.split() )
            nword = ' '.join( wl )
            item = ( nword, wl, count ) 
            equals[nword] = word
            v[ num ] = item

def statist( original_testname, interval = MONTH ):

    testname = 'statistics_' + original_testname
    fromdate = (datetime.date.today() - datetime.timedelta(interval) ).isoformat()
    todate = datetime.date.today().isoformat()

    data = imp.load_source('testdata', './reports/' + testname + '.py' )

    full_data_sorter( data.v )
    for r in data.v:
        """Преобразование к целому последнего числа, чтобы дальше не мучаться"""
        data.v[ r ] = [ ( x[0], x[1], int( x[2] ) ) for x in data.v[r] ]


    all_days = data.v.keys()
    active_days = []
    for i in all_days:
        if fromdate <= i and i <= todate:
            active_days.append(i)
        
    active_days.sort()
    table = {}
    for i in active_days:
        vals = data.v[i]
        for j in vals:
            word, link, count = j
            if word in table:
                table[word][i] = int(count)
            else:
                table[word] = {i: int(count) }

    result_report = []

    #for i in table:
    #    print i.decode( 'utf-8' ), table[i]
    #print table
    #Найдем самые маленькие значения на каждый день, для статистики
    min_keys = data.v.keys()
    min_items = {}
    for mk in min_keys:
        mv = min( sorted( [ x[2] for x in data.v[ mk ] ] ) )
        min_items[mk]=mv

    #print "min_items", min_items
    for word in table.keys():
        vals = table[word]

        for d in active_days:
            if d not in vals:
                vals[d] = 0

        first_count = vals[ active_days[0] ] 
        base = first_count if first_count > 0 else min_items[ active_days[0] ] - 1
        absolute_positive, absolute_negative, absolute_progress, positive, negative, progress = 0, 0, 0.0, 0, 0, 0.0
        for day in active_days[1:]:
            vals[day] -= first_count
            first_count += vals[day]

            if vals[day] > 0 : 
                absolute_positive += vals[day]
            else:
                absolute_negative -= vals[day]

        absolute_progress = absolute_positive - absolute_negative
        positive = float( absolute_positive ) / base
        negative = float( absolute_negative ) / base
        progress = ( float( sum( [vals[x] for x in vals] ) ) / base - 1.0 ) * 100.0
        result_report.append( (word, base, sum( [vals[x] for x in vals] ), progress, vals,) )
        result_report = sorted( result_report, key=lambda x: -x[3] )

    html_report( result_report, original_testname )

def create_index( reports ):
    out = file( 'index.html', 'w' )
    out.write( '<html><head></head><body>' )
    for r in reports:
        print r
        out.write( '<a href="%s">%s</a><br/>' % ( './reports/' + str( r.attrib['id'] ) + '.html', r.attrib['id'] ) )

    out.write( '</body></html>' )

def main():
    items = wordstat.load_rbuild( 'reports.xml' )    
    for i in items:
        print i.id
        report_name = i.id
        statist( report_name )

    create_index( items )

if __name__ == '__main__' : 
    main() 

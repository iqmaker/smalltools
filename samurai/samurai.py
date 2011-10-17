# -*- coding: utf-8 -*-
import urllib
import urllib2
from urllib import FancyURLopener
from random import choice
import mechanize
import re
import os
import random
user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
    'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; InfoPath.3; MS-RTC LM 8; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; chromeframe/12.0.742.112)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; yie8)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET CLR 1.1.4322; .NET4.0C; Tablet PC 2.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; FunWebProducts)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/11.0.696.57)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; chromeframe/11.0.696.57)',
    'Mozilla/5.0 ( ; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/4.0; FDM; MSIECrawler; Media Center PC 5.0)',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; OfficeLiveConnector.1.4; OfficeLivePatch.1.3; .NET4.0C; .NE',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 7.1; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; AskTB5.5)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.2; .NET4.0C; .NET4.0E)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; FDM; .NET CLR 1.1.4322; .NET4.0C; .NET4.0E; Tablet PC 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; Tablet PC 2.0; InfoPath.3; .NET4.0E)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; FDM; .NET4.0C; .NET4.0E; chromeframe/11.0.696.57)',
]

headers = {
    'Host' : 'www.ripn.net',
    'User-Agent' : choice( user_agents ), #'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.1.16) Gecko/20101130 Firefox/3.5.16',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language' : 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding' : 'gzip,deflate',
    'Accept-Charset' : 'windows-1251,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive' : '300',
    'Connection' : 'keep-alive',
    'Referer' : 'http://www.ripn.net/nic/whois/',
    'Content-Type' : 'application/x-www-form-urlencoded',
    'Server' : 'nginx/0.7.63',
    'Date' : 'Wed, 19 Jan 2011 22:38:32 GMT',
    'Content-Type' : 'text/html; charset=windows-1251',
}

def text_loader( filename ):
    pass

form_data = { 
    'fio':[ 'Автозапчасти для Мазда 3', 'Бу запчасти mazda', 'Бу запчасти для мазда', 'Запчасти для мазда 3', 'Запчасти для mazda 3/6', 'Бу запчасти для мазда 3 мазда 6', 'Авторазборка мазда', 'Разборка мазда', 'Кузовные детали для мазда 3 мазда 6', 'Автозапчасти для Мазда 6', 'Бу запчасти mazda 6/3', 'Бу запчасти для мазда 3/6', 'Запчасти для мазда 6', 'Запчасти для mazda 6/3', 'Бу запчасти для мазда 6 мазда 3', 'Авторазборка мазд', 'Разборка мазд', 'Кузовные детали для мазды 6 мазда 3' ],
    'tel1':[ '+7(916)730-34-73', '8(916)730-34-73', '(916)730-34-73', '8916-730-34-73', '8(916)73-034-73', '+7(916)73-034-73' ],
    's_time':[ '7:00', '8:00', '9:00', '10:00' ],
    'do_time':[ '19:00','20:00', '21:00', '18:00' ],
    'title':[ 'Бу запчасти', 'Разборка Mazda', 'Бу запчасти для Мазда 3 Мазда 6', 'Мазда 3 Мазда 6 запчасти БУ', 'Бу запчасти для Мазда', 'Мазда 3 Мазда 6', 'Запчасти  для Мазды', 'Запчасти с разборки', 'Разборка предлагает запчасти', 'Оригинальные запчасти для Мазда', 'Бу для Мазда', 'Хороший ассортимент запчастей для Мазда', 'Мазда запчасти', 'Запчасти для мазды', 'Разборка мазды', 'Авторазбор мазда', 'Детали с разборки', 'Оригинальные запчасти Мазды', 'Разбор Mazda', 'Мазда3 Мазда6', 'Детали бу мазда', 'Разборка мазда 3 мазда 6', ]
} 

form_text = [ 
    """Оригинальные бу запчасти для мazda 3( 2003-2011), мazda 6 (2008-2011), Mitsubishi Lancer X. Весь ассортимент бу запчастей на указанные автомобили, работаем с раннего утра до позднего вечера. Будем рады помочь. """,
    """Оригинальные бу запчасти для мазда 3, мазда 6. Отличное качество запчастей. Детали все отобраны нашими специалистами. Вы получаете качество оригинала за полцены или даже дешевле. Наша разборка работает до позднего вечера. Уважительное отношение. Звоните будем рады помочь.""",
    """Авторазборка mazda 3, mazda 6 (2008-2011). Отличное состояние запчастей, полный контроль качества продаваемых запчастей. Наша разборка Мазда 3 и Мазда 6, а так же Митсубиси Лансер 10, работает до позднего вечера. Весь ассортимент запчастей на указанные автомобили. Хорошие люди, хорошие запчасти. Будем рады помочь в выборе деталей.""",
    """Разборка мазда 3, мазда 6 (2008-2011), предлагает бу запасти с разборки в отличном состоянии. Наша разборка поможет сэкономить Ваши время и деньги. У нас вы можете приобрести Бампер, Дверь, Капот, Телевизор, Двери, Салон, Аирбэг, Фары, Фонари, Стекла, Привода, Коробку, Двигатель, Рычаги и многое другое на ваш автомобиль Мазда. Вежливые люди, в будни работаем до позднего вечера. Звоните будем рады помочь в выборе.""",
    """Разборка мазда 3 предлагает оригинальные бу запчасти в отличном состоянии, за умеренную плату. Мы отбираем детали в самом лучшем состоянии, наши специалисты помогут выбрать деталь на ваш автомобиль мазда 3, мазда 6 (2008-2011). По желанию покупателя разборка будет работать в любое время суток вплоть до самого позднего вечера или самого раннего утра. Дружелюбное отношение и качественные запчасти. Звоните будем рады помочь.""",
    """Разборка мазда 3, Мазда 6(2008-2011) предлагает оригинальные бу запчасти в отличном состоянии по отличным ценам. Только проверенные детали. На автомобиль мазда 3 у нас есть весь перечень запчастей, начиная от кузова и заканчивая подвеской, салоном, электрикой. Доброжелательное отношение. Звоните будем рады помочь и определиться с выбором деталей.""",
    """Бу запчасти для мазда 3, Мазда 6(2008-2011) в отличном состоянии предлагает разборка. Бампера, двери, капоты, крылья, ходовая, электрика, салон и все остальное что может потребоваться вашему автомобилю. Работаем до позднего вечера, вежливые люди. Будем рады помочь в выборе деталей. """,
    """Бу запчасти для мазда 3, Мазда 6 (2008-2011). Авторазборка предлагает бу запчасти в отличном состоянии для вашего авто. Наши детали проходят обязательную проверку специалистами. Наша разборка поможет сэкономить ваши средства и получить максимум качества от оригинала по отличным ценам. Вежливые люди помогут подобрать и определиться с деталями. Звоните будем рады помочь. """,
    """Оригинальные бу запчасти для мазда 3(2004-2011), Мазда 6(2008-2011) от разборки автомобилей. Весь ассортимент на данные автомобили оригинальных бу запчастей в отличном состоянии. Вежиливое отношение, работаем до позднего вечера, отличное состояние запчастей. Будем рады помочь в выборе. """,
    """Авторазборка японских автомобилей мазда 3(2004-2011), Мазда 6(2008-2011), предлагает бу детали на данные автомобили в отличном состоянии, самый полный перечень деталей для Мазда 3. Работаем до позднего вечера. Будем рады помочь выбрать оптимальный вариант.""",
    """Авторазборка автомобилей мазда, предлагает бу детали для мазда 3( 2004-2011). Мазда 6(2008-2011). Все детали проходят проверку, и вы получаете детали в отличном состоянии. У нас вы можете найти весь перечень запчастей на данные автомобили. Все детали кузова, ходовой, электрики, салона и пр и пр. Работаем до 21:00 и позже. Вежливые люди. Будем рады помочь.""",
    """Оригинальные бу запчасти для мазда 3 и мазда 6 (в новом кузове). На нашем складе доступны весь ассортимент бу запчастей. Отличное качество автозапчастей, дружелюбное отношение. Господа и дамы, при выборе запчасти практически всегда (если это не расходная деталь) лучше выбрать оригинал от производителя, а если цена кусается выбирайте бу оригинал, в нашем случае разницы практически никакой т.к. состояние деталей отличное а цена отличается в 2 а иногда даже в 5 раз по сравнению с новым оригиналом. Будем рады помочь.""",
    """Авторазборка мазда 3, мазда 6 (2008-2011), предлагает весь спектр запчастей на данные автомобили. Отличные цены, доброжелательные люди. Бампера, крылья, двери, ходовая, электрика, шины, диски, стекла, фары, салон и пр. позиции. Будем рады помочь, в подборе запчастей.""",
    """Автозапчасти для вашего автомобиля Мазда 3 и для вашего автомобиля Мазда 6(2008-2011), предлагает разборка данных моделей автомобилей. Мы отбираем только проверенные детали. Таким образом вы гарантированно получаете рабочие запчасти. На детали качество которых не возможно проверить на месте, мы даем гарантийный срок на установку, т.е. гарантируем, что данная деталь работает, иначе мы вернем средства или обменяем деталь. Работаем 7 дней в неделю. Будем рады помочь в покупке и выборе запчастей.""",
]

mechanize_header = [ ( i, headers[i] ) for i in headers ]  

URL = "http://www.7samuraev.ru/add_z.php?marka=MAZDA"

import re

class MyOpener(FancyURLopener, object):
    version = choice(user_agents)


def salt():
    pass

def LastMessageIsMy( model ):
    myopener = MyOpener()
    result = myopener.open(u'http://7samuraev.ru/zap.php?model=%s'% urllib.quote( model.encode( 'utf-8') ) )
    data = result.read()
    phones = re.findall( 'Телефон: <B>(.+)</B>', data.decode("cp1251").encode("utf-8") )
    if phones[0] in form_data['tel1']:
        return True
    return False
    
def transform_text( text ):
    result = []
    for i in text:
        if i == ' ':
            i = i * ( int(random.random() * 2 ) + 1)
            result.append( i )
        else:
            result.append( i )
    return  ''.join( result )
  
def get_image( ):
    import os
    return os.getcwd() + '/disk.bmp'

def AddMessage( model ):

    br = mechanize.Browser()
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.addheaders = mechanize_header

    url =  URL
    br.open( url )
    br.select_form(nr=0)
    br.find_control(name="model").value = [model]

    br.form["fio"] = choice( form_data["fio"] ).decode("utf-8").encode( "cp1251" )
    br.form["tel1"] = choice( form_data["tel1"] ).decode("utf-8").encode( "cp1251" )
    br.form["s_time"] = choice( form_data["s_time"] ).decode("utf-8").encode( "cp1251" )
    br.form["do_time"] = choice( form_data["do_time"] ).decode("utf-8").encode( "cp1251" )
    br.form["title"] = choice( form_data["title"] ).decode("utf-8").encode( "cp1251" )
    br.form["text"] = transform_text( choice( form_text ) ).decode("utf-8").encode( "cp1251" )
    #br.find_control( name='userfile1' ).add_file( open( get_image() ), 'image/jpeg', get_image() )
    br.submit()
    html = br.response().read()
    file( '/tmp/samuray_response%s.html' % model, 'w' ).write( html )
    #print br

def SmartAddMessage( model ):
    if not LastMessageIsMy( model ):
        AddMessage( model )
        return True
    return False

if __name__ == "__main__":
    #AddMessage( '6' )
    print SmartAddMessage( "3" )
    print SmartAddMessage( "6" )

import urllib2
headers = {
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

req = urllib2.Request( "http://ya.ru", headers=headers )
response = urllib2.urlopen( req )
data = response.read()
print( data )



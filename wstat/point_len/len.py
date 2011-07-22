import math

class Point:
    def __init__(self, s, d):
        self.s = s * (math.pi / 180.0)
        self.d = d * (math.pi / 180.0)
        #print(s, math.radians(s), self.s )


def len_point(p1, p2):
    a = p1.d - p2.d
    if a < 0.0:
        a = -a
    if a > math.pi:
        a = 2.0 * math.pi - a

    r=math.sin(p1.s) * math.sin(p2.s) + math.cos(p1.s) * math.cos(p2.s) * math.cos(a)
    l = math.acos(r)* 6367444.6571225
    return l

#http://maps.google.com/maps/geo?q=%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F+%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F+%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%96%D0%B0%D0%B2%D0%BE%D1%80%D0%BE%D0%BD%D0%BA%D0%B8&output=csv&oe=utf8\&sensor=false&key=ABQIAAAAuupUR-QeA1RBqW27VezpmBTTtjJ_JLIdQD6J5MpXezDsbLpPWRSYD8KZWgZlZ5cYxC8q8uszRiymdQ

#Широта, Долгота
#Пятницкое шоссе д. 23 55.8486978,37.3684392
#Метро митино 55.8460374,37.3609895
#Жаворонки 55.6419972,37.0969333
#Москва 55.7557860,37.6176330
#Вологда 59.2152406,39.8767089
#Ивана Франко д. 30 55.7284008,37.4265157
#Митинская 36 55.8460067,37.3632520

pf = Point( 55.400165011944446, 37.280001693333334 )
pt = Point( 55.400160009444444, 37.280160005000002 )

print len_point(pf, pt)
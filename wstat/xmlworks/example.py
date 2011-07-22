import xml.etree.ElementTree as etree

class Report:
    def __init__(self):
        self.attrib = {}
        self.items = []

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
        
        

if __name__ == '__main__':
    tree = etree.parse("reports.xml")
    root = tree.getroot()
    nodes = root.findall( "report" )
    for i in nodes:
        r = Report()
        r.load_from_node(i)
        print( r )
        

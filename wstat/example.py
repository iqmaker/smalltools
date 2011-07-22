import xml.etree.ElementTree as etree


        
        

if __name__ == '__main__':
    tree = etree.parse("reports.xml")
    root = tree.getroot()
    nodes = root.findall( "report" )
    for i in nodes:
        r = Report()
        r.load_from_node(i)
        print( r )
        

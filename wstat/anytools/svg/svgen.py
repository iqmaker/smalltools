#coding -*- utf-8 -*-
from xml.dom.minidom import Document, parseString

def main():

    # Create the minidom document
    doc=Document()
    # Create the <wml> base element

    svg = doc.createElement("svg")
    svg.setAttribute('version', '1.1')
    svg.setAttribute('baseProfile', 'full')
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
    svg.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
    svg.setAttribute('xmlns:ev', 'http://www.w3.org/2001/xml-events')
    svg.setAttribute('height', '400px')
    svg.setAttribute('width', '400px')
    doc.appendChild(svg)

    rect = doc.createElement('rect')
    rect.setAttribute( 'x', '0' )
    rect.setAttribute( 'y', '0' )
    rect.setAttribute( 'width', '200' )
    rect.setAttribute( 'height', '200' )
    rect.setAttribute( 'fill', 'none' )
    rect.setAttribute( 'stroke', 'black' )
    rect.setAttribute( 'stroke-width', '5px' )
    rect.setAttribute( 'stroke-opacity', '0.5' )

    svg.appendChild( rect )
    print doc.toprettyxml(indent="  ")

if __name__ == "__main__":
    main()
__author__ = 'vitorio'

from lxml import etree
import os
import argparse

# from ocropodium ocradmin/nodelib/utils.py
# Apache License 2.0
def hocr_from_abbyy(abbyyxml, xsltfile):
    """
    Apply some XSL to transform Abbyy XML to HOCR.
    """
    with open(os.path.join(os.path.dirname(__file__), xsltfile), "r") as tmpl:
        with open(abbyyxml, "r") as abbyy:
            xsl = etree.parse(tmpl)
            xml = etree.parse(abbyy)
            transform = etree.XSLT(xsl)
            return unicode(transform(xml))

parser = argparse.ArgumentParser(description='Transform an ABBYY XML file to an hOCR file.  This assumes an Internet Archive-generated ABBYY FineReader 6 XML file.  This can take a long time!  A 73MB XML file can take over 10 minutes to transform.')
parser.add_argument('abbyyxml', help='The ABBYY XML file to transform to hOCR')
parser.add_argument('hocrfile', help='The hOCR file to write to')
parser.add_argument('-x', '--xslt', help='XSLT file to transform the ABBYY file with', default='abbyy2hocr-ocropodium-6v1.xsl')
args = parser.parse_args()

with open(args.hocrfile, 'wb') as hocr:
    hocr.write(hocr_from_abbyy(args.abbyyxml, args.xslt).encode('utf8'))
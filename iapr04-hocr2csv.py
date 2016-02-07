__author__ = 'vitorio'

from bs4 import BeautifulSoup
import csv
import cgi
import argparse

parser = argparse.ArgumentParser(description='Turn an hOCR file into a Mechanical Turk CSV input file (URL, PAGE, LINE, OCR). This assumes an Internet Archive format set of image names (name_0000.0.png).')
parser.add_argument('hocrfile', help='The hOCR file to read from')
parser.add_argument('csvfile', help='The Mechanical Turk CSV file to write to')
parser.add_argument('urlpath', help='The URL path and prefix for images')
args = parser.parse_args()

with open(args.csvfile, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['URL', 'PAGE', 'LINE', 'OCR'])
    soup = BeautifulSoup(open(args.hocrfile))

    for page in soup.find_all(class_='ocr_page'):
        for line in page.find_all(class_='ocr_line'):
            writer.writerow(['%s_%04d.%d.png' % (args.urlpath, int(page['id'].split('_')[1]) - 1, int(line['id'].split('_')[1])),
                             page['id'],
                             line['id'],
                             cgi.escape(line.contents[0], quote=True).encode('utf8')])

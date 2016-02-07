__author__ = 'vitorio'

from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description='Remove (unwrap) any markup inside "ocr_line" content in an hOCR file')
parser.add_argument('hocrfile', help='The hOCR file to read from')
args = parser.parse_args()

soup = BeautifulSoup(open(args.hocrfile))

for line in soup.find_all(class_='ocr_line'):
    foundtag = False
    for tag in line.find_all(True):
        tag.unwrap()
        foundtag = True
    if foundtag:
        line.string = ''.join(line.contents)

html = soup.prettify('utf-8')
with open(args.hocrfile, 'wb') as file:
    file.write(html)

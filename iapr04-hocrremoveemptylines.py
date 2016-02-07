__author__ = 'vitorio'

from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description='Remove empty lines from an hOCR file ("ocr_line" with no content, "ocr_carea" with no "ocr_line")')
parser.add_argument('hocrfile', help='The hOCR file to read from')
args = parser.parse_args()

soup = BeautifulSoup(open(args.hocrfile))

for page in soup.find_all(class_='ocr_page'):
    for line in page.find_all(class_='ocr_line'):
        if line.contents[0].strip() == "":
            line.decompose()
    for carea in page.find_all(class_='ocr_carea'):
        if len(carea.find_all(class_='ocr_line')) == 0:
            carea.decompose()

html = soup.prettify('utf-8')
with open(args.hocrfile, 'wb') as file:
    file.write(html)
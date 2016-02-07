__author__ = 'vitorio'

from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description='Remove empty text-related markup from an hOCR file ("ocr_line" with no content, "ocr_carea" with no "ocr_line", "ocr_page" with no "ocr_line" or floats)')
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
    if len(page.find_all(class_=['ocr_line', 'ocr_float', 'ocr_separator', 'ocr_textfloat', 'ocr_textimage', 'ocr_image',
                                 'ocr_linedrawing', 'ocr_photo', 'ocr_header', 'ocr_footer', 'ocr_pageno', 'ocr_table'])) == 0:
        page.decompose()

html = soup.prettify('utf-8')
with open(args.hocrfile, 'wb') as file:
    file.write(html)
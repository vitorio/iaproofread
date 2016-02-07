__author__ = 'vitorio'

from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description='Prettify an hOCR file to help make differencing uniform')
parser.add_argument('hocrfile', help='The hOCR file to prettify')
args = parser.parse_args()

soup = BeautifulSoup(open(args.hocrfile))

html = soup.prettify('utf-8')
with open(args.hocrfile, 'wb') as file:
    file.write(html)
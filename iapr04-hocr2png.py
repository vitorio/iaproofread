__author__ = 'vitorio'

from bs4 import BeautifulSoup
from wand.image import Image
import os
import argparse

parser = argparse.ArgumentParser(description='Turn an hOCR file and a directory of JPEG2000 images into another directory of PNG images. This assumes an Internet Archive format set of JPEG2000 image names (name_0000.jp2).')
parser.add_argument('hocrfile', help='The hOCR file to read from')
parser.add_argument('jp2dir', help='The folder of JPEG2000 images to read from')
parser.add_argument('pngdir', help='The folder of PNG images to write to')
args = parser.parse_args()

soup = BeautifulSoup(open(args.hocrfile))

for page in soup.find_all(class_='ocr_page'):
    with Image(filename=os.path.join(args.jp2dir, '%s_%04d.jp2' % (args.jp2dir.split('_')[0], int(page['id'].split('_')[1]) - 1))) as original:
        for line in page.find_all(class_='ocr_line'):
            with original.convert('png') as img:
                img.crop(*[int(x) for x in line['title'].split()[1:5]])
                img.save(filename=os.path.join(args.pngdir, '%s_%04d.%d.png' % (args.jp2dir.split('_')[0], int(page['id'].split('_')[1]) - 1, int(line['id'].split('_')[1]))))

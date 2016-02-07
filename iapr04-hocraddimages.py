__author__ = 'vitorio'

from bs4 import BeautifulSoup
import os
import argparse

parser = argparse.ArgumentParser(description='Take an hOCR file and a directory of images and add the image names into the hOCR file. This assumes the directory has the same number of images as the hOCR file has pages, and they are in order.')
parser.add_argument('hocrfile', help='The hOCR file to read from')
parser.add_argument('imgspec', help='The folder and type of images to use, e.g. "images/*.jp2" (quoted so your shell doesn\'t expand it)')
parser.add_argument('-sp', '--swap-path', help='Replace the folder name in the image path with something else')
#parser.add_argument('-r', '--replace-images', help='Replace existing image paths', action='store_true')
args = parser.parse_args()

soup = BeautifulSoup(open(args.hocrfile))

imgspec = os.path.split(args.imgspec)
imgext = os.path.splitext(imgspec[1])[1]

hocrpagecount = len(soup.find_all(class_='ocr_page'))
imglist = [img for img in os.listdir(imgspec[0]) if os.path.splitext(img)[1] == imgext and os.path.isfile(os.path.join(imgspec[0], img))]
imagecount = len(imglist)

# There's probably a proper way to do this as part of the parser argument evaluation
if hocrpagecount != imagecount:
    parser.exit(3, 'The number of pages in the hOCR file (%d) is not the same as the number of images in %s (%d).\n' % (int(hocrpagecount), args.imgspec, imagecount))

imglist.sort()

for count, page in enumerate(soup.find_all(class_='ocr_page')):
    if 'image' in [x.split()[0] for x in page['title'].split(';')]: #and not args.replace_images:
        parser.exit(4, 'At least page %d already has an image.\n' % int(page['id'].split('_')[1]))

    pagetitle = [x.split() for x in page['title'].split(';')]

    if args.swap_path is None:
        pagetitle.append(['image', os.path.join(imgspec[0], imglist[count])])
    else:
        pagetitle.append(['image', '%s%s' % (args.swap_path, imglist[count])])

    page['title'] = '; '.join([' '.join(x) for x in pagetitle])

html = soup.prettify('utf-8')
with open(args.hocrfile, 'wb') as file:
    file.write(html)
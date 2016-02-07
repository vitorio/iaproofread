# iaproofread
Crowd-sourced OCR proofreading

Python scripts towards a workflow that takes an Internet Archive-scanned book, decomposes it to lines of text and images of those lines, submits them to Amazon Mechanical Turk for correction, and reconstitues a proofed copy from the results.

Currently incomplete, and not necessarily less expensive than a professional, human editor.

## Usage

Deprecated:

 * `iapr04-hocr2png` doesn't use embedded image data
 * `iapr04-hocrremoveemptylines` superceded by `hocrremoveempties`
 * `iapr04-hocrremoveemptypages` superceded by `hocrremoveempties`

Current:

 * `iapr04-abbyy2hocr` turns the ABBYY file into an hOCR file
 * `iapr04-hocrprettify` cleans up the formatting to make it easier to diff
 * `iapr04-hocraddimages` adds image data to each `ocr_page`
 * `iapr04-hocrremoveempties` removes empty markup which seems to confuse moz-hocr-edit
 * `iapr04-hocrunwraplines` removes additional markup from inside each `ocr_line`
 * `iapr04-hocr2csv` generates an MT input CSV for use with MT templates
 * `iapr04-hocr2outputcsv` takes an original hOCR and a corrected hOCR and generates a minimal MT output CSV.

In progress:

 * `iapr04-csv2hocr` reconciles one or more sets of corrected MT CSVs

## Original code dedicated to public domain

iapr04-abbyy2hocr.py, iapr04-csv2hocr.py, iapr04-hocr2csv.py, iapr04-hocr2outputcsv.py, iapr04-hocr2png.py, iapr04-hocraddimages.py iapr04-hocrprettify.py, iapr04-hocrremoveempties.py, iapr04-hocrremoveemptylines.py, iapr04-hocrunwraplines.py, iaproofread01.py, iaproofread02.py, iaproofread03-brittlenames.py, iaproofread03-gen.py, iaproofread03-imagemap.jinja2, iaproofread03-maphilight.html, iaproofread03-words.py, iaproofread03.html, iaproofread03.jinja2, iaproofread03.py

Written in 2013 by [Vitorio Miliano](http://vitor.io/).

To the extent possible under law, the author has dedicated all copyright and related and neighboring rights to this software to the public domain worldwide.  This software is distributed without any warranty.

You should have received a copy of the CC0 Public Domain Dedication along with this software.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

## Third-party code

- abbyy2hocr-ocropodium-6v1.xsl, abbyy2hocr-ocropodium-8v2.xsl: from Ocropodium (archived at <https://github.com/vitorio/ocropodium>), licensed Apache
- abbyy2hocr-rodpage.xsl: by @rdmpage from <https://gist.github.com/tfmorris/5977784>, unknown license

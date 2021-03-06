__author__ = 'vitorio'

from bs4 import BeautifulSoup
import csv
import cgi
import argparse

parser = argparse.ArgumentParser(description='Turn a corrected hOCR file into a Mechanical Turk CSV output file (Input.URL, Input.PAGE, Input.LINE, Input.OCR, Answer.answer, Answer.transcription).')
parser.add_argument('hocrfile1', metavar='FILE', help='The unedited hOCR file to read from')
parser.add_argument('hocrfile2', metavar='FILE', help='The corrected hOCR file to read from')
parser.add_argument('csvfile', metavar='FILE', help='The Mechanical Turk CSV file to write to')
parser.add_argument('-i', '--workerid', metavar='STRING', help='A unique string to use as the faux worker ID')
parser.add_argument('-t', '--worktimeinseconds', metavar='SECONDS', help='The total time in seconds the hOCR corrections took', type=int)
parser.add_argument('-l', '--lastline', metavar='ID', help='The last line ID to process, stopping output after that')
args = parser.parse_args()

with open(args.csvfile, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    csvheader = []
    timepos = 0
    if args.workerid:
        csvheader.append('WorkerId')
        timepos = timepos + 1
    if args.worktimeinseconds:
        csvheader.append('WorkTimeInSeconds')
    csvheader.extend(['Input.URL', 'Input.PAGE', 'Input.LINE', 'Input.OCR', 'Answer.answer', 'Answer.transcription'])
    writer.writerow(csvheader)
    soup1 = BeautifulSoup(open(args.hocrfile1))
    soup2 = BeautifulSoup(open(args.hocrfile2))

    right = 0
    fixed = 0
    csvrows = []
    for page in soup1.find_all(class_='ocr_page'):
        breakout = False
        for line in page.find_all(class_='ocr_line'):
            csvrow = []
            oldlinetext = cgi.escape(line.contents[0], quote=True).encode('utf8').strip()
            newline = soup2.find(id=line['id'])
            newlinetext = cgi.escape(newline.contents[0], quote=True).encode('utf8').strip()
            if ' '.join(oldlinetext.split()) != ' '.join(newlinetext.split()):
                fixed = fixed + 1
                answer = 'fixed'
            else:
                right = right + 1
                answer = 'right'
            if args.workerid:
                csvrow.append(args.workerid)
            if args.worktimeinseconds:
                csvrow.append(0)
            imageurl = ''
            titlestring = [x.split() for x in page['title'].replace('&amp;', '&').split(';')]
            for i in titlestring:
                if 'image' in i[0]:
                    imageurl = i[1] #.replace('&', '&amp;')
            csvrow.append(imageurl)
            csvrow.append(page['id'])
            csvrow.append(line['id'])
            csvrow.append(oldlinetext)
            csvrow.append(answer)
            csvrow.append(newlinetext)
            csvrows.append(csvrow)
            if line['id'] == args.lastline:
                breakout = True
                break
        if breakout:
            break

    if args.worktimeinseconds:
        # Let's estimate that fixing a line takes 5x the time of just reading a line
        seconds = float(args.worktimeinseconds) / (right + (fixed * 5))
        print('%d lines total, %d the same (~%.2fs), %d corrected (~%.2fs)' % (right + fixed, right, round(5*seconds, 2), fixed, round(seconds, 2)))

        for row in csvrows:
            if row[-2] == 'right':
                row[timepos] = round(seconds, 2)
            else:
                row[timepos] = round(5*seconds, 2)

    writer.writerows(csvrows)

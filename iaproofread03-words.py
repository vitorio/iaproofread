# -*- coding: utf-8 -*-
__author__ = 'vitorio'

from xml.dom import minidom
import os.path
import pickle

#IA_NAME = 'windinwillows00grah'
#IA_NAME = 'artpracticeoftyp00gres'
#IA_NAME = 'manualoflinotype00merg'
IA_NAME = 'glimpsesofworldp00stod'

# must already exist
OUTPUT_FOLDER = 'iapr'

djvuxml = minidom.parse('%s_djvu.xml' % IA_NAME)

# apparently case-sensitive, is this something I have to account for somehow?
objectlist = djvuxml.getElementsByTagName('OBJECT')
print '%d object elements' % len(objectlist)

brittlenames = pickle.load(open(os.path.join(OUTPUT_FOLDER, '%s_brittlenames.pickle' % IA_NAME), 'rb'))
print '%d lines' % len(brittlenames)

brittlefragments = []

for idx_nam, a in enumerate(brittlenames):
    idx_obj, idx_reg, idx_par, idx_lin = [int(b) for b in a.split('-')]

    words = objectlist[idx_obj].getElementsByTagName('REGION')[idx_reg].getElementsByTagName('PARAGRAPH')[idx_par].getElementsByTagName('LINE')[idx_lin].getElementsByTagName('WORD')

    # this shouldn't happen
    if len(words) == 0:
        continue

    # this is the JP2 filename
    jp2name = ''
    params = objectlist[idx_obj].getElementsByTagName('PARAM')
    for b in params:
        if b.attributes['name'].value == 'PAGE':
            c = b.attributes['value'].value
    if c == '':
        if objectlist[idx_obj].attributes['usemap'].value != '':
            c = objectlist[idx_obj].attributes['usemap'].value
        else:
            print 'Missing a page name for %s' % a
            continue
    jp2name = os.path.splitext(c)[0]

    # this is the bounding box, coordinates are saved lower left to upper right per the source file
    bounds = [int(g) for g in words[0].attributes['coords'].value.split(',')]

    # this adjusts the size of the bounding box based on the words' bounds
    for h in words:
        boundingbox = [int(i) for i in h.attributes['coords'].value.split(',')]
        if boundingbox[0] < bounds[0]:
            bounds[0] = boundingbox[0]
        if boundingbox[1] > bounds[1]:
            bounds[1] = boundingbox[1]
        if boundingbox[2] > bounds[2]:
            bounds[2] = boundingbox[2]
        if boundingbox[3] < bounds[3]:
            bounds[3] = boundingbox[3]

    # this makes an object with all the words and their imagemap coordinates
    brittlewords = []
    for idx_wor, i in enumerate(words):
        boundingbox = [int(j) for j in i.attributes['coords'].value.split(',')]
        brittlewords.append({'wordnum': idx_wor, 'word': i.firstChild.data.encode('utf8').decode('utf8'),
                             'x1': boundingbox[0] - bounds[0], 'y1': boundingbox[3] - bounds[3],
                             'x2': boundingbox[2] - bounds[0], 'y2': bounds[1] - boundingbox[3]})

    brittlefragments.append({'name': a,
                             'jp2name': jp2name,
                             'fragment': {'text': ' '.join([f.firstChild.data for f in words]).encode('utf8').decode('utf8'),
                                          'width': bounds[2]-bounds[0], 'height': bounds[1]-bounds[3]},
                             'geometrystring': '%dx%d+%d+%d' % (bounds[2]-bounds[0], bounds[1]-bounds[3], bounds[0], bounds[3]),
                             'words': brittlewords})

print '%d fully computed fragments' % len(brittlefragments)

pickle.dump(brittlefragments, open(os.path.join(OUTPUT_FOLDER, '%s_brittlefragments.pickle' % IA_NAME), 'wb'))

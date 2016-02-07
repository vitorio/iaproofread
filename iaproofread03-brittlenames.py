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

brittlenames = []

for idx_obj, a in enumerate(objectlist):
    # REGIONs apparently only have PARAGRAPHs
    regionlist = a.getElementsByTagName('REGION')
    for idx_reg, c in enumerate(regionlist):
        paragraphs = c.getElementsByTagName('PARAGRAPH')
        for idx_par, d in enumerate(paragraphs):
            lines = d.getElementsByTagName('LINE')
            for idx_lin, e in enumerate(lines):
                words = e.getElementsByTagName('WORD')
                # apparently an empty <LINE></LINE> can happen
                if len(words) == 0:
                    continue
                brittlenames.append('%d-%d-%d-%d' % (idx_obj, idx_reg, idx_par, idx_lin))

print '%d lines' % len(brittlenames)

pickle.dump(brittlenames, open(os.path.join(OUTPUT_FOLDER, '%s_brittlenames.pickle' % IA_NAME), 'wb'))

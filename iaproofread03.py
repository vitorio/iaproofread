__author__ = 'vitorio'

from xml.dom import minidom
import os.path
import pickle
import PythonMagick
import jinja2

IA_NAME = 'windinwillows00grah'
# IA_NAME = 'artpracticeoftyp00gres'
# IA_NAME = 'manualoflinotype00merg'

# must already exist
OUTPUT_FOLDER = 'iapr'

djvuxml = minidom.parse('%s_djvu.xml' % IA_NAME)

# apparently case-sensitive, is this something I have to account for somehow?
objectlist = djvuxml.getElementsByTagName('OBJECT')
print '%d object elements' % len(objectlist)

brittlenames = []

for idx_obj, a in enumerate(objectlist):
    # this is silly because OBJECT usemap always has useful data and it's always the same as the PARAM
    jp2name = ''
    params = a.getElementsByTagName('PARAM')
    for b in params:
        if b.attributes['name'].value == 'PAGE':
            jp2name = b.attributes['value'].value
    if jp2name == '':
        if a.attributes['usemap'].value != '':
            jp2name = a.attributes['usemap'].value
        else:
            # maybe this should fail silently and log something instead
            raise Exception('Missing a page name at %s' % a.toxml())
    jp2name = os.path.splitext(jp2name)[0]

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

print len(brittlenames)

pickle.dump(brittlenames, open(os.path.join(OUTPUT_FOLDER, '%s_brittlenames' % IA_NAME), 'wb'))

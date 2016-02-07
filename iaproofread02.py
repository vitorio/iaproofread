__author__ = 'vitorio'

from xml.dom import minidom
import os.path
import PythonMagick

IA_NAME = 'windinwillows00grah'
# IA_NAME = 'artpracticeoftyp00gres'
# IA_NAME = 'manualoflinotype00merg'

djvuxml = minidom.parse('%s_djvu.xml' % IA_NAME)

# apparently case-sensitive, is this something I have to account for somehow?
objectlist = djvuxml.getElementsByTagName('OBJECT')
print '%d object elements' % len(objectlist)

# regionscanhave = {}

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

#     regionlist = a.getElementsByTagName('REGION')
#     for c in regionlist:
#         children = c.childNodes
#         for d in children:
#             if regionscanhave.has_key(d.localName):
#                 regionscanhave[d.localName] = regionscanhave[d.localName] + 1
#             else:
#                 regionscanhave[d.localName] = 1
#
# print regionscanhave

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
                fragment = ' '.join([f.firstChild.data for f in words])
                # coords are lower left to upper right
                bounds = [int(g) for g in words[0].attributes['coords'].value.split(',')]
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

                geometrystring = '%dx%d+%d+%d' % (bounds[2]-bounds[0], bounds[1]-bounds[3], bounds[0], bounds[3])

                jp2file = PythonMagick.Image(str(os.path.join('%s_jp2' % IA_NAME, '%s.jp2' % jp2name)))
                jp2file.crop(geometrystring)
                # oh god this file name is so brittle
                jp2file.write('%d-%d-%d-%d.png' % (idx_obj, idx_reg, idx_par, idx_lin))

                print ('%d-%d-%d-%d.png :: %s' % (idx_obj, idx_reg, idx_par, idx_lin, fragment))


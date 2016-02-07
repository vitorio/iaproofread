# -*- coding: utf-8 -*-
__author__ = 'vitorio'

from xml.dom import minidom
import os.path
import pickle
import cgi
import PythonMagick
import jinja2

env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
template = env.get_template('iaproofread03.jinja2')

#IA_NAME = 'windinwillows00grah'
#IA_NAME = 'artpracticeoftyp00gres'
#IA_NAME = 'manualoflinotype00merg'
IA_NAME = 'glimpsesofworldp00stod'

# must already exist
OUTPUT_FOLDER = 'iapr'

brittlefragments = pickle.load(open(os.path.join(OUTPUT_FOLDER, '%s_brittlefragments.pickle' % IA_NAME), 'rb'))
print '%d fully computed fragments' % len(brittlefragments)

for idx_fra, a in enumerate(brittlefragments):
    idx_obj, idx_reg, idx_par, idx_lin = [int(b) for b in a['name'].split('-')]

    # let's assume if the PNG exists, it's correct.  this may not be true!
    if not os.path.exists(os.path.join(OUTPUT_FOLDER, '%s.png' % a['name'])):
        jp2file = PythonMagick.Image(str(os.path.join('%s_jp2' % IA_NAME, '%s.jp2' % a['jp2name'])))
        jp2file.crop(a['geometrystring'])
        jp2file.write(os.path.join(OUTPUT_FOLDER, '%s.png' % a['name']))

    a['fragment']['unicodetext'] = cgi.escape(a['fragment']['text']).encode('utf8').decode('utf8')
    a['fragment']['unicodeinputtext'] = cgi.escape(a['fragment']['text'], quote=True).encode('utf8').decode('utf8')
    output_from_parsed_template = template.render(a=a)

    # to save the results
    with open(os.path.join(OUTPUT_FOLDER, '%s.html' % a['name']), 'wb') as fh:
        fh.write(output_from_parsed_template.encode('utf8'))

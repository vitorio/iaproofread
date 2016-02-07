__author__ = 'vitorio'

import os
import djvu.decode

def _get_text(sexpr, level=0):
    txt=''
    if (isinstance(sexpr, djvu.sexpr.ListExpression) and len(sexpr) !=0):
        txt = ''
        for child in sexpr[5:]:
            txt = txt + _get_text(child, level + 1)
        return txt
    else:
        txt = str(sexpr)
        txt = txt.strip('"') + ' '
        return  txt

def _get_word(sexpr, level=0):
    wl = []
    if (isinstance(sexpr, djvu.sexpr.ListExpression) and len(sexpr) !=0):
        if str(sexpr[0].value) == 'word':
          wl.append(sexpr)
          return wl
        for child in sexpr[5:]:
            res = _get_word(child, level + 1)
            if res is not None:
              wl.extend(res)
        return wl

def _slice(x, start, end):
  return [int(x[i]) for i in range(start, end+1)]

class context(djvu.decode.Context):

    def __init__(self, infile):
      self.infile = infile
      self.document = self.new_document(djvu.decode.FileURI(self.infile))
      self.document.decoding_job.wait()
      self.pages = len(self.document.pages)

    def _handle_message(self, message):
      if isinstance(message, djvu.decode.ErrorMessage):
        print >> sys.stderr, message
        sys.exit(1)

    def get_pages(self):
      return self.pages

    def get_text(self):
      text = []
      for page in self.document.pages:
        text.append(_get_text(page.text.sexpr))
      return text

    def get_page_text(self, pageno):
      page = self.document.pages[pageno]
      return _get_text(page.text.sexpr)

    def get_wordlist_page(self, pageno):
      page = self.document.pages[pageno]
      sexpr = page.text.sexpr
      wl = []
      if (isinstance(sexpr, djvu.sexpr.ListExpression) and len(sexpr) !=0):
        wl = _get_word(sexpr)
      return wl

    def _process(self):
      i=0
      print self.document.pages
      for page in self.document.pages:
        #info(page)
        print "-"*15, "\n"
        print page.n
        print page.get_info()
        print page
        print page.text.sexpr
        text = _get_text(page.text.sexpr)
        print text
        if i > 5:
          break
        i=i+1
      return text

djvf = context('/home/vitorio/wikicaptcha/aliceinwonderland.djvu')

print djvf.pages

print djvf.get_wordlist_page(30)
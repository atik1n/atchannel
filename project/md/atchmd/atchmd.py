"""
@chMD | Расширение Markdown
==================================================
Данное расширение объединяет в себе свои наработки
и исправления пользовательских расширений MD

URLify:
  https://github.com/selcuk/markdown-urlify/blob/master/urlify.py
Newtab:
  https://github.com/kriwil/markdown-newtab/blob/master/markdown_newtab/__init__.py
"""

from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern, InlineProcessor
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import \
	LinkInlineProcessor, ReferenceInlineProcessor, AutolinkInlineProcessor, AutomailInlineProcessor, \
	LINK_RE, REFERENCE_RE, AUTOLINK_RE, AUTOMAIL_RE
from markdown.util import etree
import re

# Автор: mahorin. Пакет: atchmd
DEL_RE = r'(~~)(.*?)~~'
INS_RE = r'(__)(.*?)__'
SPOIL_RE = r'(\|\|)(.*?)\|\|'
ATCHQUOTE_RE = r'()>(.*?)(?:\n|$)'
ATCHLINK_RE = r'(>>)\s?([0-9]+)'

# Автор: selcuk. Пакет: urlify
urlfinder = re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+(:[0-9]+)?|'
                       r'(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:/[\+~%/\.\w\-_]*)?\??'
                       r'(?:[\-\+=&;%@\.\w_]*)#?(?:[\.!/\\\w]*))?)')

class ATchMD(Extension):
  def __init__(self, *args, **kwargs):
    super(ATchMD, self).__init__(*args, **kwargs)
        
  def extendMarkdown(self, md):
    # Автор: mahorin. Пакет: atchmd
    md.parser.blockprocessors.deregister('quote')
    md.parser.blockprocessors.deregister('hashheader')
    md.parser.blockprocessors.deregister('setextheader')
    md.parser.blockprocessors.deregister('olist')
    md.parser.blockprocessors.deregister('ulist')
    
    md.preprocessors.deregister('html_block')
    md.inlinePatterns.deregister('html')
    
    md.inlinePatterns.deregister('reference')
    md.inlinePatterns.deregister('link')
    md.inlinePatterns.deregister('image_link')
    md.inlinePatterns.deregister('image_reference')
    md.inlinePatterns.deregister('linebreak')

    del_tag = SimpleTagPattern(DEL_RE, 'del')
    md.inlinePatterns.register(del_tag, 'del', 71)
    
    ins_tag = SimpleTagPattern(INS_RE, 'ins')
    md.inlinePatterns.register(ins_tag, 'ins', 72)
    
    spoil_tag = SimpleTagPattern(SPOIL_RE, 'spoiler')
    md.inlinePatterns.register(spoil_tag, 'spoil', 73)
    
    link_tag = AtchLinkInlineProcessor(ATCHLINK_RE)
    link_tag.md = md
    md.inlinePatterns.register(link_tag, 'atchlink', 75)
    
    quote_tag = AtchQuoteInlineProcessor(ATCHQUOTE_RE)
    quote_tag.md = md
    md.inlinePatterns.register(quote_tag, 'atchquote', 74)
    
    # Автор: selcuk. Пакет: urlify
    md.preprocessors.register(URLify(md), 'urlify', 76)
    
    # Автор: kriwil. Пакет: newtab
    md.inlinePatterns['link'] = NewTabLinkPattern(LINK_RE, md)
    md.inlinePatterns['reference'] = NewTabReferencePattern(REFERENCE_RE, md)
    md.inlinePatterns['short_reference'] = NewTabReferencePattern(REFERENCE_RE, md)
    md.inlinePatterns['autolink'] = NewTabAutolinkPattern(AUTOLINK_RE, md)
    md.inlinePatterns['automail'] = NewTabAutomailPattern(AUTOMAIL_RE, md)
        
        
class AtchQuoteInlineProcessor(InlineProcessor):
  # Автор: mahorin. Пакет: atchmd
  def __init__(self, pattern):
    super(AtchQuoteInlineProcessor, self).__init__(pattern)

  def handleMatch(self, m, data):
    a = etree.Element('quote')
    a.text = '&gt;%s' % m.group(2)
    #a.tail = '\n'
    return a, m.start(0), m.end(0)
        
class AtchLinkInlineProcessor(InlineProcessor):
  # Автор: mahorin. Пакет: atchmd
  def __init__(self, pattern):
    super(AtchLinkInlineProcessor, self).__init__(pattern)

  def handleMatch(self, m, data):
    a = etree.Element('a')
    a.text = '&gt;&gt;%s' % m.group(2)
    a.set('href', '#post-%s' % m.group(2))
    a.set('style', 'color:blue;')
    return a, m.start(0), m.end(0)
      
class URLify(Preprocessor):
  # Автор: selcuk. Пакет: urlify
  def run(self, lines):
    return [urlfinder.sub(r'<\1>', line) for line in lines]
    
class NewTabMixin(object):
  # Автор: kriwil. Пакет: newtab
	def handleMatch(self, m, data):
		el, _, _ = super(NewTabMixin, self).handleMatch(m, data)
		if el != None: el.set('target', '_blank')
		return el, m.start(0), m.end(0)
    
# Автор: kriwil. Пакет: newtab
class NewTabLinkPattern(NewTabMixin, LinkInlineProcessor): pass
class NewTabReferencePattern(NewTabMixin, ReferenceInlineProcessor): pass
class NewTabAutolinkPattern(NewTabMixin, AutolinkInlineProcessor): pass
class NewTabAutomailPattern(NewTabMixin, AutomailInlineProcessor): pass
        
def makeExtension(*args, **kwargs):
  return ATchMD(*args, **kwargs)
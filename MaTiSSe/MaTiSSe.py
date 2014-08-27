#!/usr/bin/env python
"""
MaTiSSe.py, Markdown To Impressive Scientific Slides
"""
__appname__ = "MaTiSSe.py"
__description__ = "MaTiSSe.py, Markdown To Impressive Scientific Slides"
__version__ = "v0.0.1"
__author__ = "Stefano Zaghi"
__author_email__ = "stefano.zaghi@gmail.com"
__license__ = "GNU General Public License v3 (GPLv3)"
__url__ = "https://github.com/szaghi/MaTiSSe"
# modules loading
import sys
try:
  import os
except:
  print("Module 'os' not found")
  sys.exit(1)
try:
  from shutil import copyfile
except:
  print("Module 'shutil' not found")
  sys.exit(1)
try:
  import argparse
except:
  print("Module 'argparse' not found")
  sys.exit(1)
try:
  import re
except:
  print("The regular expression module 're' not found")
  sys.exit(1)
try:
  from yattag import Doc,indent
except:
  print("Module 'yattag' not found")
  sys.exit(1)
try:
  import markdown
  #__md__ = markdown.Markdown(output_format='html5',extensions=['fenced_code','footnotes','tables','smart_strong','codehilite(noclasses=True,pygments_style=vim)','toc'])
  #__md__ = markdown.Markdown(output_format='html5',extensions=['fenced_code','footnotes','tables','smart_strong','codehilite','toc'])
  __md__ = markdown.Markdown(output_format='html5',extensions=['fenced_code','footnotes','tables','smart_strong'])
except:
  print("Module 'markdown' not found")
  sys.exit(1)
try:
  from multiprocessing import Pool
  __parallel__ = True
except:
  print("Module 'multiprocessing' not found: parallel compilation disabled")
  __parallel__ = False
# engines global data
__engines__ = ['impress.js','jmpress.js','reveal.js']
__slide_tag_names__ = {'impress.js':'div','jmpress.js':'div','reveal.js':'section'}
__slide_tag_attrs__ = {'impress.js':[['class','step slide'],['data-from-markdown','']],
                       'jmpress.js':[['class','step']],
                       'reveal.js': [['data-from-markdown','']]}
# setting CLI
__cliparser__ = argparse.ArgumentParser(prog=__appname__,description='MaTiSSe.py, Markdown To Impressive Scientific Slides')
__cliparser__.add_argument('-v','--version',                    action='version',                                  help='Show version',version='%(prog)s '+__version__)
__cliparser__.add_argument('input',                             action='store',               default=None,        help='Input file name of markdown source to be parsed')
__cliparser__.add_argument('-o','--output',      required=False,action='store',               default=None,        help='Output directory name containing the presentation files')
__cliparser__.add_argument('-e','--engine',      required=False,action='store',               default='impress.js',help='Engine powering html presentation',choices=__engines__)
__cliparser__.add_argument('--print-preamble',   required=False,action='store_true',          default=None,        help='Print the preamble data as parsed from source')
#regular expressions
__expr__ = r"(?P<expr>.*)"
__regex_metadata__ = re.compile(r"(?P<mdata>[-]{3}metadata.*?[-]{3}endmetadata)",re.DOTALL)
__regex_themedata__ = re.compile(r"(?P<tdata>[-]{3}theme.*?[-]{3}endtheme)",re.DOTALL)
__regex_section__ = re.compile(r"[^#]#\s+"+__expr__)
__regex_subsection__ = re.compile(r"[^#]##\s+"+__expr__)
__regex_slide__ = re.compile(r"[^#]###\s+"+__expr__)
__regex_codeblock__ = re.compile(r"(?P<cblock>[`]{3}.*?[`]{3})",re.DOTALL)
# regex for theming: tuples with regex and default values
__regex_css_slide_width__ = (re.compile(r"#SLIDE-WIDTH"),'900px')
__regex_css_slide_height__ = (re.compile(r"#SLIDE-HEIGHT"),'700px')
__regex_css_slide_background_color__ = (re.compile(r"#SLIDE-BACKGROUND-COLOR"),'white')
__regex_css_slide_border_radius__ = (re.compile(r"#SLIDE-BORDER-RADIUS"),'10px')
__regex_css_slide_color__ = (re.compile(r"#SLIDE-COLOR"),'black')
__regex_css_slide_font_size__ = (re.compile(r"#SLIDE-FONT-SIZE"),'32px')
__regexs_css_slide__ = {}
for key, val in locals().items():
  match = re.match(r"^__regex_css_slide_(?P<key>.*)__",key)
  if (match and
      not re.match(r"^__regex_css_slide_content_.*__",key) and
      not re.match(r"^__regex_css_slide_header_.*__",key) and
      not re.match(r"^__regex_css_slide_footer_.*__",key) and
      not re.match(r"^__regex_css_slide_sidebarL_.*__",key) and
      not re.match(r"^__regex_css_slide_sidebarR_.*__",key)):
    __regexs_css_slide__[match.group('key')] = val

__regex_css_slide_content_width__ = (re.compile(r"#SLIDE-CONTENT-WIDTH"),'100%')
__regex_css_slide_content_height__ = (re.compile(r"#SLIDE-CONTENT-HEIGHT"),'100%')
__regex_css_slide_content_background_color__ = (re.compile(r"#SLIDE-CONTENT-BACKGROUND-COLOR"),'white')
__regex_css_slide_content_border_radius__ = (re.compile(r"#SLIDE-CONTENT-BORDER-RADIUS"),'0 0 0 0')
__regex_css_slide_content_color__ = (re.compile(r"#SLIDE-CONTENT-COLOR"),'black')
__regexs_css_slide_content__ = {}
for key, val in locals().items():
  match = re.match(r"^__regex_css_slide_content_(?P<key>.*)__",key)
  if match:
    __regexs_css_slide_content__[match.group('key')] = val

__regex_css_slide_header_height__ = (re.compile(r"#SLIDE-HEADER-HEIGHT"),'0%')
__regex_css_slide_header_background_color__ = (re.compile(r"#SLIDE-HEADER-BACKGROUND-COLOR"),'white')
__regex_css_slide_header_border_radius__ = (re.compile(r"#SLIDE-HEADER-BORDER-RADIUS"),'10px 10px 0 0')
__regex_css_slide_header_color__ = (re.compile(r"#SLIDE-HEADER-COLOR"),'')
__regexs_css_slide_header__ = {}
for key, val in locals().items():
  match = re.match(r"^__regex_css_slide_header_(?P<key>.*)__",key)
  if match:
    __regexs_css_slide_header__[match.group('key')] = val

__regex_css_slide_footer_height__ = (re.compile(r"#SLIDE-FOOTER-HEIGHT"),'0%')
__regex_css_slide_footer_background_color__ = (re.compile(r"#SLIDE-FOOTER-BACKGROUND-COLOR"),'white')
__regex_css_slide_footer_border_radius__ = (re.compile(r"#SLIDE-FOOTER-BORDER-RADIUS"),'0 0 10px 10px')
__regex_css_slide_footer_color__ = (re.compile(r"#SLIDE-FOOTER-COLOR"),'')
__regexs_css_slide_footer__ = {}
for key, val in locals().items():
  match = re.match(r"^__regex_css_slide_footer_(?P<key>.*)__",key)
  if match:
    __regexs_css_slide_footer__[match.group('key')] = val

__regex_css_slide_sidebarL_width__ = (re.compile(r"#SLIDE-SIDEBARL-WIDTH"),'0%')
__regex_css_slide_sidebarL_height__ = (re.compile(r"#SLIDE-SIDEBARL-HEIGHT"),'0%')
__regex_css_slide_sidebarL_background_color__ = (re.compile(r"#SLIDE-SIDEBARL-BACKGROUND-COLOR"),'white')
__regex_css_slide_sidebarL_border_radius__ = (re.compile(r"#SLIDE-SIDEBARL-BORDER-RADIUS"),'0 10px 0 0')
__regex_css_slide_sidebarL_color__ = (re.compile(r"#SLIDE-SIDEBARL-COLOR"),'')
__regexs_css_slide_sidebarL__ = {}
for key, val in locals().items():
  match = re.match(r"^__regex_css_slide_sidebarL_(?P<key>.*)__",key)
  if match:
    __regexs_css_slide_sidebarL__[match.group('key')] = val

__regex_css_slide_sidebarR_width__ = (re.compile(r"#SLIDE-SIDEBARR-WIDTH"),'0%')
__regex_css_slide_sidebarR_height__ = (re.compile(r"#SLIDE-SIDEBARR-HEIGHT"),'0%')
__regex_css_slide_sidebarR_background_color__ = (re.compile(r"#SLIDE-SIDEBARR-BACKGROUND-COLOR"),'white')
__regex_css_slide_sidebarR_border_radius__ = (re.compile(r"#SLIDE-SIDEBARR-BORDER-RADIUS"),'0 0 10px 0')
__regex_css_slide_sidebarR_color__ = (re.compile(r"#SLIDE-SIDEBARR-COLOR"),'')
__regexs_css_slide_sidebarR__ = {}
for key, val in locals().items():
  match = re.match(r"^__regex_css_slide_sidebarR_(?P<key>.*)__",key)
  if match:
    __regexs_css_slide_sidebarR__[match.group('key')] = val
# whole css regexs
__regexs_css__ = {}
for key, val in locals().items():
  match = re.match(r"^__regex_css_(?P<key>.*)__",key)
  if match:
    __regexs_css__[match.group('key')] = val
# classes definitions
class Theme_Slide_Content(object):
  """
  Theme_Slide_Content is an object that handles the presentation theme slide content, its attributes and methods.
  """
  def __init__(self):
    # initializing theme slide content data
    self.data = {'active' : False}
    for k,v in __regexs_css_slide_content__.items():
      self.data[k] = v[1]
class Theme_Slide_Header(object):
  """
  Theme_Slide_Header is an object that handles the presentation theme slide header, its attributes and methods.
  """
  def __init__(self):
    # initializing theme slide header data
    self.data = {'active' : False}
    for k,v in __regexs_css_slide_header__.items():
      self.data[k] = v[1]
class Theme_Slide_Footer(object):
  """
  Theme_Slide_Footer is an object that handles the presentation theme slide footer, its attributes and methods.
  """
  def __init__(self):
    # initializing theme slide footer data
    self.data = {'active' : False}
    for k,v in __regexs_css_slide_footer__.items():
      self.data[k] = v[1]
class Theme_Slide_SidebarL(object):
  """
  Theme_Slide_SidebarL is an object that handles the presentation theme slide sidebarL, its attributes and methods.
  """
  def __init__(self):
    # initializing theme slide sidebarL data
    self.data = {'active' : False}
    for k,v in __regexs_css_slide_sidebarL__.items():
      self.data[k] = v[1]
class Theme_Slide_SidebarR(object):
  """
  Theme_Slide_SidebarR is an object that handles the presentation theme slide sidebarR, its attributes and methods.
  """
  def __init__(self):
    # initializing theme slide sidebarR data
    self.data = {'active' : False}
    for k,v in __regexs_css_slide_sidebarR__.items():
      self.data[k] = v[1]
class Theme(object):
  """
  Theme is an object that handles the presentation theme, its attributes and methods.
  """
  def __init__(self):
    # initializing theme data
    self.data = {'header'  : False,
                 'sidebarL': False,
                 'sidebarR': False,
                 'footer'  : False}
    for k,v in __regexs_css__.items():
      self.data[k] = v[1]
  def __str__(self):
    ps = 'Theme settings:\n\n'
    for k, v in self.data.items():
      ps += '  '+k+' = '+str(v)+'\n'
    return ps
  def has_header(self):
    """
    Method for inquiring the presence of header.
    """
    return self.data['header']
  def has_sidebarL(self):
    """
    Method for inquiring the presence of sidebarL.
    """
    return self.data['sidebarL']
  def has_sidebarR(self):
    """
    Method for inquiring the presence of sidebarR.
    """
    return self.data['sidebarR']
  def has_footer(self):
    """
    Method for inquiring the presence of footer.
    """
    return self.data['footer']
  def make(self):
    """
    Method for creating a theme css accordingly to the user options.
    It is made parsing the "MaTiSSe/css/themes/default-skeleton.css" file.
    The returned string contains the css theme.
    """
    # dimensioning slide content size accordingly to other theme's elements
    scw = int(self.data['slide_content_width'].strip('%')) # slide content width (in percent %)
    sce = int(self.data['slide_content_height'].strip('%')) # slide content height (in percent %)
    if self.has_header():
      sce -= int(self.data['slide_header_height'].strip('%'))
    if self.has_footer():
      sce -= int(self.data['slide_footer_height'].strip('%'))
    if self.has_sidebarL():
      scw -= int(self.data['slide_sidebarL_width'].strip('%'))
    if self.has_sidebarR():
      scw -= int(self.data['slide_sidebarR_width'].strip('%'))
    self.data['slide_content_width'] = str(scw)+'%'
    self.data['slide_content_height'] = str(sce)+'%'
    # loading skeleton
    css = os.path.join(os.path.dirname(__file__), 'css/themes/default-skeleton.css')
    with open(css,'r') as sk_css:
      skeleton = sk_css.read()
    # substituting values
    for k, v in __regexs_css__.items():
      skeleton = re.sub(v[0],self.data[k],skeleton)
    return skeleton
class Engine(object):
  """
  Engine is an object that handles the "engine" powering the html presentation.
  Supported engines are:
  - impress.js;
  - jmpress.js;
  - reveal.js;
  """
  def __init__(self,name):
    self.name = name
    if not name in __engines__:
      self.name = __engines__[0]
    self.slide_tag_name =  __slide_tag_names__[self.name]
    self.slide_tag_attr =  __slide_tag_attrs__[self.name]
  def is_reveal(self):
    """
    Method for checking if the engine is "reveal.js".
    """
    return self.name == 'reveal.js'
  def is_impress(self):
    """
    Method for checking if the engine is "impress.js".
    """
    return self.name == 'impress.js'
  def is_jmpress(self):
    """
    Method for checking if the engine is "jmpress.js".
    """
    return self.name == 'jmpress.js'
  def make_output_tree(self,output,theme):
    """
    Method for creating output tree and copy the correct engine files.
    """
    output = os.path.normpath(output)+"/"
    if not os.path.exists(output):
      os.makedirs(output)
    if not os.path.exists(output+'css'):
      os.makedirs(output+'css')
    # some useful css
    css = os.path.join(os.path.dirname(__file__), 'css/normalize.css')
    copyfile(css,output+'css/normalize.css')
    with open(output+'css/theme.css','w') as css_theme:
      css_theme.writelines(theme)
    if not os.path.exists(output+'js'):
      os.makedirs(output+'js')
    # impress.js files
    if self.is_impress:
      js = os.path.join(os.path.dirname(__file__), 'js/impress/impress.js')
      copyfile(js,output+'js/impress.js')
    # reveal.js files
    if self.is_reveal():
      css = os.path.join(os.path.dirname(__file__), 'css/reveal/reveal.css')
      copyfile(css,output+'css/reveal.css')
      css = os.path.join(os.path.dirname(__file__), 'css/reveal/theme/serif.css')
      copyfile(css,output+'css/serif.css')
      js = os.path.join(os.path.dirname(__file__), 'js/reveal/reveal.js')
      copyfile(js,output+'js/reveal.js')
    return output
  def put_styles(self,tag,doc):
    """
    Method for inserting the styles into html.
    """
    # default theme
    doc.stag('link',rel='stylesheet', href='css/theme.css')
    # impress.js styles
    if self.is_impress():
      pass
    # reveal.js styles
    if self.is_reveal():
      doc.stag('link',rel='stylesheet', href='css/reveal.css')
      doc.stag('link',rel='stylesheet', href='css/serif.css',id='theme')
    # some useful styles
    doc.stag('link',rel='stylesheet', href='css/normalize.css')
  def put_scripts(self,tag,doc):
    """
    Method for inserting the scripts into html.
    """
    # impress.js scritps
    if self.is_impress():
      with tag('script'):
        doc.attr(src='js/impress.js')
      with tag('script'):
        doc.asis('impress().init();')
    # reveal.js scritps
    if self.is_reveal():
      with tag('script'):
        doc.attr(src='js/reveal.js')
      with tag('script'):
        doc.asis("""
          Reveal.initialize({
            controls: false,
            progress: true,
            history: true,
            center: true,
          });
        """)
      return
    return
class Preamble(object):
  """
  Preambles is an object that handles the preamble, its attributes and methods.
  """
  def __init__(self,source):
    # initializing metadata
    self.metadata = {'title'              : '',
                     'subtitle'           : '',
                     'authors'            : [],
                     'authors_short'      : [],
                     'emails'             : [],
                     'affiliations'       : [],
                     'affiliations_short' : [],
                     'location'           : '',
                     'location_short'     : '',
                     'date'               : '',
                     'conference'         : '',
                     'conference_short'   : '',
                     'session'            : '',
                     'session_short'      : '',
                     'logo'               : ''}
    # extracting metadata from markdown source
    matching = __regex_metadata__.search(source)
    if matching:
      metadata = matching.group('mdata').split('\n')
      for i,m in enumerate(metadata):
        metadata[i] = m.split('=')
      for m in metadata:
        if m[0].strip() in self.metadata:
          if isinstance(self.metadata[m[0].strip()], str):
            self.metadata[m[0].strip()] = m[1].strip()
          elif isinstance(self.metadata[m[0].strip()], list) or isinstance(self.metadata[m[0].strip()], bool):
            self.metadata[m[0].strip()] = eval(m[1].strip())
          else:
            self.metadata[m[0].strip()] = m[1]
    # initializing theme
    self.theme = Theme()
    # extracting theme settings from markdown source
    matching = __regex_themedata__.search(source)
    if matching:
      themedata = matching.group('tdata').split('\n')
      for i,t in enumerate(themedata):
        themedata[i] = t.split('=')
      for t in themedata:
        if t[0].strip() in self.theme.data:
          if isinstance(self.theme.data[t[0].strip()], str):
            self.theme.data[t[0].strip()] = t[1].strip()
          elif isinstance(self.theme.data[t[0].strip()], list) or isinstance(self.theme.data[t[0].strip()], bool):
            self.theme.data[t[0].strip()] = eval(t[1].strip())
          else:
            self.theme.data[t[0].strip()] = t[1]
  def __str__(self):
    ps = 'Preamble metadata:\n\n'
    for k, v in self.metadata.items():
      ps += '  '+k+' = '+str(v)+'\n'
    ps += str(self.theme)
    return ps
  def strip(self,source):
    """
    Method for striping preamble from source.
    """
    strip_source = re.sub(__regex_metadata__,'',source)
    strip_source = re.sub(__regex_themedata__,'',strip_source)
    return strip_source
class Section(object):
  """
  Section is an object that handles a single section, its attributes and methods.
  """
  def __init__(self,title='',raw_body='',slides=None):
    self.title = title
    self.raw_body = raw_body
    self.slides = slides
  def to_html(self,tag,doc,engine,theme,slides_number):
    """
    Method for converting section slides content into html format.
    """
    if not engine.is_reveal:
      with tag('div',klass='section',id=self.title):
        for slide in self.slides:
          slides_number += 1
          slide.to_html(tag,doc,engine,theme,slides_number)
    else:
      for slide in self.slides:
        slides_number += 1
        slide.to_html(tag,doc,engine,theme,slides_number)
    return slides_number
class Slide(object):
  """
  Slide is an object that handles a single slide, its attributes and methods.
  """
  def __init__(self,title='',raw_body=''):
    self.title = title
    self.raw_body = raw_body
  def to_html(self,tag,doc,engine,theme,slides_number):
    """
    Method for converting slide content into html format.
    """
    with tag(engine.slide_tag_name,('title',self.title)):
      for a in engine.slide_tag_attr:
        doc.attr((a[0],a[1]))
      if engine.is_impress():
        doc.attr(('data-x',str(slides_number+slides_number*1000)))
      if theme.has_header():
        with tag('div',('class','slide-header')):
          with tag('div',('class','padding')): # padded container
            with tag('div',('class','title')):
              doc.asis(self.title)
      if theme.has_sidebarL():
        with tag('div',('class','slide-sidebarL')):
          with tag('div',('class','padding')): # padded container
            doc.asis('Left Sidebar')

      with tag('div',('class','slide-content')):
        with tag('div',('class','padding')): # padded container
          doc.asis('\n'+__md__.convert(self.raw_body))

      if theme.has_sidebarR():
        with tag('div',('class','slide-sidebarR')):
          with tag('div',('class','padding')): # padded container
            doc.asis('Right Sidebar')
      if theme.has_footer():
        with tag('div',('class','slide-footer')):
          with tag('div',('class','padding')): # padded container
            doc.asis('footer')
    return
# functions definitions
def purge_codeblocks(source):
  """
  Function for removing code blocks from a source string and replacing with an equivalent number of spaces as the removed characters.
  """
  purged_source = source
  for match in re.finditer(__regex_codeblock__,purged_source):
    chars_skipped = len(match.group('cblock'))
    sub = ''
    for n in range(chars_skipped):
      sub += ' '
    purged_source = re.sub(__regex_codeblock__,sub,purged_source,1)
  return purged_source
def get_sections(source,engine):
  """
  Function for tokenizing source into sections.
  """
  secs = []
  sections = []
  # remove code blocks from string parsed in searching sections
  purged_source = purge_codeblocks(source)
  for match in re.finditer(__regex_section__,purged_source):
    secs.append([match.group('expr'),match.start(),match.end()])
  if len(secs)==0:
    # there is no section thus crate one with no title as a generic container
    sections.append(Section(title='',raw_body=source))
  else:
    for s,sec in enumerate(secs):
      if s < len(secs)-1:
        sections.append(Section(title=sec[0],raw_body=source[sec[2]+1:secs[s+1][1]-1]))
      else:
        sections.append(Section(title=sec[0],raw_body=source[sec[2]+1:]))
  return sections
def get_slides(sections):
  """
  Function for tokenizing sections into slides.
  """
  for section in sections:
    slds = []
    section.slides = []
    # remove code blocks from string parsed in searching slides
    purged_source = purge_codeblocks(section.raw_body)
    for match in re.finditer(__regex_slide__,purged_source):
      slds.append([match.group('expr'),match.start(),match.end()])
    for s,sld in enumerate(slds):
      if s < len(slds)-1:
        section.slides.append(Slide(title=sld[0],raw_body=section.raw_body[sld[2]+1:slds[s+1][1]]))
      else:
        section.slides.append(Slide(title=sld[0],raw_body=section.raw_body[sld[2]+1:]))
def parse_file(md_file,engine,output=None):
  """
  Function for parsing a single file.
  """
  if not os.path.exists(md_file):
    print('Error: input file "'+md_file+'" not found!')
    sys.exit(1)
  else:
    # reading input source as single stream
    with open(md_file,'r') as md:
      source = md.read()
    # parsing eventual preamble data
    preamble = Preamble(source=source)
    # creating output tree
    if not output:
      output = os.path.splitext(os.path.basename(md_file))[0]
    output = engine.make_output_tree(output,preamble.theme.make())
    # parsing input stream
    source = preamble.strip(source=source)
    sections = get_sections(source,engine)
    get_slides(sections)
    # creating html presentation
    slides_number = 0
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
      doc.attr(title = preamble.metadata['title'])
      with tag('head'):
        doc.stag('meta',charset='utf-8')
        # presentation metadata
        doc.stag('meta',author=' and '.join(preamble.metadata['authors']))
        with tag('title'):
          text(preamble.metadata['title'])
        doc.stag('meta',subtitle=preamble.metadata['subtitle'])
        # styles
        engine.put_styles(tag,doc)
      with tag('body'):
        if engine.is_reveal():
          with tag('div',klass='reveal'):
            with tag('div',klass='slides'):
              for section in sections:
                slides_number = section.to_html(tag,doc,engine,preamble.theme,slides_number)
        elif engine.is_impress():
          with tag('div',id='impress'):
            for section in sections:
              slides_number = section.to_html(tag,doc,engine,preamble.theme,slides_number)
        else:
          for section in sections:
            slides_number = section.to_html(tag,doc,engine,preamble.theme,slides_number)
        # scripts
        engine.put_scripts(tag,doc)
    # saving presentation
    with open(output+'index.html','w') as html_presentation:
      html_presentation.write(indent(doc.getvalue()))
  return preamble
def main():
  """
  Main function.
  """
  cliargs = __cliparser__.parse_args()
  if cliargs.input:
    engine = Engine(name=cliargs.engine)
    preamble = parse_file(md_file=cliargs.input,engine=engine,output=cliargs.output)
    if cliargs.print_preamble:
      print(preamble)
# main loop
if __name__ == '__main__':
  main()

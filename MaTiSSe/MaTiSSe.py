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
# setting CLI
__cliparser__ = argparse.ArgumentParser(prog=__appname__,description='MaTiSSe.py, Markdown To Impressive Scientific Slides')
__cliparser__.add_argument('-v','--version',                    action='version',                                  help='Show version',version='%(prog)s '+__version__)
__cliparser__.add_argument('input',                             action='store',               default=None,        help='Input file name of markdown source to be parsed')
__cliparser__.add_argument('-o','--output',      required=False,action='store',               default=None,        help='Output directory name containing the presentation files')
__cliparser__.add_argument('--print-preamble',   required=False,action='store_true',          default=None,        help='Print the preamble data as parsed from source')
#regular expressions
__expr__ = r"(?P<expr>.*)"
__regex_section__ = re.compile(r"[^#]#\s+"+__expr__)
__regex_subsection__ = re.compile(r"[^#]##\s+"+__expr__)
__regex_slide__ = re.compile(r"[^#]###\s+"+__expr__)
__regex_codeblock__ = re.compile(r"(?P<cblock>[`]{3}.*?[`]{3})",re.DOTALL)
# classes definitions
class Raw_Data(object):
  """
  Object for handling raw data of presentation preamble.
  """
  def __init__(self,regex_start,regex_end):
    self.regex_start = regex_start
    self.regex_end = regex_end
    self.regex = re.compile(r"(?P<rdata>"+regex_start+r".*?"+regex_end+")",re.DOTALL)
  def get(self,source):
    """
    Method for getting raw data from source.
    """
    matching = self.regex.search(source)
    if matching:
      self.data = matching.group('rdata').split('\n')
      for i,d in enumerate(self.data):
        if re.search(self.regex_start,d) or re.search(self.regex_end,d):
          self.data.pop(i)
        if d == '':
          self.data.pop(i)
      for i,d in enumerate(self.data):
        self.data[i] = [d.split('=')[0].strip(),d.split('=')[1].strip()]
    return
  def __str__(self):
    string = ''
    for d in self.data:
      string += '  '+d[0]+' = '+d[1]+'\n'
    return string
  def strip(self,source):
    """
    Method for striping raw data from source.
    """
    return re.sub(self.regex,'',source)
class Metadata(object):
  """
  Object for handling presentation metadata.
  """
  def __init__(self):
    self.raw_data = Raw_Data(regex_start='[-]{3}metadata',regex_end='[-]{3}endmetadata')
    self.data = {'title'              : '',
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
  def __str__(self):
    string = 'Presentation metadata:\n'
    for k, v in self.data.items():
      string += '  '+k+' = '+str(v)+'\n'
    return string
  def get_raw_data(self,source):
    """
    Method for getting raw data from source.
    """
    self.raw_data.get(source)
    return
  def get_values(self):
    """
    Method for getting values from raw data parsed from source.
    """
    for t in self.raw_data.data:
      k = t[0].strip()
      v = t[1].strip()
      if k in self.data:
        if isinstance(self.data[k], str):
          self.data[k] = v
        elif isinstance(self.data[k], list) or isinstance(self.data[k], bool):
          self.data[k] = eval(v)
        else:
          self.data[k] = v
    return
  def strip(self,source):
    """
    Method for striping raw metadata from source.
    """
    strip_source = self.raw_data.strip(source)
    return strip_source
class Theme_Element(object):
  """
  Object for handling a theme element.
  """
  def __init__(self,
               raw_data,      # raw data extracted from source
               data_dic,      # dictionary containing data of element
               css,           # css skeleton
               active=False): # element is active or not
    self.raw_data = raw_data
    self.data = {}
    for k,v in data_dic.items():
      self.data[k] = v
    self.css = css
    self.active = active
    self.elements = {}
    return
  def __str__(self):
    string = ''
    if self.active:
      for k, v in self.data.items():
        if isinstance(v, list):
          string += '  '+k+' = '+str(v[1])+'\n'
        else:
          string += '  '+k+' = '+str(v)+'\n'
    return string
  def get_raw_data(self,source):
    """
    Method for getting raw data from source.
    """
    self.raw_data.get(source)
    return
  def get_values(self):
    """
    Method for getting values from raw data parsed from source.
    """
    for t in self.raw_data.data:
      k = t[0].strip()
      v = t[1].strip()
      if k in self.data:
        if isinstance(self.data[k][1], str):
          self.data[k][1] = v
        elif isinstance(self.data[k][1], list) or isinstance(self.data[k][1], bool):
          self.data[k][1] = eval(v)
        else:
          self.data[k][1] = v
    return
  def get_css(self):
    """
    Method for setting css theme element values accordingly to the element data.
    """
    css = self.css
    if self.active:
      for k,v in self.data.items():
        if k != 'elements':
          css = re.sub(v[0],v[1],css)
    return css
class Theme_Slide_Content(Theme_Element):
  """
  Theme_Slide_Content is an object that handles the presentation theme slide content, its attributes and methods.
  """
  def __init__(self):
    super(Theme_Slide_Content, self).__init__(raw_data=Raw_Data(regex_start=r'[-]{3}theme_slide_content',regex_end=r'[-]{3}endtheme_slide_content'),
                                              data_dic={'width'            : [re.compile(r"#WIDTH"),'100%'],
                                                        'height'           : [re.compile(r"#HEIGHT"),'100%'],
                                                        'background_color' : [re.compile(r"#BACKGROUND-COLOR"),'white'],
                                                        'border_radius'    : [re.compile(r"#BORDER-RADIUS"),'0 0 0 0'],
                                                        'color'            : [re.compile(r"#COLOR"),'black']},
                                              css = "\n.slide-content {\n  float: left;\n  width: #WIDTH;\n  height: #HEIGHT;\n  color: #COLOR;\n  background: #BACKGROUND-COLOR;\n  border-radius: #BORDER-RADIUS;\n}\n",
                                              active=True)
    return
  def adjust_dims(self,headers,footers,sidebars):
    """
    Method for adjusting content dimensions accordingly to the settings of other elements of the slide theme.
    """
    sw = int(self.data['width'][1].strip('%')) # slide content width (in percent %); should be always 100% initially
    sh = int(self.data['height'][1].strip('%')) # slide content height (in percent %); should be always 100% initially
    for h in headers:
      if h.active:
        sh -= int(h.data['height'][1].strip('%'))
    for f in footers:
      if f.active:
        sh -= int(f.data['height'][1].strip('%'))
    for s in sidebars:
      if s.active:
        sw -= int(s.data['width'][1].strip('%'))
    self.data['width'][1] = str(sw)+'%'
    self.data['height'][1] = str(sh)+'%'
    return
  def to_html(self,tag,doc,content=''):
    """
    Method for inserting slide content into html.
    """
    if self.active:
      with tag('div',('class','slide-content')):
        with tag('div',('class','padding')):
          doc.asis(content)
    return
class Theme_Slide_Header(Theme_Element):
  """
  Theme_Slide_Header is an object that handles the presentation theme slide header, its attributes and methods.
  """
  def __init__(self,number,active=False):
    self.number = number
    super(Theme_Slide_Header, self).__init__(raw_data=Raw_Data(regex_start=r'[-]{3}theme_slide_header_'+str(self.number),regex_end=r'[-]{3}endtheme_slide_header_'+str(self.number)),
                                             data_dic={'height'           : [re.compile(r"#HEIGHT"),'0%'],
                                                       'background_color' : [re.compile(r"#BACKGROUND-COLOR"),'white'],
                                                       'border_radius'    : [re.compile(r"#BORDER-RADIUS"),'10px 10px 0 0'],
                                                       'color'            : [re.compile(r"#COLOR"),''],
                                                       'elements'         : ['',[]]},
                                             css = "\n.slide-header_"+str(self.number)+" {\n  height: #HEIGHT;\n  color: #COLOR;\n  background: #BACKGROUND-COLOR;\n  border-radius: #BORDER-RADIUS;\n}\n",
                                             active=active)
  def to_html(self,tag,doc,content=''):
    """
    Method for inserting slide header content into html.
    """
    if self.active:
      with tag('div',('class','slide-header_'+str(self.number))):
        with tag('div',('class','padding')):
          doc.asis(content)
    return
class Theme_Slide_Footer(Theme_Element):
  """
  Theme_Slide_Footer is an object that handles the presentation theme slide footer, its attributes and methods.
  """
  def __init__(self,number,active=False):
    self.number = number
    super(Theme_Slide_Footer, self).__init__(raw_data=Raw_Data(regex_start=r'[-]{3}theme_slide_footer_'+str(self.number),regex_end=r'[-]{3}endtheme_slide_footer_'+str(self.number)),
                                             data_dic={'height'           : [re.compile(r"#HEIGHT"),'0%'],
                                                       'background_color' : [re.compile(r"#BACKGROUND-COLOR"),'white'],
                                                       'border_radius'    : [re.compile(r"#BORDER-RADIUS"),'0 0 10px 10px'],
                                                       'color'            : [re.compile(r"#COLOR"),'']},
                                             css = "\n.slide-footer_"+str(self.number)+" {\n  clear: both;\n  height: #HEIGHT;\n  color: #COLOR;\n  background: #BACKGROUND-COLOR;\n  border-radius: #BORDER-RADIUS;\n}\n",
                                             active=active)
  def to_html(self,tag,doc,content=''):
    """
    Method for inserting slide footer content into html.
    """
    if self.active:
      with tag('div',('class','slide-footer_'+str(self.number))):
        with tag('div',('class','padding')):
          doc.asis(content)
    return
class Theme_Slide_Sidebar(Theme_Element):
  """
  Theme_Slide_Sidebar is an object that handles the presentation theme slide sidebars, their attributes and methods.
  """
  def __init__(self,number,position='R',active=False):
    self.number = number
    self.position = position
    super(Theme_Slide_Sidebar, self).__init__(raw_data=Raw_Data(regex_start=r'[-]{3}theme_slide_sidebar_'+str(self.number),regex_end=r'[-]{3}endtheme_slide_sidebar_'+str(self.number)),
                                              data_dic={'width'            : [re.compile(r"#WIDTH"),'0%'],
                                                        'height'           : [re.compile(r"#HEIGHT"),'100%'],
                                                        'background_color' : [re.compile(r"#BACKGROUND-COLOR"),'white'],
                                                        'border_radius'    : [re.compile(r"#BORDER-RADIUS"),'0 0 10px 0'],
                                                        'color'            : [re.compile(r"#COLOR"),''],
                                                        'position'         : [re.compile(r"#POSITION"),self.position]},
                                              css = "\n.slide-sidebar_"+str(self.number)+" {\n  /*POS #POSITION*/\n  float: left;\n  width: #WIDTH;\n  height: #HEIGHT;\n  color: #SCOLOR;\n  background: #BACKGROUND-COLOR;\n  border-radius: #BORDER-RADIUS;\n}\n",
                                              active=active)
  def adjust_dims(self,headers,footers):
    """
    Method for adjusting sidebar dimensions accordingly to the settings of other elements of the slide theme.
    """
    sh = int(self.data['height'][1].strip('%')) # slide sidebar height (in percent %); should be always 100% initially
    for h in headers:
      if h.active:
        sh -= int(h.data['height'][1].strip('%'))
    for f in footers:
      if f.active:
        sh -= int(f.data['height'][1].strip('%'))
    self.data['height'][1] = str(sh)+'%'
    return
  def update_position(self):
    """
    Method for updating the position attribute accordingly the data dictionary value.
    """
    self.position = self.data['position'][1]
    return
  def to_html(self,tag,doc,content=''):
    """
    Method for inserting slide sidebar content into html.
    """
    if self.active:
      with tag('div',('class','slide-sidebar_'+str(self.number))):
        with tag('div',('class','padding')):
          doc.asis(content)
    return
class Theme_Slide(Theme_Element):
  """
  Theme_Slide is an object that handles the presentation theme slide, its attributes and methods.
  """
  def __init__(self,
               tag_name        = 'div',
               tag_attrs       = [['class','step slide'],['data-from-markdown','']],
               content         = Theme_Slide_Content()):
    self.tag_name        = tag_name
    self.tag_attrs       = tag_attrs
    self.content         = content

    self.headers         = []
    self.headers_number  = 0
    self.footers         = []
    self.footers_number  = 0
    self.sidebars        = []
    self.sidebars_number = 0
    super(Theme_Slide, self).__init__(raw_data=Raw_Data(regex_start=r'[-]{3}theme_slide_global',regex_end=r'[-]{3}endtheme_slide_global'),
                                      data_dic={'width'            : [re.compile(r"#WIDTH"),'900px'],
                                                'height'           : [re.compile(r"#HEIGHT"),'700px'],
                                                'background_color' : [re.compile(r"#BACKGROUND-COLOR"),'white'],
                                                'border_radius'    : [re.compile(r"#BORDER-RADIUS"),'10px'],
                                                'color'            : [re.compile(r"#COLOR"),'black'],
                                                'font_size'        : [re.compile(r"#FONT-SIZE"),'32px']},
                                      css = "\n.slide {\n  display: block;\n  margin: 0 auto;\n  width: #WIDTH;\n  height: #HEIGHT;\n  color: #COLOR;\n  background: #BACKGROUND-COLOR;\n  border-radius: #BORDER-RADIUS;\n  font-family: 'Open Sans', Arial, sans-serif;\n  font-size: #FONT-SIZE;\n}\n",
                                      active=True)
  def __str__(self):
    string = 'Slide theme settings\n'
    if self.has_header():
      for i,header in enumerate(self.headers):
        string += '\n  Header n.'+str(i+1)+'\n'+str(header)
    if self.has_footer():
      for i,footer in enumerate(self.footers):
        string += '\n  Footer n.'+str(i+1)+'\n'+str(footer)
    if self.has_sidebar():
      for i,sidebar in enumerate(self.sidebars):
        string += '\n  Sidebar n.'+str(i+1)+'\n'+str(sidebar)
    string += '\n  Content\n'+str(self.content)
    return string
  def count_headers(self,source):
    """
    Method for counting the number of headers activated.
    """
    self.headers_number = source.count('theme_slide_header')/2
    return
  def count_footers(self,source):
    """
    Method for counting the number of footers activated.
    """
    self.footers_number = source.count('theme_slide_footer')/2
    return
  def count_sidebars(self,source):
    """
    Method for counting the number of sidebars activated.
    """
    self.sidebars_number = source.count('theme_slide_sidebar')/2
    return
  def has_header(self):
    """
    Method for inquiring the presence of headers.
    """
    header = False
    if len(self.headers)>0:
      for h in self.headers:
        header = h.active
        if header:
          return header
    return header
  def has_footer(self):
    """
    Method for inquiring the presence of footers.
    """
    footer = False
    for f in self.footers:
      footer = f.active
      if footer:
        return footer
    return footer
  def has_sidebar(self):
    """
    Method for inquiring the presence of sidebars.
    """
    sidebar = False
    for s in self.sidebars:
      sidebar = s.active
      if sidebar:
        return sidebar
    return sidebar
  def get_css(self,css_template):
    """
    Method for setting theme values. The theme skeleton is passed as string.
    """
    css = css_template
    if self.has_header():
      for h in self.headers:
        css += h.get_css()
    if self.has_footer():
      for f in self.footers:
        css += f.get_css()
    if self.has_sidebar():
      for s in self.sidebars:
        css += s.get_css()
    css += self.content.get_css()
    css += super(Theme_Slide,self).get_css()
    return css
class Theme(object):
  """
  Theme is an object that handles the presentation theme, its attributes and methods.
  """
  def __init__(self,source):
    self.slide = Theme_Slide()
    # parsing source for eventual global slide settings
    self.slide.get_raw_data(source)
    self.slide.get_values()
    # parsing source for eventual headers definition and settings
    self.slide.count_headers(source)
    if self.slide.headers_number>0:
      for h in range(self.slide.headers_number):
        self.slide.headers.append(Theme_Slide_Header(number=h+1,active=True))
        self.slide.headers[h].get_raw_data(source)
        self.slide.headers[h].get_values()
    # parsing source for eventual footers definition and settings
    self.slide.count_footers(source)
    if self.slide.footers_number>0:
      for f in range(self.slide.footers_number):
        self.slide.footers.append(Theme_Slide_Footer(number=f+1,active=True))
        self.slide.footers[f].get_raw_data(source)
        self.slide.footers[f].get_values()
    # parsing source for eventual sidebars definition and settings
    self.slide.count_sidebars(source)
    if self.slide.sidebars_number>0:
      for s in range(self.slide.sidebars_number):
        self.slide.sidebars.append(Theme_Slide_Sidebar(number=s+1,active=True))
        self.slide.sidebars[s].get_raw_data(source)
        self.slide.sidebars[s].get_values()
        self.slide.sidebars[s].update_position()
    # parsing source for eventual slide content settings
    self.slide.content.get_raw_data(source)
    self.slide.content.get_values()
  def __str__(self):
    string = 'Theme settings\n'
    string += str(self.slide)
    return string
  def has_header(self):
    """
    Method for inquiring the presence of headers into the slide theme.
    """
    return self.slide.has_header()
  def has_footer(self):
    """
    Method for inquiring the presence of footers into the slide theme.
    """
    return self.slide.has_footer()
  def has_sidebar(self):
    """
    Method for inquiring the presence of sidebars into the slide theme.
    """
    return self.slide.has_sidebar()
  def get_css(self):
    """
    Method for creating a theme css accordingly to the user options.
    It is made parsing the "MaTiSSe/css/themes/default-skeleton.css" file.
    The returned string contains the css theme.
    """
    # dimensioning slide content size accordingly to other theme's elements
    self.slide.content.adjust_dims(headers=self.slide.headers,footers=self.slide.footers,sidebars=self.slide.sidebars)
    # dimensioning slide sidebars size accordingly to other theme's elements
    if self.has_sidebar():
      for sidebar in self.slide.sidebars:
        sidebar.adjust_dims(headers=self.slide.headers,footers=self.slide.footers)
    # loading skeleton
    css = os.path.join(os.path.dirname(__file__), 'css/themes/default-skeleton.css')
    with open(css,'r') as sk_css:
      css_template = sk_css.read()
    return self.slide.get_css(css_template)
  def strip(self,source):
    """
    Method for striping theme raw data from source.
    """
    strip_source = self.slide.raw_data.strip(source)
    strip_source = self.slide.content.raw_data.strip(strip_source)
    return strip_source
class Engine(object):
  """
  Engine is an object that handles the "engine" powering the html presentation.
  """
  def __init__(self,source,js='impress.js'):
    self.js = js
    # initializing presentation metadata
    self.metadata = Metadata()
    # extracting raw metadata from markdown source
    self.metadata.get_raw_data(source)
    # setting presentation metadata
    self.metadata.get_values()
    # initializing theme
    self.theme = Theme(source=source)
    return
  def __str__(self):
    string = str(self.metadata)
    string += str(self.theme)
    return string
  def is_reveal(self):
    """
    Method for checking if the engine is using "reveal.js".
    """
    return self.js == 'reveal.js'
  def is_impress(self):
    """
    Method for checking if the engine is using "impress.js".
    """
    return self.js == 'impress.js'
  def is_jmpress(self):
    """
    Method for checking if the engine is using "jmpress.js".
    """
    return self.js == 'jmpress.js'
  def make_output_tree(self,output):
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
      css_theme.writelines(self.theme.get_css())
    if not os.path.exists(output+'js'):
      os.makedirs(output+'js')
    # impress.js files
    if self.is_impress():
      js = os.path.join(os.path.dirname(__file__), 'js/impress/impress.js')
      copyfile(js,output+'js/impress.js')
    # reveal.js files
    if self.is_reveal():
      pass
    return output
  def strip_preamble_data(self,source):
    """
    Method for striping preamble data from source.
    """
    strip_source = self.metadata.strip(source)
    strip_source = self.theme.strip(strip_source)
    return strip_source
  def put_styles(self,tag,doc):
    """
    Method for inserting the styles into html.
    """
    # some useful styles
    doc.stag('link',rel='stylesheet', href='css/normalize.css')
    # default theme
    doc.stag('link',rel='stylesheet', href='css/theme.css')
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
    return
class Section(object):
  """
  Section is an object that handles a single section, its attributes and methods.
  """
  def __init__(self,title='',raw_body='',slides=None):
    self.title = title
    self.raw_body = raw_body
    self.slides = slides
  def to_html(self,tag,doc,engine):
    """
    Method for converting section slides content into html format.
    """
    with tag('div',klass='section',id=self.title):
      for slide in self.slides:
        slide.to_html(tag,doc,engine)
    return
class Slide(object):
  """
  Slide is an object that handles a single slide, its attributes and methods.
  """
  def __init__(self,title='',raw_body='',number=0):
    self.title = title
    self.raw_body = raw_body
    self.number = number
  def to_html(self,tag,doc,engine):
    """
    Method for converting slide content into html format.
    """
    with tag(engine.theme.slide.tag_name,('title',self.title)):
      for a in engine.theme.slide.tag_attrs:
        doc.attr((a[0],a[1]))
      if engine.is_impress():
        doc.attr(('data-x',str(self.number+self.number*1000)))
      for h in engine.theme.slide.headers:
        h.to_html(tag=tag,doc=doc,content=self.title)
      for s in engine.theme.slide.sidebars:
        if s.position == 'L':
          s.to_html(tag=tag,doc=doc,content='Left sidebar')
      engine.theme.slide.content.to_html(tag=tag,doc=doc,content='\n'+__md__.convert(self.raw_body))
      for s in engine.theme.slide.sidebars:
        if s.position == 'R':
          s.to_html(tag=tag,doc=doc,content='Right sidebar')
      for f in engine.theme.slide.footers:
        f.to_html(tag=tag,doc=doc,content='Footer')
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
def get_sections(source):
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
def get_slides(sections,slides_number):
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
      slides_number += 1
      if s < len(slds)-1:
        section.slides.append(Slide(title=sld[0],raw_body=section.raw_body[sld[2]+1:slds[s+1][1]],number=slides_number))
      else:
        section.slides.append(Slide(title=sld[0],raw_body=section.raw_body[sld[2]+1:],number=slides_number))
  return slides_number
def parse_file(md_file,output=None):
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
    # initializing engine
    engine = Engine(source=source)
    # stripping out preamble data
    source = engine.strip_preamble_data(source)
    # creating output tree
    if not output:
      output = os.path.splitext(os.path.basename(md_file))[0]
    output = engine.make_output_tree(output)
    # parsing input stream
    slides_number = 0
    sections = get_sections(source)
    slides_number = get_slides(sections,slides_number)
    # creating html presentation
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
      doc.attr(title = engine.metadata.data['title'])
      with tag('head'):
        doc.stag('meta',charset='utf-8')
        # presentation metadata
        doc.stag('meta',author=' and '.join(engine.metadata.data['authors']))
        with tag('title'):
          text(engine.metadata.data['title'])
        doc.stag('meta',subtitle=engine.metadata.data['subtitle'])
        # styles
        engine.put_styles(tag,doc)
      with tag('body'):
        if engine.is_reveal():
          with tag('div',klass='reveal'):
            with tag('div',klass='slides'):
              for section in sections:
                section.to_html(tag,doc,engine)
        elif engine.is_impress():
          with tag('div',id='impress'):
            for section in sections:
              section.to_html(tag,doc,engine)
        else:
          for section in sections:
            section.to_html(tag,doc,engine)
        # scripts
        engine.put_scripts(tag,doc)
    # saving presentation
    with open(output+'index.html','w') as html_presentation:
      html_presentation.write(indent(doc.getvalue()))
  return engine
def main():
  """
  Main function.
  """
  cliargs = __cliparser__.parse_args()
  if cliargs.input:
    engine = parse_file(md_file=cliargs.input,output=cliargs.output)
    if cliargs.print_preamble:
      print(engine)
# main loop
if __name__ == '__main__':
  main()

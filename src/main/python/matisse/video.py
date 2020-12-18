#!/usr/bin/env python
"""
video.py, module definition of Video class.
"""
from __future__ import absolute_import
import re
from yattag import Doc
from .box import Box


class Video(Box):
  """
  Object for handling video-box. It is a subclass of Box.

  The syntax is:

  $video
  $style[style_options]
  $caption[caption_options]{caption}
  $content[content_options]{content}
  $endvideo

  Note that differently from Box class:
  1. the "content_type" and "caption_type" are automatically set to "video" and "Video" respectively; anyhow they can be still
     specified inside the $video/$endvideo environment;
  2. the "caption" is at bottom by default, but it can be also positionated at the top.

  Attributes
  ----------
  regexs: dict
    dictionary of regexs
  videos_number : int
    global number of videos (equals to the number of Video instances)
  """
  regexs = {'video': re.compile(r"(?P<video>\$video(?P<env>.*?)\$endvideo)", re.DOTALL)}
  videos_number = 0

  @classmethod
  def reset(cls):
    """Reset to default state."""
    cls.videos_number = 0
    return

  def __init__(self, source=None, theme=None):
    """
    Parameters
    ----------
    source : str, optional
      string (as single stream) containing the source

    Attributes
    ----------
    number : int
      number of video
    """
    super(Video, self).__init__(ctn_type='video')
    self.cap_type = 'Video'
    self.controls = False
    self.autoplay = False
    if theme is not None:
      for css in theme.video_content:
        for key in css:
          if 'controls' in key.lower():
            self.controls = True
          if 'autoplay' in key.lower():
            self.autoplay = True
    Video.videos_number += 1
    self.number = Video.videos_number
    if source:
      self.get(source=source)
    return

  def to_html(self):
    """Convert self data to its html stream."""
    doc = Doc()
    with doc.tag('div', id='video-' + str(self.number)):
      if self.style:
        doc.attr(style=self.style)
      else:
        doc.attr(klass='video')
      if self.cap_position is not None and self.cap_position.upper() == 'TOP':
        self.put_caption(doc=doc, klass='video-caption')
      with doc.tag('video', klass='video-content'):
        if self.controls:
          doc.attr(controls='controls')
        if self.autoplay:
          doc.attr(autoplay='autoplay')
        if self.ctn_options:
          doc.attr(style=self.ctn_options)
        else:
          doc.attr(style='width:100%;')
        doc.stag('source', src=self.ctn)
      if self.cap_position is None or self.cap_position.upper() == 'BOTTOM':
        self.put_caption(doc=doc, klass='video-caption')
    return doc.getvalue()

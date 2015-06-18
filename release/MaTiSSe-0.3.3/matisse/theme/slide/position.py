#!/usr/bin/env python
"""
position.py, module definition of Position class.
This defines the position features of the slide element.
"""
# class definition
class Position(object):
  """
  Object for handling slide position into the canvas.
  """
  def __init__(self,pos=None):
    """
    Attributes
    ----------
    position : list
      list of 3 int containing x,y,z position values
    rotation : list
      list of 3 int containing x,y,z rotation values
    scale : int
      scaling factor
    offset : int
      distance between consecutive slide in percent (%)
    """
    if pos:
      self.position = pos
    else:
      self.position = [0,0,0] # x,y,z
    self.rotation = [0,0,0] # around x,y,z
    self.scale = 1
    self.offset = 1
    return

  def __str__(self):
    string = ['\nPosition (x,y,z) = '+','.join([str(p) for p in self.position])]
    string.append('\nRotation (x,y,z) = '+','.join([str(r) for r in self.rotation]))
    string.append('\nScale factor = '+str(self.scale))
    return ''.join(string)

  @staticmethod
  def get_scale(theme):
    """Method for computing the current slide scale factor.

    Parameters
    ----------
    theme : Theme object
      current global theme

    Returns
    -------
    int
      scaling factor

    >>> from .slide import Slide
    >>> source = '---theme_slide_global data-scale = 3 ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos = Position()
    >>> pos.get_scale(theme=theme)
    3
    """
    return int(theme.data.data['data-scale'][0])

  @staticmethod
  def get_offset(theme):
    """Method for computing the current slide offset factor.

    Parameters
    ----------
    theme : Theme object
      current global theme

    Returns
    -------
    int
      offset factor

    >>> from .slide import Slide
    >>> source = '---theme_slide_global data-offset = 200 ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos = Position()
    >>> pos.get_offset(theme=theme)
    200
    """
    return int(theme.data.data['data-offset'][0])

  @staticmethod
  def get_rotation(theme):
    """Method for computing the current slide rotation.

    Parameters
    ----------
    theme : Theme object
      current global theme

    Returns
    -------
    list
      list of 3 int containing x,y,z rotation values

    >>> from .slide import Slide
    >>> source = '---theme_slide_global data-rotate-x = 45 \\n data-rotate-y = 65 \\n data-rotate-z = 85 ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos = Position()
    >>> pos.get_rotation(theme=theme)
    [45, 65, 85]
    """
    rot = int(theme.data.data['data-rotate'][0])
    rot_x = int(theme.data.data['data-rotate-x'][0])
    rot_y = int(theme.data.data['data-rotate-y'][0])
    rot_z = int(theme.data.data['data-rotate-z'][0])
    if rot_z != 0:
      rot = max(rot,rot_z)
    return [rot_x,rot_y,rot]

  def get_position(self,theme,scale,offset):
    """Method for computing the current slide position.

    Parameters
    ----------
    theme : Theme object
      current global theme
    scale : int
      factor scaling of previous slide
    offset : int
      offset factor

    Returns
    -------
    list
      list of 3 int containing x,y,z position values

    >>> from .slide import Slide
    >>> source = '---theme_slide_global slide-transition = absolute \\n data-x = 45 \\n data-y = 65 \\n data-z = 85 ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos = Position()
    >>> pos.get_position(theme=theme,scale=1,offset=1)
    [45, 65, 85]
    >>> source = '---theme_slide_global width = 1 \\n slide-transition = Horizontal ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos.get_position(theme=theme,scale=1,offset=100)
    [2.0, 0, 0]
    >>> source = '---theme_slide_global width = 1 \\n slide-transition = -Horizontal ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos.get_position(theme=theme,scale=1,offset=100)
    [-2.0, 0, 0]
    >>> source = '---theme_slide_global height = 1 \\n slide-transition = Vertical ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos.get_position(theme=theme,scale=1,offset=100)
    [0, 2.0, 0]
    >>> source = '---theme_slide_global height = 1 \\n slide-transition = -Vertical ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos.get_position(theme=theme,scale=1,offset=100)
    [0, -2.0, 0]
    >>> source = '---theme_slide_global width = 1 \\n height = 1 \\n slide-transition = Diagonal ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos.get_position(theme=theme,scale=1,offset=100)
    [2.0, 2.0, 0]
    >>> source = '---theme_slide_global width = 1 \\n height = 1 \\n slide-transition = -Diagonal ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos.get_position(theme=theme,scale=1,offset=100)
    [-2.0, -2.0, 0]
    >>> source = '---theme_slide_global width = 1 \\n height = 1 \\n slide-transition = Diagonal-X ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos.get_position(theme=theme,scale=1,offset=100)
    [-2.0, 2.0, 0]
    >>> source = '---theme_slide_global width = 1 \\n height = 1 \\n slide-transition = Diagonal-Y ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos.get_position(theme=theme,scale=1,offset=100)
    [2.0, -2.0, 0]
    """
    pos_x = int(theme.data.data['data-x'][0])
    pos_y = int(theme.data.data['data-y'][0])
    pos_z = int(theme.data.data['data-z'][0])
    slide_width = int(theme.data.data['width'][0].strip('px'))
    slide_height = int(theme.data.data['height'][0].strip('px'))
    slide_transition = theme.data.data['slide-transition'][0]
    if slide_transition.lower() == 'absolute':
      pass
    elif slide_transition.lower() == 'svgpath':
      pos_x = self.position[0]
      pos_y = self.position[1]
      pos_z = self.position[2]
    elif slide_transition.lower() == 'horizontal':
      pos_x = self.position[0] + slide_width*(max(self.scale,scale)+offset/100.0)
      pos_y = self.position[1]
    elif slide_transition.lower() == '-horizontal':
      pos_x = self.position[0] - slide_width*(max(self.scale,scale)+offset/100.0)
      pos_y = self.position[1]
    elif slide_transition.lower() == 'vertical':
      pos_x = self.position[0]
      pos_y = self.position[1] + slide_height*(max(self.scale,scale)+offset/100.0)
    elif slide_transition.lower() == '-vertical':
      pos_x = self.position[0]
      pos_y = self.position[1] - slide_height*(max(self.scale,scale)+offset/100.0)
    elif slide_transition.lower() == 'diagonal':
      pos_x = self.position[0] + slide_width*(max(self.scale,scale)+offset/100.0)
      pos_y = self.position[1] + slide_height*(max(self.scale,scale)+offset/100.0)
    elif slide_transition.lower() == '-diagonal':
      pos_x = self.position[0] - slide_width*(max(self.scale,scale)+offset/100.0)
      pos_y = self.position[1] - slide_height*(max(self.scale,scale)+offset/100.0)
    elif slide_transition.lower() == 'diagonal-x':
      pos_x = self.position[0] - slide_width*(max(self.scale,scale)+offset/100.0)
      pos_y = self.position[1] + slide_height*(max(self.scale,scale)+offset/100.0)
    elif slide_transition.lower() == 'diagonal-y':
      pos_x = self.position[0] + slide_width*(max(self.scale,scale)+offset/100.0)
      pos_y = self.position[1] - slide_height*(max(self.scale,scale)+offset/100.0)
    return [pos_x,pos_y,pos_z]

  def set_position(self,theme):
    """Method for setting positioning data inquiring the (base) theme and the eventually present overriding one.

    Parameters
    ----------
    theme : Theme object
      current theme

    >>> from .slide import Slide
    >>> source = '---theme_slide_global slide-transition = absolute \\n data-x = 45 \\n data-y = 65 \\n data-z = 85 ---endtheme_slide_global'
    >>> theme = Slide(source=source)
    >>> pos = Position()
    >>> pos.set_position(theme=theme)
    >>> pos.position
    [45, 65, 85]
    """
    scale = self.get_scale(theme=theme)
    offset = self.get_offset(theme=theme)

    self.rotation = self.get_rotation(theme=theme)

    self.position = self.get_position(theme=theme,scale=scale,offset=offset)

    self.scale = scale
    self.offset = offset
    return

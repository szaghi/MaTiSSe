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
  def __init__(self):
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
    """
    return int(theme.data.data['data-scale'][0])

  @staticmethod
  def get_rotation(theme):
    """Method for computing the current slide scale factor.

    Parameters
    ----------
    theme : Theme object
      current global theme

    Returns
    -------
    list
      list of 3 int containing x,y,z rotation values
    """
    rot = int(theme.data.data['data-rotate'][0])
    rot_x = int(theme.data.data['data-rotate-x'][0])
    rot_y = int(theme.data.data['data-rotate-y'][0])
    rot_z = int(theme.data.data['data-rotate-z'][0])
    if rot_z != 0:
      rot = max(rot,rot_z)
    return [rot_x,rot_y,rot]

  def get_position(self,theme,scale):
    """Method for computing the current slide position.

    Parameters
    ----------
    theme : Theme object
      current global theme
    scale : int
      factor scaling of previous slide

    Returns
    -------
    list
      list of 3 int containing x,y,z position values
    """
    pos_x = int(theme.data.data['data-x'][0])
    pos_y = int(theme.data.data['data-y'][0])
    pos_z = int(theme.data.data['data-z'][0])
    slide_width = int(theme.data.data['width'][0].strip('px'))
    slide_height = int(theme.data.data['height'][0].strip('px'))
    slide_transition = theme.data.data['slide-transition'][0]
    if slide_transition == 'absolute':
      pass
    elif slide_transition == 'horizontal':
      pos_x = self.position[0] + slide_width*(max(self.scale,scale)+self.offset/100.0)
      pos_y = self.position[1]
      #pos_z = self.position[2]
    elif slide_transition == '-horizontal':
      pos_x = self.position[0] - slide_width*(max(self.scale,scale)+self.offset/100.0)
      pos_y = self.position[1]
      #pos_z = self.position[2]
    elif slide_transition == 'vertical':
      pos_x = self.position[0]
      pos_y = self.position[1] + slide_height*(max(self.scale,scale)+self.offset/100.0)
      #pos_z = self.position[2]
    elif slide_transition == '-vertical':
      pos_x = self.position[0]
      pos_y = self.position[1] - slide_height*(max(self.scale,scale)+self.offset/100.0)
      #pos_z = self.position[2]
    elif slide_transition == 'diagonal':
      pos_x = self.position[0] + slide_width*(max(self.scale,scale)+self.offset/100.0)
      pos_y = self.position[1] + slide_height*(max(self.scale,scale)+self.offset/100.0)
      #pos_z = self.position[2]
    elif slide_transition == '-diagonal':
      pos_x = self.position[0] - slide_width*(max(self.scale,scale)+self.offset/100.0)
      pos_y = self.position[1] - slide_height*(max(self.scale,scale)+self.offset/100.0)
      #pos_z = self.position[2]
    elif slide_transition == 'diagonal-x':
      pos_x = self.position[0] - slide_width*(max(self.scale,scale)+self.offset/100.0)
      pos_y = self.position[1] + slide_height*(max(self.scale,scale)+self.offset/100.0)
      #pos_z = self.position[2]
    elif slide_transition == 'diagonal-y':
      pos_x = self.position[0] + slide_width*(max(self.scale,scale)+self.offset/100.0)
      pos_y = self.position[1] - slide_height*(max(self.scale,scale)+self.offset/100.0)
      #pos_z = self.position[2]
    return [pos_x,pos_y,pos_z]

  def set_position(self,theme,overtheme=None):
    """Method for setting positioning data inquiring the (base) theme and the eventually present overriding one.

    Parameters
    ----------
    theme : Theme object
      current global theme
    overtheme : Theme object
      overrinding theme
    """
    actual_theme = theme
    if overtheme:
      actual_theme = overtheme

    scale = self.get_scale(theme=actual_theme)

    self.rotation = self.get_rotation(theme=actual_theme)

    self.position = self.get_position(theme=actual_theme,scale=scale)

    self.scale = scale
    return

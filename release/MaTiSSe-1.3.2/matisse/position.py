#!/usr/bin/env python
"""
position.py, module definition of Position class.
"""
from __future__ import print_function


class Position(object):
  """
  Object for handling slide position into the infinite canvas.
  """

  @classmethod
  def reset(cls):
    """Reset to default state."""

  def __init__(self):
    """
    Attributes
    ----------
    """
    self.position = {'x': 0, 'y': 0, 'z': 0,
                     'rotx': 0, 'roty': 0, 'rotz': 0,
                     'scale': 1}

  def __update_position_absolute(self, transition):
    """Update position for absolute transition."""
    if transition['data-x'] != '':
      self.position['x'] = int(transition['data-x'])
    if transition['data-y'] != '':
      self.position['y'] = int(transition['data-y'])
    if transition['data-z'] != '':
      self.position['z'] = int(transition['data-z'])
    if transition['data-rotate-x'] != '':
      self.position['rotx'] = int(transition['data-rotate-x'])
    if transition['data-rotate-y'] != '':
      self.position['roty'] = int(transition['data-rotate-y'])
    if transition['data-rotate-z'] != '':
      self.position['rotz'] = int(transition['data-rotate-z'])
    if transition['scale'] != '':
      self.position['scale'] = int(transition['scale'])

  def __update_position_svgpath(self, transition):
    """Update position for svgpath transition."""

  def __update_position_horizontal(self, transition):
    """Update position for horizontal transition."""
    self.position['x'] = self.position['x'] + transition['width'] * (max(self.position['scale'], transition['scale']) + transition['offset'] / 100.0)

  def __update_position_neg_horizontal(self, transition):
    """Update position for -horizontal transition."""
    self.position['x'] = self.position['x'] - transition['width'] * (max(self.position['scale'], transition['scale']) + transition['offset'] / 100.0)

  def __update_position_vertical(self, transition):
    """Update position for vertical transition."""
    self.position['y'] = self.position['y'] + transition['height'] * (max(self.position['scale'], transition['scale']) + transition['offset'] / 100.0)

  def __update_position_neg_vertical(self, transition):
    """Update position for -vertical transition."""
    self.position['y'] = self.position['y'] - transition['height'] * (max(self.position['scale'], transition['scale']) + transition['offset'] / 100.0)

  def __update_position_diagonal(self, transition):
    """Update position for diagonal transition."""
    self.position['x'] = self.position['x'] + transition['width'] * (max(self.position['scale'], transition['scale']) + transition['offset'] / 100.0)
    self.position['y'] = self.position['y'] + transition['height'] * (max(self.position['scale'], transition['scale']) + transition['offset'] / 100.0)

  def __update_position_neg_diagonal(self, transition):
    """Update position for -diagonal transition."""
    self.position['x'] = self.position['x'] - transition['width'] * (max(self.position['scale'], transition['scale']) + transition['offset'] / 100.0)
    self.position['y'] = self.position['y'] - transition['height'] * (max(self.position['scale'], transition['scale']) + transition['offset'] / 100.0)

  def __update_position_diagonal_neg_x(self, transition):
    """Update position for diagonal-x transition."""
    self.position['x'] = self.position['x'] - transition['width'] * (max(self.position['scale'], transition['scale']) + transition['offset'] / 100.0)
    self.position['y'] = self.position['y'] + transition['height'] * (max(self.position['scale'], transition['scale']) + transition['offset'] / 100.0)

  def __update_position_diagonal_neg_y(self, transition):
    """Update position for diagonal-y transition."""
    self.position['x'] = self.position['x'] + transition['width'] * (max(self.position['scale'], transition['scale']) + transition['offset'] / 100.0)
    self.position['y'] = self.position['y'] - transition['height'] * (max(self.position['scale'], transition['scale']) + transition['offset'] / 100.0)

  def update_position(self, presentation_theme, overtheme=None):
    """Update the position using theme/overtheme slides-transition data.

    Parameters
    ----------
    presentation_theme: Theme()
      main presentation theme
    overtheme: Theme()
      eventual slide overtheme
    """
    update = {'absolute': self.__update_position_absolute,
              'svgpath': self.__update_position_svgpath,
              'horizontal': self.__update_position_horizontal,
              '-horizontal': self.__update_position_neg_horizontal,
              'vertical': self.__update_position_vertical,
              '-vertical': self.__update_position_neg_vertical,
              'diagonal': self.__update_position_diagonal,
              '-diagonal': self.__update_position_neg_diagonal,
              'diagonal-x': self.__update_position_diagonal_neg_x,
              'diagonal-y': self.__update_position_diagonal_neg_y}
    if overtheme is not None and overtheme.custom:
      theme = overtheme
    else:
      theme = presentation_theme

    transition = theme.get_slide_transition()
    if transition['transition'].lower() in update:
      update[transition['transition'].lower()](transition=transition)
    else:
      print('Warning: the slide transition "' + transition['transition'] + '" is unknown!')
      update['horizontal'](transition=transition)

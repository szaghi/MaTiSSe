#!/usr/bin/env python3
"""
matisse.backends.impress.position — impress.js slide position calculator.

Moved from ``matisse/position.py``.  The original module is now a thin
re-export shim:

    from matisse.backends.impress.position import Position
"""


class Position(object):
    """
    Object for handling slide position into the infinite canvas.
    """

    def __init__(self):
        self.position = {"x": 0, "y": 0, "z": 0, "rotx": 0, "roty": 0, "rotz": 0, "scale": 1}

    def __update_scale(self, transition):
        if transition["scale"] != "":
            self.position["scale"] = int(transition["scale"])

    def __update_position_absolute(self, transition):
        if transition["data-x"] != "":
            self.position["x"] = int(transition["data-x"])
        if transition["data-y"] != "":
            self.position["y"] = int(transition["data-y"])
        if transition["data-z"] != "":
            self.position["z"] = int(transition["data-z"])
        if transition["data-rotate-x"] != "":
            self.position["rotx"] = int(transition["data-rotate-x"])
        if transition["data-rotate-y"] != "":
            self.position["roty"] = int(transition["data-rotate-y"])
        if transition["data-rotate-z"] != "":
            self.position["rotz"] = int(transition["data-rotate-z"])
        self.__update_scale(transition=transition)

    def __update_position_svgpath(self, transition):
        pass

    def __update_position_horizontal(self, transition):
        self.position["x"] = self.position["x"] + transition["width"] * (
            max(self.position["scale"], transition["scale"]) + transition["offset"] / 100.0
        )
        self.__update_scale(transition=transition)

    def __update_position_neg_horizontal(self, transition):
        self.position["x"] = self.position["x"] - transition["width"] * (
            max(self.position["scale"], transition["scale"]) + transition["offset"] / 100.0
        )
        self.__update_scale(transition=transition)

    def __update_position_vertical(self, transition):
        self.position["y"] = self.position["y"] + transition["height"] * (
            max(self.position["scale"], transition["scale"]) + transition["offset"] / 100.0
        )
        self.__update_scale(transition=transition)

    def __update_position_neg_vertical(self, transition):
        self.position["y"] = self.position["y"] - transition["height"] * (
            max(self.position["scale"], transition["scale"]) + transition["offset"] / 100.0
        )
        self.__update_scale(transition=transition)

    def __update_position_diagonal(self, transition):
        self.position["x"] = self.position["x"] + transition["width"] * (
            max(self.position["scale"], transition["scale"]) + transition["offset"] / 100.0
        )
        self.position["y"] = self.position["y"] + transition["height"] * (
            max(self.position["scale"], transition["scale"]) + transition["offset"] / 100.0
        )
        self.__update_scale(transition=transition)

    def __update_position_neg_diagonal(self, transition):
        self.position["x"] = self.position["x"] - transition["width"] * (
            max(self.position["scale"], transition["scale"]) + transition["offset"] / 100.0
        )
        self.position["y"] = self.position["y"] - transition["height"] * (
            max(self.position["scale"], transition["scale"]) + transition["offset"] / 100.0
        )
        self.__update_scale(transition=transition)

    def __update_position_diagonal_neg_x(self, transition):
        self.position["x"] = self.position["x"] - transition["width"] * (
            max(self.position["scale"], transition["scale"]) + transition["offset"] / 100.0
        )
        self.position["y"] = self.position["y"] + transition["height"] * (
            max(self.position["scale"], transition["scale"]) + transition["offset"] / 100.0
        )
        self.__update_scale(transition=transition)

    def __update_position_diagonal_neg_y(self, transition):
        self.position["x"] = self.position["x"] + transition["width"] * (
            max(self.position["scale"], transition["scale"]) + transition["offset"] / 100.0
        )
        self.position["y"] = self.position["y"] - transition["height"] * (
            max(self.position["scale"], transition["scale"]) + transition["offset"] / 100.0
        )
        self.__update_scale(transition=transition)

    def update_position(self, presentation_theme, overtheme=None):
        """Update the position using theme/overtheme slides-transition data."""
        update = {
            "absolute": self.__update_position_absolute,
            "svgpath": self.__update_position_svgpath,
            "horizontal": self.__update_position_horizontal,
            "-horizontal": self.__update_position_neg_horizontal,
            "vertical": self.__update_position_vertical,
            "-vertical": self.__update_position_neg_vertical,
            "diagonal": self.__update_position_diagonal,
            "-diagonal": self.__update_position_neg_diagonal,
            "diagonal-x": self.__update_position_diagonal_neg_x,
            "diagonal-y": self.__update_position_diagonal_neg_y,
        }
        if overtheme is not None and overtheme.custom:
            theme = overtheme
        else:
            theme = presentation_theme

        transition = theme.get_slide_transition()
        if transition["transition"].lower() in update:
            update[transition["transition"].lower()](transition=transition)
        else:
            print(f'Warning: the slide transition "{transition["transition"]}" is unknown!')
            update["horizontal"](transition=transition)

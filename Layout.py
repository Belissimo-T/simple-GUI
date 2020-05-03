class PixelConstraint:
    def __init__(self, number):
        self.number = number

    def get(self, parent_widget, orientation, self_widget):
        if orientation == "x":
            if self.number < 0:
                return parent_widget.get_x() + parent_widget.get_width() / 2 - self_widget.get_width() / 2 + self.number
            else:
                return parent_widget.get_x() - parent_widget.get_width() / 2 + self_widget.get_width() / 2 + self.number
        elif orientation == "y":
            if self.number < 0:
                return parent_widget.get_y() + parent_widget.get_height() / 2 - self_widget.get_height() / 2 + self.number
            else:
                return parent_widget.get_y() - parent_widget.get_height() / 2 + self_widget.get_height() / 2 + self.number
        elif orientation == "width":
            return parent_widget.get_width() - self.number * 2
        elif orientation == "height":
            return parent_widget.get_height() - self.number * 2


class CenterConstraint:
    @staticmethod
    def get(parent_widget, orientation, self_widget):
        if orientation == "x":
            return parent_widget.get_x()  # + parent_widget.width / 2
        elif orientation == "y":
            return parent_widget.get_y()  # + parent_widget.height / 2
        else:
            raise Exception("Center Constraint can't be used for " + orientation)


class ProportionConstraint:
    def __init__(self, percent):
        self.multiplier = percent / 100

    def get(self, parent_widget, orientation, self_widget):
        if orientation == "width":
            return parent_widget.get_width() * self.multiplier
        elif orientation == "height":
            return parent_widget.get_height() * self.multiplier
        elif orientation == "x":
            return parent_widget.get_x() - parent_widget.get_width() / 2 + parent_widget.get_width() * self.multiplier
        elif orientation == "y":
            return parent_widget.get_y() - parent_widget.get_height() / 2 + parent_widget.get_height() * self.multiplier


class ConstantConstraint:
    def __init__(self, constant):
        self.constant = constant

    def get(self, parent_widget, orientation, self_widget):
        return self.constant


class DistanceConstraint:
    def __init__(self, widget, distance_constraint=ConstantConstraint(0)):
        self.widget = widget
        self.distance_constraint = distance_constraint

    def get(self, parent_widget, orientation, self_widget):
        distance = self.distance_constraint.get(parent_widget, orientation, self_widget)
        if orientation == "x":
            if distance < 0:
                return self.widget.get_x() - self.widget.get_width() / 2 + distance - self_widget.get_width() / 2
            else:
                return self.widget.get_x() + self.widget.get_width() / 2 + distance + self_widget.get_width() / 2
        elif orientation == "y":
            if distance < 0:
                return self.widget.get_y() - self.widget.get_height() / 2 + distance - self_widget.get_height() / 2
            else:
                return self.widget.get_y() + self.widget.get_height() / 2 + distance + self_widget.get_height() / 2


class ProportionOfConstraint:
    def __init__(self, widget, percent):
        self.widget = widget
        self.multiplier = percent / 100

    def get(self, parent_widget, orientation, self_widget):
        if orientation == "x":
            return self.widget.get_x() * self.multiplier
        elif orientation == "y":
            return self.widget.get_y() * self.multiplier
        elif orientation == "width":
            return self.widget.get_width() * self.multiplier
        elif orientation == "height":
            return self.widget.get_height() * self.multiplier


class AspectConstraint:
    def __init__(self, ratio):
        self.ratio = ratio

    def get(self, parent_widget, orientation, self_widget):
        if orientation == "x":
            return self_widget.get_y() * self.ratio
        elif orientation == "y":
            return self_widget.get_x() * self.ratio
        elif orientation == "width":
            return self_widget.get_height() * self.ratio
        elif orientation == "height":
            return self_widget.get_width() * self.ratio


class EmulatingConstraint:
    def __init__(self, widget, constraint, orientation=None):
        self.widget = widget
        self.constraint = constraint
        self.orientation = orientation

    def get(self, parent_widget, orientation, self_widget):
        if self.orientation:
            orientation = self.orientation

        return self.constraint.get(self.widget.parent_widget, orientation, self.widget)

class FillWallConstraint:
    def __init__(self, side="RIGHT"):
        self.side = side
    def get(self, parent_widget, orientation, self_widget):
        if self.side == "RIGHT":
            pass


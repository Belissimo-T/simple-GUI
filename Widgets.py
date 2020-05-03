from Main import *
from Layout import *

VERTICAL = "VERTICAL"
HORIZONTAL = "HORIZONTAL"


class Widget:

    def __init__(self, parent_widget):
        self.widgets = []
        self.parent_widget = parent_widget
        self.parent_widget.widgets.append(self)
        self.sf = parent_widget.sf

        self.x_constraint = 1
        self.y_constraint = 1
        self.width_constraint = None
        self.height_constraint = None

        self.pos: tuple = (1, 1)
        self.width = 1
        self.height = 1

        self.hover_events = []

    def update_x_constraint(self):
        self.pos = (self.x_constraint.get(self.parent_widget, "x", self), self.pos[1])

    def update_y_constraint(self):
        self.pos = (self.pos[0], self.y_constraint.get(self.parent_widget, "y", self))

    def update_width_constraint(self):
        self.width = self.width_constraint.get(self.parent_widget, "width", self)

    def update_height_constraint(self):
        self.height = self.height_constraint.get(self.parent_widget, "height", self)

    def add_hover_event(self, function):
        self.hover_events.append(function)

    def remove_hover_event(self, function):
        self.hover_events.remove(function)

    def update_constraints(self):
        self.update_x_constraint()
        self.update_y_constraint()
        self.update_width_constraint()
        self.update_height_constraint()
        pass

    def set_x_constraint(self, constraint):
        self.x_constraint = constraint

    def set_y_constraint(self, constraint):
        self.y_constraint = constraint

    def set_width_constraint(self, constraint):
        self.width_constraint = constraint

    def set_height_constraint(self, constraint):
        self.height_constraint = constraint

    def set_constraints(self, x_constraint=None, y_constraint=None, width_constraint=None, height_constraint=None):
        if x_constraint:
            self.set_x_constraint(x_constraint)
        if y_constraint:
            self.set_y_constraint(y_constraint)
        if width_constraint:
            self.set_width_constraint(width_constraint)
        if height_constraint:
            self.set_height_constraint(height_constraint)

    def get_x(self):
        # self.update_x_constraint()
        return self.pos[0]

    def get_y(self):
        # self.update_y_constraint()
        return self.pos[1]

    def get_width(self):
        # self.update_width_constraint()
        return self.width

    def get_height(self):
        # self.update_height_constraint()
        return self.height

    def update(self):
        self.update_constraints()
        for widget in self.widgets:
            widget.update()

    def draw(self):
        for widget in self.widgets:
            widget.draw()

    def rect(self, position_one, position_two, fill):
        self.parent_widget.rect(position_one, position_two, fill)

    def bind(self, function, press: str = "up", number: int = 1):
        self.parent_widget.bind_w(self, function, press, number)

    def bind_w(self, widget, function, press, number):
        self.parent_widget.bind_w(widget, function, press, number)

    def is_in(self, coord):
        wh = self.get_width() / 2
        hh = self.get_height() / 2
        for widget in self.widgets:
            if widget.is_in(coord):
                return False
        if (self.get_x() - wh <= coord[0] <= self.get_x() + wh) and (
                self.get_y() - hh <= coord[1] <= self.get_y() + hh):
            return True

    def get_mouse_pos(self):
        return self.parent_widget.get_mouse_pos()

    def get_surface(self):
        return self.parent_widget.get_surface()

    def get_pressed(self):
        return self.parent_widget.get_pressed()

    def text(self, position, text, size=40, color=Color("black"), font=STANDARD_FONT):
        self.parent_widget.text(position, text, size, color, font)

    def get_size_of_text(self, text, size=40, font=STANDARD_FONT):
        return self.parent_widget.get_size_of_text(text, size, font)

    def multiple_line_text(self, position, text: str, width, size=40, line_distance=2, bound="LEFT", color=Color("black"),
                           font=STANDARD_FONT):
        self.parent_widget.multiple_line_text(position, text, width, size, line_distance, bound, color, font)


class Label(Widget):
    def __init__(self, parent_widget, color: Color, text: str = "", rounded_corner_radius=0, status=True,
                 hover_color: Color = None, font=STANDARD_FONT, text_anchor="CC", text_color=Color("black"),
                 text_size=40):
        Widget.__init__(self, parent_widget)

        self._text = text
        self.font = font
        self.text_anchor = text_anchor
        self.text_color = text_color
        self.text_size = text_size

        self.rounded_corner_radius = rounded_corner_radius
        self.status = status

        self.u_color = color
        self.hover_color = color
        if hover_color:
            self.hover_color = hover_color
        self.color = self.u_color

    def draw(self):
        if self.rounded_corner_radius:

            self.parent_widget.rect((self.pos[0] - self.width / 2 + self.rounded_corner_radius,
                                     self.pos[1] - self.height / 2 + self.rounded_corner_radius),
                                    (self.pos[0] + self.width / 2 - self.rounded_corner_radius,
                                     self.pos[1] + self.height / 2 - self.rounded_corner_radius), fill=self.color)
            # four arcs
            pos_ol = (self.pos[0] - self.width / 2 + self.rounded_corner_radius,
                      self.pos[1] - self.height / 2 + self.rounded_corner_radius)
            pos_or = (self.pos[0] + self.width / 2 - self.rounded_corner_radius,
                      self.pos[1] - self.height / 2 + self.rounded_corner_radius)
            pos_ul = (self.pos[0] - self.width / 2 + self.rounded_corner_radius,
                      self.pos[1] + self.height / 2 - self.rounded_corner_radius)
            pos_ur = (self.pos[0] + self.width / 2 - self.rounded_corner_radius,
                      self.pos[1] + self.height / 2 - self.rounded_corner_radius)

            self.parent_widget.oval(pos_ol, self.rounded_corner_radius, fill=self.color)
            self.parent_widget.oval(pos_or, self.rounded_corner_radius, fill=self.color)
            self.parent_widget.oval(pos_ul, self.rounded_corner_radius, fill=self.color)
            self.parent_widget.oval(pos_ur, self.rounded_corner_radius, fill=self.color)

            # four rects
            pos1_l = (self.pos[0] - self.width / 2, self.pos[1] - self.height / 2 + self.rounded_corner_radius)
            pos2_l = (self.pos[0] - self.width / 2 + self.rounded_corner_radius,
                      self.pos[1] + self.height / 2 - self.rounded_corner_radius)
            pos1_o = (self.pos[0] - self.width / 2 + self.rounded_corner_radius, self.pos[1] - self.height / 2)
            pos2_o = (self.pos[0] + self.width / 2 - self.rounded_corner_radius,
                      self.pos[1] - self.height / 2 + self.rounded_corner_radius + 1)
            pos1_r = (self.pos[0] + self.width / 2, self.pos[1] - self.height / 2 + self.rounded_corner_radius)
            pos2_r = (self.pos[0] + self.width / 2 - self.rounded_corner_radius,
                      self.pos[1] + self.height / 2 - self.rounded_corner_radius)
            pos1_u = (self.pos[0] - self.width / 2 + self.rounded_corner_radius, self.pos[1] + self.height / 2)
            pos2_u = (self.pos[0] + self.width / 2 - self.rounded_corner_radius,
                      self.pos[1] + self.height / 2 - self.rounded_corner_radius)

            self.parent_widget.rect(pos1_l, pos2_l, fill=self.color)
            self.parent_widget.rect(pos1_o, pos2_o, fill=self.color)
            self.parent_widget.rect(pos1_r, pos2_r, fill=self.color)
            self.parent_widget.rect(pos1_u, pos2_u, fill=self.color)
        else:
            self.parent_widget.rect((self.pos[0] - self.width / 2,
                                     self.pos[1] - self.height / 2),
                                    (self.pos[0] + self.width / 2,
                                     self.pos[1] + self.height / 2), fill=self.color)

        # surface = self.font.render(self.text, (0, 0, 0))[0]
        # print("blit", self.text)
        # self.sf.blit(surface, (0, 0))
        # pos = (self.pos[0] - self.width / 2, self.pos[1] - self.height / 2)

        pos = [0, 0]
        w, h = self.get_size_of_text(self._text, self.text_size, self.font)

        if self._text:
            if self.text_anchor[1] == "W":
                pos[0] = self.pos[0] - self.width / 2
            elif self.text_anchor[1] == "C":
                pos[0] = self.pos[0] - w / 2
            elif self.text_anchor[1] == "E":
                pos[0] = self.pos[0] - w + self.width / 2

            if self.text_anchor[0] == "N":
                pos[1] = self.pos[1] - self.height / 2
            elif self.text_anchor[0] == "C":
                pos[1] = self.pos[1] - h / 2
            elif self.text_anchor[0] == "S":
                pos[1] = self.pos[1] - h + self.height / 2

        self.text(pos, self._text, self.text_size, self.text_color, self.font)

        Widget.draw(self)

    def update(self):
        Widget.update(self)
        if self.is_in(self.parent_widget.get_mouse_pos()):
            self.color = self.hover_color
        else:
            self.color = self.u_color


class Scrollbar(Widget):
    def __init__(self, parent_widget, slider_color=Color("black"), background_color=Color("white"),
                 value_range: tuple = (1, 100), standard_value=50, orientation=VERTICAL, text_size=40, viscosity=0.5):
        Widget.__init__(self, parent_widget)
        self.slider_color = slider_color
        self.background_color = background_color
        self.range = value_range
        self.standard_value = standard_value
        self.value_range = value_range
        self.orientation = orientation
        self.standard_percent = 100 * (
                (self.standard_value - self.value_range[0]) / (self.value_range[1] - self.value_range[0]))
        self.standard_percent = 0
        self.text_size = text_size

        self.viscosity = viscosity
        self.slider_rail = None
        self.slider_label = None
        self.background_label = None
        self.selected = False
        self.should_percent = -1
        self.is_percent = -1

    def select(self, *args):
        self.selected = True

    def _get(self, percent):
        return (self.value_range[1] - self.value_range[0]) * (percent / 100) + self.value_range[0]

    def get_percent(self):
        percent = None
        if self.orientation == VERTICAL:
            m = self.slider_rail.pos[1] - self.slider_rail.height / 2
            percent = 100 * ((self.slider_label.get_y() - m) / (self.slider_rail.pos[1] +
                                                                self.slider_rail.height / 2 - m))
            percent = max(min(percent, 100), 0)
        elif self.orientation == HORIZONTAL:
            m = self.slider_rail.pos[0] - self.slider_rail.width / 2
            percent = 100 * ((self.slider_label.get_x() - m) / (self.slider_rail.pos[0] +
                                                                self.slider_rail.width / 2 - m))
            percent = max(min(percent, 100), 0)
        return percent

    def get(self):
        return self._get(self.get_percent())

    def set(self, value):
        offset = self.value_range[0]
        percent = 100 * ((value - offset) / (self.value_range[1] - offset))
        if self.orientation == VERTICAL:
            self.slider_label.set_y_constraint(ProportionConstraint(percent))

        elif self.orientation == HORIZONTAL:
            self.slider_label.set_x_constraint(ProportionConstraint(percent))
        self.update()
        self.slider_label._text = str(round(self._get(percent)))
        self.is_percent = percent
        self.should_percent = percent

    def set_constraints(self, x_constraint=None, y_constraint=None, width_constraint=None, height_constraint=None):
        Widget.set_constraints(self, x_constraint, y_constraint, width_constraint, height_constraint)

        self.background_label = Label(self, self.background_color)
        self.background_label.set_constraints(PixelConstraint(0),
                                              PixelConstraint(0),
                                              ProportionConstraint(100),
                                              ProportionConstraint(100))

        self.slider_rail = Widget(self)
        if self.orientation == VERTICAL:
            self.slider_rail.set_constraints(PixelConstraint(0),
                                             CenterConstraint(),
                                             ProportionConstraint(100), )
        elif self.orientation == HORIZONTAL:
            self.slider_rail.set_constraints(CenterConstraint(),
                                             PixelConstraint(0),
                                             None,
                                             ProportionConstraint(100))

        self.slider_label = Label(self.slider_rail, self.slider_color, text_color=Color("white"),
                                  text_size=self.text_size, text=str(self.standard_value),
                                  hover_color=Color((40, 40, 40)), text_anchor="CC")

        self.slider_label.set_x_constraint(CenterConstraint())
        self.slider_label.set_y_constraint(CenterConstraint())

        if self.orientation == VERTICAL:
            self.slider_label.set_height_constraint(AspectConstraint(1))
            self.slider_label.set_width_constraint(ProportionConstraint(100))
            # self.slider_label.set_y_constraint(ProportionConstraint(self.standard_percent))

            m = self.background_label.get_y() - self.background_label.get_height() / 2

            percent = 100 * ((self.background_label.get_y() +
                              self.background_label.get_height() / 2 - self.slider_label.get_height() - m) /
                             (self.background_label.get_y() + self.background_label.get_height() / 2 - m))

            self.slider_rail.set_height_constraint(ProportionConstraint(percent))

        elif self.orientation == HORIZONTAL:
            self.slider_label.set_width_constraint(AspectConstraint(1))
            self.slider_label.set_height_constraint(ProportionConstraint(100))
            # self.slider_label.set_x_constraint(ProportionConstraint(self.standard_percent))

            m = self.background_label.get_x() - self.background_label.get_width() / 2

            percent = 100 * ((self.background_label.get_x() +
                              self.background_label.get_width() / 2 - self.slider_label.get_width() - m) /
                             (self.background_label.get_x() + self.background_label.get_width() / 2 - m))

            self.slider_rail.set_width_constraint(ProportionConstraint(percent))

        self.slider_label.bind(self.select, press="down")
        self.background_label.bind(self.select, press="down")
        self.set(self.standard_value)

    def update(self):
        Widget.update(self)
        if self.selected:
            pos = self.parent_widget.get_mouse_pos()
            percent = None
            if self.orientation == VERTICAL:
                m = self.slider_rail.pos[1] - self.slider_rail.height / 2
                percent = 100 * ((pos[1] - m) / (self.slider_rail.pos[1] + self.slider_rail.height / 2 - m))
                percent = max(min(percent, 100), 0)
                self.should_percent = percent
                # self.slider_label.set_y_constraint(ProportionConstraint(percent))
            elif self.orientation == HORIZONTAL:
                m = self.slider_rail.pos[0] - self.slider_rail.width / 2
                percent = 100 * ((pos[0] - m) / (self.slider_rail.pos[0] + self.slider_rail.width / 2 - m))
                percent = max(min(percent, 100), 0)
                self.should_percent = percent
                # self.slider_label.set_x_constraint(ProportionConstraint(percent))
            if not self.get_pressed()[0]:
                self.selected = False

        self.slider_label._text = str(round(self._get(self.is_percent)))

        if self.orientation == VERTICAL:
            m = self.background_label.get_y() - self.background_label.get_height() / 2

            percent = 100 * ((self.background_label.get_y() +
                              self.background_label.get_height() / 2 - self.slider_label.get_height() - m) /
                             (self.background_label.get_y() + self.background_label.get_height() / 2 - m))

            self.slider_rail.set_height_constraint(ProportionConstraint(percent))

        elif self.orientation == HORIZONTAL:
            m = self.background_label.get_x() - self.background_label.get_width() / 2

            percent = 100 * ((self.background_label.get_x() +
                              self.background_label.get_width() / 2 - self.slider_label.get_width() - m) /
                             (self.background_label.get_x() + self.background_label.get_width() / 2 - m))

            self.slider_rail.set_width_constraint(ProportionConstraint(percent))

        if self.is_percent != self.should_percent:
            self.is_percent += (self.should_percent - self.is_percent) * self.viscosity

            if self.orientation == VERTICAL:
                self.slider_label.set_y_constraint(ProportionConstraint(self.is_percent))
            elif self.orientation == HORIZONTAL:
                self.slider_label.set_x_constraint(ProportionConstraint(self.is_percent))


class TextLabel(Widget):
    def __init__(self, parent_widget, text, line_distance=-10, font=STANDARD_FONT, text_bound="CENTER", color=Color("black"), text_size=40,
                 background_color=Color("white")):
        Widget.__init__(self, parent_widget)
        self._text = text
        self.font = font
        self.color = color
        self.text_size = text_size
        self.line_distance = line_distance
        self.text_bound = text_bound

        self.background_color = background_color
        self.background_label = Label(self, color=self.background_color)
        self.background_label.set_constraints(PixelConstraint(0),
                                              PixelConstraint(0),
                                              ProportionConstraint(100),
                                              ProportionConstraint(100))

    def draw(self):
        Widget.draw(self)
        pos = (self.pos[0]-self.width/2, self.pos[1]-self.height/2)
        self.multiple_line_text(pos, self._text, self.width, self.text_size, self.line_distance, self.text_bound, self.color,
                                self.font)

import pygame as pg
import pygame.freetype
import copy

pygame.freetype.init()
STANDARD_FONT = pg.freetype.Font("Helvetica-Bold-Font.ttf", 40)
# STANDARD_FONT = pg.font.SysFont("comicsansms", 72)


file = open("colors.txt")
colors = []

file.readline()
for line in file.readlines():
    num, name = line.split("\t\t")
    name = name.replace("\n", "")
    num = num.replace("     ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ")
    if num.startswith(" "):
        num = "".join(list(num)[1:len(num)])
    col = ([int(rgb) for rgb in num.split(" ")], name)
    colors.append(col)
else:
    print("Colors successfully loaded!")


class Color:
    def __init__(self, color, alpha=255):
        if type(color) == str:
            for color_tupel in colors:
                if color_tupel[1] == color:
                    r = color_tupel[0][0]
                    g = color_tupel[0][1]
                    b = color_tupel[0][2]
                    self.color = (r, g, b)
        elif type(color) == tuple:
            self.color = (color[0], color[1], color[2], alpha)

    def __mul__(self, other):
        return Color((self.color[0] * other, self.color[1] * other, self.color[2] * other))

    def get(self):
        return self.color


class Window:
    widgets = []

    def __init__(self):
        self.config = {"loop": [],
                       "width": 800,
                       "height": 450,
                       "resizable": True,
                       "title": "Window",
                       "background": Color("dark grey"),
                       "events": {"quit": [self.quit]},
                       "mouse": {"down": {1: [], 2: [], 3: [], 4: [], 5: []},
                                 "up": {1: [], 2: [], 3: [], 4: [], 5: []}}
                       }

        self.width = self.config["width"]
        self.height = self.config["height"]
        self.pos = (0, 0)
        self.root = pg.display.set_mode((self.config["width"], self.config["height"]))
        self.surface = pg.Surface((self.config["width"], self.config["height"]))
        self.mainloop_thread = None
        self.title("Window")
        self.sf = self.surface
        self.clock = pg.time.Clock()
        self.mouse_pos = (1, 1)
        self.i = 0
        self.force = False

    @staticmethod
    def quit():
        pg.quit()

    def size(self, width, height):
        if self.config["resizable"]:
            self.root = pg.display.set_mode((width, height), pg.RESIZABLE)
        else:
            self.root = pg.display.set_mode((width, height))
        self.config.update({"width": width, "height": height})

    def title(self, title: str):
        pg.display.set_caption(title)
        self.config["title"] = title

    def add_loop(self, function):
        self.config["loop"].append(function)

    def get_config(self):
        return self.config

    def configure(self, config: map):
        self.config.update(config)

    def flip(self):
        self.root.blit(self.surface, (0, 0))
        pg.display.flip()

    def update(self):
        self.i += 1
        self.clock.tick()
        if (self.i % 1) == 0:
            self.mouse_pos = pg.mouse.get_pos()
        self.title(str(self.clock.get_fps()))
        self.width = self.config["width"]
        self.height = self.config["height"]
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                [func() for func in self.config["events"]["quit"]]
                return
            if event.type == pg.VIDEORESIZE:
                self.size(event.w, event.h)
                self.surface = pg.Surface((self.config["width"], self.config["height"]))
                self.surface.fill(self.config["background"].get())
                for widget in self.widgets:
                    widget.update(videoresize=True)
                    widget.draw(force=True)
                    # self.flip()
                    print("force")
            if event.type == pg.MOUSEBUTTONDOWN:
                [func(event.pos) for func in self.config["mouse"]["down"][event.button]]

            if event.type == pg.MOUSEBUTTONUP:
                [func(event.pos) for func in self.config["mouse"]["up"][event.button]]
        print("iter")
        if self.force:
            self.surface = pg.Surface((self.config["width"], self.config["height"]))
            self.surface.fill(self.config["background"].get())
            print("DELDELDELDELDELDELDELDELDELDLELDELDELDEL")
        [func() for func in self.config["loop"]]
        for widget in self.widgets:
            widget.update()
            if widget.redraw or self.force:
                widget.draw(force=self.force)
        self.flip()
        self.force = False

    def mainloop(self):
        while True:
            self.update()

    def get_mouse_pos(self):
        return self.mouse_pos

    def oval(self, position: tuple, r_y, r_x=-1, fill=Color("green")):
        fill = fill.get()

        if r_x == -1:
            r_x = r_y
        tl_x = position[0] - r_x
        tl_y = position[1] - r_y

        w = 2 * r_x
        h = 2 * r_y

        pg.draw.ellipse(self.surface, fill[0:3], pg.Rect(tl_x, tl_y, w, h))
        self.root.blit(self.surface, (0, 0))

    def rect(self, position_1: tuple, position_2: tuple, fill, width: int = 0):
        fill = fill.get()

        w = position_2[0] - position_1[0]
        h = position_2[1] - position_1[1]
        pg.draw.rect(self.surface, fill[0:3], pg.Rect(position_1[0], position_1[1], w, h), width)

        # self.root.blit(self.surface, (0, 0))

    def get_x(self):
        return self.width / 2

    def get_y(self):
        return self.height / 2

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def bind_w(self, widget, function, press: str = "up", number: int = 0):
        self.config["mouse"][press][number].append(lambda coord: function(coord) if widget.is_in(coord) else None)

    def get_surface(self):
        return self.surface

    def get_pressed(self):
        return pygame.mouse.get_pressed()

    def text(self, position, text, size=40, color=Color("black"), font=STANDARD_FONT):
        surface = font.render(text, color.get(), size=size)[0]
        self.surface.blit(surface, position)

    @staticmethod
    def get_size_of_text(text, size=40, font=STANDARD_FONT):
        surface = font.render(text, (0, 0, 0), size=size)[0]
        return surface.get_width(), surface.get_height()

    def multiple_line_text(self, position, text: str, width, size=40, line_distance=2, bound="LEFT",
                           color=Color("black"),
                           font=STANDARD_FONT):
        y = position[1]
        paragraphs = text.split("\n")
        paragraphs_grouped = []
        for paragraph in paragraphs:
            words = paragraph.split(" ")
            words_grouped = []
            temp_text = []
            for word in words:
                temp_temp_text = copy.deepcopy(temp_text)
                temp_temp_text.append(word)
                if self.get_size_of_text(" ".join(temp_temp_text), size=size, font=font)[0] <= width:
                    temp_text.append(word)
                else:
                    # render
                    surface = font.render(" ".join(temp_text), color.get(), size=size)[0]
                    pos = (0, 0)
                    if bound == "LEFT":
                        pos = (position[0], y)
                    elif bound == "CENTER":
                        pos = (position[0] + (width - surface.get_width()) * .5, y)
                    elif bound == "RIGHT":
                        pos = (position[0] + width - surface.get_width(), y)
                    self.surface.blit(surface, pos)
                    temp_text = [word]
                    y += line_distance + font.get_sized_height(size)
            paragraphs_grouped.append(words_grouped)
            y += line_distance + font.get_sized_height(size)

    def set_redraw(self, draw=True, force_redraw=False):
        self.force = self.force or force_redraw
        print("Gtogtogto DELDELDEL", draw, force_redraw)

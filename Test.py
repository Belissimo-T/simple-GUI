from Widgets import *
from Main import *
from Layout import *

root = Window()
root.title("Test")
root.config["background"] = Color((220, 220, 220))

frame = Label(root, Color("dark grey"))
frame.set_constraints(PixelConstraint(10),
                      CenterConstraint(),
                      ProportionConstraint(20),
                      PixelConstraint(10))

button1 = Label(frame, color=Color("yellow"), hover_color=Color("orange"), text="Left")
button1.set_constraints(CenterConstraint(),
                        PixelConstraint(10),
                        PixelConstraint(10),
                        ProportionConstraint(10))

button2 = Label(frame, color=Color("yellow"), hover_color=Color("orange"), text="Center")
button2.set_constraints(CenterConstraint(),
                        DistanceConstraint(button1, ConstantConstraint(10)),
                        PixelConstraint(10),
                        ProportionConstraint(10))

button3 = Label(frame, color=Color("yellow"), hover_color=Color("orange"), text="Right")
button3.set_constraints(CenterConstraint(),
                        DistanceConstraint(button2, ConstantConstraint(10)),
                        PixelConstraint(10),
                        ProportionConstraint(10))

checkbox = Checkbox(frame, "ES GEHT")
checkbox.set_constraints(CenterConstraint(),
                         DistanceConstraint(button3, ConstantConstraint(10)),
                         PixelConstraint(10),
                         ProportionConstraint(5))

frame2 = Label(root, Color("dark grey"))
frame2.set_constraints(PixelConstraint(-10),
                       CenterConstraint(),
                       ProportionConstraint(20),
                       PixelConstraint(10))

slider = Scrollbar(frame2, orientation=HORIZONTAL, standard_value=59, text_size=20, value_range=(0, 100))
slider.set_constraints(CenterConstraint(),
                       PixelConstraint(10),
                       ProportionConstraint(90),
                       ConstantConstraint(20))

slider2 = Scrollbar(frame2, orientation=VERTICAL, standard_value=50)
slider2.set_constraints(ProportionConstraint(30),
                        PixelConstraint(50),
                        ProportionConstraint(20),
                        ProportionConstraint(65))

slider3 = Scrollbar(frame2, orientation=VERTICAL, standard_value=0, value_range=(-120, 120))
slider3.set_constraints(ProportionConstraint(70),
                        PixelConstraint(50),
                        ProportionConstraint(20),
                        ProportionConstraint(65))

viscosity_label = Label(frame2, color=Color("yellow"), text="0.1", hover_color=Color("orange"))
viscosity_label.set_constraints(CenterConstraint(),
                                ProportionConstraint(85),
                                ProportionConstraint(90),
                                ProportionConstraint(8))

slider_label = Label(frame2, color=Color("orange"), hover_color=Color("yellow"))
slider_label.set_constraints(CenterConstraint(),
                             ProportionConstraint(95),
                             ProportionConstraint(90),
                             ProportionConstraint(8))

text = """
Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. 
At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. 
Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."""

text_label = TextLabel(root, text, text_size=40, background_color=Color("red"))
text_label.set_constraints(CenterConstraint(),
                           PixelConstraint(10),
                           ProportionConstraint(40),
                           PixelConstraint(10))


def set_text_bound(t):
    global text_label
    text_label.text_bound = t


frame.bind(lambda coord: print("LOL"))
button1.bind(lambda coord: set_text_bound("LEFT"))
button2.bind(lambda coord: set_text_bound("CENTER"))
button3.bind(lambda coord: set_text_bound("RIGHT"))

mode = True
amount = 2

while 1:
    root.update()
    slider_label._text = str(round(slider2.get(), 4))

    v = slider3.get()
    text_label.line_distance = v
    viscosity_label._text = str(round(v, 4))

    text_label.set_width_constraint(ProportionConstraint(slider.get()))
    text_label.text_size = slider2.get()

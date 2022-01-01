from numpy import random
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line


class PixelatedGrid(Widget):
    background = ListProperty([0, 0, 0, 1])
    grid_color = ListProperty([47/255, 79/255, 79/255, 1])
    activated_color = ListProperty([0, 1, 0, 1])
    cell_length = NumericProperty(10)
    activated_cells = ObjectProperty(set())

    def __init__(self, **kwargs):
        super(PixelatedGrid, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.bind(activated_cells=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas.before:
            Color(*self.background)
            Rectangle(pos = [0,0], size=[self.width, self.height])
        with self.canvas:
            Color(*self.grid_color)
            for x in range(0, self.width, self.cell_length):
                Line(points=[x, 0, x, self.height], width=1)
            for y in range(self.height, 0, -self.cell_length):
                Line(points=[0, y, self.width, y], width=1)

            Color(*self.activated_color)
            for x, y in self.activated_cells:
                Rectangle(pos=[x*self.cell_length, self.height-y*self.cell_length], size=[self.cell_length, self.cell_length])

    def visible_width(self):
        return self.width//self.cell_length

    def visible_height(self):
        return self.height//self.cell_length


class PixelatedGridApp(App):

    def activate_random(self, *args):
        num_cells=100
        self.container.activated_cells = set([(random.randint(0, self.container.visible_width()), random.randint(0, self.container.visible_height())) for _ in range(0,num_cells)])

    def build(self):
        self.container = PixelatedGrid()
        Clock.schedule_interval(self.activate_random, .5)
        return self.container


if __name__ == "__main__":
    PixelatedGridApp().run()

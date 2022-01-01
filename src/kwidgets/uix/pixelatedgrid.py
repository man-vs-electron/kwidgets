from numpy import random
from kivy import app
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, NumericProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

Builder.load_string("""
<Cell>:
    canvas.before:
        Color:
            rgb: self.background
        Rectangle:
            size: self.size
            pos: self.pos
    
    
<SquareCell>:
    canvas:
        Color:
            rgb: self.foreground
        Rectangle:
            size: self.size[0]-self.border_width*2, self.size[1]-self.border_width*2
            pos: self.pos[0]+self.border_width, self.pos[1]+self.border_width   
            
<CircleCell>:
    canvas:
        Color:
            rgb: self.foreground
        Ellipse:
            size: min(self.size[0], self.size[1])-self.border_width*2, min(self.size[0], self.size[1])-self.border_width*2
            pos: self.pos[0]+self.border_width, self.pos[1]+self.border_width                    
""")


class Cell(Widget):
    background = ListProperty([0, 0, 0])
    border_width = NumericProperty(1)

    def set_foreground(self, rgb):
        self.foreground = rgb

class SquareCell(Cell):
    foreground = ListProperty([0, 0, 1])

class CircleCell(Cell):
    foreground = ListProperty([0, 0, 1])

class PixelatedGrid(Widget):
    cols: int = 100
    rows: int = 100
    padding: int = 1

    def __init__(self, **kwargs):
        super(PixelatedGrid, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        cell_width = int(self.width/self.cols)
        cell_height = int(self.height/self.rows)
        self.canvas.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos = [0,0], size=[self.width, self.height])
        with self.canvas:
            Color(0, 1, 0, 1)
            for x in range(0, self.rows):
                for y in range(0, self.cols):
                    Rectangle(pos = [cell_width*x+self.padding, cell_height*y + self.padding],
                              size=[cell_width-(self.padding*2), cell_height-(self.padding*2)])


class PixelatedGridApp(App):
    def build(self):
        return PixelatedGrid()


class CellTestApp(App):
    square_cells = None
    circle_cells = None

    def random_green(self, *kwargs):
        self.square_cells[random.randint(0, 50*25)].set_foreground([0, 1, 0])

    def build(self):
        container = Builder.load_string('''
BoxLayout:
    orientation: 'horizontal'
    GridLayout:
        id: squares
        cols: 50
    GridLayout:
        id: circles
        cols: 50    
''')
        self.square_cells = [SquareCell() for _ in range(0,50*25)]
        self.square_cells[1].foreground = [0, 1, 0]
        [container.ids.squares.add_widget(x) for x in self.square_cells]

        self.circle_cells = [CircleCell() for _ in range(0,50*25)]
        self.circle_cells[1].foreground = [0, 1, 0]
        [container.ids.circles.add_widget(x) for x in self.circle_cells]
        self.container = container

        Clock.schedule_interval(self.random_green, 1)

        return container


if __name__ == "__main__":
    PixelatedGridApp().run()

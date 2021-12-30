from kivy import app
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, NumericProperty
from kivy.app import App

Builder.load_string("""
<Cell>:
    canvas.before:
        Color:
            rgba: self.background
        Rectangle:
            size: self.size
            pos: self.pos
    
    
<SquareCell>:
    canvas:
        Color:
            rgba: self.foreground
        Rectangle:
            size: self.size[0]-self.border_width*2, self.size[1]-self.border_width*2
            pos: self.pos[0]+self.border_width, self.pos[1]+self.border_width   
            
<CircleCell>:
    canvas:
        Color:
            rgba: self.foreground
        Ellipse:
            size: min(self.size[0], self.size[1])-self.border_width*2, min(self.size[0], self.size[1])-self.border_width*2
            pos: self.pos[0]+self.border_width, self.pos[1]+self.border_width                    
        Color:
            rgba: self.background
        Line:
            width: 2
            ellipse: self.pos[0]+self.border_width+5, self.pos[1]+self.border_width+5, min(self.size[0], self.size[1])-(self.border_width*2+10), min(self.size[0], self.size[1])-(self.border_width*2+10), 180, 90                 
""")


class Cell(Widget):
    background = ListProperty([.5, .5, .5, 1])
    border_width = NumericProperty(5)


class SquareCell(Cell):
    foreground = ListProperty([0, 0, 1, .75])

class CircleCell(Cell):
    foreground = ListProperty([0, 0, 1, .75])


class PixelatedGridApp(App):
    def build(self):
        container = Builder.load_string('''
BoxLayout:
    orientation: 'horizontal'
    GridLayout:
        id: squares
        cols: 2    
    GridLayout:
        id: circles
        cols: 2    
''')
        square_cells = [SquareCell() for _ in range(0,4)]
        square_cells[1].foreground = [0, 1, 0, 1]
        [container.ids.squares.add_widget(x) for x in square_cells]

        circle_cells = [CircleCell() for _ in range(0,4)]
        circle_cells[1].foreground = [0, 1, 0, 1]
        [container.ids.circles.add_widget(x) for x in circle_cells]

        return container


if __name__ == "__main__":
    PixelatedGridApp().run()

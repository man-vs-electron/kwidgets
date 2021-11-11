from typing import Union, Iterable, Tuple
import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.lang.builder import Builder
from kwidgets.dataviz.math import BoxPlotData

Builder.load_string("""
<BoxPlot>:
    on_height: self._computeAB()
    canvas:
        # draw a couple invisible lines to make the _axis_range property bound to the redraw
        Color:
            rgba: 0, 0, 0, 0
        Line:
            points: self.width-1, self.y+self._bp+self._op+(self._a*self._axis_range[0]+self._b), self.width+1, self.y+self._bp+self._op+(self._a*self._axis_range[0]+self._b)
        Line:
            points: self.width-1, self.y+self._bp+self._op+(self._a*self._axis_range[1]+self._b), self.width+1, self.y+self._bp+self._op+(self._a*self._axis_range[1]+self._b)
        Color:
            rgba: self._boxcolor
        Line:
            # box around 1st and 3rd quartiles
            rectangle: self.x+self._bp, self.y+self._bp+self._op+(self._a*self._bpd.q1+self._b), self.width - 2*self._bp, self._a*(self._bpd.q3-self._bpd.q1)
        Line:
            # the median
            points: self.x+self._bp, self.y+self._bp+self._op+(self._a*self._bpd.median+self._b), self.x+self.width-self._bp, self.y+self._bp+self._op+(self._a*self._bpd.median+self._b) 
        Line:
            # the vertical line below the box
            points: self.x+self.width/2, self.y+self._bp+self._op+(self._a*self._bpd.q1+self._b), self.x+self.width/2, self.y+self._bp+self._op+(self._a*self._bpd.min+self._b)
        Line:
            # the horizontal line indicating 1st quartile minus 1.5 IQR
            points: self.x+self._bp,  self.y+self._bp+self._op+(self._a*self._bpd.min+self._b), self.x+self.width-self._bp,  self.y+self._bp+self._op+(self._a*self._bpd.min+self._b) 
        Line:
            # the vertical line above the box
            points: self.x+self.width/2, self.y+self._bp+self._op+(self._a*self._bpd.q3+self._b), self.x+self.width/2, self.y+self._bp+self._op+(self._a*self._bpd.max+self._b)
        Line:
            # the horizontal line indicating the 3rd quartile plut 1.5 IQR
            points: self.x+self._bp,  self.y+self._bp+self._op+(self._a*self._bpd.max+self._b), self.x+self.width-self._bp,  self.y+self._bp+self._op+(self._a*self._bpd.max+self._b) 
        Line:
            # plot large outliers as extra line
            points: self.x+self._bp+(0.5*(1.0-self.outlier_proportion_large)*(self.width-2*self._bp)), self.y+self._bp+2.*self._op+(self._a*self._bpd.max+self._b), self.x+self.width-self._bp-(0.5*(1.0-self.outlier_proportion_large)*(self.width-2*self._bp)), self.y+self._bp+2.*self._op+(self._a*self._bpd.max+self._b)
        Line:
            # plot small outliers as extra line
            points: self.x+self._bp+(0.5*(1.0-self.outlier_proportion_small)*(self.width-2*self._bp)), self.y+self._bp+(self._a*self._bpd.min+self._b), self.x+self.width-self._bp-(0.5*(1.0-self.outlier_proportion_small)*(self.width-2*self._bp)), self.y+self._bp+(self._a*self._bpd.min+self._b)
        # The marker indicating some plotted value independent of the boxplot
        Color:
            rgba: self._markercolor
        Line:
            width: self._markerwidth
            points: self.x+self._bp,  self.y+self._bp+self._op+(self._a*self._markervalue+self._b), self.x+self.width-self._bp, self.y+self._bp+self._op+(self._a*self._markervalue+self._b)
""")


class BoxPlot(Widget):
    _bpd = ObjectProperty(BoxPlotData(list(np.arange(0, 1.0, 0.1))))
    _a = NumericProperty(0)
    _b = NumericProperty(1)
    _axis_range = ListProperty([0,1])
    _auto_axis = BooleanProperty(True)

    _boxcolor = ListProperty([0, 1, 0, 1])
    _bp = NumericProperty(15)
    _op = NumericProperty(15)

    _markercolor = ListProperty([1, 0, 0, 0])
    _markervalue = NumericProperty(0)
    _markerwidth = NumericProperty(2)

    def _computeAB(self):
        self._a = float((self.height-2.*(self._bp+self._op))/(self._axis_range[1]-self._axis_range[0]))
        self._b = float(-self._a*self._axis_range[0])

    @property
    def outlier_proportion_large(self):
        return min(10, len([x for x in self._bpd.outliers if x>self._bpd.max]))/10.

    @property
    def outlier_proportion_small(self):
        return min(10, len([x for x in self._bpd.outliers if x<self._bpd.min]))/10.

    @property
    def boxpadding(self):
        return self._bp

    @boxpadding.setter
    def boxpadding(self, value):
        self._bp = value

    @property
    def outlierpadding(self):
        return self._op

    @outlierpadding.setter
    def outlierpadding(self, value):
        self._op = value

    @property
    def boxcolor(self):
        return self._boxcolor

    @boxcolor.setter
    def boxcolor(self, value):
        self._boxcolor = value

    @property
    def markercolor(self):
        return self._markercolor

    @markercolor.setter
    def markercolor(self, value):
        self._markercolor = value

    @property
    def markercolor(self):
        return self._markercolor

    @markercolor.setter
    def markercolor(self, value):
        self._markercolor = value

    @property
    def markervalue(self):
        return self._markervalue

    @markervalue.setter
    def markervalue(self, value):
        self._markervalue = value

    @property
    def data(self):
        return self._bpd

    @data.setter
    def data(self, data: Union[BoxPlotData, Iterable[Union[float, int]]]):
        if isinstance(data, BoxPlotData):
            bpd = data
        else:
            bpd = BoxPlotData(data)
        self._bpd = bpd
        if self._auto_axis:
            self._axis_range = (bpd.min, bpd.max)
        self._computeAB()

    @property
    def axis_range(self):
        return self._axis_range

    @axis_range.setter
    def axis_range(self, minmax: Tuple[float, float]):
        self._axis_range = minmax
        self._auto_axis = False
        self._computeAB()


class BoxPlotApp(App):
    def build(self):
        container = Builder.load_string('''
#:import np numpy
BoxLayout:
    orientation: 'horizontal'
    BoxLayout
        orientation: 'vertical'
        Label:
            size_hint: 1, .1
            text: "Random Normal"
        BoxPlot:
            boxcolor: 1,0,0,1
            data: np.random.normal(0, 2, 500)
    BoxLayout
        orientation: 'vertical'
        Label:
            size_hint: 1, .1
            text: "Random Uniform"
        BoxPlot:
            data: np.random.uniform(0, 10, 500)
            markercolor: .7, .7, 1, 1
            markervalue: 1.5
    BoxLayout
        orientation: 'vertical'
        Label:
            size_hint: 1, .1
            text: "Random Gamma"
        BoxPlot:
            data: np.random.gamma(2, 2, 500)
    BoxLayout
        orientation: 'vertical'
        Label:
            size_hint: 1, .1
            halign: 'center'
            text: "Random Normal\\n(fixed range)"
        BoxPlot:
            boxcolor: 1,0,0,1
            data: np.random.normal(3, 2.5, 500)
            axis_range: -10, 10
    BoxLayout
        orientation: 'vertical'
        Label:
            size_hint: 1, .1
            halign: 'center'
            text: "Random Normal\\n(fixed range)"
        BoxPlot:
            boxcolor: 1,0,0,1
            data: np.random.normal(-1, 3, 500)
            axis_range: -10, 10
        
''')
        return container

if __name__ == "__main__":
    BoxPlotApp().run()

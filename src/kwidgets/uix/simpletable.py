""" A simple table for data

This class takes a dictionary
and displays the keys and values within a single LabeledValue object.
"""

from typing import Dict, List
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import DictProperty, StringProperty, ListProperty
from kwidgets.uix.labeledvalue import LabeledValue


class SimpleTable(LabeledValue):
    _data = DictProperty({})
    _keys = ListProperty(None)
    _itemformat = StringProperty(None)

    def _update(self):
        if len(self._data)==0:
            self.key = ""
            self.value = ""
        else:
            thekeys = self._keys if self._keys is not None else self._data.keys()
            self.key = "\n".join(thekeys)
            if self._itemformat is None:
                self.value = "\n".join([str(self._data[k]) for k in thekeys])
            else:
                self._value = "\n".join([self._itemformat % self._data[k] for k in thekeys])

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, d: Dict):
        self._data = d
        self._update()
        
    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, keys: List[str]):
        self._keys = keys
        self._update()

    @property
    def itemformat(self):
        return self._itemformat

    @itemformat.setter
    def itemformat(self, format: str):
        self._itemformat = format
        self._update()


class SimpleTableApp(App):
    def build(self):
        return Builder.load_string('''
SimpleTable:
    data: {'apple':1, 'banana':2, 'carrot':3}
    keys: 'apple', 'carrot'
    itemformat: "%d"
    value_halign: 'left'
    box_color: 1, 1, 0, 1
    key_size_hint_x: 0.5
''')

if __name__ == "__main__":
    SimpleTableApp().run()
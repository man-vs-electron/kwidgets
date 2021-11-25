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
    """ A simple table that uses a single LabeledValue object.

    Puts all keys and all labels together.  Relevant properties
    (in addition to LabeledValue properties) are:

    * data - a dictionary mapping from the keys to the values to display in the table
    * keys - which keys from the table to display.  If not specified, use all the keys
    * itemformat - a format to apply to each value.

    Note that other properties from LabeledValue (box_width, box_color, value_halign,
    key_halign) are relevant for this class as well.

    """
    _data = DictProperty({})
    _keys = ListProperty(None)
    _itemformat = StringProperty(None)

    def _update(self):
        """ Create the key an value string that will be displayed

        """
        if len(self._data) != 0:
            thekeys = self._keys if self._keys is not None else self._data.keys()
            self.key = "\n".join(thekeys)
            if self._itemformat is None:
                self.value = "\n".join([str(self._data[k] if k in self._data else "??") for k in thekeys])
            else:
                self._value = "\n".join([(self._itemformat % self._data[k]) if k in self._data else "??" for k in thekeys])
        else:
            self.key = ""
            self.value = ""

    @property
    def data(self):
        """ A dictionary of keys and values to display

        :return:
        """
        return self._data

    @data.setter
    def data(self, d: Dict):
        """ A dictionary of keys and values to display

        :param d:
        """
        self._data = d
        self._update()
        
    @property
    def keys(self):
        """ An optional list of keys from the main dictionary to display

        :return:
        """
        return self._keys

    @keys.setter
    def keys(self, keys: List[str]):
        """ A dictionary of keys and values to display.

        :param keys:
        """
        self._keys = keys
        self._update()

    @property
    def itemformat(self):
        """ A format string that will be applied to each value.

        :return:
        """
        return self._itemformat

    @itemformat.setter
    def itemformat(self, format: str):
        """ A format string that will be applied to each value.

        :param format:
        """
        self._itemformat = format
        self._update()


class SimpleTableApp(App):
    def build(self):
        return Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    SimpleTable:
        data: {'apple':1, 'banana':2, 'carrot':3}
        keys: 'apple', 'carrot', "invalid key"
        itemformat: "%d"
        value_halign: 'left'
        box_color: 1, 1, 0, 1
        key_size_hint_x: 0.5
    SimpleTable:
        data: {'car':'red', 'truck':'black'}
''')

if __name__ == "__main__":
    SimpleTableApp().run()
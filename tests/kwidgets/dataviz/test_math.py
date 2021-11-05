from kwidgets.dataviz.math import BoxPlotData
import numpy as np


def test_compute_boxplot():
    data = list(range(0,100))+[1000]
    ans = BoxPlotData(data)
    assert ans.median == np.median(data)
    assert ans.q1 == np.percentile(data, [25])[0]
    assert ans.q3 == np.percentile(data, [75])[0]
    assert ans.min == 0
    assert ans.max == 99
    assert ans.outliers == [1000]

from kwidgets.utils import intersperse, to_xy


def test_intersperse():
    a = "abc"
    b = "def"
    assert ''.join(list(intersperse([a,b]))) == "adbecf"

    a = [1, 2, 3]
    b = [4, 5, 6]
    assert list(intersperse([a, b])) == [1, 4, 2, 5, 3, 6]

    a = [1, 2]
    b = [4, 5, 6]
    assert list(intersperse([a, b])) == [1,4,2,5]

    a = [1,2,3,7,8,9,10]
    b = [4,5,6]
    assert list(intersperse([a,b])) == [1,4,2,5,3,6,7]


def test_to_xy():
    X,y = to_xy([1, 2, 3, 4, 5, 6])
    assert X == [1, 3, 5]
    assert y == [2, 4, 6]
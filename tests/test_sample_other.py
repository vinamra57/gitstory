# content of test_sample.py
def square(x: int | float):
    return x**2


class TestSquare:
    def test_square_1(self):
        assert square(3) == 9

    def test_square_2(self):
        assert square(4) == 16

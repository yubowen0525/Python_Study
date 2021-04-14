from math import hypot


class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __mul__(self, scalar: int):
        if type(scalar) == int:
            return Vector(self.x * scalar, self.y * scalar)
        else:
            return Vector(self.x * scalar.x, self.y * scalar.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)


if __name__ == '__main__':
    pass

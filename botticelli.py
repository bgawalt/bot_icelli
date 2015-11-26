import theanets
from scipy import ndimage
from scipy import misc
import sys
import numpy


class BottiImg(object):
    def __init__(self):
        self._img = None
        self._rows = None
        self._cols = None
        self._x = None
        self._y = None

    @property
    def is_valid(self):
        if self._img is None or self._rows is None or self._cols is None \
          or self._x is None or self._y is None:
            print 'theres a none'
            return False
        if len(self._img.shape) == 3:
            (ir, ic, iz) = self._img.shape
        else:
            (ir, ic) = self._img.shape
            iz = 1
        if ir != self._rows or ic != self._cols:
            print 'ir or ic'
            return False
        (xm, xn) = self._x.shape
        (ym, yn) = self._y.shape
        if xm != ym:
            print 'xm != ym'
            return False
        if xm != self._rows*self._cols:
            print 'xm rows * cols'
            return False
        if xn != 2:
            print 'xn != 2', xn
            return False
        if yn != 3 and yn != 1:
            print 'yn = ', yn
            return False
        if yn != iz:
            print 'yn iz', yn, iz
            return False
        return True

    def load_image(self, filename, monochrome=False):
        if monochrome:
            self._img = ndimage.imread(filename, flatten=True)
        else:
            self._img = ndimage.imread(filename, mode='RGB')
        misc.imsave('img/mario_out.png', self._img)
        if len(self._img.shape) == 3:
            (r, c, z) = self._img.shape
        else:
            (r, c) = self._img.shape
            z = 1
        self._rows = r
        self._cols = c
        self._x = numpy.zeros((r*c, 2))
        self._y = numpy.zeros((r*c, z))
        print '_x.shape', self._x.shape
        print '_y.shape', self._y.shape
        arr_row = 0
        for ri in xrange(r):
            for ci in xrange(c):
                self._x[arr_row, 0] = ri
                self._x[arr_row, 1] = ci
                for zi in xrange(z):
                    self._y[arr_row, zi] = self._img[ri, ci, zi]


def main():
    img = BottiImg()
    img.load_image("img/mario.png")
    print img.is_valid


if __name__ == "__main__":
    main()

import datetime
import math
import numpy
import pickle

import imageio.v3 as iio

from sklearn import tree

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
            print('theres a none')
            return False
        if len(self._img.shape) == 3:
            (ir, ic, iz) = self._img.shape
        else:
            (ir, ic) = self._img.shape
            iz = 1
        if ir != self._rows or ic != self._cols:
            print('ir or ic')
            return False
        (xm, xn) = self._x.shape
        (ym, yn) = self._y.shape
        if xm != ym:
            print('xm != ym')
            return False
        if xm != self._rows*self._cols:
            print('xm rows * cols')
            return False
        if xn != 2:
            print('xn != 2', xn)
            return False
        if yn != 3 and yn != 1:
            print('yn = ', yn)
            return False
        if yn != iz:
            print('yn iz', yn, iz)
            return False
        return True

    def load_image(self, filename, monochrome=False):
        if monochrome:
            self._img = iio.imread(filename, flatten=True)
        else:
            self._img = iio.imread(filename, mode='RGB')
            print(self._img.mean())
        # TODO: wtf
        iio.imwrite('img/mario_out.png', self._img, extension='.png')
        if len(self._img.shape) == 3:
            (r, c, z) = self._img.shape
        else:
            (r, c) = self._img.shape
            z = 1
        self._rows = r
        self._cols = c
        self._x = numpy.zeros((r*c, 2))
        self._y = numpy.zeros((r*c, z))
        print('_x.shape', self._x.shape)
        print('_y.shape', self._y.shape)
        arr_row = 0
        for ri in range(r):
            for ci in range(c):
                self._x[arr_row, 0] = ri
                self._x[arr_row, 1] = ci
                for zi in range(z):
                    self._y[arr_row, zi] = self._img[ri, ci, zi]
                arr_row += 1
        temp = numpy.hstack((self._x, self._y))
        numpy.random.shuffle(temp)
        self._x = temp[:, :2]
        self._y = temp[:, 2:]


def clip(x, lower=0, upper=255):
    if x < lower:
        return 0
    elif x > upper:
        return upper
    return x


def generate_circles(n=400):
    img = numpy.zeros((n, n, 3), dtype=numpy.uint8)
    for r in range(n):
        for c in range(n):
            dist_origin = math.sqrt(r*r + c*c)
            dist_opposite = math.sqrt((n - r)*(n - r) + (n - c)*(n - c))
            dist_upper = math.sqrt((n - r)*(n - r) + c*c)
            raw_red = int(455*(n - dist_origin)/n)
            raw_blue = int(455*(n - dist_opposite)/n)
            raw_green = int(455*(n - dist_upper)/n)
            img[r, c, 0] = clip(raw_red)
            img[r, c, 1] = clip(raw_green)
            img[r, c, 2] = clip(raw_blue)
    iio.imwrite("circles.png", img, extension='.png')


def arrays_to_image(x, y, filename):
    if x.shape[0] != y.shape[0]:
        raise ValueError("Must have same number of rows in x as in y")

    num_layers = y.shape[1]
    if num_layers != 1 and num_layers != 3:
        raise ValueError("Image must have one or three layers")

    if x.shape[1] != 2:
        raise ValueError("Argument x must have exactly 2 columns")
    x_min = x.min(axis=0)
    if x_min[0] < 0 or x_min[1] < 0:
        raise ValueError("All values in x must be non negative")

    x_max = x.max(axis=0)
    r = int(x_max[0]) + 1
    c = int(x_max[1]) + 1
    if num_layers == 1:
        img = y.mean()*numpy.ones((r, c))
        for i in range(x.shape[0]):
            ri = int(x[i, 0])
            ci = int(x[i, 1])
            img[ri, ci] = y[i][0]
    else:
        img = numpy.zeros((r, c, num_layers), dtype=numpy.uint8)
        y_mean = y.mean(axis=0)
        img[:, :, 0] = y_mean[0]
        img[:, :, 1] = y_mean[1]
        img[:, :, 2] = y_mean[2]
        for i in range(x.shape[0]):
            ri = int(x[i, 0])
            ci = int(x[i, 1])
            img[ri, ci, 0] = clip(int(y[i, 0]))
            img[ri, ci, 1] = clip(int(y[i, 1]))
            img[ri, ci, 2] = clip(int(y[i, 2]))
    iio.imwrite(filename, img)


# TODO: Move to new file
def decision_tree_image(img, depth):
    red_t = tree.DecisionTreeRegressor(max_depth=depth)
    blue_t = tree.DecisionTreeRegressor(max_depth=depth)
    green_t = tree.DecisionTreeRegressor(max_depth=depth)
    red_t.fit(img._x, img._y[:, 0])
    blue_t.fit(img._x, img._y[:, 1])
    green_t.fit(img._x, img._y[:, 2])
    red_pred = red_t.predict(img._x)
    blue_pred = blue_t.predict(img._x)
    green_pred = green_t.predict(img._x)
    pred = numpy.zeros(img._y.shape)
    pred[:, 0] = red_pred
    pred[:, 1] = blue_pred
    pred[:, 2] = green_pred
    arrays_to_image(img._x, pred, "results/couple_tree_"+str(depth)+".bmp")
    with open("couple_tree_"+str(depth)+".pkl", 'wb') as outfile:
        pickle.dump((red_t, blue_t, green_t), outfile)


def main():
    img = BottiImg()
    # TODO: Make this a command line flag
    pic = "couple"
    img.load_image("img/"+pic+".png")

    last = datetime.datetime.now()
    for depth in (2, 4, 8, 12, 16):
        decision_tree_image(img, depth)


if __name__ == "__main__":
    main()

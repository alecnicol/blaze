from __future__ import absolute_import, division, print_function

import numpy as np
import h5py

import pytest

from blaze import compute
from blaze.expr import Symbol
from datashape import discover
from blaze.utils import tmpfile


def eq(a, b):
    return (a == b).all()


x = np.arange(50, dtype='f4').reshape((10, 5))

@pytest.yield_fixture
def data():
    with tmpfile('.h5') as filename:
        f = h5py.File(filename)
        d = f.create_dataset('/x', shape=(10, 5), dtype='f4', fillvalue=0.0)
        d[:] = x
        yield d
        f.close()

s = Symbol('s', discover(x))


def test_slicing(data):
    for idx in [0, 1, (0, 1), slice(1, 3), (0, slice(1, 5, 2))]:
        assert eq(compute(s[idx], data), x[idx])
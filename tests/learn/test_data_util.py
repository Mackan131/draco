import os

import pandas as pd
import pytest

from draco.learn.data_util import (load_data, pickle_path, run_in_parallel,
                                   tasks_to_vec)
from draco.spec import Task


def test_load_data():
    if not os.path.isfile(pickle_path):
        pytest.skip('Test needs data file')

    train, test = load_data()

    size = len(train) + len(test)
    assert len(train) - int(0.7 * size) <= 1
    assert len(test) - int(0.3 * size) <= 1

def square(x):
    return x**2

def batch_square(d):
    _, xs = d

    s = pd.Series()
    for i, x in xs:
        s = s.append(pd.Series([x**2], index=[i]))
    return s

def test_run_in_parallel():
    a = range(100)
    expected = list(map(square, a))
    actual = run_in_parallel(batch_square, list(enumerate(a)))

    assert list(actual.values) == expected

def test_tasks_to_vec():
    task = Task.from_vegalite({
        'data': {
            'values': [{'a': 10}, {'a': 42}]
        },
        'mark': 'point',
        'encoding': {
            'x': {'field': 'a', 'type': 'quantitative'}
        }
    })

    vecs = tasks_to_vec([task, task, task])
    assert len(vecs) == 3

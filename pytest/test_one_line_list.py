import one_line_list

import pytest


@pytest.fixture()
def initial_list(request):
    lst = one_line_list.OneLineList()
    lst.append(1)
    lst.append(2)
    lst.append(3)
    lst.append(4)
    return lst


def test_check_pop(initial_list):
    assert initial_list.pop() == 4


def test_append(initial_list):
    initial_list.append(100500)
    assert initial_list.pop() == 100500


#@pytest.mark.usefixtures("initial_list")
def test_get_list(initial_list):
    res = []
    res.append(initial_list.pop())
    res.append(initial_list.pop())
    res.append(initial_list.pop())
    res.append(initial_list.pop())
    assert res == [4,3,2,1]


@pytest.mark.parametrize("x", [-1,2])
@pytest.mark.parametrize("y", [-10,11])
def test_cross_params(initial_list, x, y):
    initial_list.append(x)
    initial_list.append(y)

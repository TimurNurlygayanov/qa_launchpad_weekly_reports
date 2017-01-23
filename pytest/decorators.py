def decorator1(p="R"):

    def test_(my_func):
        def wrapper(*arg, **args):
            print "AAAA"
            print p
            my_func(*arg, **args)
            print "BBBB"

        return wrapper

    return test_


@decorator1("test")
def test_function(a="t"):
    print a


test_function("TEST")

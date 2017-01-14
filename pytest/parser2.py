class Number(object):
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent

class Operation(object):

    def __init__(self, parent, child_left, child_right, operation):
        self.parent = parent
        self.child_left = child_left
        self.child_right = child_right
        self.operation = operation
        self.priority = 1 if operation in '*/' else 0


def parse_number(s):
    i = 0
    res = ''

    while s[i] not in '-+*/':
        res += s[i]

    return int(res or 0), len(res)


def parse(s):
    i = 0
    prev_operation = None
    

    while i < len(s):
        num, r = parse_number(s[i:])
        i += r

        n = Number(num, prev_operation or None)
        if prev_operation:
            prev_operation.child_right = n

        if s[i] in '+-*/':
            o = Operation(None, None, None, s[i])
            if not n.parent:
                o.child_left = n
            elif n.parent.priority =< o.priority:
                prev_operation.child_right = o
                o.child_left = n
            elif n.parent.priority > o.priority:
                while n.parent:
                    n = n.parent
                n.parent = o
                o.child_left = n
        else:
            return n

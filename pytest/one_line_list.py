class Element(object):
    previous_element = None
    value = None

    def __init__(self, x=None):
        self.value = x


class OneLineList(object):
    last = Element()
    
    def append(self, x):
        k = Element(x)
        self.last, k.previous_element = k, self.last

    def pop(self):
        result = self.last
        if result.previous_element:
            self.last = result.previous_element
            return result.value
        else:
            raise Exception("List Is Empty!")


def reverse_element(e, w=None):
    if e.previous_element:
        r = e.previous_element
        e.previous_element = w or Element()
        root = reverse_element(r, e)
        return root
    return w
        
       
def reverse_list(lst):
    lst.last = reverse_element(lst.last)
    

t = OneLineList()

## Print default list:
t.append(1)
t.append(2)
t.append(3)
t.append(4)
print t.pop()
print t.pop()
print t.pop()
print t.pop()

print "*"*20

## Print reversed list:
t.append(1)
t.append(2)
t.append(3)
t.append(4)
reverse_list(t)
t.append(5)
print t.pop()
print t.pop()
print t.pop()
print t.pop()
print t.pop()

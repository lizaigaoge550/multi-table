class A():
    def __init__(self,name1,name2):
        self.name1 = name1
        self.name2 = name2

    def __str__(self):
        return self.name1
    def __repr__(self):
        return self.name2


class B():
    def __init__(self):
        self.a = 1
        self.b = 2

    def fun(self):
        def add():
            self.a += 1
        add()
        return self.a


b = B()
print(b.fun())

a = A('a1','a2')
print(str(a))
print(repr(a))
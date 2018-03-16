class Counter:
    class __Counter:
        def __init__(self):
            self._cnt = 0
        def __str__(self):
            return  str(self._cnt)

    instance = None

    def __init__(self):
        if not Counter.instance:
            Counter.instance =Counter.__Counter()
        #每次调用完了，自增1
        Counter.instance._cnt += 1

    @property
    def cnt(self):
        return Counter.instance._cnt


# c1 = Counter()
# print(c1.cnt)
#
# c2 = Counter()
# print(c2.cnt)


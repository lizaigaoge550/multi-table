

def add(a, l):
    if type(a) == list:
        for i in range(len(a)):
            if a[i] not in l: l.append(a[i])
    else:
        if a != None and a not in l: l.append(a)
    return l


def union(a, b):
    l = []
    # 检查类型
    l = add(a, l)
    l = add(b, l)
    if len(l) == 1: return l[0]
    if l == []: return None
    return l


def extract_option(v):
    opt = ""
    for i in range(len(v)):
        if v[i] != '(':
            opt += v[i]
        else:
            break
    return opt

def get_opt(value):
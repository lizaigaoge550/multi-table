from map_class.major_foreign import Map

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

def is_map(a,b):
    #看看a.cols 和 b.cols 有没有对应关系
    m = Map()
    if type(a.c_name) == str and type(b.c_name) == str:
        if m.is_map(a.c_name,b.c_name):
            return a.c_name,b.c_name
        return "",""
    elif type(a.c_name) == str and type(b.c_name) == list:
        for b_name in b.c_name:
            if m.is_map(a.c_name,b_name):
                return a.c_name,b_name
        return "",""
    elif type(a.c_name) == list and type(b.c_name) == list:
        for a_name in a.c_name:
            for b_name in b.c_name:
                if m.is_map(a_name,b_name):
                    return a_name,b_name
        return "",""
    else:
        raise Exception("映射不科学.....a:{0},b{1}".format(a.c_name,b.c_name))

def is_modify_allowed(p1,p2):
    #p1 和 p2 是 c,S,filter
    if p1.t_name == p2.t_name:
        return None,None,p1.c_name != p2.c_name
    else:
        #看看能不能join
        key1, key2 = is_map(p1.T,p2.T)
        if key1 != "":
            return key1,key2,True
        else:
            return "","",False

def is_project_allowed(p1,p2):
    #先得到c和t
    c = p1 if p1.value != 'T' else p2
    t = p1 if p1.value == 'T' else p2
    if c.t_name == t.t_name:
        return "","",c.c_name in t.c_name
    else:
        key1, key2 = is_map(c.T,t)
        if key1 != "":
            return key1,key2,True
        else:
            return "","",False




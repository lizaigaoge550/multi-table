from map_class.major_foreign import Map
from symbol_class.class_file import cClass,StarClass
from operation_class.count_op import Count
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
    #print(m.major_foreign)
    if type(a.c_name) == str and type(b.c_name) == str:
        if m.is_map(a.c_name,b.c_name):
            return a.c_name,b.c_name
        return "",""
    elif type(a.c_name) == str and type(b.c_name) == list:
        for b_name in b.c_name:
            if m.is_map(a.c_name,b_name):
                return a.c_name,b_name
        return "",""

    elif type(a.c_name) == list and type(b.c_name) == str:
        for a_name in a.c_name:
            if m.is_map(a_name,b.c_name):
                return a_name,b.c_name
        return "",""


    elif type(a.c_name) == list and type(b.c_name) == list:
        for a_name in a.c_name:
            for b_name in b.c_name:
                if m.is_map(a_name,b_name):
                    return a_name,b_name
        return "",""
    else:
        raise Exception("映射不科学.....a_name: {0},b_name: {1},a: {2},b: {3}".format(a.c_name,b.c_name,a,b))


def is_contained(p1,p2):
    if type(p1) == list:
        if p2 in p1:
            return True
    elif type(p2) == list:
        if p1 in p2:
            return True
    return p1 == p2



def is_modify_allowed(p1,p2):
    #p1 和 p2 是 c,S,filter
    #print('p1.t_name:{0}, p2.t_name:{1}'.format(p1.t_name,p2.t_name))
    if is_contained(p1.t_name,p2.t_name):
        return None,None,p1.c_name != p2.c_name
    else:
        #看看能不能join
        if p1.value == 'c' or p2.value == 'c':
            if type(p1) == cClass and type(p2) == cClass:
                key1, key2 = is_map(p1.T,p2.T)
            elif type(p1) == cClass:
                key1, key2 = is_map(p1.T,p2)
            elif type(p2) == cClass:
                key1, key2 = is_map(p1,p2.T)
            else:
                key1, key2 = is_map(p1,p2)
        elif p1.value == 'S':
            key1,key2 = is_map(p1,p2.T)
        else:
            key1,key2 = is_map(p1.T,p2)
        if key1 != "":
            #return p1.t_name+'.'+key1.split('.')[-1],p2.t_name + '.'+key2.split('.')[-1],True
            return key1, key2, True
        else:
            return "","",False

def is_project_allowed(p1,p2):
    #先得到c和t
    c = p1 if p1.value != 'T' else p2
    t = p1 if p1.value == 'T' else p2
    if c.t_name == t.t_name:
        return "","",c.c_name in t.c_name
    else:
        try:
            key1, key2 = is_map(c.T,t)
        except:
            key1, key2 = is_map(c,t)
        if key1 != "":
            #注意这个的key2应该是 t.t_name+'.'+col_name
            key2 = t.t_name + '.' + key2.split('.')[-1]
            return key1,key2,True
        else:
            return "","",False

def get_t_name(t1,t2):
    new_t_name = []
    if type(t1) == list and type(t2) == list:
        new_t_name.extend(t1)
        new_t_name.extend(t2)
    elif type(t1) == list:
        new_t_name.extend(t1)
        new_t_name.append(t2)
    elif type(t2) == list:
        new_t_name.append(t1)
        new_t_name.extend(t2)
    else:
        new_t_name.append(t1)
        new_t_name.append(t2)
    return new_t_name


def find_join_t(tlist,k1,k2):
    k1_t_name = k1.split('.')[0]
    k2_t_name = k2.split('.')[0]
    #先看下tlist的类型
    if type(tlist) == list:
        #找到要join的t, 看以哪张表做join
        for t in tlist:
            if t.t_name == k1_t_name or t.t_name == k2_t_name:
                return t
    else:
        return tlist

# def s_to_t_get_c_name(s):
#     #看下s的参数类型
#     if s.param_1.value == 'c' and s.param_2.value == 'c':
#         return s.param_1.c_name if s.param_1.c_type == 'string' else s.param_2.c_name
#     elif (s.param_1.value == 'c' and s.param_2.value == 'A') or (s.param_2.value == 'c' and s.param_1.value == 'A'):
#         return s.param_1.c_name if s.param_1.value == 'c' else s.param_2.c_name
#     elif (s.param_1.value == 'c' and s.param_2.value == 'T') or (s.param_2.value == 'c' and s.param_1.value == 'T'):
#         return s.param_1.c_name if s.param_1.value == 'T' else s.param_2.c_name
#     else:

def extract_c(cs,mode=""):
    s = ""
    for c in cs:
        if type(c) == cClass:
            #print(c.c_name.split('.'))
            s += c.t_name + '.' + c.c_name.split('.')[-1]+','
        if type(c) == Count:
            if mode == 'order':
                s += c.t_name+'.cnt,'
            else:
                s += 'count(%s) as cnt,'%(c.param.t_name+'.'+c.param.c_name.split('.')[-1])
        if type(c) == StarClass:
            s += str(c)+','
    return s[:-1]


def extract_where(wheres):
    s = ""
    for index in range(len(wheres)):
        s += wheres[index].key.description + '=' + wheres[index].value.description.split('.')[-1]
        if index < len(wheres)-1:
            s +=' and '
    return s


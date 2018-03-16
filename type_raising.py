#coding=utf-8
from node import Node
from operation_class.raising import Raising
from operation_class.c_raising import C_Raising
from operation_class.count_op import Count
from operation_class.filter import In
from symbol_class.class_file import cClass
import re

def create(optype, child, is_bottom):
    #optype 有两种情况 1 ""  c -- > T . 2 Raising S -- > T. 3 Rasing c --> A
    if optype == 'Raising':
        return Raising(child.val)
    if optype == "C_Raising":
        return C_Raising(child.val)
    if is_bottom == True and optype == 'count':
        return Count(child.val)
    if is_bottom == True and optype == 'Filter':
        #生成一个c
        c = cClass(child.val.t_name,child.val.c_name,child.val.c_type,child.val.t_name+'.'+child.val.c_name)
        return In(c,child.val)

def extract_opt(opt):
    if '(' not in opt:
        return ""
    #去除括号
    new_opt = ''
    for i in range(len(opt)):
        if opt[i] != '(':
            new_opt += opt[i]
        else:
            return new_opt

def extract_paramter(func):
    if '(' not in func:return None
    arg = re.search('\(.*\)', func).group()[1:-1].split(',')
    return arg

def format_(l):
    args = [extract_paramter(i) for i in l.split('.')]
    a = []
    for i in range(len(args)):
        if args[i] != None: a.extend(args[i])

    if len(a) == 1: return a[0]
    else:return ",".join(a)


def type_rasing(gDict, nodelist, start, end, key, is_bottom):
    values = []
    for node in nodelist:
        values.append(node.val.value)
    for value in values:
        #有lambda 和 没有lambda
        if value == None:
            print(key)
            raise Exception('type raising is not valid:{0}'.format(value))
        if 'lambda' not in value: #(c-- > F=count(c))
            for rhs, lhs, func in gDict:
                if rhs == value:
                    index = values.index(rhs)
                    parent = create(func, nodelist[index],is_bottom)
                    if parent == None: continue
                    values.append(lhs)
                    node = Node(nodelist[index], None, parent, start, end)
                    nodelist.append(node)
        else:
            continue
    return nodelist

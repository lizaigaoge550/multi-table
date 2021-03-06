#coding=utf-8
import re
from node import Node
from operation_class.modify import Modify
from symbol_class.class_file import SClass
from combine import composition
from map_class.major_foreign import Map
import copy

mapclass = Map()

def get_arg_express(node):
    assert 'lambda' in node.value
    arg, express = node.value.split(".")
    arg = re.search('\(.*\)', arg).group()[1:-1].split(',')
    return arg, express


def extract_paramter(func):
    if '(' not in func: return None
    arg = re.search('\(.*\)', func).group()[1:-1].split(',')
    return arg


def assignment(root,param,string=True):
    if param.t_name not in root.t_name:
        root.t_name.append(param.t_name)
    if string == True:
        if param.c_name not in root.c_name:
            if type(param.c_name) == list:
                root.c_name.extend(param.c_name)
                root.c_type.extend(param.c_type)
            else:
                root.c_name.append(param.c_name)
                root.c_type.append(param.c_type)

def fill_arg(root,param):
    for i in range(len(root.param_list)):
        if type(root) == SClass:
            if param.value == 'T':
                #是T 只可能是第一个参数
                if param.c_name == root.key1.key.split('.')[-1] and root.key1.is_pad == False:
                    root.key1.is_pad = True
                    root.param_1 = param
                    root.param_list[0] = root.param_1
                    assignment(root,param)
                    return True
                # elif  param.c_name == root.key2.key.split('.')[-1] and root.key2.is_pad == False:
                #     root.key2.is_pad = True
                #     root.param_2 = param
                #     root.param_list[1] = root.param_2
                #     assignment(root,param)
                #     return True
                return False

            #这个是string类型
            if param.description == root.key1.key and root.key1.is_pad == False:
                root.key1.is_pad = True
                root.param_1 = param
                root.param_list[0] = root.param_1
                assignment(root,param)
                return True

            #这个是number 类型
            elif param.description == root.key2.key and root.key2.is_pad == False:
                root.key2.is_pad = True
                root.param_2 = param
                root.param_list[1] = root.param_2
                assignment(root,param,string=False)
                return True
            return False
        elif type(root.param_list[i]) == Modify:
            return fill_arg(root.param_list[i], param)

def get_exp(exp,r_p):
    if len(r_p) == 0:
        return exp
    return 'lambda(%s).%s'%(r_p[0],exp)


def cut_parameters(cls, param, exp, r_p):
    res = fill_arg(cls,param)
    if res == True:
        cls.value = get_exp(exp,r_p)
        return cls
    elif res == None:
        raise Exception("cur parameter no SClass:{0}".format(cls))
    else:
        #说明没有填上
        return None


def paramter_composition(node1, node2, option):  # 只会是lambda(,,).S 和 Filter --> S
    assert option == 'modify',("paramter_composition is not correct. {0}".format(option))
    # 这个不用check条件 就是填变量
    cls = Modify(node1,node2)
    return cls


def residue_parameter(require,padded):
    i = require.index(padded)
    del require[i]
    return require

def bottom_up_parser(node1, node2, gDict, key):
    g = []
    if node1.val.value == None or node2.val.value == None:
        print(key)
        raise ("node1 or node2 is None")
    if 'lambda' in node1.val.value or 'lambda' in node2.val.value:
        if 'lambda' in node1.val.value and 'lambda' in node2.val.value:
            return g
        else:
            if 'lambda' in node1.val.value:  #lambda(c,c).S, lambda(c,A).S, lambda(c,T).S
                arg, exp = get_arg_express(node1.val)  # [c,c],S or [c]
                if node2.val.value in arg:
                    r_p = residue_parameter(arg,node2.val.value)
                    gene = cut_parameters(node1.val, node2.val, exp, r_p)
                    if gene:
                        gene = copy.deepcopy(gene)
                        node = Node(node1, node2, gene, node1.start, node2.end)
                        g += [node]
                # else:
                #     nodes = []
                #     #prefix = node1.val.value.split('.')[0]
                #     for (rhs, lhs, func) in gDict:
                #         rhs = rhs.split(',')
                #         if len(rhs) == 2:
                #             if (exp == rhs[0] and node2.val.value == rhs[1]) or (exp == rhs[1] and node2.val.value == rhs[0]):
                #                 gene = paramter_composition(node1.val, node2.val, func)
                #                 node = Node(node1, node2, gene, node1.start, node2.end)
                #                 nodes.append(node)
                #
                #     if nodes != []:
                #         g += nodes
            else:
                arg, exp = get_arg_express(node2.val)  # [N], S
                if node1.val.value in arg:
                    r_p = residue_parameter(arg, node1.val.value)
                    gene = cut_parameters(node2.val, node1.val, exp, r_p)
                    if gene:
                        gene = copy.deepcopy(gene)
                        node = Node(node1, node2, gene, node1.start, node2.end)
                        g += [node]
                # else:
                #     nodes = []
                #     #prefix = node2.val.value.split('.')[0]
                #     for (rhs, lhs, func) in gDict:
                #         rhs = rhs.split(',')
                #         if len(rhs) == 2:
                #             if (exp == rhs[0] and node1.val.value == rhs[1]) or (exp == rhs[1] and node1.val.value == rhs[0]):
                #                 #lambda 在 node2上，所以得先把node2上的lambda去掉
                #                 gene = paramter_composition(node2.val, node1.val, func)
                #                 node = Node(node1, node2, gene, node1.start, node2.end)
                #                 nodes.append(node)
                #     if nodes != []:
                #         g += nodes

    else:
        nodes = []
        for (rhs, lhs, func) in gDict:
            rhs = rhs.split(',')
            if len(rhs) == 2:
                if (node1.val.value == rhs[0] and node2.val.value == rhs[1]) or (node1.val.value == rhs[1] and node2.val.value == rhs[0]):
                    gene = composition(node1.val, node2.val, func)
                    if gene == None: continue
                    node = Node(node1, node2, gene, node1.start, node2.end)
                    nodes.append(node)
        if nodes != []:
            g += nodes
    return g
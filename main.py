#coding=utf-8
from parser_algorithm import bottom_up_parser
from grammar import Grammar
from node import Node
from type_raising import type_rasing
from read_data_2 import read_data
from expression import generate_data

def self_generate_self(leaf,gDict,key,i,j,is_bottom):
    #对这个leaf做type-raising
    nodelist = [Node(None,None,leaf,i,j)]
    return type_rasing(gDict,nodelist,i,j,key,is_bottom)



def get_non_terminal_logical(dic, start, end, gDict, key):
    assert end > start
    for p in range(start,end):
        if len(dic[start][p]) > 0 and len(dic[p+1][end]) > 0:
            #遍历dic[i][p] 和 dic[p+1][j] 中的每个元素
            for i in range(len(dic[start][p])):
                for j in range(len(dic[p+1][end])):
                    g = bottom_up_parser(dic[start][p][i], dic[p+1][end][j], gDict,key)
                    #遍历下看看又没有能type-raising的
                    gg = []
                    for g_index in range(len(g)):
                        new_g = self_generate_self(g[g_index].val, gDict, key, g[g_index].start, g[g_index].end, is_bottom=False)
                        gg.extend(new_g)
                    dic[start][end] += gg



def run(input,gDict,sql,abs):
    for key,v in input.items():
        for v_index in range(len(v)):
            n = len(v[v_index])
            dic = [[[] for _ in range(n)] for _ in range(n)]
            for length in range(n):  # length --> 0,1,2,3,4
                for i in range(n - length):
                    j = length + i
                    if i == j:
                        for k in range(len(v[v_index][i])):
                            g = self_generate_self(v[v_index][i][k][0], gDict,key,v[v_index][i][k][1],v[v_index][i][k][2],is_bottom=True)
                            dic[i][j] += g
                    else:
                        get_non_terminal_logical(dic, i, j, gDict,key)

            r = generate_data(dic, n-1, key, abs[key], sql[key])


if __name__ == '__main__':
    grammar = Grammar()
    grammar.read('grammar')
    gDict = grammar.grammar()
    input,sql,abs = read_data('测试数据post')
    run(input,gDict,sql,abs)
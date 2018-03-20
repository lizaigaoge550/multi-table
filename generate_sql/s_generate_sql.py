from symbol_class.class_file import cClass,StarClass,SClass
from operation_class.filter import In
from operation_class.generate_t import generate_Tclass
import copy
from common import find_join_t, is_contained
from operation_class.modify import Modify

#这个主要是s --> T

def find_sclass(s,sql):
    stack = [s]
    while len(stack):
        tmp_stack = []
        while len(stack):
            root = stack.pop()
            if type(root) == SClass:
                return root
            # 如果是filter，就在where中加入filter
            if root.param_1.value == 'Filter':
                sql.padding_where(root.param_1.param_1, root.param_1.param_2)
                if not is_contained(root.param_1.t_name,root.param_2.t_name):

                    sql.padding_join(find_join_t(root.param_1.T,root.key1, root.key2),root.key1, root.key2)

                tmp_stack.append(root.param_2)

            if root.param_2.value == 'Filter':
                sql.padding_where(root.param_2.param_1, root.param_2.param_2)
                if not is_contained(root.param_1.t_name,root.param_2.t_name):

                    sql.padding_join(find_join_t(root.param_2.T,root.key1, root.key2),root.key1, root.key2)

                tmp_stack.append(root.param_1)

        stack = tmp_stack


def s_generate_sql(s,sql):

    def tc(c,t_name):
        generate_cc_sql(s, sql)
        sql.padding_from(c.T)
        sql.padding_select(StarClass(t_name))
        return sql

    def ac(c,a):
        t = generate_Tclass(c, a)
        new_c = copy.copy(c)
        new_c.t_name = t.t_name
        new_a = copy.copy(a)
        new_a.t_name = t.t_name
        sql.padding_select(new_c)
        sql.padding_orderby(new_a)
        sql.padding_from(t)
        generate_ac_sql(c, sql)
        return sql

    #就遍历知道找到s
    if type(s) == Modify:
        s = find_sclass(s,sql)
    # s可以是 c,c|c,T|A,c 其中 c可以是modify，所以这个时候就要遍历
    # 1 首先判断两个参数是否同表，如果不同表就加入 join 和 on 的操作
    # 2 如果是T 或者是c(cClass, string)的话，T的话就select *  from T， c的话就select c_str from c_str.T
    # 3 如果是c_num 的话，
    if s.param_1.value == 'c' and s.param_2.value == 'c':
        sql = generate_cc_sql(s,sql)

    elif s.param_1.value == 'c' and s.param_2.value == 'T':
        sql = tc(s,s.param_2.t_name)

    elif s.param_1.value == 'T' and s.param_2.value == 'c':
        sql = tc(s,s.param_1.t_name)

    elif s.param_1.value == 'A' and s.param_2.value == 'c':
        #先生成一个T #这个A可以是A, Modify
        sql = ac(s.param_2,s.param_1)

    elif s.param_2.value == 'A' and s.param_1.value == 'c':
        sql = ac(s.param_1,s.param_2)

    return sql


def generate_ac_sql(c,sql):
    #这个只判断c 只填join 和 where
    # 如果两个参数不同表, join 和 on 操作
    if type(c) == cClass:
        return sql
    stack = [c]
    while len(stack):
        tmp_stack = []
        while len(stack):
            root = stack.pop()
            if not is_contained(root.param_1.t_name , root.param_2.t_name):
                if root.param_1.value != 'c' and root.param_1.c_type != 'string':
                    sql.padding_join(find_join_t(root.param_1.T, root.key1, root.key2),root.key1, root.key2)
            # 如果是filter，就在where中加入filter
            if root.param_1.value == 'Filter':
                sql.padding_where(root.param_1.param_1, root.param_1.param_2)
            if root.param_2.value == 'Filter':
                sql.padding_where(root.param_2.param_1, root.param_2.param_2)
            if type(root.param_1) != cClass and type(root.param_1) != In:
                tmp_stack.append(root.param_1)
            if type(root.param_2) != cClass and type(root.param_2) != In:
                tmp_stack.append(root.param_2)
        stack = tmp_stack
    return sql



def generate_cc_sql(s,sql):
    #如果两个参数不同表, join 和 on 操作
    stack = [s]
    while len(stack):
        tmp_stack = []
        while len(stack):
            root = stack.pop()
            if not is_contained(root.param_1.t_name , root.param_2.t_name):
                if root.param_1.value == 'T':
                    sql.padding_join(root.param_1, root.key1,root.key2)
                elif root.param_1.value != 'c' and root.param_1.c_type != 'string':
                    sql.padding_join(find_join_t(root.param_1.T,root.key1,root.key2), root.key1, root.key2)
                elif root.param_2.value != 'c' and root.param_2.type != 'string':
                    sql.padding_join(find_join_t(root.param_2.T, root.key1, root.key2),root.key1,root.key2)
            #如果是filter，就在where中加入filter
            if root.param_1.value == 'Filter':
                sql.padding_where(root.param_1.param_1, root.param_1.param_2)

            elif root.param_2.value == 'Filter':
                sql.padding_where(root.param_2.param_1, root.param_2.param_2)
            #如果是c_str 就在select中加入c
            if type(root.param_1) == cClass:
                if root.param_1.c_type == 'string':
                    sql.padding_select(root.param_1)
                    sql.padding_from(root.param_1.T)
                #不是cstring 就是cnumber
                else:
                    sql.padding_orderby(root.param_1)

            if type(root.param_2) == cClass:
                if root.param_2.c_type == 'string':
                    sql.padding_select(root.param_2)
                    sql.padding_from(root.param_2.T)
                else: sql.padding_orderby(root.param_2)

            if  type(root.param_1) != In and type(root.param_1) != cClass:
                tmp_stack.append(root.param_1)
            if  type(root.param_2) != In and type(root.param_2) != cClass:
                tmp_stack.append(root.param_2)
        stack = tmp_stack
    return sql



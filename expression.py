from operation_class.raising import Raising
from operation_class.c_raising import C_Raising
from symbol_class.class_file import cClass
from operation_class.count_op import Count
import pymysql
def postprocessing(dic,length):
    new_node = []
    for root in dic[0][length]:
        if 'lambda' in root.val.value:
            continue

        if root.val.value == 'T':
            new_node.append(root)

        elif root.val.value == 'c' or root.val.value == 'S':
            #这个操作是要type-raising
            if root.val.value == 'c':
                new_node.append(C_Raising(root))
            else:
                new_node.append(Raising(root))
    return new_node


def extract_c(cs):
    s = ""
    for c in cs:
        if type(c) == cClass:
            s += c.param.t_name+'.'+c.param.c_name + ','
        if type(c) == Count:
            s += 'count(%s) as cnt,'%(c.param.t_name+'.'+c.param.c_name)
    return s[:-1]


def get_mysql_drive():
    db = pymysql.connect('localhost', 'root', '123456789', 'geo')
    cursor = db.cursor()
    return cursor

def remove_outer_bracket(gene_sql):
    #先定位
    return gene_sql[1:gene_sql.rfind(')')]


def generate_sql_expression(dic,length):
    roots = postprocessing(dic, length)
    for root in roots:
        #现在每个sql都是一个T类型，都保存了sql字段
        gene_sql = str(root.sql)
        #去掉最外层的括号
        gene_sql = remove_outer_bracket(gene_sql)

        cursor = get_mysql_drive()
        cursor.execute(gene_sql)











# def generate_sql(sql):
#     res_str = ""
#     #取出sql, 主要是join的T和
#     if len(sql.Select) > 0:
#         res_str = 'select ' + extract_c(sql.Select)
#     elif len(sql.From) > 0:
#         res_str += ' from ' + str(sql.From[0].sql)
#     elif len(sql.Join) > 0:
#         res_str += ' join ' + str(sql.Join[0].t.sql)
#         res_str += ' on ' + str(sql.Join[0].condition)
#     elif len(sql.Groupby) > 0:
#         res_str += 'group by ' + extract_c(sql.Groupby)
#     elif len(sql.Orderby) > 0:
#         res_str += ' order by '+extract_c(sql.Orderby) + 'desc limit 1'
#     return res_str
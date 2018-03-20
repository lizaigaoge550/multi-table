from operation_class.raising import Raising
from operation_class.c_raising import C_Raising

import pymysql
import re
import os
from generate_sql.filter_generate_sql import Filter_to_t
def postprocessing(dic,length):
    new_node = []
    for root in dic[0][length]:
        #可能是Filter
        if root.val.value == 'Filter':
            new_node.append(Filter_to_t(root))
        if root.val.value == 'T':
            new_node.append(root)
    return new_node


def get_mysql_drive():
    db = pymysql.connect('localhost', 'root', '123456789', 'geo')
    cursor = db.cursor()
    return cursor

def remove_outer_bracket(gene_sql):
    #先定位
    return gene_sql[1:gene_sql.rfind(')')]


def generate_sql_expression(dic,length, file_name):
    non_analysis = open('non_analysis.txt','a')
    roots = postprocessing(dic, length)

    file_name = re.sub("[?,$%^*(+\"\']+", "", file_name)

    if len(roots) == 0:
        non_analysis.write(file_name+'\n')
        non_analysis.close()
    fw = open(os.path.join('result_output',file_name),'a')
    for root in roots:
        #现在每个sql都是一个T类型，都保存了sql字段
        gene_sql = str(root.val.sql)
        #print(gene_sql)
        #去掉最外层的括号
        gene_sql = remove_outer_bracket(gene_sql)
        print(gene_sql)
        fw.write(gene_sql+'\n')
        #输出到文件
    fw.close()
        # cursor = get_mysql_drive()
        # cursor.execute(gene_sql)
        # results = cursor.fetchall()
        # for result in results:
        #     print("result:{0}".format(result))





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
from .c_generate_sql import c_generate_sql
from common import find_join_t

#c 和 t做project操作
def c_project_t(c,t,sql,key1,key2):
    if c.t_name != t.t_name:
        sql.padding_join(t, key1, key2)
    #遍历c
    sql = c_generate_sql(c,sql)
    return sql
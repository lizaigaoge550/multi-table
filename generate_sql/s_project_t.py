from .s_generate_sql import s_generate_sql
from common import find_join_t
def s_project_t(s,t,sql,key1,key2):
    if s.t_name != t.t_name:
        sql.padding_join(t,key1,key2)
    #遍历s
    sql = s_generate_sql(s,sql)
    return sql


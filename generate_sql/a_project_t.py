from common import find_join_t
from .a_generate_sql import a_generate_sql


#这个是用来 a , t -- > t
def a_project_t(c,t,sql,key1,key2):
    if c.t_name != t.t_name:
        sql.padding_join(t,key1,key2)

    sql = a_generate_sql(c, sql)

    return sql
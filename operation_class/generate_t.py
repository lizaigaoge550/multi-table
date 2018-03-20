#a1 和 a2 一个是c 一个是A
#sql: select c,A as a from c.T groupby c
from symbol_class.class_file import TClass
from count_class.counter_class import Counter
from sql_class.sql import SQL
from generate_sql.a_generate_sql import a_generate_sql

def generate_Tclass(a1,a2):
    #a2可以是modify的A
    t = TClass(get_t_name(),c_name=[a1.c_name,a2.description],c_type=['string','number'])
    t.sql = SQL()
    # t.sql.padding_select(a2)
    a_generate_sql(a2, t.sql)
    t.sql.padding_select(a1)
    t.sql.padding_from(a1.T)
    t.sql.padding_groupby(a1)
    t.sql.t_name = t.t_name
    #print('genetate_Tclass:{0}'.format(t.sql))
    return t

def get_t_name():
    c = Counter()
    t_name = 'tmp_table' + str(c.cnt)
    return t_name
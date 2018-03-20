import copy
from sql_class.sql import SQL
from symbol_class.class_file import StarClass
from node import Node

def Filter_to_t(root):
    param_1, param_2 = root.val.param_1, root.val.param_2
    c = param_1 if param_1.value == 'c' else param_2
    v = param_1 if param_1.value != 'c' else param_2
    t = copy.copy(param_1.T)
    t.sql = SQL()
    t.sql.padding_select(StarClass(t_name=param_1.t_name))
    t.sql.padding_where(c,v)
    t.sql.padding_from(param_1.T)
    t.sql.t_name = t.t_name
    return Node(root,None,t,root.start,root.end)




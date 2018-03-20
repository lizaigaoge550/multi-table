from common import find_join_t,is_contained
from operation_class.count_op import Count
from operation_class.filter import In
def a_generate_sql(c, sql):
    # 这个c是modify的c, 遇到cClass放到select中，Filter放到where中
    # 如果两个参数不同表, join 和 on 操作
    if type(c) == Count:
        sql.padding_select(c)
        return sql
    stack = [c]
    while len(stack):
        tmp_stack = []
        while len(stack):
            root = stack.pop()
            if is_contained(root.param_1.t_name,root.param_2.t_name):
                # join filter.T
                if root.param_1.value == 'Filter':
                    sql.padding_join(find_join_t(root.param_1.T, root.key1, root.key2), root.key1, root.key2)
                else:
                    sql.padding_join(find_join_t(root.param_2.T, root.key1, root.key2), root.key1, root.key2)
            if root.param_1.value == 'Filter':
                sql.padding_where(root.param_1.param_1, root.param_1.param_2)
            if root.param_2.value == 'Filter':
                sql.padding_where(root.param_2.param_1, root.param_2.param_2)
            if type(root.param_1) == Count:
                # 放到select中
                sql.padding_select(root.param_1)
            if type(root.param_2) == Count:
                sql.padding_select(root.param_2)
            if root.param_1 and type(root.param_1) != In and type(root.param_1) != Count:
                tmp_stack.append(root.param_1)
            if root.param_2 and type(root.param_2) != In and type(root.param_2) != Count:
                tmp_stack.append(root.param_2)
        stack = tmp_stack
    return sql
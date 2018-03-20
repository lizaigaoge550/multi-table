from sql_class.sql import SQL
from generate_sql.c_generate_sql import c_generate_sql
from count_class.counter_class import Counter

class C_Raising(object):
    def __init__(self,param):
        self.param = param
        self.param_list = [self.param]
        # 填写属性
        self.t_name = self._get_t_name()
        self.c_name = self._get_c_name()
        self.c_type = self._get_c_type()
        self.parent_t_name = self._get_parent_t_name()
        #有两种情况 一种是S-->T 还有一种是 c-->T
        self.value = self._get_value()
        self.sql = SQL()
        self._get_sql()
        self.sql.t_name = self.t_name

    def _get_sql(self):
        self.sql = c_generate_sql(self.param,self.sql)


    @classmethod
    def _condition(cls,p1):
        if 'lambda' in p1.value:
            return False
        return True

    def __new__(cls,p1):
        f = C_Raising._condition(p1)
        if f == True:
            instance = super(C_Raising, cls).__new__(cls)
            return instance
        return None

    def _get_t_name(self):
        #首先获取一个全局计数器
        c = Counter()
        t_name = 'tmp_table'+str(c.cnt)
        return t_name

    def _get_parent_t_name(self):
        return self.param.t_name

    def _get_c_name(self):
        return self.param.c_name

    def _get_c_type(self):
        return self.param.c_type

    def _get_value(self):
        return 'T'
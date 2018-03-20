from sql_class.sql import SQL
from count_class.counter_class import Counter
from generate_sql.s_generate_sql import s_generate_sql
#from common import s_to_t_get_c_name

class Raising(object):
    def __init__(self,param):
        self.param = param
        self.param_list = [self.param]
        # 填写属性
        self.t_name = self._get_t_name()
        self.c_name = self._get_c_name()
        self.c_type = self._get_c_type()
        self.parent_t_name = self._get_parent_t_name()
        self.value = self._get_value()
        #有两种情况 一种是S-->T 还有一种是 c-->T
        self.sql = SQL()
        self._get_sql()
        self.sql.t_name = self.t_name
        #print(self.sql)


    def _get_sql(self):
        self.sql = s_generate_sql(self.param,self.sql)


    @classmethod
    def _condition(cls,p1):
        if 'lambda' in p1.value:
            return False
        return True

    def __new__(cls,p1):
        #instance = super(Raising,cls).__new__(cls)
        f = Raising._condition(p1)
        if f == True:
            #instance.__init__(p1)
            instance = super(Raising, cls).__new__(cls)
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
        #S raising 成 T
        # c,c a,c col应该是cstring 的col
        # T,c col应该是T的col
        return self.param.c_name
        #return s_to_t_get_c_name(self.param)

    def _get_c_type(self):
        return self.param.c_type

    def _get_value(self):
        return 'T'








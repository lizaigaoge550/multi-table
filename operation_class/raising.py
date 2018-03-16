from sql_class.sql import SQL
from count_class.counter_class import Counter
from symbol_class.class_file import StarClass
from .generate_t import generate_Tclass
from copy import deepcopy


from generate_sql.s_generate_sql import s_generate_sql
class Raising(object):
    def __init__(self,param):
        self.param = param
        # 填写属性
        self.t_name = self._get_t_name()
        self.c_name = self._get_c_name()
        self.c_type = self._get_c_type()
        self.parent_t_name = self._get_parent_t_name()
        self.value = self._get_value()
        #有两种情况 一种是S-->T 还有一种是 c-->T
        self.sql = SQL()
        self._get_sql()


    def _get_sql(self):
        self.sql = s_generate_sql(self.param,self.sql)


    @classmethod
    def _condition(cls,p1):
        if 'lambda' in p1:
            return False
        return True

    def __new__(cls,p1):
        instance = super(Raising,cls).__new__(cls)
        f = Raising._condition(p1)
        if f == True:
            return instance.__init__(p1)
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








from common import is_project_allowed,union
from sql_class.sql import SQL
from count_class.counter_class import Counter
from generate_sql.s_project_t import s_project_t
from generate_sql.c_project_t import c_project_t
from generate_sql.a_project_t import a_project_t

class Project(object):
    def __init__(self,param1,param2):
        self.param_1 = param1
        self.param_2 = param2
        self.param_list = [self.param_1,self.param_2]
        k1, k2, f = Project._condition(param1, param2)
        self.key1 = k1
        self.key2 = k2 #当前的表名+列名
        # 填写属性
        self.t_name = self._get_t_name()
        self.c_name = self._get_c_name()
        self.c_type = self._get_c_type()
        self.parent_t_name = self._get_parent_t_name()
        self.value = self._get_value()
        self.sql = SQL()
        self._get_sql()
        self.sql.t_name = self.t_name


    def _get_sql(self):
        # 可以是(c,T),(c,T),(A,T),(A,T)
        # select c from T
        # 先搞清楚哪个是c, 哪个是T
        c = self.param_1 if self.param_1.value != 'T' else self.param_2
        t = self.param_1 if self.param_1.value == 'T' else self.param_2
        if c.value == 'S':
            self.sql = s_project_t(c, t, self.sql, self.key1, self.key2)
        elif c.value == 'c':
            self.sql = c_project_t(c, t, self.sql, self.key1, self.key2)
        elif c.value == 'A':
            self.sql = a_project_t(c, t, self.sql, self.key1, self.key2)
        else:
            print("c.value ", c.value)


    @classmethod
    def _condition(cls,p1,p2):
        if 'lambda' in p1.value or 'lambda' in p2.value:return "","",False
        key1, key2, allowed = is_project_allowed(p1, p2)
        if allowed == True:
            return key1, key2, True
        else:
            return "", "", False

    def __new__(cls,p1,p2, p1_key="", p2_key=""):
        #instance = super(Project,cls).__new__(cls)
        k1,k2,f = Project._condition(p1,p2)
        if f == True:
            instance = super(Project, cls).__new__(cls)
            return instance
        return None

    def _get_t_name(self):
        #首先获取一个全局计数器
        c = Counter()
        t_name = 'tmp_table'+str(c.cnt)
        return t_name

    def _get_parent_t_name(self):
        if self.param_2.value == 'T':
            return union(self.param_1.t_name,self.param_2.parent_t_name)
        else:
            return union(self.param_2.t_name,self.param_1.parent_t_name)

    def _get_c_name(self):
        if self.param_1.value != 'T':return self.param_1.c_name
        else:return self.param_2.c_name

    def _get_c_type(self):
        if self.param_1.value != 'T':return self.param_1.c_type
        else:return self.param_2.c_type

    def _get_value(self):
        return 'T'
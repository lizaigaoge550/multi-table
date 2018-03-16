from common import is_project_allowed,union
from sql_class.sql import SQL
from count_class.counter_class import Counter
from generate_sql.s_project_t import s_project_t
from generate_sql.c_project_t import c_project_t

class Project(object):
    def __init__(self,param1,param2,p1_key="",p2_key=""):
        self.param_1 = param1
        self.param_2 = param2
        self.param_1_key = p1_key
        self.param_2_key = p2_key
        # 填写属性
        self.t_name = self._get_t_name()
        self.c_name = self._get_c_name()
        self.c_type = self._get_c_type()
        self.parent_t_name = self._get_parent_t_name()
        self.value = self._get_value()
        # 如果self.value中没有lambda则要生成对应的sql
        if 'lambda' not in self.value:
            self.sql = SQL()
            self._get_sql()
        else:
            self.sql = None

    def _get_sql(self):
        # 可以是(c,T),(c,T),(A,T),(A,T)
        # select c from T
        # 先搞清楚哪个是c, 哪个是T
        c = self.param_1 if self.param_1.value != 'T' else self.param_2
        t = self.param_1 if self.param_1.value == 'T' else self.param_2
        if c.value == 'S':
            self.sql = s_project_t(c, t, self.sql, self.param_1_key, self.param_2_key)
        elif c.value == 'c':
            self.sql = c_project_t(c,t, self.sql, self.param_1_key, self.param_2_key)


    @classmethod
    def _condition(cls,p1,p2):
        key1, key2, allowed = is_project_allowed(p1, p2)
        if allowed == True:
            return key1, key2, True
        else:
            return "", "", False

    def __new__(cls,p1,p2,p1_key="",p2_key=""):
        instance = super(Project,cls).__new__(cls)
        f,k1,k2 = Project._condition(p1,p2)
        if f == True:
            return instance.__init__(p1,p2,p1_key=k1,p2_key=k2)
        return None

    def _get_t_name(self):
        #首先获取一个全局计数器
        c = Counter()
        t_name = 'tmp_table'+str(c.cnt)
        return t_name

    def _get_parent_t_name(self):
        return union(self.param_1.t_name,self.param_2.t_name)

    def _get_c_name(self):
        if self.param_1.value != 'T':return self.param_1.c_name
        else:return self.param_2.c_name

    def _get_c_type(self):
        if self.param_1.value != 'T':return self.param_1.c_type
        else:return self.param_2.c_type

    def _get_value(self):
        if 'lambda' in self.param_1.value:
            prefix = ".".join(self.param_1.value.split('.')[:-1])
        elif 'lambda' in self.param_2.value:
            prefix = ".".join(self.param_2.value.split('.')[:-1])
        else:
            prefix = ""
        return prefix + '.' + 'T' if prefix != "" else 'T'
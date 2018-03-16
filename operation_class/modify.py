from common import is_modify_allowed
class Modify(object):
    def __init__(self, param1, param2, key1=None, key2=None):
        self.param_1 = param1
        self.param_2 = param2
        # 填写属性
        self.t_name = self._get_t_name()
        self.c_name = self._get_c_name()
        self.c_type = self._get_c_type()
        self.value = self._get_value()
        self.key1 = key1
        self.key2 = key2
        self.description = None

    @classmethod
    def _condition(cls, p1, p2):
        # p1.t_name,p2.t_name可能是list, 如果是多表得判断下能不能join
        key1,key2,allowed = is_modify_allowed(p1,p2)
        if allowed == True:
            return key1,key2,True
        else:
            return "","",False

       #return p1.t_name != p2.t_name or (p1.t_name == p2.t_name and p1.c_name != p2.c_name)

    def __new__(cls, p1, p2):
        instance = super(Modify, cls).__new__(cls)
        key1, key2, allowed = Modify._condition(p1, p2)
        if allowed == True:

            return instance.__init__(p1, p2, key1, key2)
        return None

    def _get_t_name(self):
        if self.param_1.t_name == self.param_2.t_name:return self.param_1.t_name
        else:
            if type(self.param_1.t_name) == list:
                return self.param_1.t_name + [self.param_2.t_name]
            elif type(self.param_2.t_name) == list:
                return self.param_2.t_name + [self.param_1.t_name]
            else:
                return [self.param_1.t_name, self.param_2.t_name]

    def _get_c_name(self):
        if self.param_1.value != 'F':return self.param_1.c_name
        else:return self.param_2.c_name

    def _get_c_type(self):
        if self.param_1.value != 'F':return self.param_1.c_type
        else:return self.param_2.c_type

    def _get_value(self):
        if 'c' in self.param_1.value or 'c' in self.param_2.value:
            r = 'c'
            self.description = self._get_description()

        elif 'S' in self.param_1.value or 'S' in self.param_2.value:r = 'S'

        else: raise ("modify param is not corrrect:{0},{1}".format(self.param_1.value,self.param_2.value))

        if 'lambda' in self.param_1.value:
            prefix = ".".join(self.param_1.value.split('.')[:-1])

        elif 'lambda' in self.param_2.value:
            prefix = ".".join(self.param_2.value.split('.')[:-1])

        else:
            prefix = ""

        return prefix + '.' + r if prefix != "" else r

    def _get_description(self):
        if 'c' in self.param_1.value:
            return self.param_1.description
        else:
            return self.param_2.description
from common import is_modify_allowed,get_t_name
class Modify(object):
    def __init__(self, param1, param2):
        self.param_1 = param1
        self.param_2 = param2
        self.param_list = [self.param_1,self.param_2]
        # 填写属性
        self.t_name = self._get_t_name()
        self.c_name = self._get_c_name()
        self.c_type = self._get_c_type()
        self.value = self._get_value()
        k1, k2, f = Modify._condition(param1, param2)
        #self.T = param1.T if param1.value != 'Filter' else param2
        self.key1 = k1
        self.key2 = k2
        self.description = None

    @classmethod
    def _condition(cls, p1, p2):
        # p1.t_name,p2.t_name可能是list, 如果是多表得判断下能不能join
        #print("p1_value:{0},p2_value:{1}".format(p1.value,p2.value))
        key1,key2,allowed = is_modify_allowed(p1,p2)
        if allowed == True:
            return key1,key2,True
        else:
            return "","",False

       #return p1.t_name != p2.t_name or (p1.t_name == p2.t_name and p1.c_name != p2.c_name)

    def __new__(cls, p1, p2):
        #instance = super(Modify, cls).__new__(cls)
        key1, key2, allowed = Modify._condition(p1, p2)
        if allowed == True:
            instance = super(Modify, cls).__new__(cls)
            return instance
        return None

    def _get_t_name(self):
        if self.param_1.t_name == self.param_2.t_name:
            if self.param_1.value != 'Filter':return self.param_1.t_name
            else:return self.param_2.t_name
        else:
            new_t_name = get_t_name(self.param_1.t_name,self.param_2.t_name)
            return new_t_name

    def _get_c_name(self):
        if self.param_1.value != 'Filter':return self.param_1.c_name
        else:return self.param_2.c_name

    def _get_c_type(self):
        if self.param_1.value != 'Filter':return self.param_1.c_type
        else:return self.param_2.c_type

    def _get_value(self):
        if 'c' in self.param_1.value or 'c' in self.param_2.value:
            r = 'c'
            #self.description = self._get_description()

        elif 'S' in self.param_1.value or 'S' in self.param_2.value:
            r = 'S'

        elif 'A' in self.param_1.value or 'A' in self.param_2.value:
            r = 'A'

        else: raise ("modify param is not corrrect:{0},{1}".format(self.param_1.value,self.param_2.value))

        return r
        # if 'lambda' in self.param_1.value:
        #     prefix = ".".join(self.param_1.value.split('.')[:-1])
        #
        # elif 'lambda' in self.param_2.value:
        #     prefix = ".".join(self.param_2.value.split('.')[:-1])
        #
        # else:
        #     prefix = ""
        #
        # return prefix + '.' + r if prefix != "" else r

    def _get_description(self):

        if 'c' in self.param_1.value:
            return self.param_1.description
        else:
            return self.param_2.description
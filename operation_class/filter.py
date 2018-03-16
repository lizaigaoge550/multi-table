#需要两个参数一个c 一个 v
class In(object):
    def __init__(self,param_1,param_2):
        self.param_1 = param_1
        self.param_2 = param_2
        self.t_name = self._get_t_name()
        self.c_name = self._get_c_name()
        self.value = 'F'
        self.c_type = self._get_c_type()
        self.T = self._get_T()

    def __new__(cls, p1, p2):
        instance = super(In, cls).__new__(cls)
        if In._condition(p1, p2):
            return instance.__init__(p1, p2)
        return None

    @classmethod
    def _condition(cls, p1, p2):
        return p1.t_name == p2.t_name and p1.c_name == p2.c_name


    def _get_t_name(self):
        return self.param_1.t_name

    def _get_c_name(self):
        return self.param_1.c_name

    def _get_c_type(self):
        return self.param_1.c_type

    def _get_T(self):
        return self.param_1.T
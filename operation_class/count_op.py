class Count(object):
    def __init__(self,param):
        self.param = param
        self.param_list = [self.param]
        #填写属性
        self.t_name = self._get_t_name()
        self.c_name = self._get_c_name()
        self.c_type = self._get_c_type()
        self.value = self._get_value()
        self.description = self._get_description()
        self.alias = 'cnt'
        self.T = param.T



    def _get_description(self):
        return 'count(%s)'%self.param.c_name

    def _get_t_name(self):
        return self.param.t_name

    def _get_c_name(self):
        return self.param.c_name

    def _get_c_type(self):
        return 'number'

    def _get_value(self):
        return 'A'






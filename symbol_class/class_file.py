#coding=utf-8

class BaseClass(object):
    def __init__(self, t_name, c_name, c_type):
        self.t_name = t_name
        self.c_name = c_name
        self.c_type = c_type

class cClass(BaseClass):
    def __init__(self,t_name, c_name, c_type, value):
        super(cClass,self).__init__(t_name, c_name, c_type)
        self.value = 'c'
        self.description = value
        self.dir = None
        self.T = None
        self.role = ""
    def __str__(self):
        return 'c'

class Param(object):
    #["state.state_name", False, "C"]
    def __init__(self,key,is_pad,value):
        self.key = key
        self.is_pad = is_pad
        self.value = value



class SClass(BaseClass):
    def __init__(self,t_name, c_name, c_type, value):
        super(SClass,self).__init__(t_name, c_name, c_type)
        self.value = value
        self.key1 = None
        self.key2 = None
        self.param_1 = None
        self.param_2 = None
        self.param_list = [self.param_1, self.param_2]
    def __str__(self):
        return self.value


class TClass(BaseClass):
    def __init__(self, t_name, c_name, c_type):
        super(TClass,self).__init__(t_name,c_name,c_type)
        self.description = t_name
        self.value = 'T'
        self.sql = t_name
        self.parent_name = t_name
    def __str__(self):
        return self.t_name

class VClass(BaseClass):
    def __init__(self,t_name, c_name, c_type, cell_value,value):
        super(VClass,self).__init__(t_name,c_name,c_type)
        self.value = 'V'
        self.cell_value = cell_value
        self.description = value
        self.T = None
        self.role = ""
    def __str__(self):
        return 'V'


class StarClass():
    def __init__(self,t_name):
        self.value = '%s.*'%t_name
    def __str__(self):
        return self.value



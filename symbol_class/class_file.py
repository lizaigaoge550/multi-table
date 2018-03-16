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
    def __str__(self):
        return 'c'

class Param(object):
    #["state.state_name", False, "C"]
    def __init__(self,key,is_pad,value):
        self.key = key
        self.is_pad = is_pad
        self.value = value



class SClass(BaseClass):
    def __init__(self,t_name, c_name, c_type):
        super(SClass,self).__init__(t_name, c_name, c_type)
        self.value = 'S'
        self.key1 = None
        self.key2 = None
    def __str__(self):
        return 'S'


class TClass(BaseClass):
    def __init__(self, t_name, c_name, c_type):
        super(TClass,self).__init__(t_name,c_name,c_type)
        self.description = t_name
        self.value = 'T'
        self.sql = t_name
    def __str__(self):
        return 'T'


class VClass(BaseClass):
    def __init__(self,t_name, c_name, c_type, cell_value,value):
        super(VClass,self).__init__(t_name,c_name,c_type)
        self.value = 'V'
        self.cell_value = cell_value
        self.description = value
        self.T = None
    def __str__(self):
        return 'V'


class NClass(BaseClass):
    def __init__(self,t_name, c_name, c_type, upper, lower, number_type,value):
        super(NClass,self).__init__(t_name,c_name,c_type)
        self.c_type = 'number' #N 的 type一定是number
        self.value = 'N'
        self.upper = upper
        self.lower = lower
        self.number_type = number_type
        self.description = value
    def __str__(self):
        return 'N'


class DClass(BaseClass):
    def __init__(self,t_name, c_name, c_type, upper, lower, time_type,value):
        super(DClass,self).__init__(t_name,c_name,c_type)
        self.c_type = 'date' #D 的 type一定是number
        self.value = 'D'
        self.upper = upper
        self.lower = lower
        self.time_type = time_type
        self.description = value
    def __str__(self):
        return 'D'

class BlankClass(BaseClass):
    def __init__(self,t_name,c_name,c_type,value):
        super(BlankClass,self).__init__(t_name,c_name,c_type)
        self.c_type = 'blank' #N 的 type一定是number
        self.value = 'blank'
        self.description = value
    def __str__(self):
        return 'blank'

class ExcludeClass(BaseClass):
    def __init__(self,t_name,c_name,c_type,value):
        super(ExcludeClass,self).__init__(t_name,c_name,c_type)
        self.c_type = "Excluding" #N 的 type一定是number
        self.value = 'Excluding'
        self.description = value
    def __str__(self):
        return 'Excluding'

class DirClass():
    def __init__(self,value):
        self.value= 'dir'
        self.description = value
    def __str__(self):
        return 'Dir'

class StarClass():
    def __init__(self):
        self.value = '*'
    def __str__(self):
        return '*'



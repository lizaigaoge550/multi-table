from expression import extract_c

class WhereClass():
    def __init__(self,key, value):
        self.key = key
        self.value = value
    def __cmp__(self, other):
        return self.key.description == other.description
    def __str__(self):
        return self.key.description+' : '+self.value.description


class JoinClass():
    def __init__(self, t, condition):
        self.t =  t
        self.condition = condition
    def __str__(self):
        return self.t.t_name + ' on ' +self.condition

class SQL(object):
    def __init__(self):
        self.Select = []
        self.Where = []
        self.Having = []
        self.Groupby = []
        self.Orderby = []
        self.Join = []
        self.From = []
        self.t_name = None

    #要么是c 要么是A, T
    def padding_select(self,param):
        self.Select.append(param)

    #要么是c, 要么是A
    def padding_groupby(self,param):
        self.Groupby.append(param)

    #from T
    def padding_from(self,param):
        self.From.append(param)

    # 要么是c, 要么是A
    def padding_orderby(self,param):
        self.Orderby.append(param)


    def padding_where(self,key,value):
        self.Where.append(WhereClass(key,value))

    #join 需要两个一个join哪张表，一个join的条件
    def padding_join(self,t,k1,k2):
        self.Join.append(JoinClass(t,k1+'='+k2))

    def __str__(self):
        #先提取select的东西
        res = "("
        if len(self.Select):
            res += 'select ' + extract_c(self.Select)
        if len(self.From):
            res += ' from ' + str(self.From[0])
        if len(self.Groupby):
            res += 'group by ' + extract_c(self.Groupby)
        if len(self.Join):
            res += ' join ' + str(self.Join[0].t)
            res += ' on ' + self.Join[0].condition
        if len(self.Orderby):
            res += 'order by ' + extract_c(self.Orderby) + ' desc limit 1'
        res += ')'+self.t_name
        return res

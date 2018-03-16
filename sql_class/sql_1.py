#res = {'from': [], 'select': [], 'where': [], 'orderby': [], 'groupby': [], 'join':[]}

# class SQL(object):
#     def __init__(self):
#         self.Select = []
#         self.Where = []
#         self.Having = []
#         self.Groupby = []
#         self.Orderby = []
#         self.Join = []
#         self.From = []
#
#     #要么是c 要么是A, T
#     def padding_select(self,param):
#         if param.value == 'c' or param.value == 'T':
#             self.Select.append(param.description)
#         elif param.value == 'A':
#             self.Select.append(param.param.description+type(param).__name__.lower())
#         else:
#             raise Exception("sql select is not correct:{0}".format(param.value))
#
#     #要么是c, 要么是A
#     def padding_groupby(self,param):
#         if param.value == 'c':
#             self.Select.append(param.description)
#         elif param.value == 'A':
#             self.Select.append(param.param.description+type(param).__name__.lower())
#         else:
#             raise Exception("sql groupby is not correct:{0}".format(param.value))
#
#
#     #from T
#     def padding_from(self,param):
#         assert param.value == 'T'
#         self.From.append(param)
#
#
#     # 要么是c, 要么是A
#     def padding_orderby(self,param):
#         if param.value == 'c':
#             self.Select.append(param.description)
#         elif param.value == 'A':
#             self.Select.append(param.param.description+type(param).__name__.lower())
#         else:
#             raise Exception("sql orderby is not correct:{0}".format(param.value))
#
#     #join 需要两个一个join哪张表，一个join的条件
#     def padding_join(self,param):
#



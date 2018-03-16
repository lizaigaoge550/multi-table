#coding=utf-8
#该类存储主外键的映射关系
class Map():
    def __init__(self):
        self.major_foreign = {}
        self.foreign_major = {}

    def is_map(self,major,foreign):
        if major in self.major_foreign:
            return self.major_foreign[major] == foreign
        elif major in self.foreign_major:
            return self.foreign_major[major] == foreign
        return False

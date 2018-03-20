#coding=utf-8
#该类存储主外键的映射关系
import sys
sys.path.append('.')
class Map():

    @staticmethod
    def read_major_foreign_info():
        dict_list = []
        with open('map_class\\map.txt') as fr:
            for line in fr.readlines():
                line = line.strip()
                lines = line.split(',')
                for i in range(len(lines)):
                    for j in range(len(lines)):
                        if i != j:
                            dict_list.append((lines[i], lines[j]))
        return dict_list
    def __init__(self):
        self.major_foreign = Map.read_major_foreign_info()


    def is_map(self,major,foreign):
        flag = False
        for item in self.major_foreign:
            if item[0] == major:
                if item[1] == foreign:
                    flag = True
                    return flag
        return flag

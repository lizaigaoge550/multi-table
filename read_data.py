import glob
import os
import json
from symbol_class.class_file import *
import copy
from operation_class.count_op import Count
from table_info.get_table_info import get_table


def generate_index(inital,s,count):
    if count == 0:
        s.append(copy.copy(inital))
        return
    for i in range(2):
        inital.append(i)
        generate_index(inital,s,count-1)
        del inital[-1]


def no_pat(tag,index):
    s = []
    for i in range(len(tag[index])):
        if tag[index][i] != 'verb':
            s.append(tag[index][i])
    return s

def generate_multi_tags(tags):
    #tag中可能有pat所以要拆分
    #获取pat的索引
    pat_index = []
    index_count = 0
    for tag_index in range(len(tags)):
        if 'verb' in tags[tag_index]:
            pat_index.append(tag_index)
            index_count += 1
    if index_count == 0:
        return [tags]
    #产生索引
    s = []
    generate_index([],s,index_count)
    data = []

    for s_index in range(len(s)):
        tag_copy = copy.copy(tags)
        for index,value in zip(pat_index,s[s_index]):
            if value == 0:
                tag_copy[index] = []
            else:
                tag_copy[index] = no_pat(tag_copy,index)
        tag_copy = list(filter(lambda a:a!=[],tag_copy))
        data.append(copy.deepcopy(tag_copy))
    return data



def generate_parameter(key,leixing):
    if key[-1] == 'C':
        return cClass(t_name=key[0].split('.')[0],c_name=key[0],c_type=leixing,value=key[0])
    if key[-1] == 'A':
        content = key[key.find("(") + 1:key.find(")")]
        return Count(cClass(t_name=content.split('.')[0],c_name=content,c_type='string',value=content))
    # if key[-1] == 'T':
    #     return TClass(t_name=key[0],c_name=)

def get_S_tname_cols_coltype(tag,s):
    #看看key1, key2 是不是都是false
    key1 = tag['key1']
    key2 = tag['key2']
    s.key1 = Param(key1[0],key1[1],key1[-1] if key1[-1] != 'C' else 'c')
    s.key2 = Param(key2[0],key2[1],key2[-1] if key2[-1] != 'C' else 'c')
    if key1[1] == True:
        s.t_name = [key1[0].split('.')[0]]
        s.c_name = [key1[0]]
        s.param_1 = generate_parameter(key1,'string')
    if key2[1] == True:
        s.t_name = [key2[0].split('.')[0]]
        s.c_name = [key2[0]]
        s.param_2 = generate_parameter(key2,'number')




def get_S_value(value):
    vs = list(filter(lambda a:a,value.split('.')[0].split('@')))
    new_v = 'lambda('
    for v in vs:
        if v == 'C':v = 'c'
        new_v += v + ','
    return new_v[:-1]+').S'




def read_data(path):
    data = {}
    #sql = {}
    abstract_data = {}
    for eachfile in glob.glob(os.path.join(path,'*')):
        item = json.load(open(eachfile,encoding='utf-8-sig'))
        # 拿出tag
        utterance = item['new_tag_utterance']
        tags = []
        for i in range(len(utterance)):
            tag = utterance[i]['tags']  # 是一个list
            left = utterance[i]['left_index']
            right = utterance[i]['right_index']
            label = []
            for j in range(len(tag)):
                # 首先提取type
                value = tag[j]['Type']
                if value == 'Vistype': continue
                # #如果value 是 c 和 V, T 的话
                if value == 'c' or value == 'v' or value == 'S' or value == 'verb':
                    if value == 'c' or value == 'v':
                        if value == 'c':
                            c_cls = cClass(t_name=tag[j]['tab_name'], c_name=tag[j]['value'],
                                                 c_type=tag[j]['data_type'], value=tag[j]['value'])
                            c_cls.role = tag[j]['role']
                            c_name, c_type = get_table(c_cls.t_name)
                            t = TClass(t_name=c_cls.t_name,c_name=c_name,c_type=c_type)
                            c_cls.T = t
                            label.append([c_cls,left,right])

                        if value == 'v':
                            v_cls = VClass(t_name=tag[j]['tab_name'], c_name=tag[j]['col_name'], c_type="string",
                                                cell_value=tag[j]['pure_value'],value=tag[j]['value'])
                            v_cls.role = tag[j]['role']
                            c_name, c_type = get_table(v_cls.t_name)
                            t = TClass(t_name=v_cls.t_name,c_name=c_name,c_type=c_type)
                            v_cls.T = t
                            label.append([v_cls,left,right])

                    elif value == 'S':
                        f = SClass([],[],[],get_S_value(tag[j]['value']))
                        get_S_tname_cols_coltype(tag[j],f)
                        label.append([f, left, right])

                    elif value == 'verb':
                        label.append('verb')

                    else:
                        print(value)
                        raise ('Type is not right')

            if len(label): tags.append(label)
        if len(tags) == 0: print(item);continue
        tags = generate_multi_tags(tags)
        data[item["raw_utterance"]] = tags
        #sql[item['raw_utterance']] = item["sql_info"]
        abstract_data[item['raw_utterance']] = item['abstract_utterance']

    return data, abstract_data



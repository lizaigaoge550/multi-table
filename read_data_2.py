import glob
import os
import json
from opt_class import *
from symbol_class.class_file import *

import copy

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
        if tag[index][i] != 'pat':
            s.append(tag[index][i])
    return s

def generate_multi_tags(tags):
    #tag中可能有pat所以要拆分
    #获取pat的索引
    pat_index = []
    index_count = 0
    for tag_index in range(len(tags)):
        if 'pat' in tags[tag_index]:
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




def read_data(path):
    data = {}
    sql = {}
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
                if value == 'c' or value == 'v' or value == 'T' or value == 'N' or value == 'D' or value == 'Blank' \
                        or value == 'Excluding' or value == 'dir' or value == 'pat' or value == 'S':

                    if value == 'c' or value == 'v':
                        if value == 'c':
                            label.append([cClass(t_name=tag[j]['tab_name'], c_name=tag[j]['col_name'],
                                                 c_type=tag[j]['data_type'], value=tag[j]['value']),left,right])

                        if value == 'v':
                            label.append([VClass(t_name=tag[j]['tab_name'], c_name=tag[j]['col_name'], c_type="string",
                                                cell_value=tag[j]['pure_value'],value=tag[j]['value']),left,right])

                    elif value == 'T':
                        label.append(
                            [TClass(t_name=tag[j]['tab_name'], c_name=tag[j]['col_names'], c_type=tag[j]['data_types']),left,right])

                    elif value == 'N':
                        for col in tag[j]['cols']:
                            label.append([NClass(t_name=col['tab_name'], c_name=col['col_name'], c_type='number',
                                                 upper=tag[j]['upper_bound'],number_type=tag[j]['number_type'],
                                                 lower=tag[j]['lower_bound'],value=tag[j]['value']),left,right])

                    elif value == 'D':
                        for col in tag[j]['cols']:
                            label.append([DClass(t_name=col['tab_name'], c_name=col['col_name'], c_type='number',
                                                 upper=tag[j]['upper_bound'],time_type=tag[j]['time_type'],
                                                 lower=tag[j]['lower_bound'],value=tag[j]['value']),left,right]),

                    elif value == 'Blank':
                        f = BlankClass(None, None, None, 'blank')
                        label.append([f,left,right])

                    elif value == 'Excluding':
                        f = ExcludeClass(None, None, None, 'Excluding')
                        label.append([f,left,right])

                    elif value == 'dir':
                        f = DirClass(tag[j]['direction'])
                        label.append([f,left,right])

                    elif value == 'pat':
                        label.append('pat')

                    elif value == 'S':
                        try:
                            f = SClass(tag[j]['category'])
                        except:
                            print(eachfile)
                        label.append([f, left, right])

                    else:
                        print(value)
                        raise ('Type is not right')

            if len(label): tags.append(label)
        if len(tags) == 0: print(item);continue
        tags = generate_multi_tags(tags)
        data[item["raw_utterance"]] = tags
        sql[item['raw_utterance']] = item["sql_info"]
        abstract_data[item['raw_utterance']] = item['abstract_utterance']

    return data, sql, abstract_data



import glob
import os
import json
from opt_class import *
from symbol_class.class_file import *
from getTable import get_table
import copy
t_name,Table = get_table()


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
        data.append(tag_copy)
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
                        or value == 'Excluding' or value == 'dir' or value == 'pat':

                    if value == 'pat':
                        description = tag[j]['values']
                    else:
                        description = tag[j]['value']

                    if value == 'c' or value == 'v':
                        c_name = description.split('.')[1]
                        if c_name not in Table: print(c_name); print(c_name);raise ("c_name not in Table")
                        if value == 'c':

                            label.append([cClass(t_name=t_name, c_name=c_name, c_type=Table[c_name], value=description),left,right])


                        if value == 'v':
                            label.append([VClass(t_name=t_name, c_name=c_name, c_type=Table[c_name],
                                                value=tag[j]['value']),left,right])

                    elif value == 'T':
                        label.append(
                            [TClass(t_name=t_name, c_name=list(Table.keys()), c_type=list(Table.values())),left,right])
                    elif value == 'N':
                        label.append([NClass(None, None, 'string', tag[j]['value']),left,right])
                    elif value == 'D':
                        label.append([DClass(t_name=t_name, c_name=tag[j]['col'].split('.')[-1], c_type='date', value=tag[j]['value']),
                                      left,right])
                    elif value == 'Blank':
                        f = BlankClass(None, None, None, 'blank')
                        label.append([f,left,right])
                    elif value == 'Excluding':
                        f = ExcludeClass(None, None, None, 'Excluding')
                        label.append([f,left,right])
                    elif value == 'dir':
                        f = DirClass(description)
                        label.append([f,left,right])
                    elif value == 'pat':
                        label.append('pat')
                    else:
                        print(value)
                        raise ('Type is not right')

                else:
                    func = value.split('.')[-1]  #F只能是S
                    assert func == 'S',"func is not S"
                    try:
                        f = SClass(tag[j]['Category'])
                    except:
                        print(eachfile)
                        exit(10000)
                    label.append([f,left,right])

            if len(label): tags.append(label)
        if len(tags) == 0: print(item);continue
        tags = generate_multi_tags(tags)
        data[item["raw_utterance"]] = tags
        sql[item['raw_utterance']] = item["sql_info"]
        abstract_data[item['raw_utterance']] = item['abstract_utterance']

    return data, sql, abstract_data



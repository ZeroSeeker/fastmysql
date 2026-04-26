#!/usr/bin/env python3
# coding = utf8

import datetime


def filter_data_dict_list_by_columns(
        data_dict_list: list,
        all_col_list: list
):
    """
    按目标表列名过滤输入数据，只保留表中存在的列，并丢弃无有效列的空行
    """
    all_col_set = set(all_col_list or [])
    filtered_data_dict_list = list()
    for each_data_dict in data_dict_list:
        each_data_dict_filtered = {
            each_key: each_value for each_key, each_value in each_data_dict.items()
            if each_key in all_col_set
        }
        if each_data_dict_filtered:
            filtered_data_dict_list.append(each_data_dict_filtered)
    return filtered_data_dict_list


def prepare_data_with_column_info(
        data_dict_list: list,
        column_info,
        pk_col_list: list = None
):
    """
    基于 column_info 过滤数据，并生成 clean_data 所需的列信息结构
    """
    all_col_list, pk_col_list_get, data_col_list = column_info
    filtered_data_dict_list = filter_data_dict_list_by_columns(
        data_dict_list=data_dict_list,
        all_col_list=all_col_list
    )
    column_info_dict = {
        'all_col_list': all_col_list,
        'data_col_list': data_col_list,
        'pk_col_list': pk_col_list if pk_col_list else pk_col_list_get,
    }
    return filtered_data_dict_list, column_info_dict


def collect_data_dict_keys(
        data_dict_list: list
):
    """
    从已过滤的数据中收集本次写入涉及的列
    """
    key_set = set()
    for each_data_dict in data_dict_list:
        for each_key in each_data_dict:
            key_set.add(each_key)
    return list(key_set)


def build_insert_data_list(
        data_dict_list: list,
        insert_param_list: list,
        replace_space_to_none: bool = True,
        str_f: str = None
):
    """
    将字典列表转换为 executemany 所需的 tuple 列表，并做基础值格式化
    """
    insert_data_list = list()
    for each_data_dict in data_dict_list:
        each_insert_data_list = list()
        for each_data_key in insert_param_list:
            each_data_value = each_data_dict.get(each_data_key)
            if each_data_value == "":
                if replace_space_to_none is True:
                    each_insert_data_list.append(None)
                else:
                    each_insert_data_list.append("")
            elif isinstance(each_data_value, datetime.datetime):
                if str_f:
                    each_insert_data_list.append(each_data_value.strftime(str_f))
                else:
                    each_insert_data_list.append(str(each_data_value))
            elif isinstance(each_data_value, datetime.date):
                if str_f:
                    each_insert_data_list.append(each_data_value.strftime(str_f))
                else:
                    each_insert_data_list.append(str(each_data_value))
            else:
                each_insert_data_list.append(each_data_value)
        insert_data_list.append(tuple(each_insert_data_list))
    return set(insert_data_list)

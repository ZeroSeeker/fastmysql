#!/usr/bin/env python3
# coding = utf8

import datetime
import decimal

import numpy as np


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
    return build_data_tuple_set(
        data_dict_list=data_dict_list,
        param_list=insert_param_list,
        replace_space_to_none=replace_space_to_none,
        str_f=str_f
    )


def normalize_write_value(
        value,
        replace_space_to_none: bool = True,
        str_f: str = None,
        int64_to_str: bool = False,
        decimal_to_str: bool = False,
        list_to_str: bool = False
):
    """
    统一写入前的值格式化逻辑，通过参数控制具体转换策略
    """
    if value == "":
        if replace_space_to_none is True:
            return None
        return ""

    if int64_to_str and isinstance(value, np.int64):
        return str(value)
    if decimal_to_str and isinstance(value, decimal.Decimal):
        return str(value)
    if isinstance(value, datetime.datetime):
        if str_f:
            return value.strftime(str_f)
        return str(value)
    if isinstance(value, datetime.date):
        if str_f:
            return value.strftime(str_f)
        return str(value)
    if list_to_str and isinstance(value, list):
        return str(value)
    return value


def build_data_tuple_set(
        data_dict_list: list,
        param_list: list,
        replace_space_to_none: bool = True,
        str_f: str = None,
        int64_to_str: bool = False,
        decimal_to_str: bool = False,
        list_to_str: bool = False
):
    """
    将字典列表转换为按 param_list 排序的 tuple 集合
    """
    data_list = list()
    for each_data_dict in data_dict_list:
        each_data_list = list()
        for each_data_key in param_list:
            each_data_list.append(
                normalize_write_value(
                    value=each_data_dict.get(each_data_key),
                    replace_space_to_none=replace_space_to_none,
                    str_f=str_f,
                    int64_to_str=int64_to_str,
                    decimal_to_str=decimal_to_str,
                    list_to_str=list_to_str
                )
            )
        data_list.append(tuple(each_data_list))
    return set(data_list)

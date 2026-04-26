import importlib
import datetime
import os
import sys
import unittest


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


fastmysql_module = importlib.import_module("fastmysql.fastmysql")
lazymysql_module = importlib.import_module("fastmysql.lazymysql")
data_utils_module = importlib.import_module("fastmysql._data_utils")


class FilterDataDictListByColumnsTests(unittest.TestCase):
    def test_shared_filter_module_keeps_valid_columns_without_mutating_input(self):
        raw = [
            {"id": 1, "name": "alice", "extra": "x"},
            {"invalid": 2},
            {"name": "bob", "age": 18},
        ]
        raw_snapshot = [
            {"id": 1, "name": "alice", "extra": "x"},
            {"invalid": 2},
            {"name": "bob", "age": 18},
        ]

        filtered = data_utils_module.filter_data_dict_list_by_columns(
            data_dict_list=raw,
            all_col_list=["id", "name"]
        )

        self.assertEqual(filtered, [{"id": 1, "name": "alice"}, {"name": "bob"}])
        self.assertEqual(raw, raw_snapshot)

    def test_prepare_data_with_column_info_uses_override_pk_and_filters_data(self):
        raw = [
            {"id": 1, "name": "alice", "extra": "x"},
            {"invalid": 2},
            {"name": "bob", "age": 18},
        ]

        filtered, column_info_dict = data_utils_module.prepare_data_with_column_info(
            data_dict_list=raw,
            column_info=(["id", "name"], ["id"], ["name"]),
            pk_col_list=["name"]
        )

        self.assertEqual(filtered, [{"id": 1, "name": "alice"}, {"name": "bob"}])
        self.assertEqual(
            column_info_dict,
            {"all_col_list": ["id", "name"], "data_col_list": ["name"], "pk_col_list": ["name"]}
        )

    def test_collect_keys_and_build_insert_data_list(self):
        filtered = [
            {"id": 1, "name": "alice", "created_at": datetime.datetime(2024, 1, 2, 3, 4, 5), "blank": ""},
            {"name": "bob", "id": 2, "created_at": datetime.date(2024, 1, 3), "blank": ""},
            {"id": 1, "name": "alice", "created_at": datetime.datetime(2024, 1, 2, 3, 4, 5), "blank": ""},
        ]

        insert_param_list = data_utils_module.collect_data_dict_keys(filtered)
        self.assertEqual(set(insert_param_list), {"id", "name", "created_at", "blank"})

        insert_data_list = data_utils_module.build_insert_data_list(
            data_dict_list=filtered,
            insert_param_list=["id", "name", "created_at", "blank"],
            replace_space_to_none=True,
            str_f="%Y-%m-%d"
        )

        self.assertEqual(
            insert_data_list,
            {
                (1, "alice", "2024-01-02", None),
                (2, "bob", "2024-01-03", None),
            }
        )

    def test_build_data_tuple_set_supports_clean_data_conversions(self):
        data_tuple_set = data_utils_module.build_data_tuple_set(
            data_dict_list=[
                {"id64": data_utils_module.np.int64(3), "amount": data_utils_module.decimal.Decimal("1.23"), "tags": ["a"], "day": datetime.date(2024, 1, 4), "blank": ""},
                {"id64": data_utils_module.np.int64(3), "amount": data_utils_module.decimal.Decimal("1.23"), "tags": ["a"], "day": datetime.date(2024, 1, 4), "blank": ""},
            ],
            param_list=["id64", "amount", "tags", "day", "blank"],
            replace_space_to_none=True,
            int64_to_str=True,
            decimal_to_str=True,
            list_to_str=True
        )

        self.assertEqual(
            data_tuple_set,
            {("3", "1.23", "['a']", "2024-01-04", None)}
        )

    def test_fastmysql_filter_keeps_valid_columns_without_mutating_input(self):
        raw = [
            {"id": 1, "name": "alice", "extra": "x"},
            {"invalid": 2},
            {"name": "bob", "age": 18},
        ]
        raw_snapshot = [
            {"id": 1, "name": "alice", "extra": "x"},
            {"invalid": 2},
            {"name": "bob", "age": 18},
        ]

        filtered = fastmysql_module.filter_data_dict_list_by_columns(
            data_dict_list=raw,
            all_col_list=["id", "name"]
        )

        self.assertEqual(filtered, [{"id": 1, "name": "alice"}, {"name": "bob"}])
        self.assertEqual(raw, raw_snapshot)

    def test_lazymysql_filter_keeps_valid_columns_without_mutating_input(self):
        raw = [
            {"id": 1, "name": "alice", "extra": "x"},
            {"invalid": 2},
            {"name": "bob", "age": 18},
        ]
        raw_snapshot = [
            {"id": 1, "name": "alice", "extra": "x"},
            {"invalid": 2},
            {"name": "bob", "age": 18},
        ]

        filtered = lazymysql_module.filter_data_dict_list_by_columns(
            data_dict_list=raw,
            all_col_list=["id", "name"]
        )

        self.assertEqual(filtered, [{"id": 1, "name": "alice"}, {"name": "bob"}])
        self.assertEqual(raw, raw_snapshot)


if __name__ == "__main__":
    unittest.main()

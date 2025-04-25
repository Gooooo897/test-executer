import openpyxl

import os, sys
sys.path.append(os.getcwd())
from . import test_case as ts

sys.path.append(os.getcwd() + r"..")
from testing_support_functions import common_tool as ct

class TestSuite():
    _test_suite_name:str
    _sheet_name:str
    _header_row:int
    _wb:openpyxl.Workbook

    def __init__(self) -> None:
        TestSuite._sheet_name = "test_suite"
        TestSuite._header_row = 2 # ヘッダー行（1から始まる）

    def collect(self, excel_file_path:str)->list[ts.TestCase]:
        TestSuite._wb = openpyxl.load_workbook(excel_file_path, data_only=True)
        TestSuite._test_suite_name = TestSuite._wb[TestSuite._sheet_name]['D1'].value
        excel_data_list = ct.read_excel_data(TestSuite._wb, TestSuite._sheet_name, TestSuite._header_row)
        test_suite = self.extract(excel_data_list)
        return test_suite

    def extract(self, excel_row_data_list:list[dict])->list[ts.TestCase]:
        test_suite = []
        for excel_row_data in excel_row_data_list:
            ret, t_case = ts.create_test_case(TestSuite._wb, excel_row_data)
            if ret == "end":
                break
            elif ret == "continue":
                continue
            else:
                test_suite.append(t_case)

        return test_suite

if __name__ == "__main__":
    # 使用例
    # file_path = input("テストパラメータが記載されているxlsxファイルを入力：")
    file_path = "file_path"
    t_suite = TestSuite()
    test_suite = t_suite.collect(file_path)
    print("テストスイート名:{}".format(t_suite._test_suite_name))
    # row_data_listをもとにtest_suiteを作成する。
    for t_case in test_suite:
        for worker in t_case.workers:
            for command in worker.commands:
                print(command)


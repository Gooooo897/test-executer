from dataclasses import dataclass
import openpyxl as opxl

import os, sys
sys.path.append(os.getcwd())
from . import worker

@dataclass
class TestCase:
    test_num_str: str
    start_message: str
    init_scripts: list[str]
    key_on_mask_time_sec: int
    workers: list[worker.AbstractWorker] # 同ディレクトリのworkerモジュールAbstructWorkerクラスの派生クラスが入る。

def create_test_case(wb:opxl.Workbook, excel_row_data:dict)->tuple[TestCase,str]:
    # テストケース番号を取得
    test_number = str(excel_row_data.get('test case number', None))
    if test_number == 'None':
        return "end", None

    # 実施要否を確認
    do = excel_row_data.get("do or not", "none") # 試験実施するかどうかを決められる。
    # 実施有無列が存在していて、値がno:対象外、done:済、wait:待機 のいずれかだったらテストしない。
    if do != "none" and (do == "no" or do == "done" or do == "wait"):
        return "continue", None
    else:
        pass # 実施要否列が存在していなかったら試験対象とする。

    start_msg = str(excel_row_data.get("preKeyOn message", "no message"))
    if start_msg == "no message" or start_msg == None:
        start_msg = test_number + " will start."
    else:
        start_msg = test_number + " will start.\n" + start_msg

    # 初期化スクリプトを取得
    init_script_list = str(excel_row_data.get("init script", None)).split('\n')

    # マスク時間の確認
    mask_time_sec = excel_row_data.get('postKeyOn mask time[s]', None)

    # test senarioフォーマットの確認
    test_senario_format = excel_row_data.get('test case format type', None)

    if test_senario_format == None:
        raise ValueError("{}'s format is invalid.".format(test_number))

    t_senario = worker.TestSenario.create(wb, test_senario_format)
    worker_list = t_senario.extract_workers(excel_row_data)

    t_case = TestCase(test_number,
                            start_msg,
                            init_script_list,
                            mask_time_sec,
                            worker_list,
                            )
    return "ok", t_case
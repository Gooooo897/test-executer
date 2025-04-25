import time
import tkinter as tk
import tkinter.filedialog as tfd
import warnings
import os
import configparser

from testing_support_functions import display_testing_message as display_msg
import testing_support_functions.edit_log_file as edit_log_file
import testing_components.test_suite as ts
import testing_components.worker as wk
from controller.abstruct_tool_controller import AbstructToolController
from controller.tool_controller import ToolController
from my_tkinter.select_type import SelectType

def start_test():
    root = tk.Tk()
    root.attributes('-topmost', True) # メッセージボックスを画面の最前面にする
    root.withdraw()
    display_msg.order_without_sound("CANapeを使ったテストを開始します。頑張りましょう")
    display_msg.order_without_sound("重めのアプリは閉じましたか?")
    # 事前準備
    ## コンソールに余分なエラーを出さないようにする
    warnings.simplefilter(action='ignore', category=UserWarning)

    ## 初期化
    config = configparser.ConfigParser()
    cwd = os.path.dirname(__file__)
    config.read(cwd + '/config/config.ini', 'UTF-8')

    canape_project_path            = str(config['CANape_configuration']['PROJECT_PATH'])
    log_base_folder_name                = str(config['CANape_configuration']['LOG_PATH'])
    log_folder_fullpath = canape_project_path + '\\' + log_base_folder_name
    ending_time_sec                = int(config['CANape_configuration']['END_WAIT_SEC'])

    delete_check = display_msg.DeleteLogOrNot()
    delete_check.check()
    if delete_check.responce == "yes":
        edit_log_file.delete_files_with_extension(log_folder_fullpath, "csv")
        edit_log_file.delete_files_with_extension(log_folder_fullpath, "MDF")
        edit_log_file.delete_files_with_extension(log_folder_fullpath, "png")
    root.destroy()

    ## チェッカー操作設定
    checker_control_type:str = str(config['checker_switch_control']['CONTROL_TYPE'])
    checker_ctrller = ToolController.create(checker_control_type)
    checker_ctrller.prepare()
    wk.KeyWorker.set_checker_controller(checker_ctrller)

    ## CANape設定
    CANape_control_type:str = str(config['CANape_configuration']['CONTROL_TYPE'])
    CANape_ctrller = ToolController.create(CANape_control_type)
    CANape_ctrller.prepare()

    # 処理開始
    ## 最初にコレを気づいてた方がロス少ない。
    CANape_ctrller.attention()

    ## CANape起動
    CANape_ctrller.start()

    ## 試験中にCASLスクリプトやCASLコマンドを使えるよう準備
    wk.CanapeWorker.set_module_object(CANape_ctrller.__class__._module)

    while True:
        root = tk.Tk()
        root.attributes('-topmost', True) # メッセージボックスを画面の最前面にする
        root.withdraw()
        file_path = tfd.askopenfilename(filetypes=[("Excel ブック", "*.xlsx")])

        t_suite = ts.TestSuite()
        test_case_list = t_suite.collect(file_path)

        for test_case in test_case_list:
            # テスト継続するか確認
            start_flag = display_msg.ask_continue()
            if start_flag != "yes":
                break
            display_msg.order_with_sound(test_case.start_message)

            # カメラ使う場合は写真用フォルダを作成する
            for w in test_case.workers:
                if w.__class__.__name__ == "CameraWorker":
                    ## cameraの初期設定
                    camera_log_path = os.path.join(log_folder_fullpath, "Camera_" + test_case.test_num_str)
                    wk.CameraWorker.prepare(camera_log_path)
                    break

            # チェッカーの初期化
            if display_msg.ask_checker_ready() == "no":
                exit
            CANape_ctrller.prepare_measurment(test_case.init_scripts)
            checker_ctrller.start()
            time.sleep(2)
            CANape_ctrller.start_measurment()

            # mask時間分待機
            display_msg.show_remaining_time_to_wait(test_case.key_on_mask_time_sec)

            # 測定中に模擬信号を更新したり手動操作できる
            index = 1
            for worker in test_case.workers:
                ret:str = worker.start_work()
                worker.sleep()
                index += 1
                if ret == "no":
                    break

            time.sleep(ending_time_sec)

            CANape_ctrller.stop_measurement()
            checker_ctrller.stop()

            ## ログをリネームします。
            edit_log_file.rename_latest_file(log_folder_fullpath, "csv", test_case.test_num_str + "_")

        ret = display_msg.order_without_sound("終了しますか? 「いいえ」の場合\n \
CANapeを閉じずに\n \
再度 シナリオファイルを選択するところからやり直します。")
        root.destroy()
        if ret == "yes":
            break
        else:
            continue

    CANape_ctrller.stop()

if __name__ == "__main__":
    start_test()

import pycanape
import os
import configparser
from testing_support_functions import display_testing_message as display_msg
from controller.abstruct_tool_controller import AbstructToolController

class CANapeController(AbstructToolController):
    _project_path:str
    _canape:pycanape.CANape
    _initialize_script_path:str
    _routine_script_path:str
    _routine_script:pycanape.Script
    _module:pycanape.Module # スクリプト呼び出せるならモジュールは何でもいいから、moduleなんて1つでいいでしょと思っているが...
    _ecu:pycanape.Module

    @classmethod
    def attention(self):
        display_msg.order_without_sound("CANapeで計測対象のレコードを有効にしましたか?")

    def prepare(self):
        config = configparser.ConfigParser()
        cwd = os.path.dirname(__file__)
        config.read(cwd + '/../config/config.ini', 'UTF-8')

        self.__class__._project_path = str(config['CANape_configuration']['PROJECT_PATH'])
        self.__class__._initialize_script_path = str(config['CANape_configuration']['INIT_SCRIPT'])
        self.__class__._routine_script_path = str(config['CANape_configuration']['SIMURATOR'])
        self.__class__._module = str(config['CANape_configuration']['CERTAIN_MODULE'])
        self.__class__._ecu = str(config['CANape_configuration']['XCP_MODULE'])

    def start(self):
        display_msg.order_without_sound("CANapeを起動します")
        self.__class__._canape = pycanape.CANape(
            project_path=self.__class__._project_path,
            modal_mode=True,
            clear_device_list=False,
        )
        self.__class__._module = self.__class__._canape.get_module_by_name(self.__class__._module)
        self.__class__._ecu = self.__class__._canape.get_module_by_name(self.__class__._ecu)

    def stop(self):
        self.__class__._canape.exit(close_canape=True)

    def prepare_measurment(self, additional_init_script_list:list[str]):
        default_init_script = self.__class__._module.execute_script_ex(True, self.__class__._initialize_script_path)
        default_init_script.start_script()
        # テストケース毎に追加で初期化処理したい場合はここで初期化される。空だったらforの中身は実行されない。
        for init_file in additional_init_script_list:
            if init_file == 'None':
                return
            init_s = self.__class__._module.execute_script_ex(True, init_file)
            init_s.start_script()

    def start_measurment(self):
        self._routine_script = self.__class__._module.execute_script_ex(True, self.__class__._routine_script_path)
        self._routine_script.start_script()
        self.__class__._ecu.switch_ecu_on_offline(online=True)

        # データ取得開始. CANapeプロジェクトの設定が期待通りであればレコーディングも開始される。
        self.__class__._canape.start_data_acquisition()

    def stop_measurement(self):
        # 終了処理
        ## データ取得&記録 停止
        self.__class__._canape.stop_data_acquisition()
        self.__class__._ecu.switch_ecu_on_offline(online=False)
        ## 定常実行のスクリプトを停止
        self._routine_script.stop_script()

import time
class DummyCANapeController(CANapeController):
    def attention(self):
        display_msg.order_with_sound("CANapeで計測対象のレコードを有効にしましたか? ★特にグローバル変数 漏れやすいので注意")

    def prepare(self):
        pass

    def start(self):
        display_msg.order_without_sound("CANapeを起動します")
        time.sleep(3)

    def stop(self):
        display_msg.order_without_sound("CANapeを停止します")

    def prepare_measurment(self, additional_init_script_list:list[str]):
        pass

    def start_measurment(self):
        display_msg.order_without_sound("CANape測定開始")

    def stop_measurement(self):
        display_msg.order_without_sound("CANape測定終了")
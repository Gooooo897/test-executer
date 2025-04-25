import subprocess
import os
from abc import ABC, abstractmethod
from enum import Enum
import configparser

from controller.abstruct_tool_controller import AbstructToolController
from testing_support_functions import display_testing_message as display_msg

class AbstructCheckerController(AbstructToolController):
    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def key_on(self):
        pass
    def key_off(self):
        pass

class ManualCheckerController(AbstructCheckerController):
    def prepare(self):
        pass

    def start(self):
        display_msg.ask_checker_sw_control("起動")
        # print("起動")

    def stop(self):
        display_msg.ask_checker_sw_control("停止")
        # print("停止")

    def key_on(self):
        display_msg.order_with_sound("KeyのみOnしてください")

    def key_off(self):
        display_msg.order_with_sound("KeyのみOffしてください")

class RelayCheckerController(AbstructCheckerController):
    def prepare(self):
        config = configparser.ConfigParser()
        cwd = os.path.dirname(__file__)
        config.read(cwd + '/../config/config.ini', 'UTF-8')

        bat_relative_path = str(config['relay_checker_control']['BAT_RELATIVE_PATH'])

        power_on_bat      = str(config['relay_checker_control']['POWER_ON_BAT'])
        key_on_bat        = str(config['relay_checker_control']['KEY_ON_BAT'])
        vis_on_bat        = str(config['relay_checker_control']['VIS_ON_BAT']) # Vis SWは最初からON側にしておけば、わざわざ操作する必要ないのでコメントアウト
        key_off_bat       = str(config['relay_checker_control']['KEY_OFF_BAT'])
        vis_off_bat       = str(config['relay_checker_control']['VIS_OFF_BAT'])
        power_off_bat     = str(config['relay_checker_control']['POWER_OFF_BAT'])

        self.power_on_bat_path  = os.path.join(os.path.dirname(__file__), bat_relative_path, power_on_bat)
        self.key_on_bat_path    = os.path.join(os.path.dirname(__file__), bat_relative_path, key_on_bat)
        self.vis_on_bat_path    = os.path.join(os.path.dirname(__file__), bat_relative_path, vis_on_bat)
        self.key_off_bat_path   = os.path.join(os.path.dirname(__file__), bat_relative_path, key_off_bat)
        self.vis_off_bat_path   = os.path.join(os.path.dirname(__file__), bat_relative_path, vis_off_bat)
        self.power_off_bat_path = os.path.join(os.path.dirname(__file__), bat_relative_path, power_off_bat)

    def start(self):
        display_msg.order_with_sound("リレー制御基板でチェッカーをPower On、Key On、Vis Onします。")
        bat_ret = subprocess.run([self.power_on_bat_path])
        bat_ret = subprocess.run([self.key_on_bat_path])
        bat_ret = subprocess.run([self.vis_on_bat_path])
        if bat_ret.returncode == 0:
            result = 0
        else:
            result = -1
        return result

    def stop(self):
        display_msg.order_with_sound("リレー制御基板でチェッカーをKey Off、Vis Off、Power Offします。")
        bat_ret = subprocess.run([self.key_off_bat_path])
        bat_ret = subprocess.run([self.vis_off_bat_path])
        bat_ret = subprocess.run([self.power_off_bat_path])
        if bat_ret.returncode == 0:
            result = 0
        else:
            result = -1
        return result

    def key_on(self):
        display_msg.order_with_sound("リレー制御基板でKey Onします。")
        bat_ret = subprocess.run([self.key_on_bat_path])
        return bat_ret

    def key_off(self):
        display_msg.order_with_sound("リレー制御基板でKey Offします。")
        bat_ret = subprocess.run([self.key_off_bat_path])
        return bat_ret

class CheckerController(Enum):
    Manual = ManualCheckerController
    Relay = RelayCheckerController

    @classmethod
    def create(self, control_type:str):
        for c in CheckerController:
            if control_type == c.name:
                return c.value()

if __name__ == "__main__":
    checker_controller:AbstructCheckerController = CheckerController.create("Manual")
    # checker_controller:AbstructCheckerController = CheckerController.create("Relay")
    checker_controller.prepare()
    checker_controller.start()
    input("状態を確認してください")
    checker_controller.stop()
    input("状態を確認してください")

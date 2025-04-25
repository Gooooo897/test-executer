from enum import Enum
from abc import ABC, abstractmethod
import pycanape
import openpyxl as opx
import cv2

import os,sys
sys.path.append(os.path.join(os.getcwd(), ".."))
from testing_support_functions import common_tool as ct
from controller.checker_controller import AbstructCheckerController

class AbstructTestSenarioFormat(ABC):
    wb:opx.Workbook
    header_row:int

    def __init__(self, wb:opx.Workbook) -> None:
        super().__init__()
        AbstructTestSenarioFormat.wb = wb
        AbstructTestSenarioFormat.header_row = 1

    @abstractmethod
    def extract_workers(self, excel_row_data:dict):
        pass

class HorizontalTestSenarioFormat(AbstructTestSenarioFormat):
    def __init__(self, wb:opx.Workbook) -> None:
        super().__init__(wb)

    def extract_workers(self, excel_row_data:dict)->list:
        worker_list:list[AbstractWorker] = []
        i = 1
        while True:
            command_key_name = "input" + str(i)
            interval_key_name = "standby time" + str(i) + "[s]"
            commands_str:str = excel_row_data.get(command_key_name, None)
            interval_time_s = excel_row_data.get(interval_key_name, None)
            if commands_str == None or interval_time_s == None: # セルの中身が空またはキーがない場合はNone
                break
            command_list = commands_str.split('\n')
            worker:AbstractWorker = Worker.create(w_type=command_list[0], commands=command_list[1:],interval_time=interval_time_s)
            worker_list.append(worker)
            i += 1

        return worker_list

class VerticalTestSenarioFormat(AbstructTestSenarioFormat):
    def __init__(self, wb:opx.Workbook) -> None:
        super().__init__(wb)

    def extract_workers(self, test_suite_sheet_row_data:dict)->list:
        # 別シートの情報を取得する必要がある。
        test_case_sheet_name = test_suite_sheet_row_data.get("ref sheet name", None)
        if test_case_sheet_name == None:
            return None
        excel_row_data_list:list[dict] = ct.read_excel_data(
            VerticalTestSenarioFormat.wb,
            test_case_sheet_name,
            AbstructTestSenarioFormat.header_row
        )

        worker_list:list[AbstractWorker] = []
        for excel_row_data in excel_row_data_list:
            command_key_name = "input"
            interval_key_name = "standby time[s]"
            commands_str = excel_row_data.get(command_key_name, None)
            interval_time_s = excel_row_data.get(interval_key_name, None)
            if commands_str == None or interval_time_s == None: # セルの中身が空またはキーがない場合はNone
                break
            command_list = commands_str.split('\n')
            worker:AbstractWorker = Worker.create(w_type=command_list[0], commands=command_list[1:],interval_time=interval_time_s)
            worker_list.append(worker)

        return worker_list

class TestSenario(Enum):
    horizontal = HorizontalTestSenarioFormat
    vertical = VerticalTestSenarioFormat

    @classmethod
    def create(self, wb:opx.Workbook, test_senario_format_type:str):
        for m in TestSenario:
            if test_senario_format_type == m.name:
                return m.value(wb)


class AbstractWorker(ABC):
    def __init__(self, commands, interval_time_s) -> None:
        super().__init__()
        self.commands = commands
        self.interval_s = interval_time_s

    @abstractmethod
    def start_work(self) -> str:
        pass
        return 0

    def sleep(self):
        time.sleep(self.interval_s)

from tkinter import messagebox
import time

class ManualWorker(AbstractWorker):
    def __init__(self, commands, interval_time_s) -> None:
        super().__init__(commands, interval_time_s)
    def start_work(self) -> None:
        for command in self.commands:
            return messagebox.askquestion("手順", command)

class CanapeWorker(AbstractWorker):
    module:pycanape.Module

    def __init__(self, commands, interval_time_s, script_flag) -> None:
        super().__init__(commands, interval_time_s)
        self.flag = script_flag

    def set_module_object(mod:pycanape.Module):
        CanapeWorker.module = mod

    def start_work(self) -> None:
        if CanapeWorker.module == None:
            raise ValueError("No canape object is set.")
        for command in self.commands:
            single_script = CanapeWorker.module.execute_script_ex(self.flag, str(command))
            single_script.start_script()
        return None


class GlobalValuableCanapeWorker(CanapeWorker):
    def __init__(self, commands, interval_time_s) -> None:
        super().__init__(commands, interval_time_s, False)

class ScriptCanapeWorker(CanapeWorker):
    def __init__(self, commands, interval_time_s) -> None:
        super().__init__(commands, interval_time_s, True)

class BatWorker(AbstractWorker):
    def __init__(self, commands, interval_time_s) -> None:
        super().__init__(commands, interval_time_s)
    def start_work(self) -> None:
        pass #まだ実装しなくていい
        return None

class PycanSendWorker(AbstractWorker):
    def __init__(self, commands, interval_time_s) -> None:
        super().__init__(commands, interval_time_s)
    def start_work(self) -> None:
        pass #まだ実装しなくていい
        return None

class CameraWorker(AbstractWorker):
    _log_path:str

    def __init__(self, commands, interval_time_s):
        super().__init__(commands, interval_time_s)
    def start_work(self) -> None:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret == False:
            print("Cameraが他に使われている可能性あり")
            return
        file_name = self.commands[0] + ".png"
        file_path = os.path.join(self.__class__._log_path, file_name)
        ret = cv2.imwrite(file_path, frame)
        return None
    @classmethod
    def prepare(cls, path:str):
        os.makedirs(path, exist_ok=True)
        cls._log_path = path

class NoCameraWorker(CameraWorker):
    def __init__(self, commands, interval_time_s):
        super().__init__(commands, interval_time_s)
    def start_work(self) -> None:
        return None

class KeyWorker(AbstractWorker):
    def __init__(self, commands, interval_time_s):
        super().__init__(commands, interval_time_s)
    def start_work(self):
        for c in self.commands:
            if c == "key_on":
                self.__class__._controller.key_on()
            elif c == "key_off":
                self.__class__._controller.key_off()
            else:
                print("入力エラー")
    @classmethod
    def set_checker_controller(cls, controller:AbstractWorker):
        cls._controller:AbstructCheckerController = controller

class Worker(Enum):
    manual = ManualWorker
    canape_g = GlobalValuableCanapeWorker
    canape_s= ScriptCanapeWorker
    bat= BatWorker
    pycan_send= PycanSendWorker
    camera = CameraWorker
    # camera = NoCameraWorker
    checker_sw = KeyWorker

    @classmethod
    def create(self, w_type:str, commands, interval_time):
        for w in Worker:
            if w.name == w_type:
                return w.value(commands, interval_time)
        raise ValueError('{} is not valide value of worker type.'.format(w_type))

if __name__ == "__main__":
    CameraWorker.prepare(r"C:\Users\<user_name>\Desktop\temp\img")
    c = Worker.create("camera", ["data2"], 3)
    c.start_work()
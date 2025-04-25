from enum import Enum

from controller import canape_controller, checker_controller

class ToolController(Enum):
    CANapeControl = canape_controller.CANapeController
    ManualCheckerControl = checker_controller.ManualCheckerController
    RelayCheckerControl = checker_controller.RelayCheckerController

    @classmethod
    def create(self, control_type:str):
        for c in ToolController:
            if control_type == c.name:
                return c.value()
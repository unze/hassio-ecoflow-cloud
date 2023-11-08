from typing import Any

from . import BaseDevice, const
from .. import EcoflowMQTTClient
from ..entities import BaseSensorEntity, BaseNumberEntity, BaseSwitchEntity, BaseSelectEntity
from ..select import DictSelectEntity
from ..sensor import OutWattsSensorEntity, InWattsSensorEntity, LevelSensorEntity, \
    RemainSensorEntity

MODES = {
    "Auto": {"sta": 0, "ctrl_mode": 0},
    "Grid": {"sta": 0, "ctrl_mode": 1},
    "Battery": {"sta": 1, "ctrl_mode": 1},
    "Off": {"sta": 2, "ctrl_mode": 1}
}


class ModeDictSelectEntity(DictSelectEntity):

    def __init__(self, client: EcoflowMQTTClient, n: int):
        super().__init__(client, "loadCmdChCtrlInfos[%i]" % n, const.SHP_CIRCUIT_N_MODE % (n + 1), MODES,
                         lambda value: {"sta": value.sta, "ctrlMode": value.ctrl_mode, "ch": 0, "cmdSet": 11, "id": 16})

    def _update_value(self, val: Any) -> bool:
        return super()._update_value({"sta": val.sta, "ctrl_mode": val.ctrlMode})


class SmartHomePanel(BaseDevice):

    def sensors(self, client: EcoflowMQTTClient) -> list[BaseSensorEntity]:
        res = [
            LevelSensorEntity(client, "energyInfos[0].batteryPercentage", const.SHP_AC_N_BATTERY_LEVEL % 1),
            OutWattsSensorEntity(client, "energyInfos[0].outputPower", const.SHP_AC_N_OUT_POWER % 1),
            InWattsSensorEntity(client, "energyInfos[0].lcdInputWatts", const.SHP_AC_N_IN_POWER % 1),
            RemainSensorEntity(client, "energyInfos[0].chargeTime", const.SHP_AC_N_CHARGE_TIME % 1),
            RemainSensorEntity(client, "energyInfos[0].dischargeTime", const.SHP_AC_N_DISCHARGE_TIME % 1),

            LevelSensorEntity(client, "energyInfos[1].batteryPercentage", const.SHP_AC_N_BATTERY_LEVEL % 2),
            OutWattsSensorEntity(client, "energyInfos[1].outputPower", const.SHP_AC_N_OUT_POWER % 2),
            InWattsSensorEntity(client, "energyInfos[1].lcdInputWatts", const.SHP_AC_N_IN_POWER % 2),
            RemainSensorEntity(client, "energyInfos[1].chargeTime", const.SHP_AC_N_CHARGE_TIME % 2),
            RemainSensorEntity(client, "energyInfos[1].dischargeTime", const.SHP_AC_N_DISCHARGE_TIME % 2),
        ]

        return res

    def numbers(self, client: EcoflowMQTTClient) -> list[BaseNumberEntity]:
        return [

        ]

    def switches(self, client: EcoflowMQTTClient) -> list[BaseSwitchEntity]:
        return [

        ]

    def selects(self, client: EcoflowMQTTClient) -> list[BaseSelectEntity]:
        res = []
        res.extend(self.generate_mode_selects(client))

        return res

    def generate_power_sensors(self, client: EcoflowMQTTClient) -> list[BaseSensorEntity]:
        res = []
        for i in range(0, 11):
            res.append(InWattsSensorEntity(client, "infoList[%i].chWatt", const.SHP_CIRCUIT_N_POWER % (i + 1)))
        return res


    def generate_mode_selects(self, client: EcoflowMQTTClient) -> list[DictSelectEntity]:
        res = []
        for i in range(0, 10):
            res.append(ModeDictSelectEntity(client, i))
        return res

#!/usr/bin/env python3
# encoding: utf-8
# ===============================================================================
#
#         FILE:  
#
#        USAGE:    
#
#  DESCRIPTION:  
#
#      OPTIONS:  ---
# REQUIREMENTS:  ---
#         BUGS:  ---
#        NOTES:  ---
#       AUTHOR:  YOUR NAME (), 
#      COMPANY:  
#      VERSION:  1.0
#      CREATED:  
#     REVISION:  ---
# ===============================================================================
import serial
from typing import Tuple

class FmModules(object):
    def __init__(self, port: str = "/dev/serial0", baudrate: int = 38400, timeout: int = 1):
        self._ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        # 清空输入缓冲区
        self._ser.flushInput()

    def fre_set_to(self, value: int) -> str:
        self._ser.flushInput()
        cmd = ("AT+FRE=%d" % value).encode() + b"\r\n"
        self._ser.write(cmd)
        ret = self._ser.readlines()[0].decode().replace("\r\n", "")
        # print(ret)
        return ret
    
    def vol_set_to(self, value: int) -> str:
        self._ser.flushInput()
        if value < 0:
            value = 0
        if value > 30:
            value = 30
        cmd = ("AT+VOL=%02d" % value).encode() + b"\r\n"
        self._ser.write(cmd)
        ret = self._ser.readlines()[0].decode().replace("\r\n", "")
        # print(ret)
        return ret
    
    def _fre_wheel(self, modify: str) -> str:
        self._ser.flushInput()
        if modify.lower() not in ["up", "down"]:
            modify = "up"
        if modify == "up":
            cmd = "AT+FREU".encode() + b"\r\n"
        else:
            cmd = "AT+FRED".encode() + b"\r\n"
        self._ser.write(cmd)
        ret = self._ser.readlines()[0].decode().replace("\r\n", "")
        # print(ret)
        return ret

    def fre_up(self) -> str:
        return self._fre_wheel("up")
    
    def fre_down(self) -> str:
        return self._fre_wheel("down")

    def _vol_wheel(self, modify: str) -> str:
        self._ser.flushInput()
        if modify.lower() not in ["up", "down"]:
            modify = "up"
        if modify == "up":
            cmd = "AT+VOLU".encode() + b"\r\n"
        else:
            cmd = "AT+VOLD".encode() + b"\r\n"
        self._ser.write(cmd)
        ret = self._ser.readlines()[0].decode().replace("\r\n", "")
        # print(ret)
        return ret

    def vol_up(self) -> str:
        return self._vol_wheel("up")
    
    def vol_down(self) -> str:
        return self._vol_wheel("down")
    
    def set_status(self, status: str = "play") -> str:
        status = status.upper()
        if status not in ["PLAY", "PAUS"]:
            return "ERR"
        info = self.get_info()
        status_now = info[2]
        if status == status_now:
            return status
        self._ser.flushInput()
        cmd = "AT+PAUS".encode() + b"\r\n"
        # print(cmd)
        self._ser.write(cmd)
        ret = self._ser.readlines()
        # print(ret)
        info = self.get_info()
        # print(info)
        return info[2]

    def get_info(self) -> Tuple[str]:
        self._ser.flushInput()
        cmd = "AT+RET".encode() + b"\r\n"
        self._ser.write(cmd)
        ret = self._ser.readlines()
        # print(ret)
        vol = ret[1].decode().replace("\r\n", "")
        fre = ret[2].decode().replace("\r\n", "")
        status = ret[3].decode().replace("\r\n", "")
        bank = ret[4].decode().replace("\r\n", "")
        campos_status = ret[5].decode().replace("\r\n", "")
        # print("{}, {}, {}, {}, {}".format(vol, fre, status, bank, campos_status))
        return vol, fre, status, bank, campos_status
    
    def set_bank(self, value: int = 20, alway_on: bool = False, alway_off: bool = False):
        if alway_on is True or alway_off is True:
            # check detail
            if alway_on is True and alway_off is False:
                value = 1
            else:
                value = 0
        self._ser.flushInput()
        if value < 0:
            value = 0
        if value > 99:
            value = 99
        cmd = ("AT+BANK=%02d" % value).encode() + b"\r\n"
        self._ser.write(cmd)
        ret = self._ser.readlines()[0].decode().replace("\r\n", "")
        # print(ret)
        return ret

    def factory_reset(self):
        self._ser.flushInput()
        cmd = "AT+CR".encode() + b"\r\n"
        self._ser.write(cmd)
        ret = self._ser.readlines()[0].decode().replace("\r\n", "")
        return ret


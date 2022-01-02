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
import unittest
from os import environ

from fm import FmModules

class TestFmModules(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        port = environ.get("TEST_SER_PORT", "/dev/serial0")
        baudrate = int(environ.get("TEST_SER_BAUDRATE", "38400"))
        timeout = int(environ.get("TEST_SER_TIMEOUT", "1"))
        # print("Test use port: %s, baudrate: %s, timeout: %s" % (port, baudrate, timeout))
        self.fm = FmModules(port=port, baudrate=baudrate, timeout=timeout)
        self.fm.get_info()

    def test_fre_set_to(self):
        ret = self.fm.fre_set_to(1037)
        self.assertEqual(ret, "FRE=1037", msg="Test set fre to 103.7")
    
    def test_fre_up(self):
        self.fm.fre_set_to(1037)
        ret = self.fm.fre_up()
        self.assertEqual(ret, "FRE=1038", msg="Test fre up from 103.7")
    
    def test_fre_down(self):
        self.fm.fre_set_to(1037)
        ret = self.fm.fre_down()
        self.assertEqual(ret, "FRE=1036", msg="Test fre down from 103.7")

    def test_vol_set_to(self):
        ret = self.fm.vol_set_to(-1)
        self.assertEqual(ret, "VOL=00")
        ret = self.fm.vol_set_to(31)
        self.assertEqual(ret, "VOL=30")
        ret = self.fm.vol_set_to(29)
        self.assertEqual(ret, "VOL=29")

    def test_vol_up(self):
        self.fm.vol_set_to(1)
        ret = self.fm.vol_up()
        self.assertEqual(ret, "VOL=02")
        ret = self.fm.vol_up()
        self.assertEqual(ret, "VOL=03")
        ret = self.fm.vol_up()
        self.assertEqual(ret, "VOL=04")
        self.fm.vol_set_to(29)
        ret = self.fm.vol_up()
        self.assertEqual(ret, "VOL=30")
        ret = self.fm.vol_up()
        self.assertEqual(ret, "VOL=30")
        self.fm.vol_set_to(20)

    def test_vol_down(self):
        self.fm.vol_set_to(30)
        ret = self.fm.vol_down()
        self.assertEqual(ret, "VOL=29")
        ret = self.fm.vol_down()
        self.assertEqual(ret, "VOL=28")
        ret = self.fm.vol_down()
        self.assertEqual(ret, "VOL=27")
        self.fm.vol_set_to(1)
        ret = self.fm.vol_down()
        self.assertEqual(ret, "VOL=00")
        ret = self.fm.vol_down()
        self.assertEqual(ret, "VOL=00")
        self.fm.vol_set_to(20)

    def test_set_bank(self):
        self.fm.vol_set_to(20)
        self.fm.set_status("play")
        self.fm.fre_set_to(1017)
        ret = self.fm.set_bank(10)
        self.assertEqual(ret, "BANK=10s")
        ret = self.fm.set_bank(20)
        self.assertEqual(ret, "BANK=20s")
        ret = self.fm.set_bank(99)
        self.assertEqual(ret, "BANK=99s")
        ret = self.fm.set_bank(990099)
        self.assertEqual(ret, "BANK=99s")
        ret = self.fm.set_bank(-1)
        self.assertEqual(ret, "BANK_OFF")
        ret = self.fm.set_bank(2)
        self.assertEqual(ret, "BANK=02s")
        ret = self.fm.set_bank(20, alway_on=True, alway_off=True)
        self.assertEqual(ret, "BANK_OFF")
        ret = self.fm.set_bank(20, alway_on=True, alway_off=False)
        self.assertEqual(ret, "BANK_ON")
        ret = self.fm.set_bank(20, alway_on=False, alway_off=True)
        self.assertEqual(ret, "BANK_OFF")
        ret = self.fm.set_bank(20, alway_on=False, alway_off=False)
        self.assertEqual(ret, "BANK=20s")
    
    def test_set_status(self):
        self.fm.vol_set_to(20)
        ret = self.fm.set_status("play1")
        self.assertEqual(ret, "ERR")
        ret = self.fm.set_status("play")
        info = self.fm.get_info()
        self.assertEqual(ret, info[2])
        ret = self.fm.set_status("play")
        info = self.fm.get_info()
        self.assertEqual(ret, info[2])
        ret = self.fm.set_status("play")
        info = self.fm.get_info()
        self.assertEqual(ret, info[2])
        ret = self.fm.set_status("paus")
        info = self.fm.get_info()
        self.assertEqual(ret, info[2])
        ret = self.fm.set_status("paus")
        info = self.fm.get_info()
        self.assertEqual(ret, info[2])
        ret = self.fm.set_status("paus")
        info = self.fm.get_info()
        self.assertEqual(ret, info[2])
        ret = self.fm.set_status("play")
        info = self.fm.get_info()
        self.assertEqual(ret, info[2])
        ret = self.fm.set_status("paus")
        info = self.fm.get_info()
        self.assertEqual(ret, info[2])
        ret = self.fm.set_status("play")
        info = self.fm.get_info()
        self.assertEqual(ret, info[2])
        ret = self.fm.set_status("paus")
        info = self.fm.get_info()
        self.assertEqual(ret, info[2])
        ret = self.fm.set_status("play")
        info = self.fm.get_info()
        self.assertEqual(ret, info[2])
        ret = self.fm.set_status("paus")
        info = self.fm.get_info()
        self.assertEqual(ret, info[2])
        self.fm.set_status("play")


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # same as
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestFmModules)
    # unittest.TextTestRunner(verbosity=2).run(suite)

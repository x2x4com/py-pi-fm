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
from fm import FmModules

# TODO: Here is business code

radio = FmModules(port="/dev/serial0", baudrate=38400, timeout=1)
print(radio.get_info())

print(radio.factory_reset())

print(radio.get_info())

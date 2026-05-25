#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
#
"""OpusLib Package."""

import ctypes  # type: ignore
import os

try:
    dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "libopus.dll"))
    libopus = ctypes.cdll.LoadLibrary(dll_path)
except OSError as e:
    raise RuntimeError(f"[!] Failed to load libopus DLL from __init__.py: {dll_path}\n{e}")

# ctypes pointer 타입들 정의
c_int_pointer = ctypes.POINTER(ctypes.c_int)
c_int16_pointer = ctypes.POINTER(ctypes.c_int16)
c_float_pointer = ctypes.POINTER(ctypes.c_float)

__author__ = 'Никита Кузнецов <self@svartalf.info>'
__copyright__ = 'Copyright (c) 2012, SvartalF'
__license__ = 'BSD 3-Clause License'


if __name__ == '__main__':
    print(dll_path)
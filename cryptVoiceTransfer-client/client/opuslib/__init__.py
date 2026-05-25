import ctypes
import os
from .exceptions import OpusError

# DLL 경로 고정
a = os.path.join(os.path.dirname(__file__), '..\libopus-0.dll')
# print(a)
dll_path = a

#dll_path = r"C:\Users\SY\Desktop\Project\src\libopus-0.dll"
libopus = ctypes.cdll.LoadLibrary(dll_path)

# 예시 함수 바인딩
def opus_encoder_get_size(channels):
    libopus.opus_encoder_get_size.argtypes = [ctypes.c_int]
    libopus.opus_encoder_get_size.restype = ctypes.c_int
    return libopus.opus_encoder_get_size(channels)



APPLICATION_AUDIO = 2049
APPLICATION_VOIP = 2048
APPLICATION_RESTRICTED_LOWDELAY = 2051


OK = 0
BAD_ARG = -1
UNIMPLEMENTED = -5

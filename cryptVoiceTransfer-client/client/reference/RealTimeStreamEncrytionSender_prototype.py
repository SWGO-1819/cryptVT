import pyaudio
import socket
from Crypto.Cipher import AES # type: ignore
from Crypto.Random import get_random_bytes # type: ignore
from Crypto.Util import Counter # type: ignore
import hashlib


# 마이크 설정값
FORMAT = pyaudio.paInt24
CHANNELS = 1
RATE = 48000
CHUNK = 1200
UDP_IP = "192.168.1.53"
UDP_PORT = 8080
INPUT_DEVICE_INDEX = 1


# PyAudio 초기화
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=INPUT_DEVICE_INDEX,
                frames_per_buffer=CHUNK)


# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("실시간 송신 시작")


# 암호화 키 설정(서버에서 송신측과 동일한 키 받음)
PASSWORD = b"koreapolytechnic" # 16바이트
KEY = hashlib.sha256(PASSWORD).digest() # 32바이트
# print(len(bytearray(KEY)))


# AES CTR 모드 설정
# nonce는 송신측에서 생성하여 수신측으로 전송
# 암호화하여 전송해야하지만 nonce는 암호화하지 않음
nonce = get_random_bytes(8)
ctr = Counter.new(64, prefix=nonce)
cipher = AES.new(KEY, AES.MODE_CTR, counter=ctr)


# 첫 패킷에 nonce 전송(복호화에 필요) / CBC 모드에서는 IV 전송하지만 CTR 모드에서는 nonce 전송 / 용어만 다를 뿐 비슷한 역할임
sock.sendto(nonce, (UDP_IP, UDP_PORT))
# print(f"nonce: {nonce}")


try:
    # 송신 루프
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        print(type(data), len(data))
        encrypted = cipher.encrypt(data)
        sock.sendto(encrypted, (UDP_IP, UDP_PORT))


# 키보드 인터럽트 발생 시 b"__END__" 신호 송신
except KeyboardInterrupt:
    sock.sendto(b"__END__", (UDP_IP, UDP_PORT))
    print("키보드 인터럽트 발생")


# 송신 종료 및 리소스 해제 완료
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    sock.close()
    print("송신 종료 및 리소스 해제 완료")
import socket
import pyaudio

# 마이크 설정값
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
CHUNK = 1200
UDP_IP = "127.0.0.1"
UDP_PORT = 8080
INPUT_DEVICE_INDEX = 1

# PyAudio & UDP 초기화
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=INPUT_DEVICE_INDEX,
                frames_per_buffer=CHUNK)

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# A = b'\x01\x02\x03\x04\x05\x06\x07\x08'
print("실시간 송신 시작")

# sock.sendto(A, (UDP_IP, UDP_PORT)) # 암호화 여부 확인용 0

# 송신 루프
try:
    while True:
        data = stream.read(CHUNK)
        sock.sendto(data, (UDP_IP, UDP_PORT))
        # sock.sendto(A, (UDP_IP, UDP_PORT)) # 암호화 여부 확인용 0
except KeyboardInterrupt:
    print("키보드 인터럽트")
    sock.sendto(b"__END__", (UDP_IP, UDP_PORT))

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    sock.close()
    # print("송신 종료 및 리소스 해제 완료")

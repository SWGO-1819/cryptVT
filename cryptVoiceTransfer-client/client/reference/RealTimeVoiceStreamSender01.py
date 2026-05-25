# 파일 수신
# UDP_cli.py

import socket
import pyaudio
# 설정값 정의(아직은 정적) >>> 이후에 입력값에 맞게 적용하는 방식(동적)으로 변경할 예정
FORMAT = pyaudio.paInt32  # 16비트 PCM <<< 일반적인 mic
CHANNELS = 2  # 스테레오 # 1 = mono, 2 = stereo
RATE = 44100    # 샘플링 레이트 # 44.1kHz <<< 일반적인 mic
CHUNK = 1024  # 실시간 & 안정성 고려해서 441로 설정하면 10.0ms 단위로 읽기
INPUT_DEVICE_INDEX = 1  # 사용 가능한 마이크 인덱스로 설정

# PyAudio 객체 생성
p = pyaudio.PyAudio()


# 입력 스트림 열기
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=INPUT_DEVICE_INDEX,
                frames_per_buffer=CHUNK)

UDP_IP = "127.0.0.1"
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
try :

    # 파일 열기 및 전송
    while True:
        data = stream.read(CHUNK)
        sock.sendto(data, (UDP_IP, UDP_PORT))

except KeyboardInterrupt as e:
    print("Error: 키보드 인터럽트", e)


finally:
    sock.sendto(b"__END__", (UDP_IP, UDP_PORT))
    sock.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
    sock.close()
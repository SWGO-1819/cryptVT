import socket
import pyaudio

# 오디오 설정
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
CHUNK = 1200
UDP_IP = "127.0.0.1"
UDP_PORT = 8080

# PyAudio 초기화
p = pyaudio.PyAudio()
stream_out = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"실시간 재생 중... UDP {UDP_PORT} 포트에서 수신 대기 중")

# 실시간 수신 + 재생 루프
while True:
    data, _ = sock.recvfrom(CHUNK * 4)

    if data == b"__END__":
        print("송신 종료 감지")
        break

    # 바로 재생
    stream_out.write(data)

# 종료 정리

stream_out.stop_stream()
stream_out.close()
p.terminate()
sock.close()

print("스트리밍 종료 및 리소스 해제 완료")

import socket
import wave
import pyaudio
# 설정값 정의(아직은 정적) >>> 이후에 입력값에 맞게 적용하는 방식(동적)으로 변경할 예정
FORMAT = pyaudio.paInt32  # 16비트 PCM <<< 일반적인 mic
CHANNELS = 2  # 스테레오 # 1 = mono, 2 = stereo
RATE = 44100    # 샘플링 레이트 # 44.1kHz <<< 일반적인 mic
CHUNK = 4096  # 실시간 & 안정성 고려해서 441로 설정하면 10.0ms 단위로 읽기
INPUT_DEVICE_INDEX = 1  # 사용 가능한 마이크 인덱스로 설정
UDP_IP = ""   # 모든 인터페이스에서 수신
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print("Receiver is listening on port", UDP_PORT)


p = pyaudio.PyAudio()
stream_out = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)        


# 실시간 수신 + 재생 루프
try :
    while True:
        data, _ = sock.recvfrom(CHUNK*2)  # 수신 버퍼 크기와 일치하도록 설정

        if data == b"__END__":
            print("송신 종료 감지")
            break

        # 바로 재생
        stream_out.write(data)

except Exception as e:
    print("Error:", e)

finally :   
    # 종료 정리
    stream_out.stop_stream()
    stream_out.close()
    p.terminate()
    sock.close()

    print("스트리밍 종료 및 리소스 해제 완료")

    sock.close()
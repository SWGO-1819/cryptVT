import pyaudio
import socket
from Crypto.Cipher import AES # type: ignore
from Crypto.Util import Counter # type: ignore
import hashlib


# 스피커 설정값
FORMAT = pyaudio.paInt24 # paINT24 바꿀 때 해당 바이트만큼 리시브 버퍼 사이즈 변경 필요!!!
CHANNELS = 2
RATE = 48000
CHUNK = 1200
UDP_IP = "127.0.0.1"
UDP_PORT = 8080


# PyAudio 초기화
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)


# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"실시간 재생 중... UDP {UDP_PORT} 포트에서 수신 대기 중")


# 암호화 키 설정(서버에서 송신측과 동일한 키 받음)
PASSWORD = b"koreapolytechnic" # 16바이트
KEY = hashlib.sha256(PASSWORD).digest() # 32바이트


# AES CTR 모드 설정
# nonce는 송신측에서 생성하여 수신측으로 전송
# 송신측에서 nonce를 전송했으므로 수신측에서는 nonce를 수신하여 암호화 해제에 사용
# nonce는 암호화하지 않음(추후 서버에서 키 받으면 nonce도 암호화하여 전송 계획)
nonce, _ = sock.recvfrom(8) # nonce 수신
ctr = Counter.new(64, prefix=nonce)
cipher = AES.new(KEY, AES.MODE_CTR, counter=ctr)


try:
    # 실시간 수신 + 재생 루프
    while True:
        data, _ = sock.recvfrom(CHUNK * CHANNELS * 3) # 2채널, 24비트(3바이트) PCM이므로 CHUNK * CHANNELS * 3 바이트 수신

        # 송신 종료 신호(b"__END__") 수신시 종료
        if data == b"__END__": 
            print("송신 종료 감지")
            break

        # 바로 재생
        decrypted = cipher.decrypt(data)
        stream.write(decrypted)


# 키보드 인터럽트 발생 시 종료
except KeyboardInterrupt :
    print("키보드 인터럽트 발생")


# 수신 종료 및 리소스 해제
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    sock.close()
    print("수신 종료 및 리소스 해제 완료")
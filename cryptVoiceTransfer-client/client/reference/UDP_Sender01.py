import socket
import time
import os

UDP_IP = "192.168.1.15"  # 수신자 IP 주소
UDP_PORT = 8080
BUF_SIZE = 1024

file_path = 'C:/Users/SY2/output.wav'
file_name = os.path.basename(file_path)

print('Sending file:', file_name)

try:
    # 소켓 생성
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 파일 이름 전송
    sock.sendto(file_name.encode(), (UDP_IP, UDP_PORT))

    # 파일 열기 및 전송
    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sock.sendto(data, (UDP_IP, UDP_PORT))
            time.sleep(0.02)  # 수신자 처리 시간 확보

    # 파일 전송 종료 신호
    sock.sendto(b"__END__", (UDP_IP, UDP_PORT))

    print("File sent successfully.")

except Exception as e:
    print("Error:", e)

finally:
    sock.close()

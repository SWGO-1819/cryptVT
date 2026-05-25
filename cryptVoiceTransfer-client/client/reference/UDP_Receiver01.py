import socket

UDP_IP = ""   # 모든 인터페이스에서 수신
UDP_PORT = 8080
BUF_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Receiver is listening on port", UDP_PORT)

# 첫 번째 패킷은 파일 이름
file_name_bytes, addr = sock.recvfrom(BUF_SIZE)
file_name = file_name_bytes.decode(errors="ignore")
print("Receiving file:", file_name)

# 저장 경로 (현재 폴더에 저장)
save_path = "./received_" + file_name

with open(save_path, "wb") as f:
    while True:
        data, addr = sock.recvfrom(BUF_SIZE)
        if data == b"__END__":
            print("File transfer complete.")
            break
        f.write(data)

sock.close()
print("Saved as:", save_path)

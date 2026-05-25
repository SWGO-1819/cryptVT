import pyaudio
import socket
from Crypto.Cipher import AES # type: ignore
from Crypto.Util import Counter # type: ignore
from Crypto.Random import get_random_bytes # type: ignore
import hashlib
import queue
import client.RealTimeGUIandRollback as roll
import client.OpusCodec as opus
import json
import socketio

class encryptVar :
    def __init__(self):
        """
        self.nonce= nonce 설정
        self.cipher = cipher 설정
        """
        # 암호화 키 설정(서버에서 송신측과 동일한 키 받음)
        PASSWORD = b"koreapolytechnic" # 16바이트
        self.KEY = hashlib.sha256(PASSWORD).digest() # 32바이트
        self.nonce = get_random_bytes(8)
        #self.nonce=None
    def cipherSet(self,nonce) :
        self.nonce=nonce
        ctr = Counter.new(64, prefix=nonce)
        cipher = AES.new(self.KEY, AES.MODE_CTR, counter=ctr)
        return cipher

class EncrytSend() :
    """
    실시간 송신 암호화.
    UDP_IP : Destination IP Addr
    UDP_PORT : Destination PORT Addr
    CHANNELS : 음성(마이크) 채널
    nonce = 암호화 CTR에 같이쓸 nonce추가
    """
    def __init__(self,UDP_IP="",UDP_PORT=5060,CHANNELS=1,nonce=b""):
        self.UDP_IP=UDP_IP
        self.UDP_PORT=UDP_PORT
        self.CHANNELS=CHANNELS
        self.FORMAT = pyaudio.paInt16 # paINT24 바꿀 때 해당 바이트만큼 리시브 버퍼 사이즈 변경 필요!!!
        self.RATE = 48000
        self.CHUNK = 960
        self.INPUT_DEVICE_INDEX = 1
        # UDP 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._buff = queue.Queue()
        print("실시간 송신 시작")
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        input_device_index=self.INPUT_DEVICE_INDEX,
                        frames_per_buffer=self.CHUNK, 
                        stream_callback=self.mic_callback)
        #self.cipher
        
        # PyAudio 초기화
        #sock.sendto(nonce, (self.UDP_IP, self.UDP_PORT))
    def mic_callback(self,in_data, frame_count, time_info, status):
        """마이크로부터 들어온 오디오 데이터를 처리하는 콜백 함수."""
        
        if status == pyaudio.paInputOverflow:
            print("[⚠️ 오버플로우] 무음으로 대체")
            silent = b'\x00' * 1200 * self.CHANNELS * 3  # 3: 24bit = 3bytes
            self._buff.put(silent)
        else:
            self._buff.put(in_data)
        return (None, pyaudio.paContinue)


    def SendStart(self,buff,cipher) :
        if self.UDP_IP != "" :
            try:
                while True:  # 큐에 데이터 다 처리
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock :
                        #ip=socket.gethostbyname(socket.gethostname())
                        #print("ip : "+str(ip))
                        data = buff.get_nowait()
                        #opus추가
                        encoder = opus.OpusEncoder(rate=self.RATE, channels=self.CHANNELS, frame_size=self.CHUNK)
                        data=encoder.encode(data)
                        #print(data)
                        # 👉 여기에 AES 복호화 / Opus 디코딩 / GUI 표시 등
                        encrypted = cipher.encrypt(data)
                        sock.sendto(encrypted, ("192.168.125.134", 8080))
            except queue.Empty:
                pass
    def SendPreparation(self,id,myid,enc):
        try:
            #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :
                # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
                # payload = {
                #     "type":"CALL_START",
                #     "id": id,
                #     "myid":myid
                # }
                #s.setblocking(True) #로그인 성공 후 클라이언트에게 전송
                #s.settimeout(5)
                #s.connect(("192.168.125.134", 34567))  # 연결 먼저
                # s.sendall(json.dumps(payload).encode())
                # s.close()
            sio = socketio.Client()
            sio.connect("http://192.168.125.134:34567",transports=["websocket"])
            sio.emit("call_start",{"id1":id,"id2":myid})
            
            @sio.on('call_start')
            def nonce_set(nonce) :
                print(type(nonce))
                enc.cipherSet(bytes(nonce))

        except socket.timeout:
            print("⛔ 서버로부터 응답이 없습니다.")
            return False
        except Exception as e:
            print(f"에러 발생: {e}")
            return False

    def RecStart(self):
        #with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock :

            try:
                data, _ = self.sock.recv(self.CHUNK * self.CHANNELS * 2)
            except BlockingIOError:
                return True
            if data == b"__END__":
                print("송신 종료 감지")
                return False
            #enc=encryptVar()
            #cipher=enc.cipherSet(nonce)
            #opus추가
            decoder = opus.OpusDecoder(rate=self.RATE, channels=self.CHANNELS)
            #data=decoder.decode(data)

            #decrypted = cipher.decrypt(data)
            self.stream.write(data)
            print("수신 중")
            return True
    

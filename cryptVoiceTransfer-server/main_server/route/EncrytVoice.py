import socket
import queue
import json
import time
class EncrytVoice() :
    """
    실시간 송신 암호화.
    UDP_IP : Destination IP Addr
    UDP_PORT : Destination PORT Addr
    CHANNELS : 음성(마이크) 채널
    nonce = 암호화 CTR에 같이쓸 nonce추가
    """
    def __init__(self,IP="",PORT=34567):
        self.IP=IP
        self.PORT=PORT
        self.CHANNELS=1
        self.initialized = False
        self.RATE = 48000
        self.CHUNK = 960
        self.INPUT_DEVICE_INDEX = 1
        self._UDPON = True
        self.call_dict=None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.sock.settimeout(2)
    def set_call_dict(self,call_dict):
        self.call_dict=call_dict
    def UDPRec(self):
        #Rec 함수 무한 루프#login
        try:
            self.sock.bind(("192.168.1.112", 10001))
        except Exception as e :
            print(e)
        finally :
            while self._UDPON:
                #if self._UDPON :
                self.UDPRecStart()
                time.sleep(1)
    def UDPRecStart(self):
            data = b""
            addr=""
            try:
                # 첫 패킷 수신 시 nonce 처리
                data, addr = self.sock.recvfrom(1920)
                print("test:"+str(data))
            # except BlockingIOError:
            #     return True
            # except TimeoutError :
            #     #return True
            #     pass
            except Exception as e :
                print(e)
            finally :
                try :
                    #print(addr)
                    if data == b"__END__":
                        print("송신 종료 감지")
                        self._UDPON = True
                        self.sock.sendto(data, (self.call_dict[addr[0]], 10001))
                        #self.call_dict = None
                        return False
                    if self.call_dict != None and addr!=None :
                        #print("test:"+str(data))
                        self.sock.sendto(data, (self.call_dict[addr[0]], 10001))
                    return True
                except Exception as e :
                    #self.call_dict = None
                    print(e)
"""    def ClientRecStart(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("192.168.125.128", 34569))
            sock.listen()
            print(f"Server listening on {self.IP}:34569")
            conn, addr = sock.accept()
            try:
                data= conn.recv(1024)
                sock.close()
                return data
            except BlockingIOError:
                print("") # 아직 데이터 없음"""
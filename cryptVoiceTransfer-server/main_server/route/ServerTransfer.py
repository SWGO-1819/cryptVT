
import asyncio
import threading
import json
import socket
import os
import signal
import sys
from multiprocessing import Process
from flask import Blueprint, Flask, Response, request
from http import HTTPMethod
from exception.sign_exception import SignInValidationError, UserNotFoundError


# def LoginCheckRec(Rec,data,ip="") :
#             #Rec = EncrytVoice.EncrytVoice()
#             #print("test")
#                 #data=b'{"id":"test","passwd":"test"}'
        
#         if isinstance(data, bytes):
#             data = data.decode()
#         print("pid:")
#         print(data)
#         data1=json.loads(data)
        
        # if data1 == None :
        #     pass
        # elif "CALL_START" in data1["type"] :
        #     print("CALL_START")
        #     data=Rec.SendStart(data=data)
        #     data=data.decode()
        #     print("data:")
        #     print(data)
        #     data1=json.loads(data)
        #     #ip save
        #     print("data1:")
        #     print(data1)
        #     call_dict={data1["ip1"]:data1["ip2"],data1["ip2"]:data1["ip1"]}
        #     UDPON=True
        # elif "INSERT_ID" in data1["type"] :
        #     data=Rec.SendStart(data=data)
        #     data=data.decode()
        #     data1=json.loads(data)
        #     Rec.SendStart(IP=data1["ipinfo"],data=data)
            
        # elif "NEED_USER" in data1["type"]:
        #     data=Rec.SendStart(data=data)
        #     data=data.decode()
        #     data1=json.loads(data)
        #             #data1=json.loads(data)
        #     Rec.SendStart(ip,data=data)
        #     data1=None
        #         #login check
        # elif "CHECK_LOGIN" in data1["type"]:
        #     data=Rec.SendStart(data=data)
        #     data=json.loads(data)
        #     Rec.SendStart(ip,data=data)
        #     #conn.close()
#         #             #print(Rec.RecStart())
#         #             #print("계속 도는 중")ign'
# class ServerTran() :
#     def __init__(self):
#         self.call_dict = None
#         self.UDPON = False
        
#     async def UDPRec(self,Rec):
#         #Rec 함수 무한 루프#login
#         while True:
#             #Rec = EncrytVoice.EncrytVoice("192.168.125.201")
#             #print("data1:"+data)
#             if self.UDPON == True :
#                 print("still connect")
#                 Rec.UDPRecStart(self.call_dict)
#             #print("data2:"+data)
#             #print(data)
#             #if "id" in data :
#             #Rec.SendStart(data=data)
#             #print(Rec.RecStart())
            
#             await asyncio.sleep(1)
    
                
                
    # def test(self,sock) :
    #     Rec = EncrytVoice.EncrytVoice()
        
    #     while True :
    #         conn, addr = sock.accept()
    #         data= conn.recv(1024)
    #         conn.close()
    #         #data, conn=Rec.RecStart(conn)
    #         p1 = Process(target=LoginCheckRec,args=(Rec,data,addr[0]),daemon=True)
    #         p1.start()
    #         """
    #         pid = os.fork()

    #         if pid == 1 :
    #             conn.close()
    #             continue
    #         else:
    #             sock.close()
    #             self.LoginCheckRec(Rec,data,conn)
    #         #await asyncio.sleep(1)"""

    # async def ServerMain(self) :
    #     Rec = EncrytVoice.EncrytVoice()
    #     await asyncio.gather(
    #         self.UDPRec(Rec)
    #     )
# if __name__ == "__main__":
#     tran = ServerTran()
#     #signal.signal(signal.SIGCHLD,signal_running)
#     # sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#     # sock.setblocking(True)
#     # sock.bind(("192.168.125.134", 34567))
#     # sock.listen()
#     # gui_thread = threading.Thread(target=tran.test,args=(sock,), daemon=True)
#     # gui_thread.start()
#     # gui_thread.join()
#     asyncio.run(tran.ServerMain())
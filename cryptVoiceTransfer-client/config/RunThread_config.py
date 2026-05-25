import asyncio

from client.RealTimeSnR import EncrytRec
from client.RealTimeSnR import EncrytSend
import time
class RunThr:
    def __init__(self):
        self.start = True
        self.Rec = EncrytRec()
        self.Send = EncrytSend()
        self.__buff = None
        self.__cipher = None
        pass
    
    def setStart(self,start) :
        self.start=start
        print("start : "+str(start))
    def setSend(self,__buff,__cipher) :
        self.__buff=__buff
        self.__cipher=__cipher
    async def RealTimeRec(self):
        # #Rec 함수 무한 루프
        while True :
            if thr.start :
                try :
                    self.Rec.RecStart()
                    print("계속 도는 중1")
                except Exception as e :
                    print(e)
            await asyncio.sleep(0.5)
            #await asyncio.sleep(1)

    async def RealTimeSend(self):
        while True :
            if thr.start :
                if self.__buff!=None and self.__cipher!=None:
                    try :
                        self.Send.SendStart(self.__buff,self.__cipher)
                        print("계속 도는 중2")
                    except Exception as e :
                        print(e)
            await asyncio.sleep(0.5)
    async def SnR(self):
        await asyncio.gather(
            self.RealTimeRec(),
            self.RealTimeSend()
        )
    def main(self):
        # 백그라운드 비동기 작업을 서브 쓰레드에서 실행
        # await self.RealTimeRec()
        print("test")
        asyncio.run(self.SnR())
        #gui_thread.join()
        #await asyncio.gather(self.RealTimeRec())
        # GUI는 메인 쓰레드에서 실행
        

        #background_thread.join()
thr = RunThr()

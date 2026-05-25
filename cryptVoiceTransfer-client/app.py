from client.LoginGUI_rev import LoginGUI
# from client.RealTimeSnR import EncrytRec
from config.RunThread_config import thr
import asyncio
import threading
import multiprocessing
def setGUI() :
    app = LoginGUI()
    app.mainloop()

if __name__ == "__main__":
    # bg_thread = threading.Thread(target=thr.main,daemon=True)
    # bg_thread.start()
    setGUI()
    # gui_thread = threading.Thread(target=setGUI,daemon=True)
    # test=threading.Thread(target=thr.main(),daemon=True)
    # # gui_thread2 = threading.Thread(target=Rec.RecStart)
    # gui_thread.start()
    # test.join()
    # gui_thread.join()
    # test.start()

    # gui_thread2.start()
    
    #gui_thread.join()
    # gui_thread2.join()
    # asyncio.run(thr.main())
    #multiprocessing.freeze_support()
    # gui_process = multiprocessing.Process(target=setGUI)
    # gui_process.start()
    
   
    
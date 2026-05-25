import customtkinter as ctk
import client.RealTimeSnR as SnR
from config.encryptVar_config import enc
from config.RunThread_config import thr
import threading
import time
class SnRGUI(ctk.CTk):
    """
    송수신 GUI 입니다
    """
    def __init__(self,id,myid):
        super().__init__()
        self.title("Encrypted Voice Call")
        self.geometry("400x300")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        #self.stop_event = threading.Event()
        self.id = id
        print("ip:"+id)
        self.myid=myid
        #self.sendToR = RTSR.EncrytSend("192.168.125.134",8080,nonce = enc.nonce)
        self.sendToR = None
        bg_color = "#1A1A1A"
        card_color = "#2C2C2C"
        entry_color = "#3A3A3A"
        blue_color = "#2979FF"
        green_color = "#26FE4A"
        hover_color = "#1565C0"
        gray_text = "#AAAAAA"
        red_color = "red"
        orange_color = "orange"
        self.font_bold_16 = ctk.CTkFont(size=16, weight="bold")
        self.font_bold_14 = ctk.CTkFont(size=14, weight="bold")
        self.font_bold_12 = ctk.CTkFont(size=12, weight="bold")
        self.font_16 = ctk.CTkFont(size=16)
        self.font_14 = ctk.CTkFont(size=14)
        self.font_12 = ctk.CTkFont(size=12)
        #self.back_to_list_callback = back_to_list_callback
        # 텍스트 박스 (IP 입력)
        #self.textbox = ctk.CTkEntry(self, placeholder_text="id", width=250)
        #self.textbox.pack(pady=40)
        
        # 원형 버튼
        self.button_style = {
            "fg_color": blue_color,
            "hover_color": hover_color,
            "text_color": "white",
            "corner_radius": 15,
            "height": 42,
            "font": self.font_14 ### 필요하면 위에서 정의한대로 변경
        }
        self.circle_button = ctk.CTkButton(
            self,
            text="📞",
            width=60,
            height=60,
            corner_radius=60,
            font=ctk.CTkFont(size=30, weight="bold"),
            command=self.on_call_toggle
        )
        self.test_button = ctk.CTkButton(
            self,
            text="🔴",
            width=60,
            height=60,
            corner_radius=30,
            font=ctk.CTkFont(size=30, weight="bold"),
            command=self.off_call_toggle
        )
        self.circle_button.pack(pady=20)
        self.test_button.pack(pady=20)
        #ctk.CTkButton(self, text="돌아가기", width=240, command=self.back_to_list, **self.button_style).pack()
        # self.process_queue()
        self.mainloop()
    def on_call_toggle(self):
        self.sendToR = SnR.EncrytSend("192.168.1.112", 34567)
        self.sendToR.SendPreparation(self.id,self.myid)
        time.sleep(1)
        thr.setSend(self.sendToR.data,enc.return_cipher(enc.nonce))
        thr.setStart(True)
            #thr.main()
        bg_thread = threading.Thread(target=thr.main,daemon=True)
        bg_thread.start()
        #thr.main()
        # self.sendToR.SendStart(self.sendToR._buff,enc.cipherSet(enc.nonce))
    def off_call_toggle(self):
        self.sendToR.sock.sendto(b"__END__", (self.sendToR.UDP_IP, self.sendToR.UDP_PORT))
        self.sendToR.stream.stop_stream()
        self.sendToR.stream.close()
        self.sendToR.p.terminate()
    #def back_to_list(self):
        #self.destroy()
        #if self.back_to_list_callback:
        #    self.back_to_list_callback()
    # def process_queue(self):
    #     if self.winfo_exists():
    #         # self.sendToR.SendStart(self.sendToR._buff,enc.cipherSet(enc.nonce))
    #         self.after(500, self.process_queue)
#if __name__ == "__main__":
#    app = SnRGUI()
#    app.mainloop()

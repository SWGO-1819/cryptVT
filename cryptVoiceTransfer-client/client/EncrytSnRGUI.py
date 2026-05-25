import customtkinter as ctk
import RealTimeSnR as RTSR
import config.RunThread_config as RT
import multiprocessing as mp
class SnRGUI(ctk.CTk):
    """
    EncrytSnR앱 GUI입니다.
    circle_button : 전화 송신 버튼
    flag : 통신 종료 flag
    """
    def __init__(self):
        self.flag=True
        super().__init__()
        self.title("CustomTkinter App")
        self.geometry("400x300")
        ctk.set_appearance_mode("dark")  # 또는 "dark"
        ctk.set_default_color_theme("blue")  # 테마 설정
        # 텍스트 박스
        self.textbox = ctk.CTkEntry(self, placeholder_text="text box", width=250)
        self.textbox.pack(pady=40)

        # 원형 버튼 (라벨을 그림처럼 보이게 하기 위해 아이콘 없이 설정)
        self.circle_button = ctk.CTkButton(
            self,
            text="📞",  # 간단한 회전 느낌의 유니코드 심볼 사용
            width=60,
            height=60,
            corner_radius=60,  # 반지름을 버튼 높이의 절반으로 해서 원형으로 만들기
            font=ctk.CTkFont(size=30, weight="bold"),
            command=self.on_button_click
        )
        self.circle_button.pack(pady=20)
        
    def on_button_click(self):
        print("입력된 텍스트:", self.textbox.get())
        if self.flag :
            send=RTSR.EncrytSend(UDP_IP=self.textbox.get(),UDP_PORT=8080)
            send.SendStart(not self.flag)
            self.flag=not self.flag



if __name__ == "__main__":
    print("Main Process start")
    Rec=RTSR.EncrytRec(UDP_IP="192.168.1.53")
    #p1 = mp.Process(name="Main Process", target=gui)
    print("test")
    p2 = mp.Process(name="Sub Process",target=Rec.RecStart())
    #p1.start()
    #p1.join()
    p2.start()
    p2.join()
    print("Main Process end")
    app = SnRGUI()
    app.mainloop()
    #rt=RT.RunThr(app)
    
    
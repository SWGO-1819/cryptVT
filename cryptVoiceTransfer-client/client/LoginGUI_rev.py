import customtkinter as ctk
import threading

import client.RealTimeGUIandRollback as MainGUI
from client.SignUp import SignUpGUI # type:ignore
from http import HTTPStatus
import requests
import socketio
import ast
sio = socketio.Client()

class LoginGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("암호화 통신 프로그램")
        self.geometry("500x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.stop_event = threading.Event()
        # 텍스트 박스 (IP 입력)

        self.rebuild_login_widgets()
    
    def login_on(self):
        user_id = self.textbox1.get()
        password = self.textbox2.get()
        if user_id == "" or user_id == None:
            pass
        # 예시: ID/비밀번호 확인 로직
        #ith socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)
        #print(self.MakeButton())
        
        if self.checkLogin(user_id,password):
            self.signup_button.destroy()
            self.circle_button.destroy()
            self.textbox1.destroy()
            self.textbox2.destroy()
            sio.connect("http://192.168.1.34:34567",transports=["websocket"])
            #sio.on("example", lambda data: print(data))
            #requests.post("http://192.168.125.134:34567/list/usrlist")
            sio.emit("usrlist","test")
            @sio.on("usrlist")
            def get_usrlist(data):
                for i in ast.literal_eval(data["id"]) :
                    button = ctk.CTkButton(
                        master=self,  # ★ self로 마스터 지정
                        text=i,
                        command=lambda i=i: self.callon(i,user_id)  # ★ self 메서드로 연결
                    )
                    button.pack(pady=10)  # 또는 button.grid(row=i, column=0)
        else:
            ctk.CTkMessagebox(title="로그인 실패", message="아이디 또는 비밀번호가 올바르지 않습니다.")
    def callon(self,id,myid):
        
        self.destroy()         # 현재 로그인 창 닫기
        MainGUI.SnRGUI(id,myid)       # 메인 GUI 열기
    #def MakeButton(self) :
        
        # try:
        #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :
        #         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #         payload = {
        #             "type" : "NEED_USER"
        #         }
        #         #s.setblocking(True) #로그인 성공 후 클라이언트에게 전송
        #         #s.settimeout(5)
        #         s.connect(("192.168.125.134", 34567)) # 연결 먼저
        #         #    print("NEED connect error")
        #         #print(json.dumps(payload).encode())
        #         s.sendall(json.dumps(payload).encode())
        #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
        #         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        #         s.bind(("192.168.125.128", 34567))
        #         s.listen()
        #         conn, addr = s.accept()
        #         data = conn.recv(1024)
        #         print(data)
        #         data=data.decode()
        #         data = json.loads(data)
        #         #s.settimeout(5)
        #         print(data)
        #         return data
                
        # except socket.timeout:
        #     print("⛔ 서버로부터 응답이 없습니다.")
        #     return False
        # except Exception as e:
        #     print(f"에러 발생: {e}")
        #     return False
    def checkLogin(self,id,pw) :    
        res = requests.post(url="http://192.168.1.34:34567/sign/sign-in", json={"id":id,"password":pw})
        return res.status_code == HTTPStatus.OK
        # test = http.client
        # connection=test.HTTPConnection(host="localhost",port=5000)
        # connection.request(method="post",url="/sign-in",body={id,pw},headers={"Content-Type":"application/json"})
        # res=connection.getresponse()
        # print(res.read().decode())
        # try:
            
        #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
        #         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        #         payload = {
        #             "type":"CHECK_LOGIN",
        #             "id": id,
        #             "passwd": pw
        #         }
        #             #s.setblocking(True) #로그인 성공 후 클라이언트에게 전송
        #             #s.settimeout(5)
        #         s.connect(("192.168.125.134", 34567))  # 연결 먼저
        #         s.sendall(json.dumps(payload).encode())
        #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        #         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        #         s.bind(("192.168.125.128", 34567))
        #         s.listen()
        #         conn, _=s.accept()
        #         data = conn.recv(1024)
        #         data=data.decode()
        #         data = json.loads(data)
        #         print(data)
        #         #s.settimeout(5)
        #         if data["CheckLogin"]=="1":
        #             self.myid=id
        #             return True
        #         else :
        #             return False
        # except socket.timeout:
        #     print("⛔ 서버로부터 응답이 없습니다.")
        #     return False
        # except Exception as e:
        #     print(f"에러 발생: {e}")
        #     return False
            
    def signup_on(self):
        self.clear_login_widgets()
        self.signup_frame = SignUpGUI(master=self, back_to_login_callback=self.rebuild_login_widgets)
        self.signup_frame.pack(expand=True, fill="both")

    def clear_login_widgets(self):
        self.textbox1.destroy()
        self.textbox2.destroy()
        self.circle_button.destroy()
        self.signup_button.destroy()

    def rebuild_login_widgets(self):
        self.textbox1 = ctk.CTkEntry(self, placeholder_text="id", width=250)
        self.textbox1.pack(pady=20)

        self.textbox2 = ctk.CTkEntry(self, placeholder_text="passwd", width=250, show="*")
        self.textbox2.pack(pady=20)

        self.circle_button = ctk.CTkButton(
            self,
            text="로그인",
            width=40,
            height=40,
            corner_radius=60,
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self.login_on
        )
        self.circle_button.pack(pady=20)

        self.signup_button = ctk.CTkButton(
            self,
            text="회원가입",
            width=40,
            height=40,
            corner_radius=60,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.signup_on
        )
        self.signup_button.pack(pady=(0, 10))

    def restore_login(parent):
        parent.signup_frame.destroy()  # 회원가입 프레임 제거(메모리에서 날림)
        del parent.signup_frame        # 속성도 제거해 다음에 다시 만들 수 있음
        parent.rebuild_login_widgets() # 로그인 위젯 다시 띄움


# if __name__ == "__main__":
#     app = LoginGUI()
    
#     app.mainloop()

import customtkinter as ctk
from tkinter import messagebox
import re
import json
import socket
import requests
from http import HTTPStatus
import requests
import socketio

# 주소 지정
server_host = "192.168.125.134"
server_port = int("34567")

# 색상 정의
bg_color = "#1A1A1A"
card_color = "#2C2C2C"
entry_color = "#3A3A3A"
blue_color = "#2979FF"
green_color = "#26FE4A"
hover_color = "#1565C0"
gray_text = "#AAAAAA"
red_color = "red"
orange_color = "orange"
sio = socketio.Client()
class SignUpGUI(ctk.CTkFrame):
    # 생성자
    def __init__(self, master, back_to_login_callback = None, signup_callback = None):
        super().__init__(master, fg_color = bg_color)
        self.master = master
        self.back_to_login_callback = back_to_login_callback
        self.signup_callback = signup_callback

        self.pack(padx = 30, pady = (30, 20))

        # 폰트 정의
        self.font_bold_16 = ctk.CTkFont(size=16, weight="bold")
        self.font_bold_14 = ctk.CTkFont(size=14, weight="bold")
        self.font_bold_12 = ctk.CTkFont(size=12, weight="bold")
        self.font_16 = ctk.CTkFont(size=16)
        self.font_14 = ctk.CTkFont(size=14)
        self.font_12 = ctk.CTkFont(size=12)


        # 버튼 공통 스타일
        self.button_style = {
            "fg_color": blue_color,
            "hover_color": hover_color,
            "text_color": "white",
            "corner_radius": 15,
            "height": 42,
            "font": self.font_14 ### 필요하면 위에서 정의한대로 변경
        }


        ''' --- 카드 프레임 --- '''
        form_frame = ctk.CTkFrame(self, fg_color=card_color, corner_radius=20)
        form_frame.pack(padx=20, pady=20)


        ''' ----- ID 입력 ----- '''
        self.id_entry = ctk.CTkEntry(form_frame, placeholder_text="id", width=200,
                                     fg_color=entry_color, text_color="white", height=36)
        self.id_entry.grid(row=0, column=0, padx=(15, 5), pady=(20, 5), sticky="w")
        self.id_entry.bind("<KeyRelease>", self.reset_id_status)

        self.id_check_button = ctk.CTkButton(
            form_frame, text="중복 확인", width=90,
            command=self.check_duplicate, **self.button_style
        )
        self.id_check_button.grid(row=0, column=1, padx=(5, 15), pady=(20, 5), sticky="e")

        self.id_status_label = ctk.CTkLabel(
            form_frame, text="ID 중복 확인이 필요합니다",
            text_color=gray_text, font=self.font_bold_12
        )
        self.id_status_label.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")


        ''' ----- PW 입력 ----- '''
        self.pw_entry = ctk.CTkEntry(form_frame, show="*", placeholder_text="password", width=200,
                                     fg_color=entry_color, text_color="white", height=36)
        self.pw_entry.grid(row=2, column=0, padx=(15, 5), pady=(0, 5), sticky="w")
        self.pw_entry.bind("<KeyRelease>", self.check_strength)

        self.strength_label = ctk.CTkLabel(
            form_frame, text="강도:", text_color=gray_text, font=self.font_bold_12
        )
        self.strength_label.grid(row=2, column=1, padx=(5, 15), pady=(0, 5), sticky="w")


        ''' --- 경고 메시지 (카드 안으로 이동) ---'''
        self.warning_label = ctk.CTkLabel(
            form_frame, text="", text_color=red_color,
            font=self.font_bold_12, justify="center", anchor="center"
        )
        self.warning_label.grid(row=3, column=0, columnspan=2, pady=(5, 10), sticky="ew")


        ''' ----- 버튼들 (카드 바깥) ----- '''
        ctk.CTkButton(self, text="가입신청", width=240, command=self.try_signup, **self.button_style).pack(pady=(10, 10))
        ctk.CTkButton(self, text="돌아가기", width=240, command=self.back_to_login, **self.button_style).pack()


    def reset_id_status(self, event=None):
        self.id_status_label.configure(text="ID 중복 확인이 필요합니다", text_color = gray_text)


    def check_duplicate(self):
        uid = self.id_entry.get()

        if len(uid) == 0:
            self.id_status_label.configure(text = "ID를 입력하세요", text_color = gray_text)
        elif len(uid) <= 4:
            self.id_status_label.configure(text = "ID 4자 이상으로 입력하세요", text_color = red_color)
        elif uid == "admin":
            self.id_status_label.configure(text = "❌ 사용할 수 없는 ID입니다", text_color = red_color)

        ########## 소켓 구현되면 삭제할 내용 ##########
        # elif uid == "중복":
        #     self.id_status_label.configure(text = "❗ 다른 ID를 입력하세요", text_color = red_color)

        # else:
        #     self.id_status_label.configure(text = "✅ 사용 가능", text_color = green_color)
        #################### 끝 #####################

        # 서버 통신 최소화를 위해 특정 조건에 만족할 때만 쿼리 날림
        # 쿼리 메소드는 아래에 있으며, 쿼리로 대답 받는 단어는 임시로 OK, Duplicated로 정의함
        else:
            uid_query_result = self.query_id_check(uid)
            if uid_query_result:
                self.id_status_label.configure(text = "✅ 사용 가능", text_color = green_color)
            else:
                self.id_status_label.configure(text = "❗ 다른 ID를 입력하세요", text_color = red_color)

    def check_strength(self, event=None):
        pw = self.pw_entry.get()
        self.warning_label.configure(text="")

        length_ok = len(pw) >= 8
        has_letter = re.search(r"[a-zA-Z]", pw) is not None
        has_digit = re.search(r"\d", pw) is not None
        has_special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw) is not None

        score = sum([length_ok, has_letter, has_digit, has_special])

        if len(pw) == 0:
            msg, color = "강도", gray_text
        elif score < 3:
            msg, color = "강도 Weak", red_color
        elif score == 3:
            msg, color = "강도 Normal", orange_color
        else:
            msg, color = "강도 Good", green_color

        self.strength_label.configure(text=msg, text_color=color)

    def try_signup(self):
        uid = self.id_entry.get()
        pw = self.pw_entry.get()

        if "Good" not in self.strength_label.cget("text"):
            self.warning_label.configure(
                text = "비밀번호가 너무 약합니다.\n대소문자, 숫자, 특수문자를 포함해 8자 이상으로 설정해주세요.",
                text_color = red_color
            )
            return

        if "✅" not in self.id_status_label.cget("text"):
            self.warning_label.configure(
                text = "❗ID 중복 확인이 필요합니다.",
                text_color = red_color
            )
            return

        self.warning_label.configure(text="")
        #여기서부터는 회원 가입
        self.InsertSignUp(uid,pw)

        messagebox.showinfo("가입 완료", "회원가입이 성공적으로 완료되었습니다!")

        if self.signup_callback:
            self.signup_callback(uid, pw)

        self.back_to_login()


    def back_to_login(self):
        self.destroy()
        if self.back_to_login_callback:
            self.back_to_login_callback()


    def query_id_check(self, uid: str) -> str:
        data = requests.post('http://192.168.125.134:34567/sign/check', json={"id":uid})
        return data.status_code == 200
        # try:
        #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # 끝나면 자동 소켓 반환
        #         s.connect((self.server_host, self.server_port))

        #         # JSON 형식으로 요청 보냄
        #         request = {
        #             "type": "CHECK_ID",
        #             "id": uid
        #         }
        #         s.sendall(json.dumps(request).encode())

        #         # 응답 받기
        #         response = s.recv(1024).decode().strip()
        #         data = json.loads(response) # 문자열 형식의 JSON을 다시 딕셔너리 객체로 파싱(e.g. '{"result": "OK"}' → {"result": "OK"})
        #         return data.get("result", "ERROR")
        #         # 응답 딕셔너리에서 "result" 키 값을 가져옴. 없으면 "ERROR"를 기본값으로 반환
        #         # e.g. {"result": "DUPLICATED"} → "DUPLICATED"
        #         # e.g. {"result": "OK"} -> "OK"
        #         # e.g. {} -> ERROR

        # except Exception as e:
        #     print(f"서버 연결 실패: {e}")
        #     return "ERROR"
    def InsertSignUp(self,id,pw) :
        ip=socket.gethostbyname(socket.gethostname())
        name="test"
        requests.post('http://192.168.125.134:34567/sign/sign-up', json={"id":id,"password":pw,"name":name,"ip":ip})
        # print("test")
        # try:
        #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # 끝나면 자동 소켓 반환
        #         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        #         s.setblocking(True)
        #         s.settimeout(5)
        #         s.connect(("192.168.125.134", 34567))
        #         hostname = socket.gethostname()
        #         myIp=socket.gethostbyname(hostname)
        #         print(myIp)
        #         payload = {
        #             "type": "INSERT_ID",
        #             "id": id,
        #             "passwd":pw,
        #             "ipinfo":myIp
        #         }
        #         s.sendall(json.dumps(payload).encode())
        # except Exception as e:
        #     print(f"서버 연결 실패: {e}")
        #     return "ERROR"
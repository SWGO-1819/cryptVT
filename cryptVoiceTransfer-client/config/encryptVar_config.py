from Crypto.Cipher import AES # type: ignore
from Crypto.Util import Counter # type: ignore
from Crypto.Random import get_random_bytes # type: ignore
import hashlib

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
enc = encryptVar()
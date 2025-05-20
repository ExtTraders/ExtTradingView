#-*-coding:utf-8 -*-

'''
여러분의 시크릿 키와 엑세스 키를 
ende_key.py에 있는 키를 활용해서 암호화한 값을 넣으세요

마찬가지 방법으로 아래 로직을 실행하시면 됩니다.. (ende_key.py 참조)

from cryptography.fernet import Fernet

class SimpleEnDecrypt:
    def __init__(self, key=None):
        if key is None: # 키가 없다면
            key = Fernet.generate_key() # 키를 생성한다
        self.key = key
        self.f   = Fernet(self.key)
    
    def encrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.encrypt(data) # 바이트형태이면 바로 암호화
        else:
            ou = self.f.encrypt(data.encode('utf-8')) # 인코딩 후 암호화
        if is_out_string is True:
            return ou.decode('utf-8') # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou
        
    def decrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.decrypt(data) # 바이트형태이면 바로 복호화
        else:
            ou = self.f.decrypt(data.encode('utf-8')) # 인코딩 후 복호화
        if is_out_string is True:
            return ou.decode('utf-8') # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou

         

simpleEnDecrypt = SimpleEnDecrypt(b'NcUgge50agCYGXpJmpcxsE5_0do84kKNdI6DsG-iwm8=') #ende_key.py 에 있는 키를 넣으세요

access = "A0X27AGgl8UYAC2cFMYzyrMlfxn1DsgrxoGjLVc2"          # 본인 값으로 변경
secret = "JkaADmlhsKOAcOlSsYw1WJ7DIpSnM9gGzP7dLRBx"          # 본인 값으로 변경


print("access_key: ", simpleEnDecrypt.encrypt(access))

print("scret_key: ", simpleEnDecrypt.encrypt(secret))

'''

upbit_access = "gAAAAABhHynXP_5VsBAOYlfea10cwe34wcs3tpcTnqp1bpkg0YoNNl2RFvgf5m23UQS2VaCyxCUx9GUZgua4IKjBI1an0dYeA2iWxnPiz2ioTmzXfdj1Iq7hbYuzacSazXqrNef1_XM"          # 본인 값으로 변경
upbit_secret = "gAAAABfgyoC6DsPtHr89Y9icIWZhEks0DeMLrsqaERI2vVE6d_kZi50JBOcthIshxEb7F-s0_3QiZmlM87K7ZmEs9yskevVy5P2BcYTypKh16Kf64Bxa117nJtHfgfICWmlcN__"          # 본인 값으로 변경

binance_access = "gAAAAABoLHT_qx__omS4PMnLlri3bwcMqhq_9QW3z_9aGbkV9IdO31cbytwCywVdqcJQ_i1NUJd69aB8dFD_gRnEIgraSydqR1ZOFaGFgWhX5iEgJ0zYv_ii5QzKLGFmn_btnYRpWin3Zz9ed3gqPflzv5e1xKyW1WXxdK-nbpmphwOPNs8IhW4="          # 본인 값으로 변경
binance_secret = "gAAAAABoLHT_OpR-YRNgKSEZpYH5dFW16ajych7RtolgPiXFpHpTgNmCJ9yuDjUerL1_69kRBQGcq4k7EupIYJnz_ADNUAgXf7FaTFGQRMFMuyth4r9J_5rnyXgc1yROyPXe-6cTfPlECl-Z7jZTWQ6YlRA8IYKWqSwo2jjlbqeabX7WfQnghfY="
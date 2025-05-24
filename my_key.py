#-*-coding:utf-8 -*-
'''
이 키값을 그대로 쓰셔도 되지만 아나콘다 쥬피터 노트북 상에서 아래 로직 실행해서 새로 키를 받으세요.
물론 비쥬얼 스튜디오 코드에서도 아래처럼 코딩해서 키 값을 얻으셔도 되요. 편하신 걸로 ㅎ
'''

upbit_access = ""          # 본인 값으로 변경
upbit_secret = ""          # 본인 값으로 변경

binance_access = "gAAAAABoLHT_qx__omS4PMnLlri3bwcMqhq_9QW3z_9aGbkV9IdO31cbytwCywVdqcJQ_i1NUJd69aB8dFD_gRnEIgraSydqR1ZOFaGFgWhX5iEgJ0zYv_ii5QzKLGFmn_btnYRpWin3Zz9ed3gqPflzv5e1xKyW1WXxdK-nbpmphwOPNs8IhW4="          # 본인 값으로 변경
binance_secret = "gAAAAABoLHT_OpR-YRNgKSEZpYH5dFW16ajych7RtolgPiXFpHpTgNmCJ9yuDjUerL1_69kRBQGcq4k7EupIYJnz_ADNUAgXf7FaTFGQRMFMuyth4r9J_5rnyXgc1yROyPXe-6cTfPlECl-Z7jZTWQ6YlRA8IYKWqSwo2jjlbqeabX7WfQnghfY="

bybit_access = "gAAAAABoMThbpbezOsxlQkylLhuMMgfX9od9EBtjPoVywCfI0JCZHefjXeruAlN7zbbL2nNptcMAaWYohW7PefE95TYuKORuIm7WXMCeF-3JzqyUv7CvWXI="
bybit_secret = "gAAAAABoMThbJ8pmknXww2Q8TqcOPBj4mw1NEBoxN9fXRMnUybq-kgKqbdtmm-Jxzs1FEXkD5acj5w01E_jYV4jLemnIw29AS5fVJ3M7nLQBaOhP52O7EgjaIiVt4qaQMlzdJvH_-zOv"

bybit_test_access = "gAAAAABoMXukp_rQFxsJ9iKeyvKSXJsOpOF2M65oVTNTkmnaW2E9S-QFzyxW3PHWIyPqqMmfW4DSjbUB6BzEaXemQ_1gaqsZWYxUW7mlUvrA8iiKOb8GZn4="
bybit_test_secret = "gAAAAABoMXukYlDU8R76kZACrLpNqtHIfqUqmPnXDALTARHHTlSqYFrBkGCJ0_m08ocrkS2oVLexGL1TwJCJUFwM6Hbgn21YCOh9Wz5lAkws9FO9zMpd1RxkyIVUSkm5FeNTUmVhW1Ej"
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


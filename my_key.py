#-*-coding:utf-8 -*-
'''
이 키값을 그대로 쓰셔도 되지만 아나콘다 쥬피터 노트북 상에서 아래 로직 실행해서 새로 키를 받으세요.
물론 비쥬얼 스튜디오 코드에서도 아래처럼 코딩해서 키 값을 얻으셔도 되요. 편하신 걸로 ㅎ
'''

upbit_access = ""          # 본인 값으로 변경
upbit_secret = ""          # 본인 값으로 변경

binance_access = "gAAAAABoMZfPJP3fTbBGt0n2Wcgdi-MO70afmNrkEljsu7r72I0fm7DhmLb1y1K84a6SmGDT_s5ugFshDpaUBEc5-qNGeB5dYHt2LGjR1nrIvV3apMcp6kPWOX4q_uTFmeqPcrwpxSGj-JmWksdfqXD7lqb5rbH4VFE5QEkPy5sqS42fmxzV2JE="
binance_secret = " gAAAAABoMZfPWvHlnX1eYPN5jOkbirlyETjyCS4Whx2E70ZTEmyWLc8UybEToMQiEGKP2qO0xarxfBllnGpp1_1AplLgKSjUUh06dH1yeQ6URG79cO8eagRYXswT1XLSY2B01ImK8CDY06l11yhmcwSSyWVcIspD-JTLJbj5B-t-zuzbsHFPM9s="

bybit_access = "gAAAAABoMZs2cCorWKqRww0Lo-GzKpZFzFmx0qNU_pzDVe9IJOj-QAO3GFJ6z7NJCA4viTm_qH8Qte20O1gJotQ3xDez4DWUiTvl4oLrfoIfxJdOT_XTyx4="
bybit_secret = "gAAAAABoMZs2sk7n9Z_3uE43aGkoFw99sr8ZSnYlaxSKmPL37lsPh_06-lk5PIgt-SsTgAYfZmwyZ-auIZVU7CecadvUhjPWE9ugttaI6kuQPP-CGQRRU85G8PvUuzuz-QJlFtyAUgdn"

bybit_test_access = "tnD5L9GELr8LaJj5Ax"
bybit_test_secret = "pvuHSQRXviblmzS43mH6y38ME3Flc1OAowkF"
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


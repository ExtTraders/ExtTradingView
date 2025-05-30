# ExtTradingView

# How to Start
```bash
pip install ccxt

pip install fastapi uvicorn
```

# Server Setup
```bash
sudo apt-get update && \
sudo apt-get upgrade python3 -y && \
sudo apt install python3-pip -y

---
pip3 --version
---
git clone https://github.com/ExtTraders/ExtTradingView.git && \
cd ExtTradingView && \
sudo apt install python3.10-venv -y && \
sudo python3 -m venv .venv
source .venv/bin/activate

sudo chown -R ubuntu:ubuntu .venv/

uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### externally-managed-environment 문제 발생시
```bash
sudo rm /usr/lib/python3.12/EXTERNALLY-MANAGED
sudo pip3 install ccxt
```

# 레드헷 계열(AMS)
```bash
sudo yum update -y
sudo yum install python3 pip3 -y
python3 --version
pip3 --version
pip3 install cctx
```

# 참고소스
https://blog.naver.com/PostView.naver?blogId=zacra&logNo=222638332849

# 키 암호화
```
pip install jupyter
jupyter notebook
```

# 패키지 뽑고 설치하기
```
pip install pipreqs
---
pipreqs . --force
pip install -r requirements.txt
```


# 인증서 받기(cert, key)
- 도메인을 받은 경우
```
sudo apt install certbot -y
sudo apt install python3-certbot-nginx -y
sudo certbot certonly --standalone -d 내도메인.com
```
- 테스트용인 경우
```
mkdir -p nginx

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/key.pem -out nginx/cert.pem \
  -subj "/C=KR/ST=Seoul/L=Seoul/O=MyOrg/OU=Dev/CN=localhost"
```
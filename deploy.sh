#!/bin/bash

# EC2에서 실행할 배포 스크립트
# 파일명: deploy.sh

echo "Starting deployment..."

# Docker 및 Docker Compose 설치 확인
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# 프로젝트 디렉토리로 이동
cd /home/ubuntu/your-app-name

# 최신 이미지 가져오기
echo "Pulling latest images..."
sudo docker-compose pull

# 컨테이너 재시작
echo "Restarting containers..."
sudo docker-compose down
sudo docker-compose up -d

# 사용하지 않는 이미지 정리
echo "Cleaning up unused images..."
sudo docker image prune -f

# 서비스 상태 확인
echo "Checking service status..."
sudo docker-compose ps

echo "Deployment completed!"

# 포트 80, 440이 열려있는지 확인
echo "Checking if ports are accessible..."
sudo netstat -tlnp | grep -E ':80|:440'
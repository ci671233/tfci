#!/bin/bash

# MCP 서버 배포 스크립트

set -e

echo "🚀 MCP Time Series Prediction Server 배포 시작"

# 1. 환경 변수 설정
DOCKER_USERNAME=${DOCKER_USERNAME:-"your-username"}
IMAGE_NAME="mcp-predictor"
TAG=${TAG:-"latest"}

# 2. Docker 이미지 빌드
echo "📦 Docker 이미지 빌드 중..."
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$TAG .

# 3. Docker Hub에 푸시
echo "📤 Docker Hub에 푸시 중..."
docker push $DOCKER_USERNAME/$IMAGE_NAME:$TAG

# 4. 배포 완료 메시지
echo "✅ 배포 완료!"
echo "이미지: $DOCKER_USERNAME/$IMAGE_NAME:$TAG"
echo ""
echo "다른 환경에서 실행하려면:"
echo "docker pull $DOCKER_USERNAME/$IMAGE_NAME:$TAG"
echo "docker run -p 8080:8080 $DOCKER_USERNAME/$IMAGE_NAME:$TAG" 
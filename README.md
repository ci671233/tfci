# MCP Predictor

시계열 예측을 위한 MCP (Model Context Protocol) 서버입니다. 데이터베이스에서 데이터를 로드하여 시계열 예측 모델을 학습하고 예측 결과를 제공합니다.

## 주요 기능

- **다양한 데이터 소스 지원**: DB2, PostgreSQL, MongoDB, CSV 파일
- **시계열 예측**: Prophet 모델을 사용한 시계열 예측
- **JSON-RPC 프로토콜**: 표준 MCP 프로토콜 지원
- **Docker 지원**: 컨테이너화된 배포
- **설정 기반**: YAML 설정 파일을 통한 유연한 구성

## 설치 및 실행

### 1. 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 설정 파일 생성 (config/mcp_config.yaml 참조)
cp config/mcp_config.yaml config.yaml
# config.yaml 파일에서 데이터베이스 연결 정보 수정

# 기존 배치 예측 파이프라인
python main.py

# MCP 서버 실행
python mcp/mcp_server.py

# HTTP 서버 실행
python servers/http_mcp_server.py
```

### 2. Docker 실행

```bash
# Docker 이미지 빌드 및 실행
docker-compose up --build

# 또는 직접 Docker 실행
docker build -t mcp-predictor .
docker run -it --rm -p 8080:8080 mcp-predictor
```



## 설정 파일 (config/mcp_config.yaml)

```yaml
input:
  source_type: "db"       # db | csv
  db_type: "db2"          # db2 | postgresql | mongodb
  connection:
    host: "YOUR_HOST"
    port: 25010
    user: "YOUR_USER"
    password: "YOUR_PASSWORD"
    database: "YOUR_DATABASE"
  table: "YOUR_TABLE"
  features: ["RGN_CD", "CRTR_YR"]
  target: ["GRDR1_STDNT_NOPE", "GRDR2_STDNT_NOPE"]

prediction:
  task_type: "timeseries"
  future_steps: 5
  time_col: "CRTR_YR"
  group_key: "RGN_CD"

output:
  source_type: "csv"
  csv_path: "./data/output.csv"
```

## API 사용법

### JSON-RPC 요청 예시

```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "config_path": "config/mcp_config.yaml"
  },
  "id": 1
}
```

```json
{
  "jsonrpc": "2.0",
  "method": "predict",
  "params": {
    "features": {
      "RGN_CD": "서울",
      "CRTR_YR": 2024
    },
    "prediction_config": {
      "future_steps": 3
    }
  },
  "id": 2
}
```

## 프로젝트 구조

```
mcp-predictor/
├── config/              # 설정 관련 모듈
├── core/               # 핵심 예측 로직
├── data/               # 데이터 로드/저장 모듈
├── model/              # 머신러닝 모델
├── util/               # 유틸리티
├── mcp/                # MCP 프로토콜 구현
│   ├── __init__.py
│   └── mcp_server.py   # JSON-RPC MCP 서버
├── servers/            # 서버 구현체
│   ├── __init__.py
│   ├── http_mcp_server.py  # HTTP API 서버
│   └── run_mcp_server.py   # 서버 실행 스크립트

├── scripts/            # 배포 및 관리 스크립트
│   ├── __init__.py
│   └── deploy.sh       # 배포 스크립트
├── docs/               # 문서
├── main.py             # 기존 배치 예측 파이프라인
├── config.yaml         # 기존 설정 (민감한 정보 포함)
├── config/mcp_config.yaml  # MCP 설정 템플릿
├── Dockerfile          # Docker 설정
├── docker-compose.yml  # Docker Compose
└── requirements.txt    # Python 의존성
```

## 배포

### GitHub Actions를 통한 자동 배포

1. GitHub 저장소에 코드 푸시
2. GitHub Actions가 자동으로 Docker 이미지 빌드
3. Docker Hub 또는 GitHub Container Registry에 푸시

### 수동 배포

```bash
# Docker Hub에 푸시
docker tag mcp-predictor your-username/mcp-predictor
docker push your-username/mcp-predictor

# 다른 환경에서 실행
docker pull your-username/mcp-predictor
docker run -p 8080:8080 your-username/mcp-predictor
```

## 라이선스


## 기여

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request# Test commit for auto-deployment
# Auto-deployment test - #오후

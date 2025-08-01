# 프로젝트 구조 문서

## 📁 전체 구조

```
mcp-predictor/
├── 📁 config/              # 설정 관련 모듈
│   ├── __init__.py
│   ├── config.py           # 설정 로드 및 검증
│   └── mcp_config.yaml    # MCP 설정 템플릿 (민감한 정보 제거)
├── 📁 core/               # 핵심 예측 로직
│   ├── __init__.py
│   └── predictor.py       # 예측 파이프라인 (MCP 메서드 포함)
├── 📁 data/               # 데이터 로드/저장 모듈
│   ├── __init__.py
│   ├── csv.py             # CSV 파일 처리
│   ├── data.py            # 데이터 전처리 및 피처 선택
│   └── db.py              # 데이터베이스 연결 (DB2, PostgreSQL, MongoDB)
├── 📁 model/              # 머신러닝 모델
│   ├── __init__.py
│   └── model.py           # 시계열 예측 모델 (Prophet, LightGBM)
├── 📁 util/               # 유틸리티
│   └── __init__.py
├── 📁 mcp/                # MCP 프로토콜 구현
│   ├── __init__.py
│   └── mcp_server.py      # JSON-RPC MCP 서버
├── 📁 servers/            # 서버 구현체
│   ├── __init__.py
│   ├── http_mcp_server.py # HTTP API 서버
│   └── run_mcp_server.py  # 서버 실행 스크립트
├── 📁 examples/           # 예제 및 테스트
│   ├── __init__.py
│   └── test_mcp_client.py # MCP 클라이언트 테스트
├── 📁 scripts/            # 배포 및 관리 스크립트
│   ├── __init__.py
│   └── deploy.sh          # 배포 스크립트
├── 📁 docs/               # 문서
│   └── STRUCTURE.md       # 이 파일
├── 📁 .github/            # GitHub Actions
│   └── workflows/
│       └── deploy.yml     # 자동 배포 워크플로우
├── main.py                # 기존 배치 예측 파이프라인
├── config.yaml            # 기존 설정 (민감한 정보 포함, .gitignore)
├── Dockerfile             # Docker 설정
├── docker-compose.yml     # Docker Compose
├── requirements.txt       # Python 의존성
├── README.md             # 프로젝트 문서
└── .gitignore            # Git 제외 파일
```

## 🎯 각 디렉토리 역할

### 📁 `config/` - 설정 관리
- **config.py**: YAML 설정 파일 로드 및 검증
- **mcp_config.yaml**: MCP 서버용 설정 템플릿 (민감한 정보 제거)

### 📁 `core/` - 핵심 로직
- **predictor.py**: 예측 파이프라인 (기존 + MCP 메서드)

### 📁 `data/` - 데이터 처리
- **csv.py**: CSV 파일 로드/저장
- **data.py**: 데이터 전처리 및 피처 선택
- **db.py**: 데이터베이스 연결 (DB2, PostgreSQL, MongoDB)

### 📁 `model/` - 머신러닝
- **model.py**: 시계열 예측 모델 (Prophet, LightGBM)

### 📁 `mcp/` - MCP 프로토콜
- **mcp_server.py**: JSON-RPC 기반 MCP 서버

### 📁 `servers/` - 서버 구현
- **http_mcp_server.py**: HTTP API 서버 (Flask)
- **run_mcp_server.py**: 서버 실행 스크립트

### 📁 `examples/` - 예제 및 테스트
- **test_mcp_client.py**: MCP 서버 테스트 클라이언트

### 📁 `scripts/` - 배포 스크립트
- **deploy.sh**: Docker 배포 스크립트

## 🚀 실행 방법

### 1. 기존 배치 예측
```bash
python main.py
```

### 2. MCP 서버 (JSON-RPC)
```bash
python mcp/mcp_server.py
```

### 3. HTTP 서버
```bash
python servers/http_mcp_server.py
```

### 4. 테스트
```bash
python examples/test_mcp_client.py
```

### 5. Docker 실행
```bash
docker-compose up --build
```

## 🔧 설정 파일

### 기존 설정 (로컬용)
- **config.yaml**: 민감한 정보 포함 (DB 연결 정보 등)
- `.gitignore`에 포함되어 GitHub에 업로드되지 않음

### MCP 설정 (공개용)
- **config/mcp_config.yaml**: 템플릿 (민감한 정보 제거)
- GitHub에 공개되어 다른 사용자가 참고 가능

## 📦 패키지 구조

각 디렉토리는 Python 패키지로 구성되어 있어 모듈화가 잘 되어 있습니다:

```python
# MCP 서버 사용 예시
from mcp.mcp_server import MCPServer
from servers.http_mcp_server import HTTPMCPServer
from examples.test_mcp_client import MCPClient
```

이 구조를 통해 기존 기능과 새로운 MCP 기능이 명확히 분리되어 관리가 용이합니다. 
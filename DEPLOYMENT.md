# TFCI 배포 가이드

## 자동 배포 설정

### 1. PyPI API 토큰 설정

1. [PyPI](https://pypi.org)에 로그인
2. Account Settings → API tokens → Add API token
3. 토큰 생성 후 복사

### 2. GitHub Secrets 설정

1. GitHub 저장소 → Settings → Secrets and variables → Actions
2. `New repository secret` 클릭
3. Name: `PYPI_API_TOKEN`
4. Value: PyPI에서 생성한 API 토큰 입력

### 3. 배포 방법

#### 자동 배포 (권장)
```bash
# 태그 생성 및 푸시
git tag v1.0.2
git push origin v1.0.2
```

#### 수동 배포
```bash
# 빌드
python -m build

# PyPI 업로드
python -m twine upload dist/*
```

## 버전 관리

### 버전 형식
- `v1.0.0`: 메이저.마이너.패치
- `v1.0.1`: 패치 업데이트
- `v1.0.2`: group_key 리스트 지원 추가
- `v1.1.0`: 마이너 업데이트
- `v2.0.0`: 메이저 업데이트

### 배포 순서
1. 코드 수정
2. `pyproject.toml`의 버전 업데이트
3. `tfci/__init__.py`의 `__version__` 업데이트
4. 커밋 및 푸시
5. 태그 생성 및 푸시
6. GitHub Actions가 자동으로 PyPI에 배포

## 테스트

### 로컬 테스트
```bash
# 패키지 설치
pip install -e .

# 라이브러리 테스트
python -c "from tfci import predict; print('OK')"

# group_key 리스트 테스트
python -c "from tfci import predict; predict('test_config.yaml')"
```

### GitHub Actions 테스트
- `main` 브랜치에 푸시하면 자동으로 테스트 실행
- Python 3.8, 3.9, 3.10, 3.11에서 테스트

## 패키지 구조

### 라이브러리 구조
```
tfci/
├── tfci/                 # 메인 패키지
│   └── __init__.py       # 라이브러리 API
├── core/                 # 핵심 로직
├── data/                 # 데이터 처리
├── model/                # 예측 모델
├── config/               # 설정 관리
└── mcp/                  # MCP 서버
```

### 주요 변경사항
- `lib_tfci.py` 제거 → `tfci/__init__.py`로 통합
- group_key 리스트 지원 추가
- 보안 강화 (YAML 파일 gitignore 추가)

## 문제 해결

### PyPI 업로드 실패
1. API 토큰 확인
2. 패키지 이름 중복 확인
3. 버전 번호 확인

### 빌드 실패
1. `pyproject.toml` 문법 확인
2. 의존성 확인
3. Python 버전 확인

### group_key 리스트 오류
1. 설정 파일에서 group_key 형식 확인
2. 단일 문자열: `group_key: "RGN_CD"`
3. 리스트: `group_key: ["RGN_CD", "SCHL_TYPE_NM"]` 
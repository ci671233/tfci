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
git tag v1.0.0
git push origin v1.0.0
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
- `v1.1.0`: 마이너 업데이트
- `v2.0.0`: 메이저 업데이트

### 배포 순서
1. 코드 수정
2. `pyproject.toml`의 버전 업데이트
3. 커밋 및 푸시
4. 태그 생성 및 푸시
5. GitHub Actions가 자동으로 PyPI에 배포

## 테스트

### 로컬 테스트
```bash
# 패키지 설치
pip install -e .

# 라이브러리 테스트
python -c "from tfci import predict; print('OK')"
```

### GitHub Actions 테스트
- `main` 브랜치에 푸시하면 자동으로 테스트 실행
- Python 3.8, 3.9, 3.10, 3.11에서 테스트

## 문제 해결

### PyPI 업로드 실패
1. API 토큰 확인
2. 패키지 이름 중복 확인
3. 버전 번호 확인

### 빌드 실패
1. `pyproject.toml` 문법 확인
2. 의존성 확인
3. Python 버전 확인 
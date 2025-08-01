import sys
import traceback
from config.config import load_config
from core.predictor import Predictor

def main():
    try:
        # 1) config 로드
        config = load_config("config.yaml")

        # 2) 예측 파이프라인 실행
        pipeline = Predictor(config)
        pipeline.run()

    except KeyboardInterrupt:
        print("\n[INFO] 사용자에 의해 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] MCP 실행 중 오류 발생: {e}")
        print(f"[ERROR] 상세 오류 정보:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

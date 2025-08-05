#!/usr/bin/env python3
"""
TFCI (Time Forecasting CI) - 로컬 실행용
"""

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
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
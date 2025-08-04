#!/usr/bin/env python3
"""
TFCI (Time Forecasting CI) - MCP 서버 배포용

Example:
python mcp_tfci.py --config config1.yaml
python mcp_tfci.py --config config2.yaml  
python mcp_tfci.py --config config3.yaml
"""

import sys
import traceback
import argparse
from config.config import load_config
from core.predictor import Predictor

def main():
    """메인 함수 - 명령행 인자 처리"""
    parser = argparse.ArgumentParser(description="TFCI MCP 서버")
    parser.add_argument("--config", default="config.yaml", 
                       help="설정 파일 경로 (기본값: config.yaml)")
    
    args = parser.parse_args()
    
    try:
        config = load_config(args.config)
        pipeline = Predictor(config)
        pipeline.run()
        print(f"[SUCCESS] 예측 완료: {args.config}")
    except Exception as e:
        print(f"[ERROR] 예측 실패: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 
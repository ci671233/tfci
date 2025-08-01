#!/usr/bin/env python3
"""
MCP 서버 실행 스크립트
"""

import sys
import os
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='MCP Time Series Prediction Server')
    parser.add_argument('--config', '-c', default='mcp_config.yaml', 
                       help='설정 파일 경로 (기본값: mcp_config.yaml)')
    parser.add_argument('--port', '-p', type=int, default=8080,
                       help='서버 포트 (기본값: 8080)')
    parser.add_argument('--host', default='localhost',
                       help='서버 호스트 (기본값: localhost)')
    
    args = parser.parse_args()
    
    # 설정 파일 존재 확인
    if not os.path.exists(args.config):
        print(f"[ERROR] 설정 파일이 존재하지 않습니다: {args.config}")
        print("[INFO] mcp_config.yaml 파일을 생성하고 데이터베이스 연결 정보를 설정하세요.")
        sys.exit(1)
    
    # MCP 서버 실행
    try:
        print(f"[INFO] MCP 서버를 시작합니다...")
        print(f"[INFO] 설정 파일: {args.config}")
        print(f"[INFO] 서버 주소: {args.host}:{args.port}")
        print("[INFO] JSON-RPC 요청을 stdin으로 받습니다.")
        print("[INFO] 종료하려면 Ctrl+C를 누르세요.")
        print("-" * 50)
        
        # MCP 서버 실행
        subprocess.run([sys.executable, "mcp/mcp_server.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n[INFO] MCP 서버가 종료되었습니다.")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] MCP 서버 실행 중 오류 발생: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 예상치 못한 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
MCP 서버 테스트 클라이언트
"""

import json
import subprocess
import sys
import os
import time
from typing import Dict, Any

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MCPClient:
    def __init__(self, server_process):
        self.server_process = server_process
        
    def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """MCP 서버에 JSON-RPC 요청 전송"""
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": 1
        }
        
        # 요청 전송
        request_str = json.dumps(request, ensure_ascii=False) + "\n"
        self.server_process.stdin.write(request_str.encode('utf-8'))
        self.server_process.stdin.flush()
        
        # 응답 읽기
        response_line = self.server_process.stdout.readline().decode('utf-8').strip()
        response = json.loads(response_line)
        
        return response

def test_mcp_server():
    """MCP 서버 테스트"""
    print("[INFO] MCP 서버 테스트 시작")
    
    try:
        # MCP 서버 프로세스 시작
        server_process = subprocess.Popen(
            [sys.executable, "mcp/mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        client = MCPClient(server_process)
        
        # 1. 서버 초기화 테스트
        print("\n[TEST] 1. 서버 초기화")
        init_response = client.send_request("initialize", {"config_path": "mcp_config.yaml"})
        print(f"초기화 결과: {json.dumps(init_response, ensure_ascii=False, indent=2)}")
        
        if init_response.get("result", {}).get("status") != "success":
            print("[ERROR] 서버 초기화 실패")
            return
        
        # 2. 설정 조회 테스트
        print("\n[TEST] 2. 설정 조회")
        config_response = client.send_request("get_config")
        print(f"설정 조회 결과: {json.dumps(config_response, ensure_ascii=False, indent=2)}")
        
        # 3. 예측 테스트
        print("\n[TEST] 3. 예측 실행")
        predict_response = client.send_request("predict", {
            "features": {
                "RGN_CD": "서울",
                "CRTR_YR": 2024
            },
            "prediction_config": {
                "future_steps": 3
            }
        })
        print(f"예측 결과: {json.dumps(predict_response, ensure_ascii=False, indent=2)}")
        
        print("\n[INFO] 모든 테스트 완료")
        
    except Exception as e:
        print(f"[ERROR] 테스트 중 오류 발생: {e}")
    finally:
        # 서버 프로세스 종료
        if 'server_process' in locals():
            server_process.terminate()
            server_process.wait()

if __name__ == "__main__":
    test_mcp_server() 
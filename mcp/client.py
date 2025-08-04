#!/usr/bin/env python3
"""
TFCI MCP Client for Time Series Prediction
"""

import json
import subprocess
import sys
from typing import Dict, Any, List

class TFCIMCPClient:
    def __init__(self, server_script: str = "mcp/mcp_server.py"):
        self.server_script = server_script
        self.process = None

    def start_server(self):
        """MCP 서버 시작"""
        try:
            self.process = subprocess.Popen(
                [sys.executable, self.server_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            print("[INFO] TFCI MCP 서버가 시작되었습니다.")
            return True
        except Exception as e:
            print(f"[ERROR] 서버 시작 실패: {e}")
            return False

    def stop_server(self):
        """MCP 서버 종료"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("[INFO] TFCI MCP 서버가 종료되었습니다.")

    def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """JSON-RPC 요청 전송"""
        if not self.process:
            return {"error": "서버가 시작되지 않았습니다."}

        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": 1
        }

        try:
            # 요청 전송
            request_str = json.dumps(request, ensure_ascii=False) + "\n"
            self.process.stdin.write(request_str)
            self.process.stdin.flush()

            # 응답 수신 (여러 줄 처리)
            response_lines = []
            while True:
                line = self.process.stdout.readline().strip()
                if not line:
                    break
                response_lines.append(line)
                
                # JSON 응답 완료 확인
                try:
                    json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue

            if response_lines:
                return json.loads(response_lines[-1])  # 마지막 JSON 응답 사용
            else:
                return {"error": "서버 응답이 없습니다."}

        except Exception as e:
            return {"error": f"요청 전송 실패: {e}"}

    def initialize(self, config_path: str = "config.yaml") -> Dict[str, Any]:
        """서버 초기화"""
        return self.send_request("initialize", {"config_path": config_path})

    def predict(self, config_path: str) -> Dict[str, Any]:
        """YAML 설정으로 예측 실행"""
        return self.send_request("predict", {"config_path": config_path})

    def list_configs(self, pattern: str = "*.yaml") -> Dict[str, Any]:
        """사용 가능한 설정 파일 목록 조회"""
        return self.send_request("list_configs", {"pattern": pattern})

    def get_results(self) -> Dict[str, Any]:
        """마지막 예측 결과 조회"""
        return self.send_request("get_results")

    def validate_config(self, config_path: str) -> Dict[str, Any]:
        """설정 파일 검증"""
        return self.send_request("validate_config", {"config_path": config_path})

    def get_server_info(self) -> Dict[str, Any]:
        """서버 정보 조회"""
        return self.send_request("get_server_info")

def main():
    """MCP 클라이언트 테스트"""
    print("TFCI MCP 클라이언트 테스트")
    print("=" * 50)

    client = TFCIMCPClient()

    try:
        # 서버 시작
        if not client.start_server():
            return

        # 서버 정보 조회
        print("\n1. 서버 정보 조회:")
        info = client.get_server_info()
        print(json.dumps(info, indent=2, ensure_ascii=False))

        # 설정 파일 목록 조회
        print("\n2. 사용 가능한 설정 파일 목록:")
        configs = client.list_configs("*.yaml")
        print(json.dumps(configs, indent=2, ensure_ascii=False))

        # 설정 파일 검증
        if configs.get("status") == "success" and configs.get("config_files"):
            first_config = configs["config_files"][0]["filename"]
            print(f"\n3. 설정 파일 검증 ({first_config}):")
            validation = client.validate_config(first_config)
            print(json.dumps(validation, indent=2, ensure_ascii=False))

            # 예측 실행
            if validation.get("status") == "success":
                print(f"\n4. 예측 실행 ({first_config}):")
                prediction = client.predict(first_config)
                print(json.dumps(prediction, indent=2, ensure_ascii=False))

                # 결과 조회
                print("\n5. 예측 결과 조회:")
                results = client.get_results()
                print(json.dumps(results, indent=2, ensure_ascii=False))

    except KeyboardInterrupt:
        print("\n[INFO] 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"[ERROR] 클라이언트 오류: {e}")
    finally:
        client.stop_server()

if __name__ == "__main__":
    main() 
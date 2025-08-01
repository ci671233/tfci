#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server for Time Series Prediction
"""

import json
import sys
import traceback
from typing import Any, Dict, List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import load_config
from core.predictor import Predictor


class MCPServer:
    def __init__(self):
        self.config = None
        self.predictor = None
        
    def initialize(self, config_path: str = "config.yaml"):
        """서버 초기화"""
        try:
            self.config = load_config(config_path)
            self.predictor = Predictor(self.config)
            return {"status": "success", "message": "MCP 서버가 초기화되었습니다."}
        except Exception as e:
            return {"status": "error", "message": f"초기화 실패: {str(e)}"}

    def predict(self, features: Dict[str, Any], prediction_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """시계열 예측 수행"""
        try:
            if not self.predictor:
                return {"status": "error", "message": "서버가 초기화되지 않았습니다."}
            
            # 예측 설정 병합
            if prediction_config:
                merged_config = self.config.copy()
                merged_config["prediction"].update(prediction_config)
            else:
                merged_config = self.config
            
            # 예측 실행
            result = self.predictor.run_with_custom_config(merged_config, features)
            
            return {
                "status": "success",
                "predictions": result,
                "message": "예측이 완료되었습니다."
            }
            
        except Exception as e:
            return {"status": "error", "message": f"예측 실패: {str(e)}"}

    def get_config(self) -> Dict[str, Any]:
        """현재 설정 반환"""
        if not self.config:
            return {"status": "error", "message": "서버가 초기화되지 않았습니다."}
        
        return {
            "status": "success",
            "config": self.config
        }

    def update_config(self, new_config: Dict[str, Any]) -> Dict[str, Any]:
        """설정 업데이트"""
        try:
            self.config = new_config
            self.predictor = Predictor(self.config)
            return {"status": "success", "message": "설정이 업데이트되었습니다."}
        except Exception as e:
            return {"status": "error", "message": f"설정 업데이트 실패: {str(e)}"}


def handle_request(server: MCPServer, request: Dict[str, Any]) -> Dict[str, Any]:
    """JSON-RPC 요청 처리"""
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")
    
    try:
        if method == "initialize":
            config_path = params.get("config_path", "config.yaml")
            result = server.initialize(config_path)
        elif method == "predict":
            features = params.get("features", {})
            prediction_config = params.get("prediction_config")
            result = server.predict(features, prediction_config)
        elif method == "get_config":
            result = server.get_config()
        elif method == "update_config":
            new_config = params.get("config", {})
            result = server.update_config(new_config)
        else:
            result = {"status": "error", "message": f"지원하지 않는 메서드: {method}"}
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
        
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32603,
                "message": f"내부 오류: {str(e)}"
            }
        }


def main():
    """MCP 서버 메인 함수"""
    server = MCPServer()
    
    print("MCP Time Series Prediction Server 시작")
    print("JSON-RPC 요청을 stdin으로 받습니다.")
    print("종료하려면 Ctrl+C를 누르세요.")
    
    try:
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = handle_request(server, request)
                print(json.dumps(response, ensure_ascii=False))
                sys.stdout.flush()
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "JSON 파싱 오류"
                    }
                }
                print(json.dumps(error_response, ensure_ascii=False))
                sys.stdout.flush()
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"서버 오류: {str(e)}"
                    }
                }
                print(json.dumps(error_response, ensure_ascii=False))
                sys.stdout.flush()
                
    except KeyboardInterrupt:
        print("\n[INFO] MCP 서버가 종료되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] MCP 서버 오류: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 
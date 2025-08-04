#!/usr/bin/env python3
"""
TFCI MCP (Model Context Protocol) Server for Time Series Prediction
"""

import json
import sys
import traceback
import os
import glob
from typing import Any, Dict, List, Optional
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import load_config
from core.predictor import Predictor

class TFCIMCPServer:
    def __init__(self):
        self.predictor = None
        self.config = None
        self.last_prediction_result = None

    def initialize(self, config_path: str = "config.yaml") -> Dict[str, Any]:
        """서버 초기화"""
        try:
            print(f"[INFO] TFCI MCP 서버 초기화: {config_path}")
            self.config = load_config(config_path)
            self.predictor = Predictor(self.config)
            return {
                "status": "success", 
                "message": "TFCI MCP 서버 초기화 완료",
                "server_info": {
                    "name": "TFCI Time Series Prediction Server",
                    "version": "1.0.4",
                    "capabilities": ["predict", "list_configs", "get_results", "validate_config"]
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}

    def predict(self, config_path: str) -> Dict[str, Any]:
        """YAML 설정 파일로 예측 실행 및 DB 저장"""
        try:
            print(f"[INFO] TFCI MCP 예측 시작: {config_path}")
            
            # config 파일 로드
            config = load_config(config_path)
            
            # 예측 실행
            predictor = Predictor(config)
            result = predictor.run()
            
            # 결과 저장
            self.last_prediction_result = {
                "config_path": config_path,
                "timestamp": datetime.now().isoformat(),
                "result": result,
                "status": "completed"
            }
            
            return {
                "status": "success", 
                "message": f"예측 완료: {config_path}",
                "config_used": config_path,
                "timestamp": self.last_prediction_result["timestamp"],
                "prediction_summary": {
                    "input_table": config.get("input", {}).get("table", "N/A"),
                    "output_table": config.get("output", {}).get("table", "N/A"),
                    "features": config.get("input", {}).get("features", []),
                    "targets": config.get("input", {}).get("target", []),
                    "future_steps": config.get("prediction", {}).get("future_steps", 0)
                }
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": str(e), 
                "traceback": traceback.format_exc(),
                "config_path": config_path
            }

    def list_configs(self, pattern: str = "*.yaml") -> Dict[str, Any]:
        """사용 가능한 YAML 설정 파일 목록 조회"""
        try:
            config_files = []
            for file_path in glob.glob(pattern):
                if os.path.isfile(file_path):
                    config_files.append({
                        "filename": file_path,
                        "size": os.path.getsize(file_path),
                        "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                    })
            
            return {
                "status": "success",
                "config_files": config_files,
                "total_count": len(config_files)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_results(self) -> Dict[str, Any]:
        """마지막 예측 결과 조회"""
        if self.last_prediction_result:
            return {
                "status": "success",
                "last_prediction": self.last_prediction_result
            }
        else:
            return {
                "status": "error",
                "message": "아직 예측이 실행되지 않았습니다."
            }

    def validate_config(self, config_path: str) -> Dict[str, Any]:
        """YAML 설정 파일 검증"""
        try:
            config = load_config(config_path)
            
            # 필수 섹션 검증
            required_sections = ["input", "prediction", "output"]
            missing_sections = [section for section in required_sections if section not in config]
            
            if missing_sections:
                return {
                    "status": "error",
                    "message": f"필수 섹션이 누락되었습니다: {missing_sections}",
                    "config_path": config_path
                }
            
            # 예측 설정 검증
            prediction_config = config.get("prediction", {})
            required_prediction_fields = ["task_type", "future_steps", "time_col", "group_key"]
            missing_prediction_fields = [field for field in required_prediction_fields if field not in prediction_config]
            
            if missing_prediction_fields:
                return {
                    "status": "error",
                    "message": f"예측 설정에 필수 필드가 누락되었습니다: {missing_prediction_fields}",
                    "config_path": config_path
                }
            
            return {
                "status": "success",
                "message": "설정 파일이 유효합니다.",
                "config_path": config_path,
                "validation_summary": {
                    "input_source": config.get("input", {}).get("source_type", "N/A"),
                    "output_target": config.get("output", {}).get("source_type", "N/A"),
                    "prediction_type": prediction_config.get("task_type", "N/A"),
                    "future_steps": prediction_config.get("future_steps", 0)
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "traceback": traceback.format_exc(),
                "config_path": config_path
            }

    def get_server_info(self) -> Dict[str, Any]:
        """서버 정보 조회"""
        return {
            "status": "success",
            "server_info": {
                "name": "TFCI Time Series Prediction Server",
                "version": "1.0.4",
                "description": "Time Forecasting CI - 시계열 예측 및 DB 저장 MCP 서버",
                "capabilities": [
                    "predict - YAML 설정으로 예측 실행",
                    "list_configs - 사용 가능한 설정 파일 목록",
                    "get_results - 마지막 예측 결과 조회",
                    "validate_config - 설정 파일 검증"
                ],
                "supported_formats": ["YAML"],
                "supported_databases": ["DB2", "PostgreSQL", "MongoDB"],
                "supported_outputs": ["Database", "CSV"]
            }
        }

def handle_request(server: TFCIMCPServer, request: Dict[str, Any]) -> Dict[str, Any]:
    """JSON-RPC 요청 처리"""
    try:
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if method == "initialize":
            config_path = params.get("config_path", "config.yaml")
            result = server.initialize(config_path)
        elif method == "predict":
            config_path = params.get("config_path")
            if not config_path:
                return {"error": {"code": -32602, "message": "config_path is required"}}
            result = server.predict(config_path)
        elif method == "list_configs":
            pattern = params.get("pattern", "*.yaml")
            result = server.list_configs(pattern)
        elif method == "get_results":
            result = server.get_results()
        elif method == "validate_config":
            config_path = params.get("config_path")
            if not config_path:
                return {"error": {"code": -32602, "message": "config_path is required"}}
            result = server.validate_config(config_path)
        elif method == "get_server_info":
            result = server.get_server_info()
        else:
            return {"error": {"code": -32601, "message": f"Method {method} not found"}}

        return {"jsonrpc": "2.0", "result": result, "id": request_id}

    except Exception as e:
        return {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": request.get("id")}

def main():
    print("TFCI MCP Time Series Prediction Server 시작")
    print("JSON-RPC 요청을 stdin으로 받습니다.")
    print("사용 가능한 메서드:")
    print("  - initialize(config_path)")
    print("  - predict(config_path)")
    print("  - list_configs(pattern)")
    print("  - get_results()")
    print("  - validate_config(config_path)")
    print("  - get_server_info()")
    print("종료하려면 Ctrl+C를 누르세요.")
    print("-" * 50)

    server = TFCIMCPServer()

    try:
        while True:
            line = input()
            if not line:
                continue

            try:
                request = json.loads(line)
                response = handle_request(server, request)
                print(json.dumps(response, ensure_ascii=False))
                sys.stdout.flush()
            except json.JSONDecodeError:
                print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None}))
                sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n[INFO] TFCI MCP 서버가 종료되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] 서버 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
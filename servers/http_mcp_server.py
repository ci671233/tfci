#!/usr/bin/env python3
"""
HTTP 기반 MCP 서버
"""

import json
import traceback
from typing import Any, Dict, Optional
from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import load_config
from core.predictor import Predictor

app = Flask(__name__)

# 전역 서버 인스턴스
mcp_server = None

class HTTPMCPServer:
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

# 전역 서버 인스턴스 초기화
mcp_server = HTTPMCPServer()

@app.route('/health', methods=['GET'])
def health_check():
    """헬스 체크 엔드포인트"""
    return jsonify({
        "status": "healthy",
        "service": "MCP Time Series Prediction Server"
    })

@app.route('/initialize', methods=['POST'])
def initialize():
    """서버 초기화"""
    try:
        data = request.get_json()
        config_path = data.get('config_path', 'config.yaml') if data else 'config.yaml'
        
        result = mcp_server.initialize(config_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"초기화 중 오류 발생: {str(e)}"
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    """예측 실행"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "요청 데이터가 없습니다."
            }), 400
        
        features = data.get('features', {})
        prediction_config = data.get('prediction_config')
        
        result = mcp_server.predict(features, prediction_config)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"예측 중 오류 발생: {str(e)}"
        }), 500

@app.route('/config', methods=['GET'])
def get_config():
    """설정 조회"""
    try:
        result = mcp_server.get_config()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"설정 조회 중 오류 발생: {str(e)}"
        }), 500

@app.route('/config', methods=['PUT'])
def update_config():
    """설정 업데이트"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "설정 데이터가 없습니다."
            }), 400
        
        result = mcp_server.update_config(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"설정 업데이트 중 오류 발생: {str(e)}"
        }), 500

@app.route('/api/v1/predict', methods=['POST'])
def api_predict():
    """RESTful API 예측 엔드포인트"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "요청 데이터가 없습니다."
            }), 400
        
        features = data.get('features', {})
        prediction_config = data.get('prediction_config')
        
        result = mcp_server.predict(features, prediction_config)
        
        if result['status'] == 'success':
            return jsonify({
                "success": True,
                "data": result['predictions'],
                "message": result['message']
            })
        else:
            return jsonify({
                "success": False,
                "error": result['message']
            }), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"서버 오류: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("HTTP MCP Time Series Prediction Server 시작")
    print("서버 주소: http://localhost:5000")
    print("API 문서:")
    print("  GET  /health          - 헬스 체크")
    print("  POST /initialize      - 서버 초기화")
    print("  POST /predict         - 예측 실행")
    print("  GET  /config          - 설정 조회")
    print("  PUT  /config          - 설정 업데이트")
    print("  POST /api/v1/predict  - RESTful API 예측")
    print("-" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True) 
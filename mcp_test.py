#!/usr/bin/env python3
"""
TFCI MCP 테스트 - 라이브러리처럼 사용
"""

from mcp.client import TFCIMCPClient

# MCP 클라이언트 생성
client = TFCIMCPClient()

# 서버 시작
client.start_server()

# 예측 실행 (라이브러리처럼 간단하게)
client.predict("T_PBAF3202S.yaml")
client.predict("T_PBAF3301S.yaml")

# 서버 종료
client.stop_server() 
#!/usr/bin/env python3
"""
TFCI MCP 패키지 테스트
"""

from tfci_mcp import TFCIMCPClient

def test_mcp_client():
    """MCP 클라이언트 테스트"""
    print("TFCI MCP 패키지 테스트 시작")
    print("=" * 50)
    
    # 클라이언트 생성
    client = TFCIMCPClient()
    
    try:
        # 서버 시작
        if not client.start_server():
            print("[ERROR] 서버 시작 실패")
            return
        
        # 예측 실행
        print("\n예측 실행 테스트:")
        result = client.predict("T_PBAF3202S.yaml")
        print(f"결과: {result}")
        
        # 추가 예측
        print("\n추가 예측 테스트:")
        result2 = client.predict("T_PBAF3301S.yaml")
        print(f"결과: {result2}")
        
    except Exception as e:
        print(f"[ERROR] 테스트 오류: {e}")
    finally:
        # 서버 종료
        client.stop_server()
        print("\n[INFO] 테스트 완료")

if __name__ == "__main__":
    test_mcp_client() 
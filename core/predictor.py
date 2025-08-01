from data.db import Database
from data.csv import Csv
from data.data import Data
from model.model import Model
from typing import Dict, Any, Optional

class Predictor:
    def __init__(self, config):
        self.config = config

    def run(self):
        print("[INFO] MCP 파이프라인 시작")

        # 1) 데이터 로드
        source_type = self.config["input"]["source_type"]
        if source_type == "db":
            loader = Database(self.config["input"])
            df = loader.load()
        elif source_type == "csv":
            loader = Csv(self.config["input"])
            df = loader.load()
        else:
            raise ValueError(f"지원하지 않는 source_type: {source_type}")

        print(f"[INFO] 데이터 로드 완료: {len(df)} rows")

        # 2) 전처리
        df = Data.preprocess(df)

        # 3) Feature/Target 분리 (+ time_col, group_key 처리)
        X, y = Data.select_features(
            df,
            self.config["input"],
            self.config.get("prediction", {})
        )

        # 4) 모델 학습 및 예측
        print("[INFO] 모델 학습 및 예측 실행")
        model = Model(self.config)
        predictions = model.train_and_predict(X, y)

        # 5) 결과 저장
        output_type = self.config["output"]["source_type"]
        if output_type == "db":
            saver = Database(self.config["output"])
            saver.save(predictions)
        elif output_type == "csv":
            saver = Csv(self.config["output"])
            saver.save(predictions)
        else:
            raise ValueError(f"지원하지 않는 output source_type: {output_type}")

        print("[INFO] MCP 파이프라인 완료")

    def run_with_custom_config(self, config: Dict[str, Any], features: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """MCP 서버용 커스텀 설정으로 예측 실행"""
        print("[INFO] MCP 서버 예측 시작")

        # 1) 데이터 로드
        source_type = config["input"]["source_type"]
        if source_type == "db":
            loader = Database(config["input"])
            df = loader.load()
        elif source_type == "csv":
            loader = Csv(config["input"])
            df = loader.load()
        else:
            raise ValueError(f"지원하지 않는 source_type: {source_type}")

        print(f"[INFO] 데이터 로드 완료: {len(df)} rows")

        # 2) 전처리
        df = Data.preprocess(df)

        # 3) Feature/Target 분리 (+ time_col, group_key 처리)
        X, y = Data.select_features(
            df,
            config["input"],
            config.get("prediction", {})
        )

        # 4) 모델 학습 및 예측
        print("[INFO] 모델 학습 및 예측 실행")
        model = Model(config)
        predictions = model.train_and_predict(X, y)

        # 5) 결과 반환 (저장하지 않음)
        return {
            "predictions": predictions,
            "data_shape": {
                "input_rows": len(df),
                "features": X.shape if hasattr(X, 'shape') else len(X),
                "targets": y.shape if hasattr(y, 'shape') else len(y)
            },
            "config_used": config
        }

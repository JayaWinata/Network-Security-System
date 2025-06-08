from datetime import datetime
import os
from src import constant

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = constant.PIPELINE_NAME
        self.artifact_name = constant.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)
        self.timestamp = timestamp

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            constant.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir,
            constant.DATA_INGESTION_FEATURE_STORE_DIR,
            constant.FILE_NAME
        )
        self.training_file_path: str = os.path.join(
                self.data_ingestion_dir, constant.DATA_INGESTION_INGESTED_DIR, constant.TRAIN_FILE_NAME
            )
        self.testing_file_path: str = os.path.join(
                self.data_ingestion_dir, constant.DATA_INGESTION_INGESTED_DIR, constant.TEST_FILE_NAME
            )
        self.train_test_split_ratio: float = constant.DATA_INGESTION_TEST_RATIO
        self.collection_name: str = constant.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = constant.DATA_INGESTION_DATABASE_NAME
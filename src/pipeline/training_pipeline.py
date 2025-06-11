from src.exception.exception import NetworkSecurityException
from src.logging.logger import logger

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, TrainingPipelineConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact
from src.cloud.blob_syncer import BlobSync
from src.constant import BLOB_URL, BLOB_URL_PARAMS

import os, sys


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.blob_sync = BlobSync()

    def ingest_data(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Starting data ingestion...")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logger.info(f"Data ingestion completed with the artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_data(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Starting data validation...")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logger.info(f'Data validation completed with the artifact: {data_validation_artifact}')
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def transform_data(self, data_validation_artifact: DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Starting data transformation...")
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, data_transformation_config=data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logger.info(f'Data transformation completed with the artifact: {data_transformation_artifact}')
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Starting model training...")
            model_trainer = ModelTrainer(
                model_trainer_config=self.model_trainer_config,
                data_transformation_artifact=data_transformation_artifact
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logger.info(f"Model training completed with the artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def sync_artifacts_to_blob_storage(self):
        try:
            blob_url = f'{BLOB_URL}/artifact/{self.training_pipeline_config.timestamp}?{BLOB_URL_PARAMS}'
            self.blob_sync.sync_folder_to_blob(folder=self.training_pipeline_config.artifact_dir, blob_url=blob_url)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def sync_model_to_blob_storage(self):
        try:
            blob_url = f'{BLOB_URL}/final_model/{self.training_pipeline_config.timestamp}?{BLOB_URL_PARAMS}'
            self.blob_sync.sync_folder_to_blob(folder=self.training_pipeline_config.model_dir, blob_url=blob_url)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.ingest_data()
            data_validation_artifact = self.validate_data(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.transform_data(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.train_model(data_transformation_artifact=data_transformation_artifact)
            self.sync_artifacts_to_blob_storage()
            self.sync_model_to_blob_storage()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

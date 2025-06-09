from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception.exception import NetworkSecurityException
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig, TrainingPipelineConfig, DataTransformationConfig, ModelTrainerConfig
from src.logging.logger import logger

import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestiion = DataIngestion(data_ingestion_config)
        logger.info("Initiate the data ingestion...")
        data_ingestion_artifact = data_ingestiion.initiate_data_ingestion()
        logger.info("Data ingestion step completed")
        print(data_ingestion_artifact)
        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(data_ingestion_artifact,data_validation_config)
        logger.info("Initiate the data validation...")
        data_validation_artifact=data_validation.initiate_data_validation()
        logger.info("Data validation step completed")
        print(data_validation_artifact)
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        logger.info("Initiate the data transformation...")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logger.info("Data transformation step completed")
        print(data_transformation_artifact)
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config,data_transformation_artifact)
        logger.info("Initiate the model training...")
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logger.info("Model training step completed")
        print(model_trainer_artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
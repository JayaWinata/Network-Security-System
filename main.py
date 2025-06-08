from src.components.data_ingestion import DataIngestion
from src.exception.exception import NetworkSecurityException
from src.entity.config_entity import DataIngestionConfig
from src.entity.config_entity import TrainingPipelineConfig
from src.logging.logger import logger

import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestiion = DataIngestion(data_ingestion_config)
        logger.info("Initiate the data ingestion...")
        data_ingestion_artifact = data_ingestiion.initiate_data_ingestion()
        print(data_ingestion_artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
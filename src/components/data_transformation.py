from src.logging.logger import logger
from src.entity.config_entity import TrainingPipelineConfig, DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from src.exception.exception import NetworkSecurityException
from src.constant import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from src.utils.utils import save_object, save_numpy_array_data

import os, sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformer_object(cls) -> Pipeline:
        '''
        Initalize a KNNImputer object with the parameters specified in the constant.
        Returning a Pipeline object with the KNNImputer object as the first step
        '''
        logger.info(
            "Entered get_data_transformer_object method in DataTransformation class"
        )
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logger.info(
                f'Initialize KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}'
            )
            preprocessor : Pipeline = Pipeline([('imputer', imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logger.info('Entered intiate_data_transformation method in DataTransformation class')
        try:
            logger.info('Starting data transformation')
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
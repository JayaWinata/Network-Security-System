import os
import sys
import numpy as np
import pandas as pd

'''
Common Constants
'''
TARGET_COLUMN = 'Result'
PIPELINE_NAME = 'NetworkSecurity'
ARTIFACT_DIR = 'Artifacts'
FILE_NAME = 'Dataset Phising Website.csv'

TRAIN_FILE_NAME = 'train.csv'
TEST_FILE_NAME = 'test.csv'

SCHEMA_FILE_PATH = os.path.join('data_schema', 'schema.yaml')

'''
Data Ingestion Constants
'''
DATA_INGESTION_COLLECTION_NAME = 'NetworkData'
DATA_INGESTION_DATABASE_NAME = 'NetworkSecuritySystem'
DATA_INGESTION_DIR_NAME = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR = 'feature_store'
DATA_INGESTION_INGESTED_DIR = 'ingested'
DATA_INGESTION_TEST_RATIO = 0.2

'''
Data Validation Constants
'''
DATA_VALIDATION_DIR_NAME = 'data_validation'
DATA_VALIDATION_VALID_DIR = 'valid'
DATA_VALIDATION_INVALID_DIR = 'invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILENAME = 'report.yaml'
PREPROCESSING_OBJECT_FILE_NAME = 'preprocessing.pkl'

'''
Data Transformation Constants
'''
DATA_TRANSFORMATION_DIR_NAME = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = 'transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = 'transformed_object'


DATA_TRANSFORMATION_IMPUTER_PARAMS = {
    'missing_values': np.nan,
    'n_neighbors': 3,
    'weights': 'uniform'
}
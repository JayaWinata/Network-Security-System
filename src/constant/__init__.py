import os
import sys
import numpy as np
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

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

SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = 'model.pkl'

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

'''
Model Trainer Constants
'''
MODEL_TRAINER_DIR_NAME = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE = 0.6
MODEL_TRAINER_OVERFIT_UNDERFIT_THRESHOLD = 0.05

'''
Cloud related constants
'''

BLOB_URL = os.getenv('BLOB_URL')
BLOB_URL_PARAMS = os.getenv('BLOB_URL_PARAMS')
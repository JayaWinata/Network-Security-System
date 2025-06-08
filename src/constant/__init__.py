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

'''
Data Ingestion Constants
'''
DATA_INGESTION_COLLECTION_NAME = 'NetworkData'
DATA_INGESTION_DATABASE_NAME = 'NetworkSecuritySystem'
DATA_INGESTION_DIR_NAME = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR = 'feature_store'
DATA_INGESTION_INGESTED_DIR = 'ingested'
DATA_INGESTION_TEST_RATIO = 0.2
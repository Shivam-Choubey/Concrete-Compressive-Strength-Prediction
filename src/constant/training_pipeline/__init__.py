import os
import sys
import numpy as np
import pandas as pd

TARGET_COLUMN = "Concrete compressive strength"
PIPELINE_NAME: str = "ConcreteStrength"
ARTIFACT_DIR:str = "Artifacts"
FILE_NAME:str = "Concrete Compressive Strength.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"


# Data Ingestion related Constants
DATA_INGESTION_COLLECTION_NAME: str = "ConcreteData"
DATA_INGESTION_DATABASE_NAME: str = "ConcreteStrengthDatabase"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

# Data validation constants
DATA_VALIDATION_DIR:str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validation"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_PATH: str = "report.yaml"

















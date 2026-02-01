import os
import sys
from src.logging.logger import logging
from src.exception.exception import ConcreteStrengthException
from src.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig


from src.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
from src.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
             raise ConcreteStrengthException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ConcreteStrengthException(e, sys)
    
    def validate_number_of_columns(self, dataframe: pd.DataFrame):
        try:
            # Instead of len(self._schema_config), count the items inside 'columns'
            expected_counts = len(self._schema_config["columns"]) 
            actual_count = len(dataframe.columns)
        
            logging.info(f"Checking columns.... Expected {expected_counts}, Gots: {actual_count}")
        
            if actual_count == expected_counts:
                return True
            return False
        except Exception as e:
            raise ConcreteStrengthException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold = 0.5) -> bool:
        try:
            status = True
            report = {}
            
            for column in base_df.columns:
                train_data = base_df[column]
                test_data = current_df[column]
                
                drift_test = ks_2samp(train_data, test_data)
                
                if threshold <= drift_test.pvalue:
                    drift_found = False
                else:
                    drift_found = True
                    status = False
                return status
                report.update({column: {
                    "p_value": float(drift_test.pvalue),
                    "drift_status": drift_found
                }})
                
            drift_report_path = self.data_validation_config.drift_report_file_path
            
            os.makedirs(os.path.dirname(drift_report_path), exist_ok=True)
            
            abs_path = os.path.abspath(drift_report_path)
            
            logging.info(f"Attempting to save drift report to: {abs_path}")
            
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=report)
            
            if os.path.exists(drift_report_path):
                logging.info(f"Drift report successfully created at: {abs_path}")
            else:
                logging.error(f"FILE SYSTEM ERROR: Report not found at {abs_path} after write command.")
                
        except Exception as e:
            raise ConcreteStrengthException(e, sys)


    def initiate_data_validation(self) -> DataIngestionArtifact:
        try:
            # 1. Get file paths from the Ingestion stage receipt
            train_path = self.data_ingestion_artifact.trained_file_path
            test_path = self.data_ingestion_artifact.test_file_path

            # 2. Load the data into tables
            train_df = self.read_data(train_path)
            test_df = self.read_data(test_path)

            if not self.validate_number_of_columns(dataframe=train_df):
                logging.warning("Training columns do not match the Schema!")
            
            if not self.validate_number_of_columns(dataframe=test_df):
                logging.warning("Testing columns do not match the Schema!")


            drift_status = self.detect_dataset_drift(base_df=train_df, current_df=test_df)


            valid_train_path = self.data_validation_config.valid_train_file_path
            os.makedirs(os.path.dirname(valid_train_path), exist_ok=True)
            
            train_df.to_csv(valid_train_path, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)


            return DataValidationArtifact(
                validation_status=drift_status,
                valid_train_file_path=valid_train_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

        except Exception as e:
            raise ConcreteStrengthException(e, sys)

















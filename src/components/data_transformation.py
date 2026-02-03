import sys
import os
import numpy as np
import pandas as pd
from pyparsing import col
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

# --- Project Specific Imports ---
# These act like configuration switches and data contracts
from src.constant.training_pipeline import TARGET_COLUMN

from src.entity.artifacts_entity import (
    DataTransformationArtifact,  # Output blueprint of this stage
    DataValidationArtifact       # Input blueprint from previous stage
)

from src.entity.config_entity import DataTransformationConfig
from src.exception.exception import ConcreteStrengthException
from src.logging.logger import logging
from src.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(self,
                 data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):

        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise ConcreteStrengthException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ConcreteStrengthException(e, sys)

    def get_data_transformer_object(self) -> Pipeline:

        logging.info("Building RobustScaler Pipeline for outlier handling...")
        try:
            scaler = RobustScaler()

            processor = Pipeline(
                steps=[
                    ("scaler", scaler)
                ]
            )

            return processor
        except Exception as e:
            raise ConcreteStrengthException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
    
        logging.info("Starting data transformation for Concrete Strength dataset...")
        try:
            # STEP 1: Load validated train and test datasets
            train_df = self.read_data(
                self.data_validation_artifact.valid_train_file_path
            )
            test_df = self.read_data(
                self.data_validation_artifact.valid_test_file_path
            )

            train_df.columns = train_df.columns.str.strip()
            test_df.columns = test_df.columns.str.strip()
           
            target_col = None
            for col in train_df.columns:
                if col.lower().startswith("concrete") and "strength" in col.lower():
                    target_col = col
                    break
            if target_col is None:
                raise ConcreteStrengthException(
                    f"Target column not found. Columns: {train_df.columns.tolist()}",
                        sys
                    )            
                
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]
                
            # STEP 3: Get the transformation blueprint
            preprocessor = self.get_data_transformer_object()

            # STEP 4: Learn scaling parameters from training data
            preprocessor_object = preprocessor.fit(input_feature_train_df)

            # STEP 5: Apply the learned transformation
            transformed_input_train_feature = preprocessor_object.transform(
                input_feature_train_df
            )
            transformed_input_test_feature = preprocessor_object.transform(
                input_feature_test_df
            )

            # STEP 6: Combine transformed features with target column
            train_arr = np.c_[
                transformed_input_train_feature,
                np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                transformed_input_test_feature,
                np.array(target_feature_test_df)
            ]

            # STEP 7: Save transformed datasets as NumPy arrays
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr
            )

            # STEP 8: Save the preprocessor object
            # This is reused during inference and deployment
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor_object
            )

            save_object(
                "final_model/preprocessor.pkl",
                preprocessor_object
            )

            # STEP 9: Create and return the artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact

        except Exception as e:
            raise ConcreteStrengthException(e, sys)

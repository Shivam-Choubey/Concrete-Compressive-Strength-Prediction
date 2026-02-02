import os
import sys

# --- 1. ERROR HANDLING & LOGGING ---
from src.exception.exception import ConcreteStrengthException
from src.logging.logger import logging

# --- 2. PIPELINE COMPONENTS ---
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

# --- 3. CONFIGURATIONS ---
from src.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)

# --- 4. ARTIFACTS ---
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)


class TrainingPipeline:
    def __init__(self):
        """
        CONSTRUCTOR:
        Initializes the master configuration for the entire pipeline.
        Sets timestamps and root artifact directories.
        """
        self.training_pipeline_config = TrainingPipelineConfig()

    # ==========================================
    # STEP 1: DATA INGESTION
    # ==========================================
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            logging.info("Step 1: Starting Data Ingestion")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise ConcreteStrengthException(e, sys)

    # ==========================================
    # STEP 2: DATA VALIDATION
    # ==========================================
    def start_data_validation(self,data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            logging.info("Step 2: Starting Data Validation")

            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=data_validation_config
            )

            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact

        except Exception as e:
            raise ConcreteStrengthException(e, sys)

    # ==========================================
    # STEP 3: DATA TRANSFORMATION
    # ==========================================
    def start_data_transformation(
        self,
        data_validation_artifact: DataValidationArtifact
    ) -> DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            logging.info("Step 3: Starting Data Transformation")

            data_transformation = DataTransformation(
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=data_transformation_config
            )

            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            return data_transformation_artifact

        except Exception as e:
            raise ConcreteStrengthException(e, sys)

    # ==========================================
    # STEP 4: MODEL TRAINING
    # ==========================================
    def start_model_trainer(
        self,
        data_transformation_artifact: DataTransformationArtifact
    ) -> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            logging.info("Step 4: Starting Model Training")

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=model_trainer_config
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise ConcreteStrengthException(e, sys)

    # ==========================================
    # MASTER FUNCTION: RUN PIPELINE
    # ==========================================
    def run_pipeline(self) -> ModelTrainerArtifact:
        """
        Connects all pipeline stages sequentially.
        Runs the complete local ML workflow.
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )

            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact=data_validation_artifact
            )

            model_trainer_artifact = self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact
            )

            logging.info("Training Pipeline completed successfully")

            return model_trainer_artifact

        except Exception as e:
            raise ConcreteStrengthException(e, sys)
 
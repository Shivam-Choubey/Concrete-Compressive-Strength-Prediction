import os, sys
from src.logging.logger import logging
from src.exception.exception import ConcreteStrengthException
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.entity.config_entity import (
    DataIngestionConfig, DataValidationConfig,DataTransformationConfig, TrainingPipelineConfig,ModelTrainerConfig
)

if __name__=='__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
    
        # DATA INGESTION (Raw Materials)
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
    
        logging.info("Initiate the data ingestion")
    
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
    
        logging.info("Data Initiation Completed")
    
        print(dataingestionartifact)
    
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        
        logging.info("Initiate the data Validation")
    
        data_validation_artifact = data_validation.initiate_data_validation()
    
        logging.info("data Validation Completed")
    
        print(data_validation_artifact)
    
    
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
    
        data_transformation_artifact = DataTransformation(data_validation_artifact, data_transformation_config)
    
        print(data_transformation_artifact)
    
        logging.info(f"Data Transformation Completed")
    
        logging.info("Model Training started")
        
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        
        # We pass the TRANSFORMATION receipt so the trainer knows where the clean numbers are
        model_trainer = ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_transformation_artifact=data_transformation_artifact
        )
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")
        print(model_trainer_artifact)
        
    except Exception as e:
        raise ConcreteStrengthException(e, sys)
    
import os, sys
from src.logging.logger import logging
from src.exception.exception import ConcreteStrengthException
from src.components.data_ingestion import DataIngestion

from src.entity.config_entity import (
    DataIngestionConfig, TrainingPipelineConfig
)

if __name__=='__main__':
    trainingpipelineonfig = TrainingPipelineConfig()
    
    # DATA INGESTION (Raw Materials)
    dataingestionconfig = DataIngestionConfig(trainingpipelineonfig)
    data_ingestion = DataIngestion(dataingestionconfig)
    
    logging.info("Initiate the data ingestion")
    
    dataingestionartifact = data_ingestion.initiate_data_ingestion()
    
    logging.info("Data Initiation Completed")
    
    print(dataingestionartifact)
    
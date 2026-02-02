from src.entity.artifacts_entity import RegressionMetricArtifact
from src.exception.exception import ConcreteStrengthException
from sklearn.metrics import f1_score,precision_score,recall_score
import sys

def get_regression_score(y_true,y_pred)->RegressionMetricArtifact:
    try:
            
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score=precision_score(y_true,y_pred)

        classification_metric =  RegressionMetricArtifact(f1_score=model_f1_score,
                    precision_score=model_precision_score, 
                    recall_score=model_recall_score)
        return classification_metric
    except Exception as e:
        raise ConcreteStrengthException(e,sys)
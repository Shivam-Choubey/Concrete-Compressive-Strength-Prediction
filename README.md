## Concrete-Compressive-Strength-Prediction

## 📁 Project Architecture
```text
Concrete-Compressive-Strength-Prediction
├── Concrete_Data/
│   └── Concrete Compressive Strength.csv
├── data_schema/
│   └── schema.yaml
├── final_model/
│   ├── model.pkl
│   └── preprocessor.pkl
├── notebook/
│   └── Cement_Strength_Prediction.ipynb
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   ├── data_validation.py
│   │   └── model_trainer.py
│   ├── constant/
│   │   ├── training_pipeline/
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── entity/
│   │   ├── __init__.py
│   │   ├── artifacts_entity.py
│   │   └── config_entity.py
│   ├── exception/
│   │   ├── __init__.py
│   │   └── exception.py
│   ├── logging/
│   │   ├── __init_-.py
│   │   └── logger.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── batch_prediction.py
│   │   └── training_pipeline.py
│   ├── utils/
│   │   ├── main_utils/
│   │   │   ├── __init__.py
│   │   │   └── utils.py
│   │   ├── ml_utils/
│   │   │   ├── metric/
│   │   │   │   ├── __init__.py
│   │   │   │   └── regression_metric.py
│   │   │   └── model/
│   │   │       ├── __init__.py
│   │   │       └── estimator.py
│   │   └── __init__.py
│   └── __init__.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── templates/
│   ├── base.html
│   ├── index.html
│   └── result.html
├── .gitignore
├── app.py
├── main.py
├── push_data.py
├── README.md
├── requirements.txt
├── setup.py
├── test_mongodb.py
└── test.py

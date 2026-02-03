from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import pickle
import os

app = Flask(__name__)

# Load the model
def load_model():
    try:
        with open("./final_model/model.pkl", "rb") as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        print("Model file not found. Please ensure model.pkl exists in final_model/")
        return None

model = load_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        # Get data from form
        data = {
            'Cement': float(request.form['cement']),
            'Blast Furnace Slag': float(request.form['slag']),
            'Fly Ash': float(request.form['fly_ash']),
            'Water': float(request.form['water']),
            'Superplasticizer': float(request.form['superplasticizer']),
            'Coarse Aggregate': float(request.form['coarse_agg']),
            'Fine Aggregate': float(request.form['fine_agg']),
            'Age (day)': int(request.form['age'])
        }
        
        # Create DataFrame
        input_df = pd.DataFrame([data])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        return render_template('result.html', 
                             prediction=f"{prediction:.2f}",
                             **data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict', methods=['POST'])
def api_predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        input_df = pd.DataFrame([[
            data['cement'],
            data['slag'],
            data['fly_ash'],
            data['water'],
            data['superplasticizer'],
            data['coarse_agg'],
            data['fine_agg'],
            data['age']
        ]], columns=[
            "Cement",
            "Blast Furnace Slag",
            "Fly Ash",
            "Water",
            "Superplasticizer",
            "Coarse Aggregate",
            "Fine Aggregate",
            "Age (day)"
        ])
        
        prediction = model.predict(input_df)[0]
        
        return jsonify({
            'prediction': prediction,
            'prediction_mpa': f"{prediction:.2f}",
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
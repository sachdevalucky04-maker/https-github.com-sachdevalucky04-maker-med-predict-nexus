from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
from ml.predict import predict_cancer_risk
from database.db import get_db_connection, init_db
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend
app.config.from_object('config')

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
init_db()

@app.route('/')
def index():
    """Home page"""
    return jsonify({"message": "Cancer Prediction API", "status": "running"})

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict cancer risk based on patient data"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['age', 'gender', 'smoking', 'drinking', 'familyHistory', 'exerciseFrequency']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Make prediction
        risk_score, risk_level, confidence = predict_cancer_risk(data)
        
        # Store prediction in database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO predictions (patient_data, risk_score, risk_level, confidence, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (json.dumps(data), risk_score, risk_level, confidence, datetime.now()))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "riskScore": risk_score,
            "riskLevel": risk_level,
            "confidence": confidence,
            "recommendations": get_recommendations(risk_level)
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Get all patient predictions"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, patient_data, risk_score, risk_level, confidence, created_at
            FROM predictions
            ORDER BY created_at DESC
            LIMIT 100
        """)
        
        predictions = cursor.fetchall()
        
        # Parse JSON patient data
        for prediction in predictions:
            prediction['patient_data'] = json.loads(prediction['patient_data'])
            prediction['created_at'] = prediction['created_at'].isoformat()
        
        cursor.close()
        conn.close()
        
        return jsonify(predictions)
        
    except Exception as e:
        logger.error(f"Error fetching patients: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/train', methods=['POST'])
def train_model():
    """Retrain the ML model"""
    try:
        from ml.train import train_models
        
        # This would typically be run as a background job
        results = train_models()
        
        return jsonify({
            "message": "Model training completed",
            "results": results
        })
        
    except Exception as e:
        logger.error(f"Training error: {str(e)}")
        return jsonify({"error": "Model training failed"}), 500

def get_recommendations(risk_level):
    """Get recommendations based on risk level"""
    recommendations = {
        "Low": [
            "Continue regular health checkups",
            "Maintain healthy lifestyle",
            "Annual screening recommended"
        ],
        "Medium": [
            "Schedule consultation with oncologist",
            "Consider additional screening tests",
            "Monitor symptoms closely",
            "Lifestyle modifications recommended"
        ],
        "High": [
            "Immediate consultation with oncologist required",
            "Comprehensive diagnostic workup needed",
            "Consider genetic counseling",
            "Frequent monitoring essential"
        ]
    }
    return recommendations.get(risk_level, [])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
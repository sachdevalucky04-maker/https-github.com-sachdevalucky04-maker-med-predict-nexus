# Cancer Prediction System - Python Backend

A comprehensive machine learning system for cancer risk prediction using Flask, Scikit-learn, and MySQL.

## 🔹 Features

- **Machine Learning Models**: Multiple algorithms (Logistic Regression, Random Forest, SVM, Neural Networks)
- **RESTful API**: Flask-based backend with CORS support for React frontend
- **Database Management**: MySQL integration with comprehensive schema
- **Data Preprocessing**: Advanced feature engineering and data cleaning
- **Model Training**: Automated training pipeline with performance evaluation
- **Risk Assessment**: Real-time cancer risk prediction with confidence scores
- **Security**: User authentication and data encryption

## 🔹 Tech Stack

- **Backend**: Flask (Python)
- **Machine Learning**: Scikit-learn, TensorFlow/Keras, Pandas, NumPy
- **Database**: MySQL
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Security**: bcrypt, JWT

## 🔹 Installation & Setup

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Git

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd cancer-prediction

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Database Setup

```bash
# Start MySQL service
# On Windows (if using XAMPP):
# Start Apache and MySQL from XAMPP Control Panel

# On macOS:
brew services start mysql

# On Linux:
sudo systemctl start mysql

# Create database (optional - will be created automatically)
mysql -u root -p
CREATE DATABASE cancer_prediction;
exit
```

### Step 3: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your database credentials
# Update MYSQL_PASSWORD with your MySQL root password
```

### Step 4: Initialize Database

```bash
# Initialize database schema
python -c "from database.db import init_db; init_db()"

# Test database connection
python database/db.py
```

### Step 5: Train ML Models

```bash
# Create required directories
mkdir -p models reports

# Train the machine learning models
python ml/train.py

# This will:
# - Generate sample dataset
# - Train multiple ML models
# - Save the best model
# - Create performance reports
```

### Step 6: Start the Server

```bash
# Start Flask development server
python app.py

# Server will run on http://localhost:5000
```

## 🔹 API Endpoints

### Health Check
```
GET /
Response: {"message": "Cancer Prediction API", "status": "running"}
```

### Predict Cancer Risk
```
POST /api/predict
Content-Type: application/json

Request Body:
{
  "age": 45,
  "gender": "Male",
  "smoking": 1,
  "drinking": 0,
  "familyHistory": 1,
  "exerciseFrequency": "rarely",
  "height": 175,
  "weight": 80
}

Response:
{
  "riskScore": 0.65,
  "riskLevel": "Medium",
  "confidence": 0.82,
  "recommendations": [
    "Schedule consultation with oncologist",
    "Consider additional screening tests",
    "Monitor symptoms closely"
  ]
}
```

### Get Predictions History
```
GET /api/patients
Response: Array of prediction records with patient data
```

### Retrain Model
```
POST /api/train
Response: Training results and model performance metrics
```

## 🔹 Project Structure

```
cancer-prediction/
├── app.py                  # Flask main application
├── requirements.txt        # Python dependencies
├── config.py              # Configuration settings
├── .env.example           # Environment variables template
├── ml/
│   ├── preprocess.py      # Data preprocessing functions
│   ├── train.py           # Model training & evaluation
│   └── predict.py         # Prediction logic
├── database/
│   ├── schema.sql         # MySQL table definitions
│   └── db.py              # Database connection & operations
├── models/                # Saved ML models (created after training)
├── reports/               # Model performance reports
└── README_PYTHON.md       # This file
```

## 🔹 Usage Examples

### Testing Predictions

```python
# Test prediction functionality
python ml/predict.py

# This will test the model with sample patient data
```

### Custom Training Data

```python
# Use your own dataset for training
python ml/train.py --data_path your_dataset.csv

# Dataset should have columns:
# age, gender, smoking, drinking, familyHistory, exerciseFrequency, cancer_diagnosis
```

### Database Operations

```python
from database.db import get_patient_by_id, save_prediction

# Get patient by ID
patient = get_patient_by_id(1)

# Save a new prediction
save_prediction(
    patient_data={"age": 45, "gender": "Male"},
    risk_score=0.65,
    risk_level="Medium",
    confidence=0.82
)
```

## 🔹 Model Performance

The system trains and compares multiple ML models:

- **Logistic Regression**: Fast, interpretable baseline
- **Decision Tree**: Simple, rule-based predictions
- **Random Forest**: Ensemble method with feature importance
- **SVM**: Support Vector Machine for complex patterns
- **Neural Network**: Deep learning approach

Performance metrics tracked:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Cross-validation scores

## 🔹 Data Security

- Password hashing with bcrypt
- JWT token authentication
- SQL injection prevention
- Input validation and sanitization
- Audit logging for all database operations

## 🔹 Integration with React Frontend

The Flask API is configured with CORS to work seamlessly with the React frontend:

```bash
# Start both servers:
# Terminal 1 (Python backend):
python app.py

# Terminal 2 (React frontend):
npm run dev

# Frontend will be available at http://localhost:5173
# Backend API at http://localhost:5000
```

## 🔹 Troubleshooting

### Common Issues

1. **MySQL Connection Error**
   ```bash
   # Check if MySQL is running
   sudo systemctl status mysql  # Linux
   brew services list | grep mysql  # macOS
   
   # Verify credentials in .env file
   ```

2. **Model Files Missing**
   ```bash
   # Train the models first
   python ml/train.py
   ```

3. **Permission Errors**
   ```bash
   # Ensure proper file permissions
   chmod +x app.py
   ```

4. **Package Installation Issues**
   ```bash
   # Upgrade pip
   pip install --upgrade pip
   
   # Install packages individually
   pip install flask scikit-learn pandas numpy
   ```

## 🔹 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🔹 License

This project is licensed under the MIT License.

## 🔹 Support

For support and questions:
- Check the troubleshooting section
- Review error logs in the console
- Ensure all dependencies are installed correctly
- Verify database connection and schema
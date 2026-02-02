# AI Impact Job Analyzer 🤖

A Streamlit web application that predicts the impact of AI on job roles using machine learning models trained on 5,000+ job postings from 2010-2025.

## 🌟 Features

- **Industry AI Adoption Stage Prediction**: Determines whether an industry is in Emerging, Growing, or Mature stage of AI adoption
- **Automation Risk Score**: Calculates the likelihood (0-100%) that a job role will be automated
- **AI Job Displacement Risk**: Assesses whether a role has Low, Medium, or High risk of being displaced by AI
- **Interactive Visualizations**: Gauge charts and bar plots for easy interpretation
- **Real-time Predictions**: Instant results based on job parameters

## 🎯 Live Demo

**[Try it on Streamlit Cloud](#)** _(Add your Streamlit Cloud URL here after deployment)_

## 📊 Model Architecture

The prediction pipeline uses a cascading approach with three CatBoost models:

1. **Model 1 (Adoption Stage)**: Predicts `industry_ai_adoption_stage` from base features
2. **Model 2 (Automation Risk)**: Uses adoption stage + base features to predict `automation_risk_score`
3. **Model 3 (Displacement Risk)**: Uses both previous predictions to predict `ai_job_displacement_risk`

### Model Performance
- **Adoption Stage Model**: 100% accuracy
- **Automation Risk Model**: R² = 0.88, RMSE = 0.088
- **Displacement Risk Model**: 33% accuracy (challenging multi-class problem)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd Datathon\ Sample
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the app locally
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
Datathon Sample/
├── app.py                              # Main Streamlit application
├── train_models.py                     # Script to train and save models
├── Modelling.ipynb                     # Original model development notebook
├── ai_impact_jobs_2010_2025(2).csv    # Training dataset (5,000 rows)
├── model_adoption.pkl                  # Trained adoption stage model
├── model_automation.pkl                # Trained automation risk model
├── model_displacement.pkl              # Trained displacement risk model
├── feature_columns.pkl                 # Feature column names
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## 🎮 How to Use

1. **Enter Job Parameters** in the sidebar:
   - Posting Year (2010-2030)
   - City location
   - Company size
   - Industry sector
   - Job title
   - Seniority level
   - AI intensity score (0.0-1.0)
   - Annual salary in USD

2. **Click "Predict"** to generate predictions

3. **View Results**:
   - Industry AI adoption stage
   - Automation risk percentage
   - Job displacement risk level
   - Interactive gauge charts
   - Personalized recommendations

## 🔧 Retraining Models

If you want to retrain the models with new data:

1. Update the CSV file `ai_impact_jobs_2010_2025(2).csv`
2. Run the training script:
```bash
python train_models.py
```
3. The script will generate new `.pkl` files

## 📦 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app.py` as the main file
5. Deploy!

**Important**: Make sure to include these files in your repository:
- `app.py`
- `requirements.txt`
- All `.pkl` model files
- `ai_impact_jobs_2010_2025(2).csv` (optional, only needed for retraining)

### Deploy to Other Platforms

The app can also be deployed to:
- **Heroku**: Use the included `requirements.txt`
- **AWS/Azure/GCP**: Run as a containerized app
- **Local Server**: Use `streamlit run app.py --server.port 80`

## 📊 Input Features

The model uses the following input features:

| Feature | Type | Description |
|---------|------|-------------|
| posting_year | Integer | Year of job posting (2010-2030) |
| city | Categorical | Job location |
| company_size | Categorical | Startup, Small, Medium, Large, Enterprise |
| industry | Categorical | Industry sector |
| job_title | Categorical | Job position |
| seniority_level | Categorical | Experience level |
| ai_intensity_score | Float | AI involvement in role (0.0-1.0) |
| salary_usd | Integer | Annual salary in USD |

## 📈 Output Predictions

| Output | Type | Possible Values |
|--------|------|-----------------|
| industry_ai_adoption_stage | Categorical | Emerging, Growing, Mature |
| automation_risk_score | Float | 0.0 to 1.0 (0% to 100%) |
| ai_job_displacement_risk | Categorical | Low, Medium, High |

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **ML Framework**: CatBoost
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly
- **Model Evaluation**: Scikit-learn

## 📝 Dataset

The model is trained on a synthetic dataset of 5,000 job postings from 2010-2025, covering:
- 8 major cities worldwide
- 8 industry sectors
- 7 job titles
- 6 seniority levels

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Singhanyadav**

## 🙏 Acknowledgments

- Dataset source: AI Impact on Jobs (2010-2025)
- Built with [Streamlit](https://streamlit.io)
- ML models powered by [CatBoost](https://catboost.ai)

---

**⭐ If you find this project useful, please give it a star!**

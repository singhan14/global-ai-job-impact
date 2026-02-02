import streamlit as st
import pandas as pd
import numpy as np
import pickle
from catboost import CatBoostRegressor, CatBoostClassifier
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="AI Impact Job Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
    }
    .prediction-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    h1, h2, h3 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_models():
    """Load pre-trained models"""
    try:
        model_automation = pickle.load(open('model_automation.pkl', 'rb'))
        model_adoption = pickle.load(open('model_adoption.pkl', 'rb'))
        model_displacement = pickle.load(open('model_displacement.pkl', 'rb'))
        feature_columns = pickle.load(open('feature_columns.pkl', 'rb'))
        return model_automation, model_adoption, model_displacement, feature_columns
    except FileNotFoundError:
        st.error("⚠️ Model files not found! Please ensure the .pkl files are in the same directory.")
        return None, None, None, None

def predict_all_outputs(user_input, model_adoption, model_automation, model_displacement, feature_columns):
    """Prediction pipeline following the notebook logic"""
    # Create input dataframe with base features
    input_df = pd.DataFrame([{col: user_input.get(col, None) for col in feature_columns}])
    
    # Step 1: Predict industry AI adoption stage
    adoption = model_adoption.predict(input_df).ravel()
    input_df["industry_ai_adoption_stage"] = adoption
    
    # Step 2: Predict automation risk score
    automation = model_automation.predict(input_df)
    input_df["automation_risk_score"] = automation
    
    # Step 3: Predict AI job displacement risk
    displacement = model_displacement.predict(input_df).ravel()
    
    return {
        "industry_ai_adoption_stage": adoption[0],
        "automation_risk_score": float(automation[0]),
        "ai_job_displacement_risk": displacement[0]
    }

def create_gauge_chart(value, title, max_value=1.0):
    """Create a gauge chart for risk scores"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24, 'color': '#333'}},
        delta={'reference': 0.5},
        gauge={
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 0.33], 'color': '#90EE90'},
                {'range': [0.33, 0.66], 'color': '#FFD700'},
                {'range': [0.66, max_value], 'color': '#FF6347'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0.8
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "darkblue", 'family': "Arial"},
        height=300
    )
    return fig

def main():
    # Header
    st.markdown("<h1 style='text-align: center; font-size: 48px;'>🤖 AI Impact Job Analyzer</h1>", 
                unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>Predict automation risk, job displacement, and industry AI adoption</h3>", 
                unsafe_allow_html=True)
    
    # Load models
    model_automation, model_adoption, model_displacement, feature_columns = load_models()
    
    if model_automation is None:
        st.stop()
    
    # Sidebar for inputs
    st.sidebar.markdown("## 📊 Job Parameters")
    st.sidebar.markdown("---")
    
    # Input fields
    posting_year = st.sidebar.slider(
        "📅 Posting Year",
        min_value=2010,
        max_value=2030,
        value=2025,
        help="Year when the job was posted"
    )
    
    city = st.sidebar.selectbox(
        "🌍 City",
        options=["Bangalore", "London", "Singapore", "Sydney", "Tokyo", "Nairobi", "New York", "San Francisco"],
        index=0,
        help="Location of the job"
    )
    
    company_size = st.sidebar.selectbox(
        "🏢 Company Size",
        options=["Startup", "Small", "Medium", "Large", "Enterprise"],
        index=3,
        help="Size of the hiring company"
    )
    
    industry = st.sidebar.selectbox(
        "🏭 Industry",
        options=["Tech", "Finance", "Healthcare", "Education", "Manufacturing", "Energy", "Government", "Retail"],
        index=0,
        help="Industry sector"
    )
    
    job_title = st.sidebar.selectbox(
        "💼 Job Title",
        options=["ML Engineer", "Data Scientist", "Software Engineer", "AI Researcher", 
                 "Product Manager", "Policy Analyst", "Business Analyst"],
        index=0,
        help="Job position"
    )
    
    seniority_level = st.sidebar.selectbox(
        "📈 Seniority Level",
        options=["Intern", "Junior", "Mid", "Senior", "Lead", "Executive"],
        index=2,
        help="Experience level required"
    )
    
    ai_intensity_score = st.sidebar.slider(
        "🧠 AI Intensity Score",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.01,
        help="How AI-intensive is this role? (0 = Low, 1 = High)"
    )
    
    salary_usd = st.sidebar.number_input(
        "💰 Salary (USD)",
        min_value=10000,
        max_value=500000,
        value=80000,
        step=5000,
        help="Annual salary in USD"
    )
    
    # Prepare user input
    user_input = {
        "posting_year": posting_year,
        "city": city,
        "company_size": company_size,
        "industry": industry,
        "job_title": job_title,
        "seniority_level": seniority_level,
        "ai_intensity_score": ai_intensity_score,
        "salary_usd": salary_usd
    }
    
    # Predict button
    st.sidebar.markdown("---")
    predict_button = st.sidebar.button("🚀 Predict", type="primary", use_container_width=True)
    
    # Main content area
    if predict_button:
        with st.spinner("🔮 Analyzing job characteristics..."):
            # Get predictions
            predictions = predict_all_outputs(
                user_input, 
                model_adoption, 
                model_automation, 
                model_displacement, 
                feature_columns
            )
            
            # Display results in columns
            st.markdown("## 📈 Prediction Results")
            st.markdown("---")
            
            # First row - Metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                    <div class="prediction-card">
                        <h3 style='color: #667eea; text-shadow: none;'>🏭 Industry AI Adoption</h3>
                        <p style='font-size: 32px; font-weight: bold; color: #333; margin: 10px 0;'>{}</p>
                        <p style='color: #666;'>Current stage of AI adoption in the industry</p>
                    </div>
                """.format(predictions["industry_ai_adoption_stage"]), unsafe_allow_html=True)
            
            with col2:
                automation_risk = predictions["automation_risk_score"]
                risk_color = "#90EE90" if automation_risk < 0.33 else ("#FFD700" if automation_risk < 0.66 else "#FF6347")
                st.markdown("""
                    <div class="prediction-card">
                        <h3 style='color: #667eea; text-shadow: none;'>⚙️ Automation Risk</h3>
                        <p style='font-size: 32px; font-weight: bold; color: {}; margin: 10px 0;'>{:.2%}</p>
                        <p style='color: #666;'>Likelihood of job automation</p>
                    </div>
                """.format(risk_color, automation_risk), unsafe_allow_html=True)
            
            with col3:
                displacement_risk = predictions["ai_job_displacement_risk"]
                st.markdown("""
                    <div class="prediction-card">
                        <h3 style='color: #667eea; text-shadow: none;'>🔄 Displacement Risk</h3>
                        <p style='font-size: 32px; font-weight: bold; color: #333; margin: 10px 0;'>{}</p>
                        <p style='color: #666;'>AI-driven job displacement risk</p>
                    </div>
                """.format(displacement_risk), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Second row - Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    create_gauge_chart(
                        predictions["automation_risk_score"],
                        "Automation Risk Score"
                    ),
                    use_container_width=True
                )
            
            with col2:
                # Risk level distribution
                risk_levels = ["Low", "Medium", "High"]
                colors_map = {"Low": "#90EE90", "Medium": "#FFD700", "High": "#FF6347"}
                current_risk = predictions["ai_job_displacement_risk"]
                
                values = [100 if level == current_risk else 20 for level in risk_levels]
                colors = [colors_map[level] if level == current_risk else "#E0E0E0" for level in risk_levels]
                
                fig = go.Figure(data=[go.Bar(
                    x=risk_levels,
                    y=values,
                    marker_color=colors,
                    text=[level if level == current_risk else "" for level in risk_levels],
                    textposition='auto',
                    textfont=dict(size=20, color='white')
                )])
                
                fig.update_layout(
                    title="Job Displacement Risk Level",
                    title_font=dict(size=24, color='#333'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(255,255,255,0.9)',
                    font={'color': "darkblue", 'family': "Arial"},
                    height=300,
                    yaxis=dict(showticklabels=False, showgrid=False),
                    xaxis=dict(title="Risk Level")
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Insights section
            st.markdown("## 💡 Key Insights")
            st.markdown("---")
            
            insights_col1, insights_col2 = st.columns(2)
            
            with insights_col1:
                st.markdown("""
                    <div class="prediction-card">
                        <h4 style='color: #667eea; text-shadow: none;'>📊 Job Profile Summary</h4>
                        <ul style='color: #333;'>
                            <li><strong>Role:</strong> {} | {}</li>
                            <li><strong>Industry:</strong> {} ({})</li>
                            <li><strong>Location:</strong> {}</li>
                            <li><strong>AI Intensity:</strong> {:.1%}</li>
                            <li><strong>Salary:</strong> ${:,}</li>
                        </ul>
                    </div>
                """.format(
                    job_title,
                    seniority_level,
                    industry,
                    company_size,
                    city,
                    ai_intensity_score,
                    salary_usd
                ), unsafe_allow_html=True)
            
            with insights_col2:
                # Generate recommendations based on predictions
                automation_risk = predictions["automation_risk_score"]
                
                if automation_risk < 0.33:
                    recommendation = "✅ Low automation risk - This role is relatively safe from automation in the near future."
                elif automation_risk < 0.66:
                    recommendation = "⚠️ Moderate automation risk - Consider upskilling in areas that complement AI capabilities."
                else:
                    recommendation = "🔴 High automation risk - Strong recommendation to develop skills in creative, strategic, or interpersonal areas."
                
                st.markdown("""
                    <div class="prediction-card">
                        <h4 style='color: #667eea; text-shadow: none;'>🎯 Recommendations</h4>
                        <p style='color: #333; font-size: 16px;'>{}</p>
                        <p style='color: #666; margin-top: 15px;'><strong>Industry Stage:</strong> The {} industry is in the <strong>{}</strong> stage of AI adoption.</p>
                    </div>
                """.format(
                    recommendation,
                    industry,
                    predictions["industry_ai_adoption_stage"]
                ), unsafe_allow_html=True)
    
    else:
        # Welcome message
        st.markdown("""
            <div style='text-align: center; padding: 50px; background: rgba(255,255,255,0.9); border-radius: 15px; margin: 50px 0;'>
                <h2 style='color: #667eea; text-shadow: none;'>👈 Enter job parameters in the sidebar</h2>
                <p style='color: #666; font-size: 18px;'>Fill in the job details and click "Predict" to analyze AI impact on the role</p>
                <br>
                <p style='color: #999;'>This AI-powered analyzer uses CatBoost models trained on 5,000+ job postings (2010-2025) to predict:</p>
                <ul style='color: #666; text-align: left; max-width: 600px; margin: 20px auto;'>
                    <li>Industry AI Adoption Stage (Emerging / Growing / Mature)</li>
                    <li>Automation Risk Score (0-100%)</li>
                    <li>AI Job Displacement Risk (Low / Medium / High)</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: white; padding: 20px;'>
            <p>Built with ❤️ using Streamlit & CatBoost | Data: AI Impact on Jobs (2010-2025)</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

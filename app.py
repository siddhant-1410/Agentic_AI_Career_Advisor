import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import os
import re
from dotenv import load_dotenv
from career_guidance_system import CareerGuidanceSystem
from career_chatbot import display_chat_interface
from email_crew import CareerEmailCrew

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Career Guidance System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .step-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .email-form {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'career_system' not in st.session_state:
        st.session_state.career_system = None
    if 'career_data' not in st.session_state:
        st.session_state.career_data = {}
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'init'
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    if 'system_initialized' not in st.session_state:
        st.session_state.system_initialized = False

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def check_api_keys():
    """Check if required API keys are available in environment"""
    mistral_key = os.getenv("MISTRAL_API_KEY")
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    return mistral_key, serpapi_key

def initialize_system():
    """Initialize the career guidance system with environment variables"""
    if st.session_state.system_initialized:
        return True
    
    mistral_key, serpapi_key = check_api_keys()
    
    if mistral_key:
        try:
            with st.spinner("🔄 Initializing AI system with Mistral..."):
                st.session_state.career_system = CareerGuidanceSystem(
                    mistral_api_key=mistral_key,
                    serpapi_key=serpapi_key
                )
                st.session_state.system_initialized = True
                st.session_state.current_step = 'profile'
                return True
        except Exception as e:
            st.error(f"❌ Error initializing system: {str(e)}")
            return False
    else:
        return False

def display_env_setup_instructions():
    """Display instructions for setting up environment variables"""
    st.markdown("## 🔧 Environment Setup Required")
    
    st.markdown("""
    ### Welcome to the AI Career Guidance System! 🎯
    
    This intelligent system leverages Mistral AI to help you with personalized career guidance.
    
    To get started, you need to set up your API keys in a `.env` file:
    """)
    

    
    st.info("💡 The system works excellently with just the Mistral API key, providing unlimited usage within the generous free tier limits.")

def display_email_interface(career_data):
    """Display email sending interface"""
    st.markdown("### 📧 Email Career Report")
    st.markdown("Send your personalized career analysis report to any email address.")
    
    with st.form("email_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            recipient_email = st.text_input(
                "📧 Recipient Email *",
                placeholder="example@email.com",
                help="Enter the email address where you want to send the report"
            )
            
        with col2:
            recipient_name = st.text_input(
                "👤 Recipient Name (Optional)",
                placeholder="John Doe",
                help="Personalize the email with recipient's name"
            )
        
        email_type = st.selectbox(
            "📄 Email Type",
            ["Simple Summary", "Detailed Analysis with CrewAI"],
            help="Choose between a quick summary or detailed analysis using CrewAI agents"
        )
        
        additional_message = st.text_area(
            "💬 Additional Message (Optional)",
            placeholder="Add any personal message you'd like to include...",
            height=100
        )
        
        submit_button = st.form_submit_button("🚀 Send Email Report", use_container_width=True)
        
        if submit_button:
            if not recipient_email:
                st.error("❌ Please enter a recipient email address.")
            elif not is_valid_email(recipient_email):
                st.error("❌ Please enter a valid email address.")
            else:
                # Initialize email crew
                if 'email_crew' not in st.session_state:
                    st.session_state.email_crew = CareerEmailCrew()
                
                with st.spinner("📨 Sending your career report..."):
                    try:
                        if email_type == "Simple Summary":
                            result = st.session_state.email_crew.send_simple_career_summary(
                                career_data, recipient_email, recipient_name
                            )
                        else:
                            result = st.session_state.email_crew.create_and_send_career_email(
                                career_data, recipient_email, recipient_name
                            )
                        
                        if result["success"]:
                            st.success(f"✅ {result['message']}")
                            st.balloons()
                        else:
                            st.error(f"❌ {result['message']}")
                            
                    except Exception as e:
                        st.error(f"❌ Unexpected error: {str(e)}")
    
    
# Dynamic visualization functions
def generate_dynamic_industry_trends(career_data):
    """Generate dynamic industry trends based on career data"""
    if not career_data or "industry_insights" not in career_data:
        # Fallback trends if no data available
        return {
            "trends": ["Remote Work", "AI Integration", "Sustainability", "Cloud Computing", "Cybersecurity"],
            "scores": [85, 92, 78, 88, 95]
        }
    
    # Extract trends from career insights using keywords
    insights_text = career_data.get("industry_insights", "").lower()
    market_text = career_data.get("market_analysis", "").lower()
    combined_text = insights_text + " " + market_text
    
    # Define trend keywords and their scoring logic
    trend_keywords = {
        "remote work": ["remote", "work from home", "telecommute", "distributed", "hybrid", "flexible"],
        "ai integration": ["artificial intelligence", "ai", "machine learning", "automation", "smart", "intelligent"],
        "sustainability": ["sustainable", "green", "environmental", "eco-friendly", "climate", "renewable"],
        "cloud computing": ["cloud", "aws", "azure", "saas", "infrastructure", "platform", "serverless"],
        "cybersecurity": ["security", "cyber", "privacy", "protection", "data security", "encryption", "breach"],
        "digital transformation": ["digital", "transformation", "modernization", "digitization", "innovation", "tech"],
        "data analytics": ["data", "analytics", "big data", "insights", "business intelligence", "metrics", "visualization"],
        "blockchain": ["blockchain", "cryptocurrency", "decentralized", "distributed ledger", "crypto", "web3"],
        "mobile technology": ["mobile", "smartphone", "app", "ios", "android", "responsive"],
        "iot": ["internet of things", "iot", "connected devices", "smart devices", "sensors"]
    }
    
    trends = []
    scores = []
    
    for trend, keywords in trend_keywords.items():
        # Calculate score based on keyword frequency in insights
        score = 0
        for keyword in keywords:
            score += combined_text.count(keyword) * 10
        
        # Add career-specific boost
        career_name = career_data.get("career_name", "").lower()
        if any(kw in career_name for kw in keywords[:2]):  # Boost if career name contains trend keywords
            score += 25
        
        # Normalize score to 0-100 range with some randomization for realism
        base_score = min(95, max(55, score + np.random.randint(10, 30)))
        
        if score > 0 or len(trends) < 5:  # Ensure at least 5 trends
            trends.append(trend.replace("_", " ").title())
            scores.append(base_score)
    
    # Ensure we have exactly 5 trends
    while len(trends) < 5:
        remaining_trends = list(trend_keywords.keys())
        for trend in remaining_trends:
            formatted_trend = trend.replace("_", " ").title()
            if formatted_trend not in trends:
                trends.append(formatted_trend)
                scores.append(np.random.randint(60, 85))
                break
    
    return {"trends": trends[:5], "scores": scores[:5]}

def display_dynamic_industry_trends(career_data):
    """Display dynamic industry trend chart"""
    trend_data = generate_dynamic_industry_trends(career_data)
    
    # Create the chart
    fig = go.Figure(data=go.Bar(
        x=trend_data["scores"],
        y=trend_data["trends"],
        orientation='h',
        marker=dict(
            color=trend_data["scores"],
            colorscale='Viridis',
            colorbar=dict(title="Impact Score"),
            line=dict(color='rgba(0,0,0,0.5)', width=1)
        ),
        text=[f'{score}' for score in trend_data["scores"]],
        textposition='inside',
        textfont=dict(color='white', size=12, family="Arial Black")
    ))
    
    fig.update_layout(
        title=f"Industry Trend Impact Scores - {career_data.get('career_name', 'Selected Career')}",
        xaxis_title="Impact Score (0-100)",
        yaxis_title="Trends",
        height=400,
        template="plotly_dark",
        showlegend=False,
        margin=dict(l=150, r=50, t=80, b=50),
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def generate_dynamic_salary_data(career_data):
    """Generate dynamic salary data based on career analysis"""
    if not career_data or "market_analysis" not in career_data:
        return {
            "experience_levels": ["Entry Level", "Mid Level", "Senior Level", "Lead/Manager"],
            "salaries": [65000, 85000, 110000, 140000]
        }
    
    market_text = career_data.get("market_analysis", "").lower()
    career_name = career_data.get("career_name", "").lower()
    
    # Base salary ranges by industry type
    base_ranges = {
        "tech": {"entry": 75000, "mid": 100000, "senior": 140000, "lead": 180000},
        "finance": {"entry": 70000, "mid": 95000, "senior": 130000, "lead": 170000},
        "healthcare": {"entry": 60000, "mid": 80000, "senior": 110000, "lead": 145000},
        "education": {"entry": 45000, "mid": 60000, "senior": 80000, "lead": 105000},
        "marketing": {"entry": 50000, "mid": 70000, "senior": 95000, "lead": 125000},
        "creative": {"entry": 45000, "mid": 65000, "senior": 90000, "lead": 120000},
        "engineering": {"entry": 70000, "mid": 90000, "senior": 125000, "lead": 160000},
        "consulting": {"entry": 80000, "mid": 110000, "senior": 150000, "lead": 200000},
        "sales": {"entry": 45000, "mid": 70000, "senior": 100000, "lead": 140000},
        "default": {"entry": 55000, "mid": 75000, "senior": 100000, "lead": 130000}
    }
    
    # Determine industry type based on career name
    industry_type = "default"
    if any(word in career_name for word in ["software", "data", "engineer", "developer", "tech", "programming", "ai", "ml", "cyber"]):
        industry_type = "tech"
    elif any(word in career_name for word in ["finance", "banking", "investment", "accounting", "financial"]):
        industry_type = "finance"
    elif any(word in career_name for word in ["healthcare", "medical", "nurse", "doctor", "therapy", "clinical"]):
        industry_type = "healthcare"
    elif any(word in career_name for word in ["teacher", "education", "professor", "instructor", "academic"]):
        industry_type = "education"
    elif any(word in career_name for word in ["marketing", "advertising", "digital marketing", "brand"]):
        industry_type = "marketing"
    elif any(word in career_name for word in ["design", "creative", "art", "graphic", "ui", "ux", "visual"]):
        industry_type = "creative"
    elif any(word in career_name for word in ["mechanical", "civil", "electrical", "chemical", "aerospace"]):
        industry_type = "engineering"
    elif any(word in career_name for word in ["consultant", "consulting", "advisory", "strategy"]):
        industry_type = "consulting"
    elif any(word in career_name for word in ["sales", "business development", "account", "revenue"]):
        industry_type = "sales"
    
    base_salary = base_ranges[industry_type]
    
    # Add multiplier based on market analysis content
    multiplier = 1.0
    if any(phrase in market_text for phrase in ["high demand", "competitive salary", "shortage", "premium"]):
        multiplier = 1.25
    elif any(phrase in market_text for phrase in ["growing", "increasing", "rising", "strong demand"]):
        multiplier = 1.15
    elif any(phrase in market_text for phrase in ["stable", "steady", "consistent"]):
        multiplier = 1.05
    elif any(phrase in market_text for phrase in ["declining", "competitive market", "oversaturated"]):
        multiplier = 0.9
    
    # Geographic adjustment (if mentioned)
    if any(city in market_text for city in ["san francisco", "silicon valley", "new york", "seattle"]):
        multiplier *= 1.3
    elif any(city in market_text for city in ["austin", "denver", "boston", "washington"]):
        multiplier *= 1.2
    
    return {
        "experience_levels": ["Entry Level (0-2 years)", "Mid Level (3-7 years)", "Senior Level (8-15 years)", "Lead/Manager (15+ years)"],
        "salaries": [
            int(base_salary["entry"] * multiplier),
            int(base_salary["mid"] * multiplier),
            int(base_salary["senior"] * multiplier),
            int(base_salary["lead"] * multiplier)
        ]
    }

def display_dynamic_salary_chart(career_data):
    """Display dynamic salary progression chart"""
    salary_data = generate_dynamic_salary_data(career_data)
    
    fig = go.Figure()
    
    # Add salary line
    fig.add_trace(go.Scatter(
        x=salary_data["experience_levels"],
        y=salary_data["salaries"],
        mode='lines+markers',
        line=dict(color='#00cc96', width=4),
        marker=dict(size=12, color='#00cc96', line=dict(color='white', width=2)),
        name='Salary Progression',
        text=[f'${salary:,}' for salary in salary_data["salaries"]],
        textposition='top center',
        textfont=dict(size=12, color='white')
    ))
    
    # Add area fill
    fig.add_trace(go.Scatter(
        x=salary_data["experience_levels"],
        y=[0] * len(salary_data["experience_levels"]),
        fill='tonexty',
        mode='none',
        fillcolor='rgba(0, 204, 150, 0.2)',
        showlegend=False
    ))
    
    fig.update_layout(
        title=f"Salary Progression - {career_data.get('career_name', 'Selected Career')}",
        xaxis_title="Experience Level",
        yaxis_title="Annual Salary ($)",
        height=400,
        template="plotly_dark",
        showlegend=False,
        yaxis=dict(tickformat='$,.0f'),
        margin=dict(l=80, r=50, t=80, b=80),
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def generate_dynamic_skills_data(career_data):
    """Generate dynamic skills data from career analysis"""
    if not career_data or "research" not in career_data:
        return {
            "skills": ["Technical Skills", "Communication", "Problem Solving", "Leadership", "Creativity"],
            "importance": [85, 75, 90, 70, 65]
        }
    
    research_text = career_data.get("research", "").lower()
    learning_text = career_data.get("learning_roadmap", "").lower()
    combined_text = research_text + " " + learning_text
    
    # Skill categories and their keywords
    skill_categories = {
        "Technical Skills": ["programming", "software", "coding", "development", "technical", "tools", "technology", "systems"],
        "Communication": ["communication", "presentation", "writing", "speaking", "collaboration", "interpersonal", "client"],
        "Problem Solving": ["problem", "analytical", "critical thinking", "troubleshooting", "analysis", "solve", "debug"],
        "Leadership": ["leadership", "management", "team", "supervision", "mentoring", "guide", "lead", "coordinate"],
        "Creativity": ["creative", "design", "innovation", "artistic", "brainstorming", "imagination", "visual", "aesthetic"],
        "Project Management": ["project", "planning", "organization", "coordination", "timeline", "management", "agile", "scrum"],
        "Data Analysis": ["data", "statistics", "excel", "reporting", "metrics", "analysis", "insights", "visualization"],
        "Customer Service": ["customer", "client", "service", "support", "relationship", "satisfaction", "user experience"],
        "Research": ["research", "investigation", "study", "analysis", "explore", "discover", "evidence", "methodology"],
        "Sales & Marketing": ["sales", "marketing", "business development", "networking", "persuasion", "negotiation"]
    }
    
    skills = []
    importance = []
    
    for skill, keywords in skill_categories.items():
        score = 0
        for keyword in keywords:
            score += combined_text.count(keyword) * 8
        
        # Boost score for career-specific skills
        career_name = career_data.get("career_name", "").lower()
        if skill == "Technical Skills" and any(word in career_name for word in ["engineer", "developer", "data", "tech"]):
            score += 30
        elif skill == "Creativity" and any(word in career_name for word in ["design", "creative", "art", "ui", "ux"]):
            score += 30
        elif skill == "Communication" and any(word in career_name for word in ["marketing", "sales", "manager", "consultant"]):
            score += 25
        
        # Normalize and add some realistic variation
        final_score = min(95, max(40, score + np.random.randint(15, 35)))
        
        if score > 0 or len(skills) < 6:
            skills.append(skill)
            importance.append(final_score)
    
    # Sort by importance and take top 6
    combined = list(zip(skills, importance))
    combined.sort(key=lambda x: x[1], reverse=True)
    
    return {
        "skills": [item[0] for item in combined[:6]],
        "importance": [item[1] for item in combined[:6]]
    }

def display_dynamic_skills_radar(career_data):
    """Display dynamic skills radar chart"""
    skills_data = generate_dynamic_skills_data(career_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=skills_data["importance"],
        theta=skills_data["skills"],
        fill='toself',
        name=f'{career_data.get("career_name", "Selected Career")} Skills',
        line=dict(color='#ff6b6b', width=3),
        fillcolor='rgba(255, 107, 107, 0.3)',
        marker=dict(size=8, color='#ff6b6b')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix='%',
                gridcolor='rgba(255,255,255,0.3)',
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.3)',
                tickfont=dict(size=11)
            )
        ),
        title=f"Key Skills Importance - {career_data.get('career_name', 'Selected Career')}",
        height=500,
        template="plotly_dark",
        showlegend=False,
        margin=dict(l=80, r=80, t=80, b=80),
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def generate_dynamic_job_market_data(career_data):
    """Generate dynamic job market distribution data"""
    if not career_data or "market_analysis" not in career_data:
        return {
            "sectors": ["Technology", "Healthcare", "Finance", "Education", "Government"],
            "percentages": [35, 25, 20, 12, 8]
        }
    
    market_text = career_data.get("market_analysis", "").lower()
    career_name = career_data.get("career_name", "").lower()
    
    # Define sector keywords
    sector_keywords = {
        "Technology": ["tech", "software", "it", "startup", "innovation", "digital", "saas", "cloud"],
        "Healthcare": ["healthcare", "medical", "hospital", "clinic", "pharma", "health", "biotech"],
        "Finance": ["finance", "banking", "investment", "insurance", "fintech", "financial services"],
        "Education": ["education", "university", "school", "academic", "training", "learning"],
        "Government": ["government", "public", "federal", "state", "municipal", "agency"],
        "Manufacturing": ["manufacturing", "industrial", "production", "factory", "automotive"],
        "Consulting": ["consulting", "advisory", "professional services", "strategy"],
        "Retail": ["retail", "sales", "commerce", "customer", "e-commerce"],
        "Energy": ["energy", "oil", "renewable", "utilities", "power"],
        "Media": ["media", "entertainment", "publishing", "broadcasting", "content"]
    }
    
    sectors = []
    percentages = []
    
    # Calculate relevance scores for each sector
    sector_scores = {}
    for sector, keywords in sector_keywords.items():
        score = 0
        for keyword in keywords:
            score += market_text.count(keyword) * 8
            if keyword in career_name:
                score += 20  # Boost if career name contains sector keywords
        sector_scores[sector] = score
    
    # Sort by score and create distribution
    sorted_sectors = sorted(sector_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Take top 5 sectors and create realistic distribution
    total_percentage = 100
    for i, (sector, score) in enumerate(sorted_sectors[:5]):
        if i == 0:  # Top sector gets largest share
            percentage = max(25, min(45, 30 + score // 4))
        elif i == 1:  # Second sector
            percentage = max(15, min(30, 20 + score // 6))
        else:  # Other sectors
            percentage = max(5, min(20, 10 + score // 8))
        
        sectors.append(sector)
        percentages.append(percentage)
        total_percentage -= percentage
    
    # Normalize to 100%
    if percentages:
        scale_factor = 100 / sum(percentages)
        percentages = [int(p * scale_factor) for p in percentages]
    
    return {"sectors": sectors, "percentages": percentages}

def display_dynamic_job_market_chart(career_data):
    """Display dynamic job market distribution chart"""
    market_data = generate_dynamic_job_market_data(career_data)
    
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0', '#ffb3e6']
    
    fig = go.Figure(data=go.Pie(
        labels=market_data["sectors"],
        values=market_data["percentages"],
        hole=0.3,
        marker=dict(colors=colors[:len(market_data["sectors"])], line=dict(color='#000000', width=2)),
        textinfo='label+percent',
        textfont=dict(size=12),
        hovertemplate='<b>%{label}</b><br>%{percent}<br>%{value}% of opportunities<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Job Market Distribution - {career_data.get('career_name', 'Selected Career')}",
        height=400,
        template="plotly_dark",
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50),
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_user_profile_form():
    """Display user profile collection form"""
    st.markdown('<div class="main-header"><h1>🎯 AI Career Guidance System</h1><p>Discover Your Perfect Career Path with Mistral AI</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 👤 Tell Us About Yourself")
    st.markdown("Help us provide personalized career recommendations by sharing some information about your background and interests.")
    
    with st.form("user_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("📝 Your Name", placeholder="Enter your full name")
            age = st.number_input("🎂 Age", min_value=16, max_value=80, value=25, step=1)
            education_level = st.selectbox(
                "🎓 Education Level",
                ["High School", "Associate Degree", "Bachelor's Degree", "Master's Degree", "PhD", "Professional Certification", "Self-taught", "Other"]
            )
            experience_years = st.number_input("💼 Years of Work Experience", min_value=0, max_value=50, value=0, step=1)
        
        with col2:
            current_field = st.text_input("🏢 Current Field/Industry (if any)", placeholder="e.g., Marketing, Engineering, Healthcare")
            location = st.text_input("📍 Location", placeholder="e.g., New York, Remote, Flexible")
            career_stage = st.selectbox(
                "🚀 Career Stage",
                ["Student/Recent Graduate", "Early Career (1-5 years)", "Mid-Career (5-15 years)", "Senior (15+ years)", "Career Change", "Returning to Work"]
            )
        
        interests = st.multiselect(
            "🎨 Interests & Passions",
            ["Technology", "Healthcare", "Business", "Creative Arts", "Education", "Science", "Finance", 
             "Engineering", "Social Impact", "Environment", "Sports", "Travel", "Writing", "Design", "Research"]
        )
        
        skills = st.text_area(
            "🛠️ Current Skills",
            placeholder="List your current skills (technical, soft skills, languages, certifications, etc.)",
            height=100
        )
        
        career_goals = st.text_area(
            "🎯 Career Goals & Aspirations",
            placeholder="What are you hoping to achieve in your career? What type of work environment do you prefer?",
            height=100
        )
        
        submit_profile = st.form_submit_button("🚀 Continue to Career Selection", use_container_width=True)
        
        if submit_profile:
            if name and interests and career_goals:
                st.session_state.user_profile = {
                    "name": name,
                    "age": age,
                    "education_level": education_level,
                    "experience_years": experience_years,
                    "current_field": current_field,
                    "location": location,
                    "career_stage": career_stage,
                    "interests": interests,
                    "skills": skills,
                    "career_goals": career_goals
                }
                st.session_state.current_step = 'career_selection'
                st.success("✅ Profile saved! Proceeding to career selection...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Please fill in at least your name, interests, and career goals.")

def display_career_selection():
    """Display career selection interface"""
    st.markdown('<div class="main-header"><h1>🎯 Select Your Career Path</h1><p>Choose a career to analyze or explore our curated options</p></div>', unsafe_allow_html=True)
    
    # Display user greeting
    user_name = st.session_state.user_profile.get("name", "")
    if user_name:
        st.markdown(f"### Hello {user_name}! 👋")
        st.markdown("Based on your profile, here are some career exploration options:")
    
    tab1, tab2 = st.tabs(["🔍 Search Any Career", "📋 Browse Categories"])
    
    with tab1:
        st.markdown("#### 🔍 Search for Any Career")
        
        # Custom career input
        col1, col2 = st.columns([3, 1])
        with col1:
            custom_career = st.text_input(
                "Enter any career you're interested in:",
                placeholder="e.g., Data Scientist, UX Designer, Marketing Manager, Software Engineer",
                key="custom_career_input"
            )
        with col2:
            analyze_custom = st.button("🔍 Analyze Career", use_container_width=True)
        
        if analyze_custom and custom_career:
            if custom_career.strip():
                st.session_state.selected_career = custom_career.strip()
                st.session_state.current_step = 'analysis'
                st.success(f"✅ Analyzing {custom_career}...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Please enter a valid career name.")
    
    with tab2:
        st.markdown("#### 📋 Explore Career Categories")
        
        if st.session_state.career_system:
            career_options = st.session_state.career_system.get_career_options()
            
            # Create columns for categories
            categories = list(career_options.keys())
            cols = st.columns(min(3, len(categories)))
            
            for idx, category in enumerate(categories):
                with cols[idx % len(cols)]:
                    with st.expander(f"🏢 {category}", expanded=False):
                        careers = career_options[category]
                        
                        for career in careers:
                            if st.button(f"📊 {career}", key=f"career_{career}_{category}", use_container_width=True):
                                st.session_state.selected_career = career
                                st.session_state.current_step = 'analysis'
                                st.success(f"✅ Analyzing {career}...")
                                time.sleep(1)
                                st.rerun()
    
    # Profile management
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Profile", use_container_width=True):
            st.session_state.current_step = 'profile'
            st.rerun()
    with col2:
        if st.button("💬 Chat with AI Assistant", use_container_width=True):
            st.session_state.current_step = 'chat'
            st.rerun()

def display_analysis_interface():
    """Display career analysis interface"""
    selected_career = st.session_state.get('selected_career', '')
    
    if not selected_career:
        st.error("❌ No career selected. Please go back and select a career.")
        if st.button("⬅️ Back to Career Selection"):
            st.session_state.current_step = 'career_selection'
            st.rerun()
        return
    
    st.markdown(f'<div class="main-header"><h1>📊 Career Analysis: {selected_career}</h1><p>Comprehensive insights powered by Mistral AI</p></div>', unsafe_allow_html=True)
    
    # Check if analysis already exists
    if selected_career in st.session_state.career_data and st.session_state.analysis_complete:
        career_data = st.session_state.career_data[selected_career]
    else:
        # Run analysis
        with st.spinner(f"🔄 Analyzing {selected_career} career... This may take a moment."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Update progress
                status_text.text("🔍 Researching career overview...")
                progress_bar.progress(25)
                time.sleep(1)
                
                status_text.text("📊 Analyzing market trends...")
                progress_bar.progress(50)
                time.sleep(1)
                
                status_text.text("📚 Creating learning roadmap...")
                progress_bar.progress(75)
                time.sleep(1)
                
                status_text.text("🏢 Gathering industry insights...")
                progress_bar.progress(90)
                
                # Run comprehensive analysis
                career_data = st.session_state.career_system.comprehensive_career_analysis(
                    selected_career, 
                    st.session_state.user_profile
                )
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                time.sleep(1)
                
                # Store results
                st.session_state.career_data[selected_career] = career_data
                st.session_state.analysis_complete = True
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                return
    
    # Display results
    if career_data:
        st.success("✅ Analysis completed successfully!")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Overview", "💼 Market Analysis", "📚 Learning Path", "🏢 Industry Insights", "📊 Data Visualizations"])
        
        with tab1:
            st.markdown("### 📋 Career Overview")
            if career_data.get('research'):
                st.markdown(career_data['research'])
            else:
                st.warning("⚠️ Career overview not available.")
        
        with tab2:
            st.markdown("### 💼 Market Analysis")
            if career_data.get('market_analysis'):
                st.markdown(career_data['market_analysis'])
            else:
                st.warning("⚠️ Market analysis not available.")
        
        with tab3:
            st.markdown("### 📚 Learning Roadmap")
            if career_data.get('learning_roadmap'):
                st.markdown(career_data['learning_roadmap'])
            else:
                st.warning("⚠️ Learning roadmap not available.")
        
        with tab4:
            st.markdown("### 🏢 Industry Insights")
            if career_data.get('industry_insights'):
                st.markdown(career_data['industry_insights'])
            else:
                st.warning("⚠️ Industry insights not available.")
        
        with tab5:
            st.markdown("### 📊 Dynamic Data Visualizations")
            
            if career_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    display_dynamic_salary_chart(career_data)
                    display_dynamic_job_market_chart(career_data)
                
                with col2:
                    display_dynamic_skills_radar(career_data)
                    display_dynamic_industry_trends(career_data)
            else:
                st.warning("⚠️ No data available for visualizations.")
        
        # Email interface
        st.markdown("---")
        display_email_interface(career_data)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💬 Chat with AI", use_container_width=True):
                st.session_state.current_step = 'chat'
                st.rerun()
        
        with col2:
            if st.button("🔍 Analyze Another Career", use_container_width=True):
                st.session_state.current_step = 'career_selection'
                st.session_state.analysis_complete = False
                st.rerun()
        
        with col3:
            if st.button("📊 View Profile", use_container_width=True):
                st.session_state.current_step = 'profile'
                st.rerun()
        
        with col4:
            if st.button("🔄 Refresh Analysis", use_container_width=True):
                # Clear existing data to force refresh
                if selected_career in st.session_state.career_data:
                    del st.session_state.career_data[selected_career]
                st.session_state.analysis_complete = False
                st.rerun()

def display_chat_interface_wrapper():
    """Wrapper for chat interface with navigation"""
    st.markdown('<div class="main-header"><h1>💬 AI Career Assistant</h1><p>Chat with Mistral AI about your career questions</p></div>', unsafe_allow_html=True)
    
    # Get current career data for context
    selected_career = st.session_state.get('selected_career', '')
    career_data = None
    
    if selected_career and selected_career in st.session_state.career_data:
        career_data = st.session_state.career_data[selected_career]
    
    # Display chat interface
    display_chat_interface(career_data, st.session_state.career_system)
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬅️ Back to Analysis", use_container_width=True):
            if selected_career:
                st.session_state.current_step = 'analysis'
            else:
                st.session_state.current_step = 'career_selection'
            st.rerun()
    
    with col2:
        if st.button("🔍 Select Career", use_container_width=True):
            st.session_state.current_step = 'career_selection'
            st.rerun()
    
    with col3:
        if st.button("👤 Edit Profile", use_container_width=True):
            st.session_state.current_step = 'profile'
            st.rerun()

def main():
    """Main application function"""
    initialize_session_state()
    
    # Check if system can be initialized
    if not initialize_system():
        display_env_setup_instructions()
        return
    
    # Main application flow
    current_step = st.session_state.get('current_step', 'profile')
    
    if current_step == 'profile':
        display_user_profile_form()
    elif current_step == 'career_selection':
        display_career_selection()
    elif current_step == 'analysis':
        display_analysis_interface()
    elif current_step == 'chat':
        display_chat_interface_wrapper()
    else:
        # Default to profile
        st.session_state.current_step = 'profile'
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🤖 Powered by Mistral AI | Built with Streamlit | Career Guidance System © 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

import streamlit as st
import pickle
import base64
import pandas as pd

# CSS to set a background image
def set_background(image_path):
    """
    Sets a background image for the Streamlit app.
    """
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_image}");
            background-size: cover; /* Show the full image */
            background-position: center;
            background-repeat: no-repeat; /* Avoid tiling */
            background-attachment: fixed; /* Ensure it stays fixed */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Load the trained model
with open('logistic_regression_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define the feature names expected by the model (replace with your actual feature names)
# Use model.feature_names_in_ if available
if hasattr(model, 'feature_names_in_'):
    feature_names = model.feature_names_in_
else:
    feature_names = [
        'Age', 'MonthlyIncome', 'JobSatisfaction', 'BusinessTravel_Travel_Frequently',
        'BusinessTravel_Travel_Rarely', 'Department_Research & Development', 'Department_Sales',
        'DistanceFromHome', 'Education', 'EnvironmentSatisfaction', 'Gender', 'JobInvolvement',
        'JobLevel', 'MaritalStatus_Married', 'MaritalStatus_Single', 'NumCompaniesWorked',
        'OverTime', 'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction',
        'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
        'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager',
        'EducationField_Life Sciences', 'EducationField_Marketing', 'EducationField_Medical',
        'EducationField_Other', 'EducationField_Technical Degree',
        'JobRole_Human Resources', 'JobRole_Laboratory Technician', 'JobRole_Manager',
        'JobRole_Manufacturing Director', 'JobRole_Research Director', 'JobRole_Research Scientist',
        'JobRole_Sales Executive', 'JobRole_Sales Representative'
    ]

# Set background image
background_image_url = "C:/Users/vinuv/Downloads/emp.image.jpg"
set_background(background_image_url)

# Streamlit app
st.title("🎈 Employee Attrition Prediction 🎈")
st.markdown("### Predict whether an employee is likely to leave the company")

# Add balloons for a celebratory effect
#st.balloons()

# Organize input fields into columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Personal Details")
    age = st.number_input("👤 Age")
    monthly_income = st.number_input("💰 Monthly Income")
    job_satisfaction = st.slider("😊 Job Satisfaction", 1, 4)
    overtime = st.selectbox("⏰ Overtime", ["No", "Yes"])
    business_travel = st.selectbox("✈️ Business Travel", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])
    department = st.selectbox("🏢 Department", ["Research & Development", "Sales", "Human Resources"])
    distance_from_home = st.number_input("🏠 Distance From Home")
    education = st.number_input("🎓 Education", 1, 5)

with col2:
    st.markdown("#### Job Details")
    education_field = st.selectbox("📚 Education Field", ["Life Sciences", "Marketing", "Medical", "Other", "Technical Degree"])
    environment_satisfaction = st.number_input("🌍 Environment Satisfaction", 1, 4)
    gender = st.selectbox("🚻 Gender", ["Male", "Female"])
    job_involvement = st.number_input("💼 Job Involvement", 1, 4)
    job_level = st.number_input("📊 Job Level", 1, 5)
    job_role = st.selectbox("👔 Job Role", [
        "Human Resources", "Laboratory Technician", "Manager", "Manufacturing Director",
        "Research Director", "Research Scientist", "Sales Executive", "Sales Representative"
    ])
    marital_status = st.selectbox("💍 Marital Status", ["Single", "Married", "Divorced"])

with col3:
    st.markdown("#### Work History")
    num_companies_worked = st.number_input("🏢 Number of Companies Worked")
    percent_salary_hike = st.number_input("📈 Percent Salary Hike")
    performance_rating = st.number_input("⭐ Performance Rating", 1, 4)
    relationship_satisfaction = st.number_input("❤️ Relationship Satisfaction", 1, 4)
    stock_option_level = st.number_input("📈 Stock Option Level", 0, 3)
    total_working_years = st.number_input("⏳ Total Working Years")
    training_times_last_year = st.number_input("📚 Training Times Last Year")
    work_life_balance = st.number_input("⚖️ Work Life Balance", 1, 4)

# Additional fields outside columns
st.markdown("#### Additional Details")
years_at_company = st.number_input("🏢 Years At Company")
years_in_current_role = st.number_input("👔 Years In Current Role")
years_since_last_promotion = st.number_input("📅 Years Since Last Promotion")
years_with_curr_manager = st.number_input("👨‍💼 Years With Current Manager")

# Predict button
if st.button("🔮 Predict Attrition Risk"):
    # Encode categorical variables
    overtime_encoded = 1 if overtime == "Yes" else 0
    business_travel_encoded = {
        "Non-Travel": [0, 0],  # Reference category
        "Travel_Rarely": [0, 1],
        "Travel_Frequently": [1, 0]
    }[business_travel]
    department_encoded = {
        "Research & Development": [1, 0],
        "Sales": [0, 1],
        "Human Resources": [0, 0]  # Reference category
    }[department]
    education_field_encoded = {
        "Life Sciences": [1, 0, 0, 0, 0],
        "Marketing": [0, 1, 0, 0, 0],
        "Medical": [0, 0, 1, 0, 0],
        "Other": [0, 0, 0, 1, 0],
        "Technical Degree": [0, 0, 0, 0, 1]
    }[education_field]
    gender_encoded = 1 if gender == "Male" else 0
    job_role_encoded = {
        "Human Resources": [1, 0, 0, 0, 0, 0, 0, 0],
        "Laboratory Technician": [0, 1, 0, 0, 0, 0, 0, 0],
        "Manager": [0, 0, 1, 0, 0, 0, 0, 0],
        "Manufacturing Director": [0, 0, 0, 1, 0, 0, 0, 0],
        "Research Director": [0, 0, 0, 0, 1, 0, 0, 0],
        "Research Scientist": [0, 0, 0, 0, 0, 1, 0, 0],
        "Sales Executive": [0, 0, 0, 0, 0, 0, 1, 0],
        "Sales Representative": [0, 0, 0, 0, 0, 0, 0, 1]
    }[job_role]
    marital_status_encoded = {
        "Single": [1, 0],
        "Married": [0, 1],
        "Divorced": [0, 0]  # Reference category
    }[marital_status]

    # Create input data as a DataFrame
    input_data = {
        'Age': age,
        'MonthlyIncome': monthly_income,
        'JobSatisfaction': job_satisfaction,
        'BusinessTravel_Travel_Frequently': business_travel_encoded[0],
        'BusinessTravel_Travel_Rarely': business_travel_encoded[1],
        'Department_Research & Development': department_encoded[0],
        'Department_Sales': department_encoded[1],
        'DistanceFromHome': distance_from_home,
        'Education': education,
        'EnvironmentSatisfaction': environment_satisfaction,
        'Gender': gender_encoded,
        'JobInvolvement': job_involvement,
        'JobLevel': job_level,
        'MaritalStatus_Married': marital_status_encoded[0],
        'MaritalStatus_Single': marital_status_encoded[1],
        'NumCompaniesWorked': num_companies_worked,
        'OverTime': overtime_encoded,
        'PercentSalaryHike': percent_salary_hike,
        'PerformanceRating': performance_rating,
        'RelationshipSatisfaction': relationship_satisfaction,
        'StockOptionLevel': stock_option_level,
        'TotalWorkingYears': total_working_years,
        'TrainingTimesLastYear': training_times_last_year,
        'WorkLifeBalance': work_life_balance,
        'YearsAtCompany': years_at_company,
        'YearsInCurrentRole': years_in_current_role,
        'YearsSinceLastPromotion': years_since_last_promotion,
        'YearsWithCurrManager': years_with_curr_manager,
        'EducationField_Life Sciences': education_field_encoded[0],
        'EducationField_Marketing': education_field_encoded[1],
        'EducationField_Medical': education_field_encoded[2],
        'EducationField_Other': education_field_encoded[3],
        'EducationField_Technical Degree': education_field_encoded[4],
        'JobRole_Human Resources': job_role_encoded[0],
        'JobRole_Laboratory Technician': job_role_encoded[1],
        'JobRole_Manager': job_role_encoded[2],
        'JobRole_Manufacturing Director': job_role_encoded[3],
        'JobRole_Research Director': job_role_encoded[4],
        'JobRole_Research Scientist': job_role_encoded[5],
        'JobRole_Sales Executive': job_role_encoded[6],
        'JobRole_Sales Representative': job_role_encoded[7]
    }
    input_df = pd.DataFrame([input_data])

    # Ensure the columns are in the same order as the training data
    input_df = input_df[feature_names]

    # Make prediction
    prediction = model.predict(input_df)
    if prediction[0] == 1:
        st.error("🚨 Attrition Risk: High, likely to leave the company 🚨")
    else:
        st.success("🎉 Attrition Risk: Low, unlikely to leave the company 🎉")
        
    # 🎈 Balloon animation for fun
    st.balloons()
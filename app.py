import os
print("Current working directory:", os.getcwd())

from google.oauth2 import service_account
import pandas as pd
import pandas_gbq
import streamlit as st
import numpy as np

# Access the credentials from Streamlit secrets
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

# def authenticate():
#     # Path to the service account key file downloaded from GCP
#     service_account_key_file = '02_WSV\myproject-patrickmesenbrock-ced7cdd7605a.json'

#     # Authenticate using service account credentials
#     credentials = service_account.Credentials.from_service_account_file(
#         service_account_key_file)

#     return credentials

# Call the authenticate function to get the credentials
# CREDENTIALS = authenticate()

PROJECT_ID = st.secrets["gcp_service_account"]["project_id"]
DATASET_ID = "world_value_survey"
TABLE_ID = "wsv_dems_num_focused_PM"
QUERY = f"select * from {DATASET_ID}.{TABLE_ID}"

# Update the in-memory credentials cache
pandas_gbq.context.credentials = CREDENTIALS
pandas_gbq.context.project = PROJECT_ID

# Run the query and return as a pandas DataFrame
df_dems_numeric_focused = pandas_gbq.read_gbq(QUERY)

#create list of unique answers for each variable as basis for defining the input fields
unique_q1_rec = sorted(df_dems_numeric_focused['Q1_rec'].unique())
unique_q2_rec = sorted(df_dems_numeric_focused['Q2_rec'].unique())
unique_q3_rec = sorted(df_dems_numeric_focused['Q3_rec'].unique())
unique_q4_rec = sorted(df_dems_numeric_focused['Q4_rec'].unique())
unique_q5_rec = sorted(df_dems_numeric_focused['Q5_rec'].unique())
unique_q6_rec = sorted(df_dems_numeric_focused['Q6_rec'].unique())
unique_q61_rec = sorted(df_dems_numeric_focused['Q61_rec'].unique())
unique_q71_rec = sorted(df_dems_numeric_focused['Q71_rec'].unique())
unique_q199_rec = sorted(df_dems_numeric_focused['Q199_rec'].unique())
unique_q260 = sorted(df_dems_numeric_focused['Q260'].unique())
unique_q275 = sorted(df_dems_numeric_focused['Q275'].unique())
unique_q288 = sorted(df_dems_numeric_focused['Q288'].unique())
unique_q262 = sorted(df_dems_numeric_focused['Q262'].unique())

#SET UP APP
st.set_page_config(layout="wide")

#Add Title
st.title("Estimating Support for Democracy - Interactive App")
st.markdown("<p style='font-size: 18px;'>Welcome! This interactive tool allows you to calculate the estimated support for democracy among people living in full or flawed democracy. Just set the demographic-socioeconomic factors and the responses to selected questions to the values you like, and see the estimated support for democracy displayed to the right.</p>", unsafe_allow_html=True)

# Create three columns
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

# Function to create a styled slider label with an optional description
def styled_slider_with_description(label, min_value, max_value, value, description=None, key=None):
    st.markdown(f"<span style='font-weight: bold; font-size:16px;'>{label}</span>", unsafe_allow_html=True)
    if description:
        st.markdown(f"<small>{description}</small>", unsafe_allow_html=True)
    slider_value = st.slider("", min_value=min_value, max_value=max_value, value=value, key=key)
    return slider_value

#put fields with Demographic Information in first column
with col1:
    st.header("Demographic Information")
    Q260 = styled_slider_with_description("Sex", min_value=int(min(unique_q260)), max_value=int(max(unique_q260)), value=int(np.median(unique_q260)), description="1 = Male, 2 = Female", key="Q260")
    Q275 = styled_slider_with_description("Education Level", min_value=int(min(unique_q275)), max_value=int(max(unique_q275)), value=int(np.median(unique_q275)), description="1 = Primary, 8 = Postgraduate", key="Q275")
    Q288 = styled_slider_with_description("Income Level", min_value=int(min(unique_q288)), max_value=int(max(unique_q288)), value=int(np.median(unique_q288)), description="1 = Lowest income, 10 = Highest income", key="Q288")
    Q262 = styled_slider_with_description("Age", min_value=int(min(unique_q262)), max_value=int(max(unique_q262)), value=int(np.median(unique_q262)), description="Age in years", key="Q262")

#put fields with Question Responses in second column
with col2:
    st.header("Question Responses")
    Q1_rec = styled_slider_with_description("Importance of Family", min_value=int(min(unique_q1_rec)), max_value=int(max(unique_q1_rec)), value=int(np.median(unique_q1_rec)), description="1 = Not important, 4 = Very important", key="Q1_rec")
    Q2_rec = styled_slider_with_description("Importance of Friends", min_value=int(min(unique_q2_rec)), max_value=int(max(unique_q2_rec)), value=int(np.median(unique_q2_rec)), description="1 = Not important, 4 = Very important", key="Q2_rec")
    Q3_rec = styled_slider_with_description("Importance of Leisure", min_value=int(min(unique_q3_rec)), max_value=int(max(unique_q3_rec)), value=int(np.median(unique_q3_rec)), description="1 = Not important, 4 = Very important", key="Q3_rec")
    Q4_rec = styled_slider_with_description("Importance of Politics", min_value=int(min(unique_q4_rec)), max_value=int(max(unique_q4_rec)), value=int(np.median(unique_q4_rec)), description="1 = Not important, 4 = Very important", key="Q4_rec")

with col3:
    st.header("")
    Q5_rec = styled_slider_with_description("Importance of Work", min_value=int(min(unique_q5_rec)), max_value=int(max(unique_q5_rec)), value=int(np.median(unique_q5_rec)), description="1 = Not important, 4 = Very important", key="Q5_rec")
    Q6_rec = styled_slider_with_description("Importance of Religion", min_value=int(min(unique_q6_rec)), max_value=int(max(unique_q6_rec)), value=int(np.median(unique_q6_rec)), description="1 = Not important, 4 = Very important", key="Q6_rec")
    Q61_rec = styled_slider_with_description("Trust in Strangers", min_value=int(min(unique_q61_rec)), max_value=int(max(unique_q61_rec)), value=int(np.median(unique_q61_rec)), description="1 = No trust, 4 = Complete trust", key="Q61_rec")
    Q71_rec = styled_slider_with_description("Confidence in Government", min_value=int(min(unique_q71_rec)), max_value=int(max(unique_q71_rec)), value=int(np.median(unique_q71_rec)), description="1 = No confidence, 4 = Complete confidence", key="Q71_rec")
    Q199_rec = styled_slider_with_description("Interest in Politics", min_value=int(min(unique_q199_rec)), max_value=int(max(unique_q199_rec)), value=int(np.median(unique_q199_rec)), description="1 = No interest, 4 = Very interested", key="Q199_rec")

#Create results column
with col4:
    st.header("Predicted Democracy Support")
    st.markdown("<p style='font-size: 18px;'>0 = It is not important for me to live in a democracy, 10 = It is vitally important for me to live in a democracy</p>", unsafe_allow_html=True)

#input prediction formula based on the stats model 
    Q250_est = (0.3845 * Q199_rec +
            0.6022 * Q1_rec +
            0.1928 * Q2_rec +
            0.3545 * Q3_rec +
            0.0809 * Q4_rec +
            0.1483 * Q5_rec +
            -0.0600 * Q6_rec +
            0.0960 * Q61_rec +
            0.1776 * Q71_rec +
            0.2771 * Q260 +
            0.0292 * Q262 +
            0.1006 * Q275 +
            0.0429 * Q288)

#display predicted support

    st.markdown(f"<h1 style='text-align: center; color: green;'>{Q250_est:.2f}</h1>", unsafe_allow_html=True)
#Notes:
# {} within a f-string tells python that the value of Q250_est will be calculated and the result then included in final string
#.2f tells python that I want the result to two decimals



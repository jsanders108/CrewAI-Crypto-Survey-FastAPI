import streamlit as st
import pandas as pd
import json
import requests  # To send data to FastAPI
import numpy as np  # Needed for handling NaN and inf values

# FastAPI Endpoint
API_URL = "http://127.0.0.1:8000/run-analysis/"  # Update if FastAPI runs elsewhere

st.title("CrewAI Survey Analysis")

st.write(
    """
    Upload your survey CSV file below. Once the file is uploaded,
    click the **Run Analysis** button to process the data using the CrewAI crew.
    """
)

# Upload widget for CSV file
survey_data_file = st.file_uploader("Upload Survey Data CSV", type=["csv"])

if survey_data_file is not None:
    try:
        df = pd.read_csv(survey_data_file)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        st.stop()  # Stops execution safely

    st.subheader("Data Preview")
    st.dataframe(df.head(10))

    # Run Analysis button: when clicked, send data to FastAPI
    if st.button("Run Analysis"):
        try:
            with st.spinner("Running analysis..."):
                # Replace infinities with NaN
                df.replace([np.inf, -np.inf], np.nan, inplace=True)

                # Convert NaN to None (valid for JSON serialization)
                df_cleaned = df.where(pd.notna(df), None)

                # Convert cleaned DataFrame to JSON
                survey_data = df_cleaned.to_dict(orient="records")

                # Send the data to FastAPI
                response = requests.post(API_URL, json={"survey_data": survey_data})

                if response.status_code == 200:
                    result = response.json().get("result", "No result returned")
                    st.success("Analysis Complete!")
                    st.markdown(result, unsafe_allow_html=True)  # Render Markdown
                else:
                    st.error(f"Error from API: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

import streamlit as st
import pandas as pd
import json
from main import kickoff

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

    # Run Analysis button: when clicked, the crew flow is triggered
    if st.button("Run Analysis"):
        try:
            with st.spinner("Running analysis..."):
                # Convert the uploaded CSV to JSON strings
                survey_data = df.to_json(orient="records")

                # Initialize the Crew Flow and assign the data to its state
                result = kickoff(survey_data)

                # Display the results
                st.success("Analysis Complete!")
                st.markdown(result, unsafe_allow_html=True)  # Render Markdown properly

        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON format: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")


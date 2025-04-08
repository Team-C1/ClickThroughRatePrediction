import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Title and instructions
st.title("Click Prediction Lookup App")
st.markdown("🔍 Enter an **ID** to check if the model predicted a **click (1)** or **no click (0)**.")

# Google Drive file ID (update this!)
GOOGLE_DRIVE_FILE_ID = "1dQXku5c4J6VX-2hQYwQLHblk4jF8PIgp"  # Replace with your actual file ID
CSV_URL = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}"

@st.cache_data(ttl=3600)  # Cache the data for 1 hour
def load_submission_file(url):
    """Downloads the CSV from Google Drive once and caches it."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        return df
    except Exception as e:
        st.error(f"Failed to load submission file: {e}")
        return None

# Load the submission.csv from Drive (cached)
submission_df = load_submission_file(CSV_URL)

if submission_df is not None:
    input_id = st.text_input("Enter ID (numeric):")

    if input_id:
        try:
            input_id = int(input_id)
            row = submission_df[submission_df['id'] == input_id]

            if not row.empty:
                click = row.iloc[0]['click']
                result = "✅ Click (1)" if click == 1 else "❌ No Click (0)"
                st.success(f"Prediction for ID `{input_id}`: **{result}**")
            else:
                st.warning("ID not found in the submission file.")
        except ValueError:
            st.error("Please enter a valid numeric ID.")
else:
    st.error("Unable to load predictions. Please check the Google Drive file ID or URL.")




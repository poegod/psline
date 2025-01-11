import streamlit as st
import pandas as pd
import re

# Helper function to process text based on your rules
def process_text(text):
    if not isinstance(text, str):
        return None  # Return None for non-string values (e.g., NaN)
    
    # Handle brackets: Remove text within brackets but keep words outside
    text = re.sub(r"\(.*?\)", "", text).strip()
    
    # Stop at special delimiters (-, ;, :, ,)
    text = re.split(r"[-;:,]", text)[0].strip()
    
    # Limit to first 4 words
    words = text.split()
    text = " ".join(words[:4])
    
    return text

# Helper function to generate subject line
def generate_subject_line(first_name, business_name, job_title):
    # Process each value based on rules
    first_name = process_text(first_name)
    business_name = process_text(business_name)
    job_title = process_text(job_title) if job_title else None
    
    # Create subject line based on the presence of a job title
    if job_title:
        subject_line = f"Your role at {business_name} (experience as {job_title})"
    else:
        subject_line = f"Your role at {business_name} (your background)"
    
    return subject_line

# Helper function to generate PS line
def generate_ps_line(first_name, business_name, job_title):
    # Process each value based on rules
    first_name = process_text(first_name)
    business_name = process_text(business_name)
    job_title = process_text(job_title) if job_title else None
    
    # Create PS line based on the presence of a job title
    if job_title:
        ps_line = f"I’d love to hear how your experience as {job_title} at {business_name} has shaped your approach."
    else:
        ps_line = f"I’d love to hear how your time at {business_name} has influenced your perspective."
    
    return ps_line

# Streamlit App
st.title("Email Subject and PS Line Generator")
st.write("Upload a CSV file, then map the columns for the generator.")

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load CSV
    data = pd.read_csv(uploaded_file)

    # Display the uploaded file
    st.write("Uploaded Data:")
    st.dataframe(data)

    # Column mapping
    st.write("**Map the columns to the required fields:**")
    first_name_col = st.selectbox("Select the column for First Name:", data.columns)
    business_name_col = st.selectbox("Select the column for Business Name:", data.columns)
    job_title_col = st.selectbox("Select the column for Job Title (optional):", ["None"] + list(data.columns))

    # Process only if all required columns are mapped
    if first_name_col and business_name_col:
        # Generate subject and PS lines
        data['Subject Line'] = data.apply(
            lambda row: generate_subject_line(
                row[first_name_col],
                row[business_name_col],
                row[job_title_col] if job_title_col != "None" else None
            ),
            axis=1
        )
        data['PS Line'] = data.apply(
            lambda row: generate_ps_line(
                row[first_name_col],
                row[business_name_col],
                row[job_title_col] if job_title_col != "None" else None
            ),
            axis=1
        )

        # Display updated data
        st.write("Updated Data with Subject and PS Lines:")
        st.dataframe(data)

        # Provide download link
        st.download_button(
            label="Download Updated CSV",
            data=data.to_csv(index=False),
            file_name="updated_email_data.csv",
            mime="text/csv"
        )
    else:
        st.error("Please ensure all required columns are mapped.")

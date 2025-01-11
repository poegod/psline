import pandas as pd
import re
import math

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

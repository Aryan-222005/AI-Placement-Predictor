import streamlit as st
import pickle
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "..", "model", "placement_model.pkl")
scaler_path = os.path.join(BASE_DIR, "..", "model", "scaler.pkl")

model = pickle.load(open(model_path, "rb"))
scaler = pickle.load(open(scaler_path, "rb"))

# Suggestion engine
def generate_suggestions(data):

    suggestions = []

    if data["Communication_Skills"] < 60:
        suggestions.append("Improve communication skills through mock interviews or presentations.")

    if data["Backlogs"] > 0:
        suggestions.append("Try to clear academic backlogs as they negatively affect placement chances.")

    if data["Projects"] < 2:
        suggestions.append("Build more real-world projects to strengthen your resume.")

    if data["Coding_Skills"] < 70:
        suggestions.append("Practice coding problems regularly (LeetCode, HackerRank, Codeforces).")

    if data["Certifications"] < 1:
        suggestions.append("Consider completing relevant certifications to strengthen your profile.")

    return suggestions


# Page title
st.title("🎓 AI Placement Predictor")

st.write("Enter your academic and skill details to estimate your placement probability and get improvement suggestions.")

# Inputs

age = st.number_input("Age", 18, 30, value=21)

cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)

internships = st.number_input("Internships", 0, 10, value=1)

projects = st.number_input("Projects", 0, 10, value=2)

coding_skills = st.slider("Coding Skills", 0, 100, 60)

communication_skills = st.slider("Communication Skills", 0, 100, 60)

aptitude = st.slider("Aptitude Test Score", 0, 100, 60)

soft_skills = st.slider("Soft Skills Rating", 0, 100, 60)

certifications = st.number_input("Certifications", 0, 10, value=0)

backlogs = st.number_input("Backlogs", 0, 10, value=0)

# Prediction button
if st.button("Predict Placement"):

    # Input format must match training features
    input_data = np.array([[
        age,            # Age
        0,              # Gender (placeholder)
        0,              # Degree (placeholder)
        0,              # Branch (placeholder)
        cgpa,
        internships,
        projects,
        coding_skills,
        communication_skills,
        aptitude,
        soft_skills,
        certifications,
        backlogs
    ]])

    # Scale input
    input_scaled = scaler.transform(input_data)

    # Predict probability
    prob = model.predict_proba(input_scaled)[0][1]

    # Convert to percentage
    percentage = prob * 100

    # Force decimal display
    st.subheader("Placement Probability: {:.2f}%".format(percentage))

    # Progress bar still needs integer
    st.progress(int(percentage))

    # Suggestions
    student_data = {
        "Communication_Skills": communication_skills,
        "Backlogs": backlogs,
        "Projects": projects,
        "Coding_Skills": coding_skills,
        "Certifications": certifications
    }

    suggestions = generate_suggestions(student_data)

    st.subheader("Suggestions")

    if len(suggestions) == 0:
        st.success("Great profile! You already have strong placement potential.")
    else:
        for s in suggestions:
            st.write("•", s)
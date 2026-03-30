ResumeIQ – AI-Powered Resume Analyzer
Overview

ResumeIQ is an AI-powered web application that analyzes resumes and provides intelligent career insights. It predicts suitable job roles, calculates ATS scores, identifies missing skills, and suggests improvements to enhance employability.
Features
Upload resumes (PDF, DOCX, TXT)
Machine Learning-based job role prediction
Match score based on model confidence
ATS (Applicant Tracking System) score calculation
Skill extraction from resume
Missing skill detection
Job role recommendations
Personalized action plan
Resume improvement feedback
Modern UI using HTML & CSS
Technologies Used
Programming Language: Python
Framework: Flask
Machine Learning:
TF-IDF (Text Vectorization)
Logistic Regression (Classification Model)
Libraries:
scikit-learn
pandas
numpy
nltk
pdfplumber
python-docx

Dataset
Source: Kaggle
Link: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
The dataset contains categorized resumes and is combined with custom data for better performance.
⚙️ Installation

Install the required dependencies:

pip install flask scikit-learn pandas numpy nltk PyPDF2
pip install pdfplumber
pip install python-docx
How to Run
Step 1: Train the Model
python train_model.py
Step 2: Run the Application
python app.py
Step 3: Open in Browser
http://127.0.0.1:5000/

How It Works
User uploads a resume
Text is extracted from the file
Text is converted into TF-IDF vectors
Logistic Regression model predicts job role
System calculates match score and ATS score
Skills are extracted and analyzed
Missing skills and suggestions are generated

Project Structure
ResumeIQ/
│
├── app.py
├── train_model.py
├── dataset.csv
│
├── model/
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── README.md


 Conclusion

ResumeIQ helps automate resume analysis using Machine Learning. It provides job role predictions, skill gap analysis, and actionable feedback, making it a useful tool for job seekers to improve their resumes and increase employability.

Author
Developed as part of an academic project --Chirag S K

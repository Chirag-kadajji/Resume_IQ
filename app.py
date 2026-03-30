from flask import Flask, render_template, request
import pickle
import pdfplumber
from docx import Document

app = Flask(__name__)

# Load model
model = pickle.load(open("model/model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

# -------------------------------
# TEXT EXTRACTION
# -------------------------------
def extract_text(file):
    text = ""
    try:
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

        elif filename.endswith(".txt"):
            text = file.read().decode("utf-8")

        elif filename.endswith(".docx"):
            doc = Document(file)
            for para in doc.paragraphs:
                text += para.text + "\n"

    except Exception as e:
        print("ERROR:", e)
        text = ""

    return text.strip()


# -------------------------------
# SKILLS
# -------------------------------
def extract_skills(text):
    skills_list = [
        "python", "java", "c++", "machine learning", "data science",
        "html", "css", "javascript", "react", "node", "sql",
        "android", "kotlin", "flask", "django"
    ]

    found = []
    text = text.lower()

    for skill in skills_list:
        if skill in text:
            found.append(skill)

    return found


# -------------------------------
# ROLE BASED ATS SCORE
# -------------------------------
role_skills = {
    "Web Development": ["html", "css", "javascript", "react", "node", "sql"],
    "Data Science": ["python", "machine learning", "pandas", "numpy", "sql"],
    "Backend Developer": ["java", "spring", "sql", "api"],
    "Android Developer": ["kotlin", "android", "java"]
}

def calculate_ats(skills, role):
    required = role_skills.get(role, [])
    if not required:
        return 0
    matched = [s for s in skills if s in required]
    return round((len(matched) / len(required)) * 100, 2)


# -------------------------------
# SKILL GAP
# -------------------------------
def skill_gap(skills, role):
    required = role_skills.get(role, [])
    return [s for s in required if s not in skills]


# -------------------------------
# JOB SUGGESTIONS
# -------------------------------
def suggest_jobs(skills):
    if "machine learning" in skills:
        return ["Data Scientist", "ML Engineer"]
    elif "html" in skills or "css" in skills:
        return ["Frontend Developer", "Web Developer", "UI Developer"]
    elif "java" in skills:
        return ["Backend Developer", "Java Developer"]
    return ["Software Engineer"]


# -------------------------------
# ✅ NEW FEATURE 1: ACTION PLAN
# -------------------------------
def generate_action_plan(role, missing_skills):
    plan = []

    if role == "Web Development":
        if "react" in missing_skills:
            plan.append("Learn React (important for frontend jobs)")
        if "node" in missing_skills:
            plan.append("Learn Node.js for backend integration")

        plan.append("Build 2 frontend projects")
        plan.append("Upload projects to GitHub")

    elif role == "Data Science":
        plan.append("Practice Machine Learning models")
        plan.append("Work on datasets (Kaggle)")
        plan.append("Build 2 data science projects")

    elif role == "Backend Developer":
        plan.append("Learn Spring Boot deeply")
        plan.append("Build REST APIs")
        plan.append("Work with SQL databases")

    elif role == "Android Developer":
        plan.append("Build Android apps using Kotlin")
        plan.append("Use Firebase for backend")
        plan.append("Publish app on Play Store")

    return plan


# -------------------------------
# ✅ NEW FEATURE 3: RESUME FEEDBACK
# -------------------------------
def resume_feedback(text, skills):
    feedback = []
    text_lower = text.lower()

    if len(skills) < 5:
        feedback.append("Add more technical skills")

    if "project" not in text_lower:
        feedback.append("Include project experience section")

    if "github" not in text_lower:
        feedback.append("Add GitHub profile link")

    if not any(word in text_lower for word in ["developed", "built", "designed"]):
        feedback.append("Use strong action words like Developed, Built, Designed")

    if len(text.split()) < 100:
        feedback.append("Resume is too short, add more content")

    # ✅ ALWAYS ADD THIS
    if not feedback:
        feedback.append("Your resume looks good, but you can improve by adding more projects and measurable achievements")

    return feedback


# -------------------------------
# MAIN ROUTE
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    skills = []
    score = 0
    ats_score = 0
    missing_skills = []
    job_roles = []
    action_plan = []
    feedback = []

    if request.method == "POST":
        file = request.files.get("resume")

        if not file or file.filename == "":
            return render_template("index.html",
                                   prediction="No file selected",
                                   score=0, ats_score=0,
                                   skills=[], missing_skills=[],
                                   job_roles=[],
                                   action_plan=[], feedback=[])

        text = extract_text(file)

        if text == "":
            return render_template("index.html",
                                   prediction="Could not read file",
                                   score=0, ats_score=0,
                                   skills=[], missing_skills=[],
                                   job_roles=[],
                                   action_plan=[], feedback=[])

        vec = vectorizer.transform([text])

        prediction = model.predict(vec)[0]

        prob = model.predict_proba(vec)
        score = round(max(prob[0]) * 100, 2)

        skills = extract_skills(text)

        ats_score = calculate_ats(skills, prediction)

        missing_skills = skill_gap(skills, prediction)
        job_roles = suggest_jobs(skills)

        # ✅ NEW FEATURES
        action_plan = generate_action_plan(prediction, missing_skills)
        feedback = resume_feedback(text, skills)

    return render_template("index.html",
                           prediction=prediction,
                           skills=skills,
                           score=score,
                           ats_score=ats_score,
                           missing_skills=missing_skills,
                           job_roles=job_roles,
                           action_plan=action_plan,
                           feedback=feedback)


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
import PyPDF2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# 📁 Make 'uploads' folder if it's not there
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 🧠 Load skill list
def load_skills():
    with open("skills_list.txt", "r") as f:
        return [line.strip().lower() for line in f]

# 📄 Load job description text
def load_job_description():
    with open("job_description.txt", "r", encoding="utf-8") as f:
        return f.read().lower()

# 📄 Extract text from resume PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text.lower()

# 🤖 Analyze skills
def analyze_skills(resume_text, job_text, skill_list):
    resume_skills = set(skill for skill in skill_list if skill in resume_text)
    job_skills = set(skill for skill in skill_list if skill in job_text)
    missing_skills = job_skills - resume_skills
    return resume_skills, missing_skills

# 🏠 Home page
@app.route("/")
def home():
    return render_template("index.html")

# 📤 Resume upload handler
@app.route("/upload", methods=["POST"])
def upload():
    if 'resume' not in request.files:
        return redirect(request.url)
    
    file = request.files['resume']
    if file.filename == '':
        return redirect(request.url)

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    resume_text = extract_text_from_pdf(filepath)
    job_text = load_job_description()
    skills = load_skills()

    resume_skills, missing_skills = analyze_skills(resume_text, job_text, skills)

    return render_template("index.html", resume_skills=resume_skills, missing_skills=missing_skills)

# 🚀 Run the app
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import joblib
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # Set a secret key for session management

# Load trained model
model = joblib.load("career_model.pkl")
encoders = joblib.load("encoders.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.json
    stage = data.get("stage", "BTech")
    stream = data.get("stream", "BTech CSE")
    interest = data.get("interest", "AI")
    goal = data.get("goal", "Job")
    # Skill was removed from UI, we will provide a default to keep the ML model happy
    skill = "Problem Solving"

    # Map new UI values to old ML dataset values if necessary
    stage_map = {
        "10th Class": "10th",
        "Intermediate": "Intermediate",
        "Diploma": "BTech", # map diploma to BTech for dummy dataset
        "B.Tech": "BTech",
        "Degree": "Degree"
    }
    
    stream_map = {
        "General": "General",
        "Not Decided Yet": "General",
        "MPC": "MPC",
        "BiPC": "BiPC",
        "MEC": "MEC",
        "CEC": "CEC",
        "Computer Science Engineering (CSE)": "BTech CSE",
        "Information Technology (IT)": "BTech CSE",
        "Artificial Intelligence & Machine Learning (AI & ML)": "BTech CSE",
        "Artificial Intelligence & Data Science (AI & DS)": "BTech CSE",
        "Electronics & Communication Engineering (ECE)": "BTech CSE", # fallback
        "Electrical & Electronics Engineering (EEE)": "BTech CSE",
        "Mechanical Engineering": "BTech CSE",
        "Civil Engineering": "BTech CSE",
        "Chemical Engineering": "BTech CSE",
        "Computer Engineering": "BTech CSE",
        "Automobile Engineering": "BTech CSE",
        "B.Sc Computer Science": "Degree",
        "BCA": "Degree",
        "B.Com": "BCom",
        "BBA": "BCom",
        "BA": "General"
    }
    
    interest_map = {
        "Artificial Intelligence": "AI",
        "Software Development": "Software",
        "Data Science": "Data Science",
        "Cyber Security": "Cyber Security",
        "Robotics": "Robotics",
        "Medicine": "Medicine",
        "Business": "Business",
        "Government Jobs": "Government",
        "Design": "Design"
    }

    goal_map = {
        "Job": "Job",
        "Business": "Startup",
        "Higher Studies": "Higher Studies"
    }

    ml_stage = stage_map.get(stage, "BTech")
    ml_stream = stream_map.get(stream, "BTech CSE")
    ml_interest = interest_map.get(interest, "AI")
    ml_goal = goal_map.get(goal, "Job")

    try:
        # Encode input
        input_data = {
            "CurrentStage": encoders["CurrentStage"].transform([ml_stage])[0],
            "Stream": encoders["Stream"].transform([ml_stream])[0],
            "Skill": encoders["Skill"].transform([skill])[0],
            "Interest": encoders["Interest"].transform([ml_interest])[0],
            "Goal": encoders["Goal"].transform([ml_goal])[0]
        }

        df = pd.DataFrame([input_data])
        result = model.predict(df)[0]
        course, career, future = result.split(" | ")
    except Exception as e:
        # Fallback if any mapping fails
        course = f"Advanced {ml_interest} Specialization"
        career = f"{ml_interest} Engineer / Specialist"
        future = "High Growth, 20%+ YoY"

    # Detailed Dynamic Data Generation
    # Generate detailed skills based on interest
    skills_map = {
        "AI": ["Python", "Machine Learning (Scikit-Learn)", "Deep Learning (PyTorch/TensorFlow)", "Mathematics (Linear Algebra, Calculus)", "Data Preprocessing"],
        "Software": ["Data Structures & Algorithms", "System Design", "Version Control (Git)", "Backend Development (Node.js/Python)", "Frontend (React/Angular)"],
        "Data Science": ["Python/R", "SQL", "Data Visualization (Tableau/PowerBI)", "Statistics & Probability", "Machine Learning Models"],
        "Cyber Security": ["Networking Protocols", "Ethical Hacking", "Cryptography", "Linux Admin", "Security Monitoring (SIEM)"],
        "Robotics": ["C++/Python", "ROS (Robot Operating System)", "Embedded Systems", "Control Theory", "Computer Vision"],
        "Medicine": ["Anatomy & Physiology", "Medical Terminology", "Patient Care", "Clinical Diagnostics", "Pharmacology basics"],
        "Business": ["Strategic Planning", "Financial Analysis", "Leadership", "Marketing Strategy", "Project Management"],
        "Government": ["Public Administration", "Constitutional Law", "General Knowledge", "Current Affairs", "Analytical Reasoning"],
        "Design": ["UI/UX Principles", "Figma/Adobe XD", "Color Theory", "Typography", "Interaction Design"]
    }
    
    # Generate detailed roadmap based on goal and interest
    roadmap_map = {
        "Job": [
            f"Month 1-3: Master the core fundamentals of {ml_interest} and complete at least 2 beginner projects.",
            f"Month 4-6: Learn advanced concepts and build a portfolio-worthy capstone project in {career}.",
            f"Month 7-8: Prepare for technical interviews, practice coding/case studies daily.",
            f"Month 9: Start networking on LinkedIn and apply for Junior {career} roles.",
            f"Month 10-12: Secure an entry-level position and focus on continuous on-the-job learning."
        ],
        "Startup": [
            f"Phase 1: Identify a unique problem in the {ml_interest} sector and validate your idea with potential customers.",
            f"Phase 2: Build a Minimum Viable Product (MVP) focusing on core features.",
            f"Phase 3: Learn basic business operations, legal structuring, and digital marketing.",
            f"Phase 4: Launch your MVP, gather user feedback, and iterate the product.",
            f"Phase 5: Pitch to angel investors or apply for startup incubators for seed funding."
        ],
        "Higher Studies": [
            f"Year 1: Maintain a high GPA and build a strong foundation in {ml_interest}.",
            f"Year 2: Participate in research projects or publish papers related to {career}.",
            f"Year 3: Prepare for entrance exams (GRE, GMAT, GATE, etc.) and shortlist top universities.",
            f"Year 4: Secure strong letters of recommendation, write a compelling Statement of Purpose, and apply."
        ]
    }
    
    # Salary mapping
    salary_map = {
        "AI": "$80,000 - $150,000 / year",
        "Software": "$70,000 - $130,000 / year",
        "Data Science": "$75,000 - $140,000 / year",
        "Cyber Security": "$85,000 - $145,000 / year",
        "Robotics": "$80,000 - $135,000 / year",
        "Medicine": "$100,000 - $250,000+ / year",
        "Business": "$60,000 - $120,000 / year",
        "Government": "$50,000 - $90,000 / year (plus benefits)",
        "Design": "$55,000 - $110,000 / year"
    }

    skills_to_learn = skills_map.get(ml_interest, ["Continuous Learning", "Problem Solving", "Adaptability", "Communication"])
    roadmap = roadmap_map.get(ml_goal, [
        f"1. Understand the core concepts of {ml_interest}.",
        f"2. Apply your skills practically in {career}.",
        f"3. Seek mentorship and network.",
        f"4. Achieve your goal in {ml_goal}."
    ])
    expected_salary = salary_map.get(ml_interest, "$50,000 - $100,000 / year")

    # Save to session
    session['dashboard_data'] = {
        "course": course,
        "career": career,
        "future": future,
        "skills": skills_to_learn,
        "roadmap": roadmap,
        "salary": expected_salary
    }

    return jsonify(session['dashboard_data'])

@app.route("/dashboard")
def dashboard():
    data = session.get('dashboard_data')
    if not data:
        # Redirect back to home if there is no data
        return redirect(url_for('home'))
    return render_template("dashboard.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
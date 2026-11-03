# SkillZen AI – AI-Driven Internship Recommendation and Skill Gap Analysis System

## 📌 Project Overview

**SkillZen AI** is an intelligent internship recommendation platform designed to help VTU engineering students find suitable internship opportunities based on their skills, CGPA, and programming language knowledge.

The platform uses Artificial Intelligence and Machine Learning techniques to recommend relevant companies, identify skill gaps, and generate personalized learning roadmaps.

The main objective is to help students make better internship decisions and improve their skills for industry requirements.

## 🎯 Objectives

- Recommend suitable internships based on student profiles.
- Match students with relevant VTU-approved companies.
- Identify missing skills required for internships.
- Generate personalized learning roadmaps.
- Help students improve their internship readiness.

## ✨ Key Features

- **AI-Based Internship Recommendation:** Matches students with companies based on their profile.
- **Personalized Matching Score:** Calculates compatibility between students and companies.
- **Company Ranking:** Ranks 15 VTU-approved companies according to student compatibility.
- **Skill Gap Analysis:** Identifies skills that students need to improve.
- **Learning Roadmap:** Generates a personalized 6-month learning roadmap across 5 domains.
- **Student Profile Analysis:** Considers CGPA, skills, and programming languages.

## 🧠 AI and Machine Learning Algorithm

SkillZen AI uses **TF-IDF Vectorization and Cosine Similarity** to analyze student profiles and company requirements.

### Algorithm

1. Collect student information such as skills, CGPA, and programming languages.
2. Collect company requirements and internship details.
3. Convert relevant text data into numerical vectors using TF-IDF.
4. Calculate similarity between student skills and company requirements using Cosine Similarity.
5. Apply weighted scoring to evaluate internship compatibility.
6. Rank companies based on the final matching score.
7. Identify skill gaps and generate a personalized learning roadmap.

### Matching Score

The platform uses the following weighted scoring system:

| Criteria | Weight |
|---|---:|
| Skills Matching | 50% |
| CGPA Matching | 30% |
| Programming Language Matching | 20% |
| **Total** | **100%** |

The final score helps determine how suitable a company is for a particular student.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Backend web framework |
| Scikit-learn | Machine Learning and AI matching |
| TF-IDF | Text vectorization |
| Cosine Similarity | Student-company similarity calculation |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend interactions |
| SQL Database | Student and company data management |

## 🏗️ System Architecture

The platform follows a full-stack web application architecture.

**Student → Profile Input → Flask Backend → AI Matching Engine → Company Ranking → Skill Gap Analysis → Learning Roadmap**

## 🚀 Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Pavan9741-ux/Skillzen_AI-Project.git
```

### 2. Navigate to the Project Directory

```bash
cd Skillzen_AI-Project
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python run.py
```

Open the local URL displayed in your terminal to access the application.

## 📊 Expected Results

- Provides personalized internship recommendations.
- Ranks companies according to student compatibility.
- Calculates internship matching scores.
- Identifies student skill gaps.
- Generates a personalized 6-month learning roadmap.

## 🎓 Project Information

- **Project Name:** SkillZen AI
- **Project Type:** Artificial Intelligence and Machine Learning
- **Domain:** Internship Recommendation and Skill Gap Analysis
- **Target Users:** VTU Engineering

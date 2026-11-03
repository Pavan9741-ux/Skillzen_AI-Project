"""
SkillZen AI v2.0 - Complete Database Models
Extended with analytics, profiles, and tracking
"""

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import json


class Admin(UserMixin, db.Model):
    """Admin user model"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'


class Company(db.Model):
    """Company model for internship opportunities"""
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    
    # Contact
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    
    # Requirements
    min_cgpa = db.Column(db.Float, default=6.0)
    min_sgpa = db.Column(db.Float, default=6.0)
    
    # Skills (JSON)
    technical_skills = db.Column(db.Text, nullable=False)
    non_technical_skills = db.Column(db.Text, nullable=True)
    programming_languages = db.Column(db.Text, nullable=False)
    
    # Details
    internship_duration = db.Column(db.String(50), nullable=True)
    stipend_range = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    vtu_approved = db.Column(db.Boolean, default=True)
    
    # Analytics
    view_count = db.Column(db.Integer, default=0)
    application_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_technical_skills(self):
        return json.loads(self.technical_skills) if self.technical_skills else []
    
    def get_non_technical_skills(self):
        return json.loads(self.non_technical_skills) if self.non_technical_skills else []
    
    def get_programming_languages(self):
        return json.loads(self.programming_languages) if self.programming_languages else []
    
    def set_technical_skills(self, skills_list):
        self.technical_skills = json.dumps(skills_list)
    
    def set_non_technical_skills(self, skills_list):
        self.non_technical_skills = json.dumps(skills_list)
    
    def set_programming_languages(self, languages_list):
        self.programming_languages = json.dumps(languages_list)
    
    def __repr__(self):
        return f'<Company {self.name}>'


class StudentProfile(db.Model):
    """Basic student profile for recommendations"""
    __tablename__ = 'student_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    
    cgpa = db.Column(db.Float, nullable=False)
    sgpa = db.Column(db.Float, nullable=True)
    
    technical_skills = db.Column(db.Text, nullable=False)
    non_technical_skills = db.Column(db.Text, nullable=True)
    programming_languages = db.Column(db.Text, nullable=False)
    
    recommendations = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<StudentProfile {self.session_id}>'


class StudentProfileExtended(db.Model):
    """Extended student profile with full details"""
    __tablename__ = 'student_profiles_extended'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Personal Information
    full_name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    phone = db.Column(db.String(20), nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    
    # Academic Information
    cgpa = db.Column(db.Float, nullable=False)
    sgpa = db.Column(db.Float, nullable=True)
    branch = db.Column(db.String(100), nullable=True)
    semester = db.Column(db.Integer, nullable=True)
    college = db.Column(db.String(200), nullable=True)
    usn = db.Column(db.String(50), nullable=True)
    
    # Skills (JSON)
    technical_skills = db.Column(db.Text, nullable=False)
    non_technical_skills = db.Column(db.Text, nullable=True)
    programming_languages = db.Column(db.Text, nullable=False)
    
    # Portfolio
    github_url = db.Column(db.String(200), nullable=True)
    linkedin_url = db.Column(db.String(200), nullable=True)
    portfolio_url = db.Column(db.String(200), nullable=True)
    resume_url = db.Column(db.String(500), nullable=True)
    
    # Projects (JSON array)
    projects = db.Column(db.Text, nullable=True)
    
    # Certifications (JSON array)
    certifications = db.Column(db.Text, nullable=True)
    
    # Achievements
    achievements = db.Column(db.Text, nullable=True)
    
    # Analytics
    profile_views = db.Column(db.Integer, default=0)
    applications_sent = db.Column(db.Integer, default=0)
    applications_accepted = db.Column(db.Integer, default=0)
    profile_completeness = db.Column(db.Float, default=0.0)
    
    # Preferences
    preferred_locations = db.Column(db.Text, nullable=True)
    preferred_stipend_min = db.Column(db.Integer, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_technical_skills(self):
        return json.loads(self.technical_skills) if self.technical_skills else []
    
    def set_technical_skills(self, skills):
        self.technical_skills = json.dumps(skills)
    
    def get_projects(self):
        return json.loads(self.projects) if self.projects else []
    
    def set_projects(self, projects_list):
        self.projects = json.dumps(projects_list)
    
    def get_certifications(self):
        return json.loads(self.certifications) if self.certifications else []
    
    def set_certifications(self, cert_list):
        self.certifications = json.dumps(cert_list)
    
    def calculate_completeness(self):
        """Calculate profile completeness percentage"""
        total_fields = 18
        filled_fields = 0
        
        if self.full_name: filled_fields += 1
        if self.email: filled_fields += 1
        if self.phone: filled_fields += 1
        if self.avatar_url: filled_fields += 1
        if self.cgpa: filled_fields += 1
        if self.branch: filled_fields += 1
        if self.college: filled_fields += 1
        if self.usn: filled_fields += 1
        if self.technical_skills: filled_fields += 1
        if self.programming_languages: filled_fields += 1
        if self.github_url: filled_fields += 1
        if self.linkedin_url: filled_fields += 1
        if self.resume_url: filled_fields += 1
        if self.projects and len(self.get_projects()) > 0: filled_fields += 1
        if self.certifications and len(self.get_certifications()) > 0: filled_fields += 1
        if self.portfolio_url: filled_fields += 1
        if self.non_technical_skills: filled_fields += 1
        if self.achievements: filled_fields += 1
        
        self.profile_completeness = round((filled_fields / total_fields) * 100, 2)
        return self.profile_completeness
    
    def __repr__(self):
        return f'<StudentProfileExtended {self.user_id}>'


class Application(db.Model):
    """Track student applications to companies"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), nullable=False, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    # Application Status
    status = db.Column(db.String(50), default='applied')  # applied, viewed, shortlisted, interview, rejected, accepted
    
    # Match Score
    match_score = db.Column(db.Float, nullable=True)
    
    # Notes
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    viewed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationship
    company = db.relationship('Company', backref='applications')
    
    def __repr__(self):
        return f'<Application {self.student_id} -> {self.company_id}>'


class SkillTrend(db.Model):
    """Track trending skills and technologies"""
    __tablename__ = 'skill_trends'
    
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False)  # technical, programming, soft_skill
    
    # Trend Data
    demand_count = db.Column(db.Integer, default=0)
    student_count = db.Column(db.Integer, default=0)
    growth_rate = db.Column(db.Float, default=0.0)
    trend_status = db.Column(db.String(20), default='stable')  # emerging, hot, stable, declining
    
    # Impact
    avg_salary_boost = db.Column(db.Float, default=0.0)
    difficulty_level = db.Column(db.String(20), default='medium')  # easy, medium, hard
    
    # Metadata
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(20), nullable=True)
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SkillTrend {self.skill_name}>'


class LearningPath(db.Model):
    """Skill learning paths and recommendations"""
    __tablename__ = 'learning_paths'
    
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), nullable=False, index=True)
    
    # Path Information
    difficulty = db.Column(db.String(20), nullable=False)
    estimated_time = db.Column(db.String(50), nullable=True)
    prerequisites = db.Column(db.Text, nullable=True)  # JSON array
    
    # Learning Resources (JSON)
    resources = db.Column(db.Text, nullable=False)
    
    # Steps (JSON)
    learning_steps = db.Column(db.Text, nullable=True)
    
    # Success metrics
    completion_rate = db.Column(db.Float, default=0.0)
    avg_time_to_learn = db.Column(db.String(50), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_resources(self):
        return json.loads(self.resources) if self.resources else {}
    
    def set_resources(self, resources_dict):
        self.resources = json.dumps(resources_dict)
    
    def get_prerequisites(self):
        return json.loads(self.prerequisites) if self.prerequisites else []
    
    def set_prerequisites(self, prereq_list):
        self.prerequisites = json.dumps(prereq_list)
    
    def get_learning_steps(self):
        return json.loads(self.learning_steps) if self.learning_steps else []
    
    def set_learning_steps(self, steps_list):
        self.learning_steps = json.dumps(steps_list)
    
    def __repr__(self):
        return f'<LearningPath {self.skill_name}>'


class PlatformAnalytics(db.Model):
    """Platform-wide analytics and statistics"""
    __tablename__ = 'platform_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False, index=True)
    
    # Daily Stats
    total_students = db.Column(db.Integer, default=0)
    active_students = db.Column(db.Integer, default=0)
    new_registrations = db.Column(db.Integer, default=0)
    
    total_companies = db.Column(db.Integer, default=0)
    active_companies = db.Column(db.Integer, default=0)
    
    total_applications = db.Column(db.Integer, default=0)
    successful_placements = db.Column(db.Integer, default=0)
    
    # Engagement
    avg_match_score = db.Column(db.Float, default=0.0)
    avg_profile_completeness = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PlatformAnalytics {self.date}>'
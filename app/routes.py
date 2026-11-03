"""
SkillZen AI v2.0 - Complete API Routes
All endpoints for advanced features
"""

from flask import Blueprint, request, jsonify, render_template, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import (
    Admin, Company, StudentProfile, StudentProfileExtended,
    Application, SkillTrend, LearningPath, PlatformAnalytics
)
from app.ai_engine import SkillZenAI
from app.ai_engine_advanced import AdvancedAI
from app.analytics import AnalyticsEngine
import json
import os
from datetime import datetime, timedelta
import uuid

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
student_bp = Blueprint('student', __name__)
admin_bp = Blueprint('admin', __name__)
api_bp = Blueprint('api', __name__)
profile_bp = Blueprint('profile', __name__)
analytics_bp = Blueprint('analytics', __name__)

# Initialize AI Engines
ai_engine = SkillZenAI()
advanced_ai = AdvancedAI(use_bert=False)  # Set to True if BERT is installed
analytics = AnalyticsEngine()

# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============== MAIN ROUTES (Template Rendering) ==============

@main_bp.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@main_bp.route('/student')
def student_page():
    """Student recommendation flow page"""
    return render_template('student.html')


@main_bp.route('/admin')
def admin_page():
    """Admin panel page"""
    return render_template('admin.html')


@main_bp.route('/profile')
def profile_page():
    """Student profile page"""
    return render_template('profile.html')


@main_bp.route('/dashboard')
def dashboard_page():
    """Analytics dashboard page"""
    return render_template('dashboard.html')


@main_bp.route('/applications')
def applications_page():
    """Application tracking page"""
    return render_template('applications.html')


@main_bp.route('/skill-trends')
def skill_trends_page():
    """Skill trends page"""
    return render_template('skill-trends.html')


@main_bp.route('/learning-paths')
def learning_paths_page():
    """Learning paths page"""
    return render_template('learning-paths.html')


# ============== AUTHENTICATION ROUTES ==============

@auth_bp.route('/login', methods=['POST'])
def login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            return jsonify({
                'message': 'Login successful',
                'admin': {
                    'id': admin.id,
                    'username': admin.username,
                    'email': admin.email
                }
            }), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Admin logout endpoint"""
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200


@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'admin': {
                'id': current_user.id,
                'username': current_user.username
            }
        }), 200
    return jsonify({'authenticated': False}), 200


# ============== STUDENT ROUTES ==============

@student_bp.route('/recommend', methods=['POST'])
def get_recommendations():
    """Get AI-powered recommendations"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['cgpa', 'technical_skills', 'programming_languages']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Prepare student data
        student_data = {
            'cgpa': float(data['cgpa']),
            'sgpa': float(data.get('sgpa', data['cgpa'])),
            'technical_skills': data['technical_skills'],
            'non_technical_skills': data.get('non_technical_skills', []),
            'programming_languages': data['programming_languages']
        }
        
        # Get all active companies
        companies = Company.query.filter_by(is_active=True, vtu_approved=True).all()
        
        if not companies:
            return jsonify({'error': 'No companies available'}), 404
        
        # Get recommendations using advanced AI
        use_advanced = data.get('use_advanced_ai', True)
        
        if use_advanced:
            recommendations = advanced_ai.recommend_with_advanced_ai(student_data, companies)
        else:
            recommendations = ai_engine.recommend_companies(student_data, companies)
        
        return jsonify({
            'success': True,
            'student_data': student_data,
            'recommendations': recommendations,
            'total_companies': len(companies),
            'eligible_companies': len([r for r in recommendations if r['eligible']]),
            'ai_engine': 'Advanced AI' if use_advanced else 'Standard AI'
        }), 200
        
    except Exception as e:
        print(f"Error in get_recommendations: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@student_bp.route('/skills/all', methods=['GET'])
def get_all_skills():
    """Get comprehensive list of all skills and languages"""
    
    technical_skills = [
        "HTML", "CSS", "JavaScript", "React", "Angular", "Vue.js", "Node.js",
        "Express.js", "Django", "Flask", "FastAPI", "Spring Boot", "ASP.NET",
        "Android Development", "iOS Development", "React Native", "Flutter", "Kotlin",
        "Python", "Java", "C++", "C", "C#", "Go", "Rust", "Ruby", "PHP",
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQL Server",
        "Firebase", "Cassandra", "DynamoDB",
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins",
        "Git", "GitHub", "GitLab", "CI/CD", "Terraform",
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn",
        "Pandas", "NumPy", "Data Analysis", "Computer Vision", "NLP",
        "REST API", "GraphQL", "Microservices", "Blockchain", "Cybersecurity",
        "UI/UX Design", "Figma", "Adobe XD", "Testing", "Agile", "Scrum"
    ]
    
    non_technical_skills = [
        "Communication", "Leadership", "Teamwork", "Problem Solving",
        "Critical Thinking", "Time Management", "Adaptability", "Creativity",
        "Presentation Skills", "Project Management", "Research", "Documentation",
        "Analytical Skills", "Decision Making", "Conflict Resolution"
    ]
    
    programming_languages = [
        "Python", "Java", "JavaScript", "C++", "C", "C#", "Go", "Rust",
        "Ruby", "PHP", "Swift", "Kotlin", "TypeScript", "R", "MATLAB",
        "Scala", "Perl", "Dart", "SQL", "Shell Script"
    ]
    
    return jsonify({
        'technical_skills': sorted(technical_skills),
        'non_technical_skills': sorted(non_technical_skills),
        'programming_languages': sorted(programming_languages)
    }), 200


# ============== PROFILE ROUTES ==============

@profile_bp.route('/create', methods=['POST'])
def create_profile():
    """Create extended student profile"""
    try:
        data = request.get_json()
        
        # Generate user ID if not provided
        user_id = data.get('user_id', str(uuid.uuid4()))
        
        # Check if profile exists
        existing = StudentProfileExtended.query.filter_by(user_id=user_id).first()
        if existing:
            return jsonify({'error': 'Profile already exists'}), 400
        
        profile = StudentProfileExtended(
            user_id=user_id,
            full_name=data.get('full_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            cgpa=float(data.get('cgpa', 0)),
            sgpa=float(data.get('sgpa', 0)),
            branch=data.get('branch'),
            semester=data.get('semester'),
            college=data.get('college'),
            usn=data.get('usn'),
            github_url=data.get('github_url'),
            linkedin_url=data.get('linkedin_url'),
            portfolio_url=data.get('portfolio_url')
        )
        
        profile.set_technical_skills(data.get('technical_skills', []))
        profile.technical_skills = json.dumps(data.get('technical_skills', []))
        profile.non_technical_skills = json.dumps(data.get('non_technical_skills', []))
        profile.programming_languages = json.dumps(data.get('programming_languages', []))
        
        # Calculate completeness
        profile.calculate_completeness()
        
        db.session.add(profile)
        db.session.commit()
        
        return jsonify({
            'message': 'Profile created successfully',
            'user_id': user_id,
            'profile_completeness': profile.profile_completeness
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/<user_id>', methods=['GET'])
def get_profile(user_id):
    """Get student profile"""
    try:
        profile = StudentProfileExtended.query.filter_by(user_id=user_id).first()
        
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404
        
        # Increment view count
        profile.profile_views += 1
        profile.last_active = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'profile': {
                'user_id': profile.user_id,
                'full_name': profile.full_name,
                'email': profile.email,
                'phone': profile.phone,
                'avatar_url': profile.avatar_url,
                'cgpa': profile.cgpa,
                'sgpa': profile.sgpa,
                'branch': profile.branch,
                'semester': profile.semester,
                'college': profile.college,
                'usn': profile.usn,
                'technical_skills': json.loads(profile.technical_skills) if profile.technical_skills else [],
                'non_technical_skills': json.loads(profile.non_technical_skills) if profile.non_technical_skills else [],
                'programming_languages': json.loads(profile.programming_languages) if profile.programming_languages else [],
                'github_url': profile.github_url,
                'linkedin_url': profile.linkedin_url,
                'portfolio_url': profile.portfolio_url,
                'resume_url': profile.resume_url,
                'projects': profile.get_projects(),
                'certifications': profile.get_certifications(),
                'achievements': json.loads(profile.achievements) if profile.achievements else [],
                'profile_views': profile.profile_views,
                'applications_sent': profile.applications_sent,
                'applications_accepted': profile.applications_accepted,
                'profile_completeness': profile.profile_completeness,
                'created_at': profile.created_at.isoformat(),
                'last_active': profile.last_active.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/<user_id>', methods=['PUT'])
def update_profile(user_id):
    """Update student profile"""
    try:
        profile = StudentProfileExtended.query.filter_by(user_id=user_id).first()
        
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'full_name' in data:
            profile.full_name = data['full_name']
        if 'email' in data:
            profile.email = data['email']
        if 'phone' in data:
            profile.phone = data['phone']
        if 'cgpa' in data:
            profile.cgpa = float(data['cgpa'])
        if 'sgpa' in data:
            profile.sgpa = float(data['sgpa'])
        if 'branch' in data:
            profile.branch = data['branch']
        if 'semester' in data:
            profile.semester = data['semester']
        if 'college' in data:
            profile.college = data['college']
        if 'usn' in data:
            profile.usn = data['usn']
        if 'github_url' in data:
            profile.github_url = data['github_url']
        if 'linkedin_url' in data:
            profile.linkedin_url = data['linkedin_url']
        if 'portfolio_url' in data:
            profile.portfolio_url = data['portfolio_url']
        
        if 'technical_skills' in data:
            profile.technical_skills = json.dumps(data['technical_skills'])
        if 'non_technical_skills' in data:
            profile.non_technical_skills = json.dumps(data['non_technical_skills'])
        if 'programming_languages' in data:
            profile.programming_languages = json.dumps(data['programming_languages'])
        
        if 'projects' in data:
            profile.set_projects(data['projects'])
        if 'certifications' in data:
            profile.set_certifications(data['certifications'])
        if 'achievements' in data:
            profile.achievements = json.dumps(data['achievements'])
        
        # Recalculate completeness
        profile.calculate_completeness()
        profile.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'profile_completeness': profile.profile_completeness
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/<user_id>/avatar', methods=['POST'])
def upload_avatar(user_id):
    """Upload profile avatar"""
    try:
        profile = StudentProfileExtended.query.filter_by(user_id=user_id).first()
        
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404
        
        if 'avatar' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['avatar']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Create uploads directory if it doesn't exist
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            os.makedirs(os.path.join(UPLOAD_FOLDER, 'avatars'), exist_ok=True)
            
            # Generate unique filename
            filename = secure_filename(f"{user_id}_{datetime.now().timestamp()}_{file.filename}")
            filepath = os.path.join(UPLOAD_FOLDER, 'avatars', filename)
            
            file.save(filepath)
            
            # Update profile
            profile.avatar_url = f"/static/uploads/avatars/{filename}"
            profile.calculate_completeness()
            db.session.commit()
            
            return jsonify({
                'message': 'Avatar uploaded successfully',
                'avatar_url': profile.avatar_url,
                'profile_completeness': profile.profile_completeness
            }), 200
        
        return jsonify({'error': 'Invalid file type'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============== ANALYTICS ROUTES ==============

@analytics_bp.route('/platform-stats', methods=['GET'])
def get_platform_stats():
    """Get platform-wide statistics"""
    try:
        stats = analytics.get_platform_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/top-skills', methods=['GET'])
def get_top_skills():
    """Get top skills"""
    try:
        limit = request.args.get('limit', 10, type=int)
        skills = analytics.get_top_skills(limit)
        return jsonify({'skills': skills}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/trending-skills', methods=['GET'])
def get_trending_skills():
    """Get trending skills"""
    try:
        skills = analytics.get_trending_skills()
        return jsonify({'skills': skills}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/student/<student_id>', methods=['GET'])
def get_student_analytics(student_id):
    """Get student-specific analytics"""
    try:
        stats = analytics.get_student_analytics(student_id)
        if stats:
            return jsonify(stats), 200
        return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/timeline', methods=['GET'])
def get_timeline_data():
    """Get timeline data for charts"""
    try:
        days = request.args.get('days', 30, type=int)
        data = analytics.get_timeline_data(days)
        return jsonify({'timeline': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============== CONTINUE WITH ADMIN ROUTES ==============
# ============== ADMIN ROUTES (Add to app/routes.py) ==============

@admin_bp.route('/companies', methods=['GET'])
@login_required
def get_companies():
    """Get all companies (admin only)"""
    try:
        companies = Company.query.all()
        
        companies_data = []
        for company in companies:
            companies_data.append({
                'id': company.id,
                'name': company.name,
                'description': company.description,
                'location': company.location,
                'email': company.email,
                'phone': company.phone,
                'website': company.website,
                'min_cgpa': company.min_cgpa,
                'min_sgpa': company.min_sgpa,
                'technical_skills': company.get_technical_skills(),
                'non_technical_skills': company.get_non_technical_skills(),
                'programming_languages': company.get_programming_languages(),
                'duration': company.internship_duration,
                'stipend_range': company.stipend_range,
                'is_active': company.is_active,
                'vtu_approved': company.vtu_approved,
                'view_count': company.view_count,
                'application_count': company.application_count,
                'created_at': company.created_at.isoformat()
            })
        
        return jsonify({'companies': companies_data}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/companies', methods=['POST'])
@login_required
def add_company():
    """Add new company (admin only)"""
    try:
        data = request.get_json()
        
        company = Company(
            name=data['name'],
            description=data.get('description'),
            location=data.get('location'),
            email=data.get('email'),
            phone=data.get('phone'),
            website=data.get('website'),
            min_cgpa=float(data.get('min_cgpa', 6.0)),
            min_sgpa=float(data.get('min_sgpa', 6.0)),
            internship_duration=data.get('duration'),
            stipend_range=data.get('stipend_range'),
            is_active=data.get('is_active', True),
            vtu_approved=data.get('vtu_approved', True)
        )
        
        company.set_technical_skills(data.get('technical_skills', []))
        company.set_non_technical_skills(data.get('non_technical_skills', []))
        company.set_programming_languages(data.get('programming_languages', []))
        
        db.session.add(company)
        db.session.commit()
        
        # Update skill trends
        analytics.update_skill_trends()
        
        return jsonify({
            'message': 'Company added successfully',
            'company_id': company.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/companies/<int:company_id>', methods=['PUT'])
@login_required
def update_company(company_id):
    """Update company (admin only)"""
    try:
        company = Company.query.get_or_404(company_id)
        data = request.get_json()
        
        if 'name' in data:
            company.name = data['name']
        if 'description' in data:
            company.description = data['description']
        if 'location' in data:
            company.location = data['location']
        if 'email' in data:
            company.email = data['email']
        if 'phone' in data:
            company.phone = data['phone']
        if 'website' in data:
            company.website = data['website']
        if 'min_cgpa' in data:
            company.min_cgpa = float(data['min_cgpa'])
        if 'min_sgpa' in data:
            company.min_sgpa = float(data['min_sgpa'])
        if 'duration' in data:
            company.internship_duration = data['duration']
        if 'stipend_range' in data:
            company.stipend_range = data['stipend_range']
        if 'is_active' in data:
            company.is_active = data['is_active']
        if 'vtu_approved' in data:
            company.vtu_approved = data['vtu_approved']
        
        if 'technical_skills' in data:
            company.set_technical_skills(data['technical_skills'])
        if 'non_technical_skills' in data:
            company.set_non_technical_skills(data['non_technical_skills'])
        if 'programming_languages' in data:
            company.set_programming_languages(data['programming_languages'])
        
        db.session.commit()
        
        return jsonify({'message': 'Company updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/companies/<int:company_id>', methods=['DELETE'])
@login_required
def delete_company(company_id):
    """Delete company (admin only)"""
    try:
        company = Company.query.get_or_404(company_id)
        db.session.delete(company)
        db.session.commit()
        
        return jsonify({'message': 'Company deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============== APPLICATION ROUTES ==============

@api_bp.route('/applications', methods=['POST'])
def create_application():
    """Create new application"""
    try:
        data = request.get_json()
        
        application = Application(
            student_id=data['student_id'],
            company_id=data['company_id'],
            match_score=data.get('match_score'),
            status='applied'
        )
        
        db.session.add(application)
        
        # Update company application count
        company = Company.query.get(data['company_id'])
        if company:
            company.application_count += 1
        
        # Update student application count
        student = StudentProfileExtended.query.filter_by(user_id=data['student_id']).first()
        if student:
            student.applications_sent += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Application submitted successfully',
            'application_id': application.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/applications/student/<student_id>', methods=['GET'])
def get_student_applications(student_id):
    """Get all applications for a student"""
    try:
        applications = Application.query.filter_by(student_id=student_id).all()
        
        apps_data = []
        for app in applications:
            apps_data.append({
                'id': app.id,
                'company': {
                    'id': app.company.id,
                    'name': app.company.name,
                    'location': app.company.location,
                    'website': app.company.website,
                    'stipend_range': app.company.stipend_range
                },
                'status': app.status,
                'match_score': app.match_score,
                'applied_at': app.applied_at.isoformat(),
                'updated_at': app.updated_at.isoformat()
            })
        
        return jsonify({'applications': apps_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/applications/<int:app_id>/status', methods=['PUT'])
def update_application_status(app_id):
    """Update application status"""
    try:
        application = Application.query.get_or_404(app_id)
        data = request.get_json()
        
        old_status = application.status
        new_status = data.get('status')
        
        application.status = new_status
        application.updated_at = datetime.utcnow()
        
        if new_status == 'viewed':
            application.viewed_at = datetime.utcnow()
        
        # Update student stats if accepted
        if new_status == 'accepted' and old_status != 'accepted':
            student = StudentProfileExtended.query.filter_by(
                user_id=application.student_id
            ).first()
            if student:
                student.applications_accepted += 1
        
        db.session.commit()
        
        return jsonify({'message': 'Status updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============== SKILL TRENDS ROUTES ==============

@api_bp.route('/skill-trends', methods=['GET'])
def get_skill_trends():
    """Get all skill trends"""
    try:
        trends = SkillTrend.query.order_by(SkillTrend.demand_count.desc()).all()
        
        trends_data = []
        for trend in trends:
            trends_data.append({
                'id': trend.id,
                'name': trend.skill_name,
                'category': trend.category,
                'demand_count': trend.demand_count,
                'student_count': trend.student_count,
                'growth_rate': trend.growth_rate,
                'trend_status': trend.trend_status,
                'avg_salary_boost': trend.avg_salary_boost,
                'difficulty_level': trend.difficulty_level,
                'description': trend.description,
                'updated_at': trend.updated_at.isoformat()
            })
        
        return jsonify({'trends': trends_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/skill-trends/update', methods=['POST'])
@login_required
def update_skill_trends():
    """Update skill trends (admin only)"""
    try:
        success = analytics.update_skill_trends()
        
        if success:
            return jsonify({'message': 'Skill trends updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update trends'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============== LEARNING PATHS ROUTES ==============

@api_bp.route('/learning-paths', methods=['GET'])
def get_learning_paths():
    """Get all learning paths"""
    try:
        paths = LearningPath.query.all()
        
        paths_data = []
        for path in paths:
            paths_data.append({
                'id': path.id,
                'skill_name': path.skill_name,
                'difficulty': path.difficulty,
                'estimated_time': path.estimated_time,
                'prerequisites': path.get_prerequisites(),
                'resources': path.get_resources(),
                'learning_steps': path.get_learning_steps(),
                'completion_rate': path.completion_rate,
                'avg_time_to_learn': path.avg_time_to_learn
            })
        
        return jsonify({'learning_paths': paths_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/learning-paths/<skill_name>', methods=['GET'])
def get_learning_path(skill_name):
    """Get learning path for specific skill"""
    try:
        path = LearningPath.query.filter_by(skill_name=skill_name).first()
        
        if not path:
            return jsonify({'error': 'Learning path not found'}), 404
        
        return jsonify({
            'learning_path': {
                'id': path.id,
                'skill_name': path.skill_name,
                'difficulty': path.difficulty,
                'estimated_time': path.estimated_time,
                'prerequisites': path.get_prerequisites(),
                'resources': path.get_resources(),
                'learning_steps': path.get_learning_steps(),
                'completion_rate': path.completion_rate,
                'avg_time_to_learn': path.avg_time_to_learn
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============== PUBLIC API ROUTES ==============

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'service': 'SkillZen AI',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get platform statistics"""
    try:
        total_companies = Company.query.filter_by(is_active=True).count()
        vtu_approved = Company.query.filter_by(vtu_approved=True).count()
        total_students = StudentProfileExtended.query.count()
        total_applications = Application.query.count()
        
        return jsonify({
            'total_companies': total_companies,
            'vtu_approved_companies': vtu_approved,
            'active_companies': total_companies,
            'total_students': total_students,
            'total_applications': total_applications
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============== COMPANY VIEW TRACKING ==============

@api_bp.route('/companies/<int:company_id>/view', methods=['POST'])
def track_company_view(company_id):
    """Track company profile view"""
    try:
        company = Company.query.get_or_404(company_id)
        company.view_count += 1
        db.session.commit()
        
        return jsonify({'message': 'View tracked'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
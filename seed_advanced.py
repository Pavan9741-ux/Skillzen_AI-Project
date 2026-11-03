"""
SkillZen AI v2.0 - Advanced Seed Data
Populates database with skill trends, learning paths, and analytics
"""
import json
from app import create_app, db
from app.models import (
    Company, Admin, SkillTrend, LearningPath, 
    PlatformAnalytics, StudentProfileExtended
)
from datetime import datetime, timedelta
import random

app = create_app()


# ============== SKILL TRENDS DATA ==============

SKILL_TRENDS_DATA = [
    # HOT SKILLS
    {
        'skill_name': 'Python',
        'category': 'programming',
        'demand_count': 45,
        'student_count': 320,
        'growth_rate': 65.5,
        'trend_status': 'hot',
        'avg_salary_boost': 25000,
        'difficulty_level': 'medium',
        'description': 'General-purpose programming language widely used in AI, web development, and data science',
        'icon': 'fab fa-python',
        'color': '#3776ab'
    },
    {
        'skill_name': 'Machine Learning',
        'category': 'technical',
        'demand_count': 38,
        'student_count': 210,
        'growth_rate': 82.3,
        'trend_status': 'hot',
        'avg_salary_boost': 40000,
        'difficulty_level': 'hard',
        'description': 'AI technology enabling systems to learn from data',
        'icon': 'fas fa-brain',
        'color': '#ff6f00'
    },
    {
        'skill_name': 'React',
        'category': 'technical',
        'demand_count': 42,
        'student_count': 285,
        'growth_rate': 58.2,
        'trend_status': 'hot',
        'avg_salary_boost': 22000,
        'difficulty_level': 'medium',
        'description': 'Popular JavaScript library for building user interfaces',
        'icon': 'fab fa-react',
        'color': '#61dafb'
    },
    {
        'skill_name': 'AWS',
        'category': 'technical',
        'demand_count': 35,
        'student_count': 195,
        'growth_rate': 72.1,
        'trend_status': 'hot',
        'avg_salary_boost': 35000,
        'difficulty_level': 'hard',
        'description': 'Amazon Web Services - leading cloud computing platform',
        'icon': 'fab fa-aws',
        'color': '#ff9900'
    },
    
    # EMERGING SKILLS
    {
        'skill_name': 'Kubernetes',
        'category': 'technical',
        'demand_count': 28,
        'student_count': 145,
        'growth_rate': 95.7,
        'trend_status': 'emerging',
        'avg_salary_boost': 38000,
        'difficulty_level': 'hard',
        'description': 'Container orchestration platform',
        'icon': 'fas fa-dharmachakra',
        'color': '#326ce5'
    },
    {
        'skill_name': 'Rust',
        'category': 'programming',
        'demand_count': 18,
        'student_count': 85,
        'growth_rate': 125.4,
        'trend_status': 'emerging',
        'avg_salary_boost': 45000,
        'difficulty_level': 'hard',
        'description': 'Systems programming language focused on safety and performance',
        'icon': 'fas fa-cog',
        'color': '#ce422b'
    },
    {
        'skill_name': 'Flutter',
        'category': 'technical',
        'demand_count': 25,
        'student_count': 165,
        'growth_rate': 88.3,
        'trend_status': 'emerging',
        'avg_salary_boost': 28000,
        'difficulty_level': 'medium',
        'description': 'Cross-platform mobile development framework',
        'icon': 'fas fa-mobile-alt',
        'color': '#02569b'
    },
    
    # STABLE SKILLS
    {
        'skill_name': 'Java',
        'category': 'programming',
        'demand_count': 50,
        'student_count': 420,
        'growth_rate': 12.5,
        'trend_status': 'stable',
        'avg_salary_boost': 20000,
        'difficulty_level': 'medium',
        'description': 'Enterprise-grade object-oriented programming language',
        'icon': 'fab fa-java',
        'color': '#007396'
    },
    {
        'skill_name': 'SQL',
        'category': 'technical',
        'demand_count': 48,
        'student_count': 390,
        'growth_rate': 8.2,
        'trend_status': 'stable',
        'avg_salary_boost': 18000,
        'difficulty_level': 'easy',
        'description': 'Database query language',
        'icon': 'fas fa-database',
        'color': '#00758f'
    },
    {
        'skill_name': 'Git',
        'category': 'technical',
        'demand_count': 52,
        'student_count': 445,
        'growth_rate': 5.3,
        'trend_status': 'stable',
        'avg_salary_boost': 5000,
        'difficulty_level': 'easy',
        'description': 'Version control system',
        'icon': 'fab fa-git-alt',
        'color': '#f05032'
    },
    
    # MORE TRENDING SKILLS
    {
        'skill_name': 'Docker',
        'category': 'technical',
        'demand_count': 32,
        'student_count': 178,
        'growth_rate': 68.9,
        'trend_status': 'hot',
        'avg_salary_boost': 30000,
        'difficulty_level': 'medium',
        'description': 'Containerization platform',
        'icon': 'fab fa-docker',
        'color': '#2496ed'
    },
    {
        'skill_name': 'Node.js',
        'category': 'technical',
        'demand_count': 40,
        'student_count': 265,
        'growth_rate': 45.2,
        'trend_status': 'hot',
        'avg_salary_boost': 24000,
        'difficulty_level': 'medium',
        'description': 'JavaScript runtime for server-side development',
        'icon': 'fab fa-node-js',
        'color': '#339933'
    },
    {
        'skill_name': 'TypeScript',
        'category': 'programming',
        'demand_count': 30,
        'student_count': 195,
        'growth_rate': 78.6,
        'trend_status': 'emerging',
        'avg_salary_boost': 26000,
        'difficulty_level': 'medium',
        'description': 'Typed superset of JavaScript',
        'icon': 'fas fa-code',
        'color': '#3178c6'
    },
    {
        'skill_name': 'MongoDB',
        'category': 'technical',
        'demand_count': 27,
        'student_count': 185,
        'growth_rate': 52.1,
        'trend_status': 'hot',
        'avg_salary_boost': 22000,
        'difficulty_level': 'medium',
        'description': 'NoSQL database',
        'icon': 'fas fa-leaf',
        'color': '#47a248'
    },
    {
        'skill_name': 'GraphQL',
        'category': 'technical',
        'demand_count': 22,
        'student_count': 125,
        'growth_rate': 92.4,
        'trend_status': 'emerging',
        'avg_salary_boost': 28000,
        'difficulty_level': 'medium',
        'description': 'Query language for APIs',
        'icon': 'fas fa-project-diagram',
        'color': '#e10098'
    }
]


# ============== LEARNING PATHS DATA ==============

LEARNING_PATHS_DATA = [
    {
        'skill_name': 'Python',
        'difficulty': 'beginner',
        'estimated_time': '8-12 weeks',
        'prerequisites': [],
        'resources': {
            'courses': [
                {'name': 'Python for Beginners', 'platform': 'Coursera', 'url': 'https://coursera.org', 'type': 'free'},
                {'name': 'Complete Python Bootcamp', 'platform': 'Udemy', 'url': 'https://udemy.com', 'type': 'paid'},
                {'name': 'Python Tutorial', 'platform': 'W3Schools', 'url': 'https://w3schools.com/python', 'type': 'free'}
            ],
            'videos': [
                {'name': 'Python Full Course', 'creator': 'FreeCodeCamp', 'url': 'https://youtube.com', 'duration': '4.5 hours'},
                {'name': 'Python Crash Course', 'creator': 'Traversy Media', 'url': 'https://youtube.com', 'duration': '1.5 hours'}
            ],
            'books': [
                {'name': 'Python Crash Course', 'author': 'Eric Matthes'},
                {'name': 'Automate the Boring Stuff', 'author': 'Al Sweigart'}
            ],
            'practice': [
                {'name': 'HackerRank Python', 'url': 'https://hackerrank.com'},
                {'name': 'LeetCode Python', 'url': 'https://leetcode.com'}
            ]
        },
        'learning_steps': [
            {'step': 1, 'title': 'Basics & Syntax', 'duration': '2 weeks', 'topics': ['Variables', 'Data Types', 'Operators', 'Control Flow']},
            {'step': 2, 'title': 'Functions & Modules', 'duration': '2 weeks', 'topics': ['Functions', 'Lambda', 'Modules', 'Packages']},
            {'step': 3, 'title': 'OOP Concepts', 'duration': '2 weeks', 'topics': ['Classes', 'Inheritance', 'Polymorphism']},
            {'step': 4, 'title': 'File Handling & Libraries', 'duration': '2 weeks', 'topics': ['File I/O', 'Common Libraries', 'APIs']},
            {'step': 5, 'title': 'Projects', 'duration': '2-4 weeks', 'topics': ['Build 3-5 projects', 'Portfolio']}
        ],
        'completion_rate': 78.5,
        'avg_time_to_learn': '10 weeks'
    },
    {
        'skill_name': 'Machine Learning',
        'difficulty': 'advanced',
        'estimated_time': '16-24 weeks',
        'prerequisites': ['Python', 'Mathematics', 'Statistics'],
        'resources': {
            'courses': [
                {'name': 'Machine Learning by Andrew Ng', 'platform': 'Coursera', 'url': 'https://coursera.org', 'type': 'free'},
                {'name': 'Deep Learning Specialization', 'platform': 'Coursera', 'url': 'https://coursera.org', 'type': 'paid'},
                {'name': 'Fast.ai Practical Deep Learning', 'platform': 'Fast.ai', 'url': 'https://fast.ai', 'type': 'free'}
            ],
            'videos': [
                {'name': 'ML Full Course', 'creator': 'FreeCodeCamp', 'url': 'https://youtube.com', 'duration': '10 hours'},
                {'name': '3Blue1Brown Neural Networks', 'creator': '3Blue1Brown', 'url': 'https://youtube.com', 'duration': '3 hours'}
            ],
            'books': [
                {'name': 'Hands-On Machine Learning', 'author': 'Aurélien Géron'},
                {'name': 'Pattern Recognition and ML', 'author': 'Christopher Bishop'}
            ],
            'practice': [
                {'name': 'Kaggle Competitions', 'url': 'https://kaggle.com'},
                {'name': 'Google Colab Projects', 'url': 'https://colab.research.google.com'}
            ]
        },
        'learning_steps': [
            {'step': 1, 'title': 'Math Foundations', 'duration': '3 weeks', 'topics': ['Linear Algebra', 'Calculus', 'Statistics', 'Probability']},
            {'step': 2, 'title': 'Python for ML', 'duration': '3 weeks', 'topics': ['NumPy', 'Pandas', 'Matplotlib', 'Scikit-learn']},
            {'step': 3, 'title': 'Supervised Learning', 'duration': '4 weeks', 'topics': ['Regression', 'Classification', 'Decision Trees', 'SVM']},
            {'step': 4, 'title': 'Deep Learning', 'duration': '4 weeks', 'topics': ['Neural Networks', 'CNN', 'RNN', 'Transfer Learning']},
            {'step': 5, 'title': 'Advanced Topics', 'duration': '3 weeks', 'topics': ['NLP', 'Computer Vision', 'Reinforcement Learning']},
            {'step': 6, 'title': 'Projects & Deployment', 'duration': '3-7 weeks', 'topics': ['Build portfolio', 'Model deployment', 'MLOps']}
        ],
        'completion_rate': 45.2,
        'avg_time_to_learn': '20 weeks'
    },
    {
        'skill_name': 'React',
        'difficulty': 'intermediate',
        'estimated_time': '8-12 weeks',
        'prerequisites': ['HTML', 'CSS', 'JavaScript'],
        'resources': {
            'courses': [
                {'name': 'React - The Complete Guide', 'platform': 'Udemy', 'url': 'https://udemy.com', 'type': 'paid'},
                {'name': 'React Official Tutorial', 'platform': 'React.dev', 'url': 'https://react.dev', 'type': 'free'},
                {'name': 'Scrimba React Course', 'platform': 'Scrimba', 'url': 'https://scrimba.com', 'type': 'free'}
            ],
            'videos': [
                {'name': 'React Course - Beginner', 'creator': 'FreeCodeCamp', 'url': 'https://youtube.com', 'duration': '12 hours'},
                {'name': 'React in 100 Seconds', 'creator': 'Fireship', 'url': 'https://youtube.com', 'duration': '2 minutes'}
            ],
            'books': [
                {'name': 'Learning React', 'author': 'Alex Banks'},
                {'name': 'React Up and Running', 'author': 'Stoyan Stefanov'}
            ],
            'practice': [
                {'name': 'Frontend Mentor', 'url': 'https://frontendmentor.io'},
                {'name': 'React Challenges', 'url': 'https://react-challenges.com'}
            ]
        },
        'learning_steps': [
            {'step': 1, 'title': 'JavaScript ES6+', 'duration': '2 weeks', 'topics': ['Arrow Functions', 'Destructuring', 'Promises', 'Async/Await']},
            {'step': 2, 'title': 'React Basics', 'duration': '2 weeks', 'topics': ['JSX', 'Components', 'Props', 'State']},
            {'step': 3, 'title': 'Advanced Concepts', 'duration': '2 weeks', 'topics': ['Hooks', 'Context API', 'Routing', 'Forms']},
            {'step': 4, 'title': 'State Management', 'duration': '2 weeks', 'topics': ['Redux', 'Redux Toolkit', 'Zustand']},
            {'step': 5, 'title': 'Projects', 'duration': '2-4 weeks', 'topics': ['Build 3-5 React apps', 'Deployment']}
        ],
        'completion_rate': 68.7,
        'avg_time_to_learn': '10 weeks'
    }
]


def seed_skill_trends():
    """Seed skill trends data"""
    print("\n🔥 Seeding Skill Trends...")
    
    SkillTrend.query.delete()
    
    for data in SKILL_TRENDS_DATA:
        trend = SkillTrend(**data)
        db.session.add(trend)
        print(f"  + {data['skill_name']} ({data['trend_status']})")
    
    db.session.commit()
    print(f"✅ Seeded {len(SKILL_TRENDS_DATA)} skill trends!")


def seed_learning_paths():
    """Seed learning paths data"""
    print("\n📚 Seeding Learning Paths...")
    
    LearningPath.query.delete()
    
    for data in LEARNING_PATHS_DATA:
        path = LearningPath(
            skill_name=data['skill_name'],
            difficulty=data['difficulty'],
            estimated_time=data['estimated_time'],
            completion_rate=data['completion_rate'],
            avg_time_to_learn=data['avg_time_to_learn']
        )
        path.set_prerequisites(data['prerequisites'])
        path.set_resources(data['resources'])
        path.set_learning_steps(data['learning_steps'])
        
        db.session.add(path)
        print(f"  + {data['skill_name']} ({data['difficulty']})")
    
    db.session.commit()
    print(f"✅ Seeded {len(LEARNING_PATHS_DATA)} learning paths!")


def seed_platform_analytics():
    """Seed platform analytics for last 30 days"""
    print("\n📊 Seeding Platform Analytics...")
    
    PlatformAnalytics.query.delete()
    
    end_date = datetime.now().date()
    
    for i in range(30):
        date = end_date - timedelta(days=i)
        
        analytics = PlatformAnalytics(
            date=date,
            total_students=100 + (i * 5) + random.randint(-10, 10),
            active_students=80 + (i * 3) + random.randint(-5, 5),
            new_registrations=random.randint(2, 10),
            total_companies=15 + random.randint(-2, 3),
            active_companies=12 + random.randint(-1, 2),
            total_applications=50 + (i * 4) + random.randint(-8, 8),
            successful_placements=10 + (i // 3) + random.randint(-2, 2),
            avg_match_score=70.0 + random.uniform(-5, 5),
            avg_profile_completeness=65.0 + random.uniform(-3, 3)
        )
        
        db.session.add(analytics)
    
    db.session.commit()
    print(f"✅ Seeded 30 days of analytics data!")


def seed_demo_students():
    """Seed demo student profiles"""
    print("\n👥 Seeding Demo Students...")
    
    demo_students = [
        {
            'user_id': 'student_demo_1',
            'full_name': 'Rahul Sharma',
            'email': 'rahul.sharma@vtu.ac.in',
            'cgpa': 8.5,
            'branch': 'Computer Science',
            'semester': 6,
            'college': 'BMS College of Engineering',
            'technical_skills': ['Python', 'Java', 'React', 'Node.js', 'MongoDB'],
            'programming_languages': ['Python', 'Java', 'JavaScript'],
            'non_technical_skills': ['Leadership', 'Communication', 'Teamwork']
        },
        {
            'user_id': 'student_demo_2',
            'full_name': 'Priya Patel',
            'email': 'priya.patel@vtu.ac.in',
            'cgpa': 9.2,
            'branch': 'Information Science',
            'semester': 7,
            'college': 'RV College of Engineering',
            'technical_skills': ['Machine Learning', 'Python', 'TensorFlow', 'Data Analysis'],
            'programming_languages': ['Python', 'R', 'SQL'],
            'non_technical_skills': ['Research', 'Problem Solving', 'Presentation']
        },
        {
            'user_id': 'student_demo_3',
            'full_name': 'Arjun Krishnan',
            'email': 'arjun.k@vtu.ac.in',
            'cgpa': 7.8,
            'branch': 'Electronics',
            'semester': 5,
            'college': 'PES University',
            'technical_skills': ['C++', 'Embedded Systems', 'IoT', 'Arduino'],
            'programming_languages': ['C++', 'C', 'Python'],
            'non_technical_skills': ['Time Management', 'Adaptability']
        }
    ]
    
    for data in demo_students:
        student = StudentProfileExtended(
            user_id=data['user_id'],
            full_name=data['full_name'],
            email=data['email'],
            cgpa=data['cgpa'],
            branch=data['branch'],
            semester=data['semester'],
            college=data['college'],
            profile_views=random.randint(10, 50),
            applications_sent=random.randint(3, 12),
            applications_accepted=random.randint(0, 3)
        )
        
        student.technical_skills = json.dumps(data['technical_skills'])
        student.programming_languages = json.dumps(data['programming_languages'])
        student.non_technical_skills = json.dumps(data['non_technical_skills'])
        student.calculate_completeness()
        
        db.session.add(student)
        print(f"  + {data['full_name']}")
    
    db.session.commit()
    print(f"✅ Seeded {len(demo_students)} demo students!")


def main():
    """Run all seed functions"""
    with app.app_context():
        print("\n" + "="*70)
        print("  SkillZen AI v2.0 - Advanced Seeding")
        print("="*70)
        
        seed_skill_trends()
        seed_learning_paths()
        seed_platform_analytics()
        seed_demo_students()
        
        print("\n" + "="*70)
        print("  ✅ ALL ADVANCED DATA SEEDED SUCCESSFULLY!")
        print("="*70 + "\n")


if __name__ == '__main__':
    main()
"""SkillZen AI - Database Seeding"""
from app import create_app, db
from app.models import Company, Admin

app = create_app()

COMPANIES = [
    {
        'name': 'Infosys Limited',
        'description': 'Global IT services leader',
        'location': 'Bangalore, Karnataka',
        'email': 'internships@infosys.com',
        'phone': '+91-80-28520261',
        'website': 'https://www.infosys.com',
        'min_cgpa': 7.0,
        'min_sgpa': 7.0,
        'technical_skills': ['Java', 'Python', 'SQL', 'Spring Boot'],
        'non_technical_skills': ['Communication', 'Teamwork'],
        'programming_languages': ['Java', 'Python', 'SQL'],
        'duration': '6 months',
        'stipend_range': '15,000 - 20,000'
    },
    {
        'name': 'TCS',
        'description': 'IT services and consulting',
        'location': 'Bangalore, Karnataka',
        'email': 'careers@tcs.com',
        'phone': '+91-22-67816000',
        'website': 'https://www.tcs.com',
        'min_cgpa': 6.0,
        'min_sgpa': 6.0,
        'technical_skills': ['Java', 'C', 'Python'],
        'non_technical_skills': ['Communication'],
        'programming_languages': ['Java', 'C', 'Python'],
        'duration': '6 months',
        'stipend_range': '10,000 - 15,000'
    },
    {
        'name': 'Wipro',
        'description': 'IT and consulting services',
        'location': 'Bangalore, Karnataka',
        'email': 'wipro@wipro.com',
        'phone': '+91-80-28440011',
        'website': 'https://www.wipro.com',
        'min_cgpa': 6.5,
        'min_sgpa': 6.5,
        'technical_skills': ['C++', 'Java', 'MySQL'],
        'non_technical_skills': ['Leadership'],
        'programming_languages': ['C++', 'Java'],
        'duration': '6 months',
        'stipend_range': '12,000 - 18,000'
    },
    {
        'name': 'Accenture',
        'description': 'Professional services',
        'location': 'Bangalore, Karnataka',
        'email': 'careers@accenture.com',
        'phone': '+91-80-67061000',
        'website': 'https://www.accenture.com',
        'min_cgpa': 7.5,
        'min_sgpa': 7.5,
        'technical_skills': ['Python', 'Machine Learning', 'Azure'],
        'non_technical_skills': ['Leadership', 'Communication'],
        'programming_languages': ['Python', 'R'],
        'duration': '6 months',
        'stipend_range': '20,000 - 25,000'
    },
    {
        'name': 'Amazon',
        'description': 'E-commerce and cloud computing',
        'location': 'Bangalore, Karnataka',
        'email': 'amazon@amazon.com',
        'phone': '+91-80-67064000',
        'website': 'https://www.amazon.jobs',
        'min_cgpa': 8.0,
        'min_sgpa': 8.0,
        'technical_skills': ['Java', 'Python', 'AWS', 'System Design'],
        'non_technical_skills': ['Problem Solving', 'Innovation'],
        'programming_languages': ['Java', 'Python', 'C++'],
        'duration': '6 months',
        'stipend_range': '50,000 - 70,000'
    }
]

def seed_database():
    with app.app_context():
        print("\n🌱 Seeding database...\n")
        
        Company.query.delete()
        
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin', email='admin@skillzen.ai')
            admin.set_password('admin123')
            db.session.add(admin)
            print("✓ Admin created (admin/admin123)")
        
        for data in COMPANIES:
            company = Company(
                name=data['name'],
                description=data['description'],
                location=data['location'],
                email=data['email'],
                phone=data['phone'],
                website=data['website'],
                min_cgpa=data['min_cgpa'],
                min_sgpa=data['min_sgpa'],
                internship_duration=data['duration'],
                stipend_range=data['stipend_range'],
                is_active=True,
                vtu_approved=True
            )
            company.set_technical_skills(data['technical_skills'])
            company.set_non_technical_skills(data['non_technical_skills'])
            company.set_programming_languages(data['programming_languages'])
            db.session.add(company)
            print(f"  + {data['name']}")
        
        db.session.commit()
        print(f"\n✅ Seeded {len(COMPANIES)} companies!\n")

if __name__ == '__main__':
    seed_database()
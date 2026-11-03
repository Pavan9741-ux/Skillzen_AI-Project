"""
SkillZen AI - Main Application Entry Point
Alternative to run.py - can be used for production deployment
"""

from app import create_app, db
from app.models import Admin, Company, StudentProfile
import os
import sys

# Create Flask application
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    Make database models available in Flask shell
    Usage: flask shell
    """
    return {
        'db': db,
        'Admin': Admin,
        'Company': Company,
        'StudentProfile': StudentProfile
    }


@app.cli.command()
def init_db():
    """
    Initialize database tables
    Usage: flask init-db
    """
    db.create_all()
    print("✅ Database tables created successfully!")


@app.cli.command()
def seed_db():
    """
    Seed database with sample data
    Usage: flask seed-db
    """
    from seed_data import seed_database
    seed_database()
    print("✅ Database seeded successfully!")


@app.cli.command()
def create_admin():
    """
    Create admin user interactively
    Usage: flask create-admin
    """
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    email = input("Enter admin email (optional): ")
    
    admin = Admin(username=username)
    admin.set_password(password)
    if email:
        admin.email = email
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"✅ Admin user '{username}' created successfully!")


@app.cli.command()
def reset_db():
    """
    Reset database (drop all tables and recreate)
    Usage: flask reset-db
    """
    confirm = input("⚠️  This will delete all data. Are you sure? (yes/no): ")
    if confirm.lower() == 'yes':
        db.drop_all()
        db.create_all()
        print("✅ Database reset successfully!")
    else:
        print("❌ Database reset cancelled.")


@app.cli.command()
def routes():
    """
    Display all registered routes
    Usage: flask routes
    """
    print("\n" + "="*80)
    print("Registered Routes:")
    print("="*80)
    
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
        print(f"{rule.endpoint:50s} {methods:20s} {rule.rule}")
    
    print("="*80 + "\n")


@app.cli.command()
def test():
    """
    Run tests
    Usage: flask test
    """
    import subprocess
    result = subprocess.run(['python', 'test_api.py'])
    sys.exit(result.returncode)


if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print("\n" + "="*80)
    print("🚀 SkillZen AI Server Starting...")
    print("="*80)
    print(f"📍 Server: http://localhost:{port}")
    print(f"🔧 Debug: {debug}")
    print(f"📊 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("="*80 + "\n")
    
    # Run the application
    app.run(host=host, port=port, debug=debug)
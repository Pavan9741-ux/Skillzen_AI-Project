"""
SkillZen AI - Database Management Script
Handles database operations, migrations, and admin tasks
"""

import sys
import os
from getpass import getpass
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import Admin, Company, StudentProfile
import json


class DatabaseManager:
    """Database management utility class"""
    
    def __init__(self):
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()
    
    def init_database(self):
        """Initialize all database tables"""
        print("\n🔧 Initializing database...")
        db.create_all()
        print("✅ Database tables created successfully!\n")
    
    def drop_database(self):
        """Drop all database tables"""
        confirm = input("⚠️  WARNING: This will delete ALL data. Type 'DELETE' to confirm: ")
        if confirm == 'DELETE':
            print("\n🗑️  Dropping all tables...")
            db.drop_all()
            print("✅ All tables dropped successfully!\n")
        else:
            print("❌ Operation cancelled.\n")
    
    def reset_database(self):
        """Reset database (drop and recreate)"""
        confirm = input("⚠️  WARNING: This will delete ALL data. Type 'RESET' to confirm: ")
        if confirm == 'RESET':
            print("\n🔄 Resetting database...")
            db.drop_all()
            db.create_all()
            print("✅ Database reset successfully!\n")
        else:
            print("❌ Operation cancelled.\n")
    
    def seed_database(self):
        """Seed database with sample data"""
        print("\n🌱 Seeding database...")
        from seed_data import seed_database
        seed_database()
    
    def create_admin(self):
        """Create admin user interactively"""
        print("\n👤 Create Admin User")
        print("="*50)
        
        username = input("Username: ").strip()
        
        # Check if username already exists
        if Admin.query.filter_by(username=username).first():
            print(f"❌ Error: Username '{username}' already exists!\n")
            return
        
        password = getpass("Password: ")
        password_confirm = getpass("Confirm Password: ")
        
        if password != password_confirm:
            print("❌ Error: Passwords do not match!\n")
            return
        
        email = input("Email (optional): ").strip() or None
        
        # Create admin
        admin = Admin(username=username, email=email)
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"✅ Admin user '{username}' created successfully!\n")
    
    def list_admins(self):
        """List all admin users"""
        print("\n👥 Admin Users")
        print("="*50)
        
        admins = Admin.query.all()
        
        if not admins:
            print("No admin users found.\n")
            return
        
        for admin in admins:
            print(f"ID: {admin.id}")
            print(f"Username: {admin.username}")
            print(f"Email: {admin.email or 'Not set'}")
            print(f"Created: {admin.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-"*50)
        
        print(f"\nTotal: {len(admins)} admin(s)\n")
    
    def delete_admin(self):
        """Delete admin user"""
        self.list_admins()
        
        username = input("Enter username to delete: ").strip()
        admin = Admin.query.filter_by(username=username).first()
        
        if not admin:
            print(f"❌ Admin '{username}' not found!\n")
            return
        
        confirm = input(f"⚠️  Delete admin '{username}'? (yes/no): ")
        if confirm.lower() == 'yes':
            db.session.delete(admin)
            db.session.commit()
            print(f"✅ Admin '{username}' deleted successfully!\n")
        else:
            print("❌ Operation cancelled.\n")
    
    def change_password(self):
        """Change admin password"""
        username = input("Enter admin username: ").strip()
        admin = Admin.query.filter_by(username=username).first()
        
        if not admin:
            print(f"❌ Admin '{username}' not found!\n")
            return
        
        new_password = getpass("New Password: ")
        confirm_password = getpass("Confirm Password: ")
        
        if new_password != confirm_password:
            print("❌ Error: Passwords do not match!\n")
            return
        
        admin.set_password(new_password)
        db.session.commit()
        
        print(f"✅ Password changed successfully for '{username}'!\n")
    
    def statistics(self):
        """Display database statistics"""
        print("\n📊 Database Statistics")
        print("="*50)
        
        total_companies = Company.query.count()
        active_companies = Company.query.filter_by(is_active=True).count()
        vtu_approved = Company.query.filter_by(vtu_approved=True).count()
        total_students = StudentProfile.query.count()
        total_admins = Admin.query.count()
        
        print(f"Companies: {total_companies}")
        print(f"  - Active: {active_companies}")
        print(f"  - VTU Approved: {vtu_approved}")
        print(f"Student Profiles: {total_students}")
        print(f"Admin Users: {total_admins}")
        print("="*50 + "\n")
    
    def backup_database(self):
        """Backup database to JSON"""
        print("\n💾 Creating database backup...")
        
        backup_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'companies': [],
            'admins': []
        }
        
        # Backup companies
        for company in Company.query.all():
            backup_data['companies'].append({
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
                'vtu_approved': company.vtu_approved
            })
        
        # Backup admins (without passwords)
        for admin in Admin.query.all():
            backup_data['admins'].append({
                'username': admin.username,
                'email': admin.email
            })
        
        filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        print(f"✅ Backup saved to: {filename}\n")
    
    def restore_database(self):
        """Restore database from JSON backup"""
        filename = input("Enter backup filename: ").strip()
        
        if not os.path.exists(filename):
            print(f"❌ File '{filename}' not found!\n")
            return
        
        confirm = input("⚠️  This will replace existing data. Continue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Operation cancelled.\n")
            return
        
        print(f"\n📂 Restoring from {filename}...")
        
        with open(filename, 'r') as f:
            backup_data = json.load(f)
        
        # Clear existing data
        Company.query.delete()
        
        # Restore companies
        for company_data in backup_data['companies']:
            company = Company(
                name=company_data['name'],
                description=company_data['description'],
                location=company_data['location'],
                email=company_data['email'],
                phone=company_data['phone'],
                website=company_data['website'],
                min_cgpa=company_data['min_cgpa'],
                min_sgpa=company_data['min_sgpa'],
                internship_duration=company_data['duration'],
                stipend_range=company_data['stipend_range'],
                is_active=company_data['is_active'],
                vtu_approved=company_data['vtu_approved']
            )
            company.set_technical_skills(company_data['technical_skills'])
            company.set_non_technical_skills(company_data['non_technical_skills'])
            company.set_programming_languages(company_data['programming_languages'])
            db.session.add(company)
        
        db.session.commit()
        print(f"✅ Database restored successfully!\n")
    
    def export_companies_csv(self):
        """Export companies to CSV"""
        import csv
        
        filename = f"companies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Name', 'Location', 'Email', 'Phone', 'Website',
                'Min CGPA', 'Min SGPA', 'Duration', 'Stipend',
                'Technical Skills', 'Programming Languages', 'Active', 'VTU Approved'
            ])
            
            # Data
            for company in Company.query.all():
                writer.writerow([
                    company.name,
                    company.location,
                    company.email,
                    company.phone,
                    company.website,
                    company.min_cgpa,
                    company.min_sgpa,
                    company.internship_duration,
                    company.stipend_range,
                    ', '.join(company.get_technical_skills()),
                    ', '.join(company.get_programming_languages()),
                    company.is_active,
                    company.vtu_approved
                ])
        
        print(f"✅ Companies exported to: {filename}\n")
    
    def cleanup(self):
        """Cleanup old student profiles"""
        from datetime import timedelta
        
        days = int(input("Delete profiles older than (days): ").strip())
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        old_profiles = StudentProfile.query.filter(
            StudentProfile.created_at < cutoff_date
        ).all()
        
        if not old_profiles:
            print(f"✅ No profiles older than {days} days found.\n")
            return
        
        print(f"Found {len(old_profiles)} old profile(s)")
        confirm = input("Delete these profiles? (yes/no): ")
        
        if confirm.lower() == 'yes':
            for profile in old_profiles:
                db.session.delete(profile)
            db.session.commit()
            print(f"✅ Deleted {len(old_profiles)} old profile(s)!\n")
        else:
            print("❌ Operation cancelled.\n")


def print_menu():
    """Print main menu"""
    print("\n" + "="*60)
    print("  SkillZen AI - Database Management Tool")
    print("="*60)
    print("\n📊 DATABASE OPERATIONS:")
    print("  1. Initialize Database")
    print("  2. Reset Database (Drop & Recreate)")
    print("  3. Seed Database (Sample Data)")
    print("  4. Database Statistics")
    print("\n👤 ADMIN MANAGEMENT:")
    print("  5. Create Admin User")
    print("  6. List Admin Users")
    print("  7. Delete Admin User")
    print("  8. Change Admin Password")
    print("\n💾 BACKUP & RESTORE:")
    print("  9. Backup Database")
    print(" 10. Restore Database")
    print(" 11. Export Companies to CSV")
    print("\n🧹 MAINTENANCE:")
    print(" 12. Cleanup Old Profiles")
    print("\n 0. Exit")
    print("="*60)


def main():
    """Main program loop"""
    manager = DatabaseManager()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            manager.init_database()
        elif choice == '2':
            manager.reset_database()
        elif choice == '3':
            manager.seed_database()
        elif choice == '4':
            manager.statistics()
        elif choice == '5':
            manager.create_admin()
        elif choice == '6':
            manager.list_admins()
        elif choice == '7':
            manager.delete_admin()
        elif choice == '8':
            manager.change_password()
        elif choice == '9':
            manager.backup_database()
        elif choice == '10':
            manager.restore_database()
        elif choice == '11':
            manager.export_companies_csv()
        elif choice == '12':
            manager.cleanup()
        elif choice == '0':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice. Please try again.\n")


if __name__ == '__main__':
    main()
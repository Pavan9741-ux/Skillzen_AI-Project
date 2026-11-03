"""
SkillZen AI - File Structure Checker
Verifies all files exist
"""

import os

print("\n" + "="*70)
print("  SkillZen AI - File Structure Verification")
print("="*70 + "\n")

files_to_check = {
    'Root Files': [
        'run.py',
        'seed_data.py',
        'test_api.py',
        'requirements.txt',
        '.env',
        '.gitignore'
    ],
    'App Files': [
        'app/__init__.py',
        'app/models.py',
        'app/routes.py',
        'app/ai_engine.py'
    ],
    'CSS Files': [
        'static/css/main.css',
        'static/css/glassmorphism.css',
        'static/css/animations.css'
    ],
    'JavaScript Files': [
        'static/js/main.js',
        'static/js/api.js',
        'static/js/theme.js'
    ],
    'Template Files': [
        'templates/index.html',
        'templates/student.html',
        'templates/admin.html'
    ]
}

all_good = True
missing_files = []

for category, files in files_to_check.items():
    print(f"📁 {category}:")
    for file in files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            missing_files.append(file)
            all_good = False
    print()

if all_good:
    print("="*70)
    print("  ✅ ALL FILES PRESENT - Structure is perfect!")
    print("="*70 + "\n")
else:
    print("="*70)
    print("  ⚠️  MISSING FILES DETECTED")
    print("="*70)
    print("\nMissing files:")
    for file in missing_files:
        print(f"  - {file}")
    print("\nPlease create the missing files.\n")
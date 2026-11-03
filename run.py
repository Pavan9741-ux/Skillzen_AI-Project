"""SkillZen AI - Entry Point"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def main():
    from app import create_app
    app = create_app()
    
    print("\n" + "="*70)
    print("🚀 SkillZen AI Server Starting...")
    print("="*70)
    print(f"📍 URL: http://localhost:5000")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
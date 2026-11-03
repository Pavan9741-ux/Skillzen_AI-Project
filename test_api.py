"""
SkillZen AI - API Testing Script
Tests all endpoints and AI recommendation functionality
Run this after starting the server
"""

import requests
import json
from pprint import pprint

# Base URL
BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_health_check():
    """Test API health endpoint"""
    print_section("TEST 1: Health Check")
    
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status Code: {response.status_code}")
    pprint(response.json())
    
    assert response.status_code == 200
    print("✅ Health check passed!")


def test_get_stats():
    """Test statistics endpoint"""
    print_section("TEST 2: Platform Statistics")
    
    response = requests.get(f"{BASE_URL}/api/stats")
    print(f"Status Code: {response.status_code}")
    pprint(response.json())
    
    assert response.status_code == 200
    print("✅ Statistics test passed!")


def test_get_all_skills():
    """Test skills listing endpoint"""
    print_section("TEST 3: Get All Skills")
    
    response = requests.get(f"{BASE_URL}/student/skills/all")
    data = response.json()
    
    print(f"Status Code: {response.status_code}")
    print(f"\nTechnical Skills Count: {len(data['technical_skills'])}")
    print(f"Sample Technical Skills: {data['technical_skills'][:5]}")
    print(f"\nNon-Technical Skills Count: {len(data['non_technical_skills'])}")
    print(f"Programming Languages Count: {len(data['programming_languages'])}")
    
    assert response.status_code == 200
    print("✅ Skills listing test passed!")


def test_admin_login():
    """Test admin authentication"""
    print_section("TEST 4: Admin Login")
    
    # Test successful login
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    print(f"Status Code: {response.status_code}")
    pprint(response.json())
    
    assert response.status_code == 200
    print("✅ Admin login test passed!")
    
    # Return session for subsequent tests
    return response.cookies


def test_recommendations_high_performer():
    """Test AI recommendations for high-performing student"""
    print_section("TEST 5: AI Recommendations - High Performer")
    
    student_data = {
        "cgpa": 8.5,
        "sgpa": 8.7,
        "technical_skills": [
            "Python", "Java", "Machine Learning", "Deep Learning",
            "TensorFlow", "AWS", "Docker", "Kubernetes", "REST API"
        ],
        "non_technical_skills": [
            "Leadership", "Communication", "Problem Solving", "Teamwork"
        ],
        "programming_languages": ["Python", "Java", "JavaScript", "C++"]
    }
    
    response = requests.post(
        f"{BASE_URL}/student/recommend",
        json=student_data
    )
    
    data = response.json()
    
    print(f"Status Code: {response.status_code}")
    print(f"\nTotal Companies: {data['total_companies']}")
    print(f"Eligible Companies: {data['eligible_companies']}")
    print(f"\nTop 3 Recommendations:")
    
    for i, rec in enumerate(data['recommendations'][:3], 1):
        print(f"\n{i}. {rec['company']['name']}")
        print(f"   Match Score: {rec['scores']['total_score']}%")
        print(f"   CGPA Score: {rec['scores']['cgpa_score']}")
        print(f"   Skill Score: {rec['scores']['tech_skill_score']}")
        print(f"   Language Score: {rec['scores']['language_score']}")
        print(f"   Eligible: {rec['eligible']}")
        
        # Show gap analysis
        gap = rec['gap_analysis']
        print(f"   Overall Match: {gap['overall_match']}%")
        
        if gap['priority_actions']:
            print("   Priority Actions:")
            for action in gap['priority_actions'][:2]:
                print(f"     - [{action['priority']}] {action['action']}")
    
    assert response.status_code == 200
    print("\n✅ High performer recommendations test passed!")


def test_recommendations_average_student():
    """Test AI recommendations for average student"""
    print_section("TEST 6: AI Recommendations - Average Student")
    
    student_data = {
        "cgpa": 7.0,
        "sgpa": 7.2,
        "technical_skills": [
            "Java", "Python", "MySQL", "HTML", "CSS"
        ],
        "non_technical_skills": [
            "Communication", "Teamwork"
        ],
        "programming_languages": ["Java", "Python", "C"]
    }
    
    response = requests.post(
        f"{BASE_URL}/student/recommend",
        json=student_data
    )
    
    data = response.json()
    
    print(f"Status Code: {response.status_code}")
    print(f"Eligible Companies: {data['eligible_companies']}")
    
    print(f"\nTop 3 Recommendations with Skill Gap Analysis:")
    
    for i, rec in enumerate(data['recommendations'][:3], 1):
        print(f"\n{i}. {rec['company']['name']}")
        print(f"   Match Score: {rec['scores']['total_score']}%")
        
        gap = rec['gap_analysis']
        
        # Show skill gaps
        if gap['skill_gaps']:
            tech_gaps = gap['skill_gaps'].get('technical', {})
            if tech_gaps.get('missing'):
                print(f"   Missing Skills: {', '.join(tech_gaps['missing'][:5])}")
        
        # Show recommendations
        if gap['recommendations']:
            print("   AI Recommendations:")
            for rec_text in gap['recommendations'][:2]:
                print(f"     - {rec_text}")
    
    assert response.status_code == 200
    print("\n✅ Average student recommendations test passed!")


def test_recommendations_low_cgpa():
    """Test AI recommendations for student with low CGPA"""
    print_section("TEST 7: AI Recommendations - Low CGPA Student")
    
    student_data = {
        "cgpa": 6.0,
        "sgpa": 6.2,
        "technical_skills": [
            "Python", "Java", "HTML", "CSS"
        ],
        "non_technical_skills": [
            "Teamwork"
        ],
        "programming_languages": ["Python", "Java"]
    }
    
    response = requests.post(
        f"{BASE_URL}/student/recommend",
        json=student_data
    )
    
    data = response.json()
    
    print(f"Status Code: {response.status_code}")
    print(f"Eligible Companies: {data['eligible_companies']}")
    
    if data['recommendations']:
        top_rec = data['recommendations'][0]
        print(f"\nTop Match: {top_rec['company']['name']}")
        print(f"Match Score: {top_rec['scores']['total_score']}%")
        
        gap = top_rec['gap_analysis']
        
        # Show CGPA analysis
        if gap['cgpa_analysis'].get('gap'):
            print(f"\nCGPA Gap Analysis:")
            print(f"   Current: {gap['cgpa_analysis']['current']}")
            print(f"   Required: {gap['cgpa_analysis']['required']}")
            print(f"   Gap: {gap['cgpa_analysis']['gap']}")
            print(f"   Message: {gap['cgpa_analysis']['message']}")
        
        # Show priority actions
        if gap['priority_actions']:
            print("\nPriority Actions:")
            for action in gap['priority_actions'][:3]:
                print(f"   [{action['priority']}] {action['action']}")
                print(f"   Impact: {action['impact']}")
    
    assert response.status_code == 200
    print("\n✅ Low CGPA student test passed!")


def test_skill_gap_analyzer():
    """Test Intelligent Skill Gap Analyzer feature"""
    print_section("TEST 8: Intelligent Skill Gap Analyzer")
    
    # Student with specific skill gaps
    student_data = {
        "cgpa": 7.5,
        "sgpa": 7.5,
        "technical_skills": [
            "Python", "HTML", "CSS"
        ],
        "non_technical_skills": [
            "Communication"
        ],
        "programming_languages": ["Python"]
    }
    
    response = requests.post(
        f"{BASE_URL}/student/recommend",
        json=student_data
    )
    
    data = response.json()
    
    # Find a company with gaps
    for rec in data['recommendations'][:5]:
        gap = rec['gap_analysis']
        
        if gap['skill_gaps'] or gap['language_gaps']:
            print(f"Company: {rec['company']['name']}")
            print(f"Match Score: {gap['overall_match']}%")
            print(f"\nDetailed Gap Analysis:")
            
            # Technical skill gaps
            if gap['skill_gaps'].get('technical'):
                tech = gap['skill_gaps']['technical']
                print(f"\nTechnical Skills:")
                print(f"  Matched: {', '.join(tech['matched']) if tech['matched'] else 'None'}")
                print(f"  Missing: {', '.join(tech['missing']) if tech['missing'] else 'None'}")
                print(f"  Match %: {tech['match_percentage']:.1f}%")
            
            # Language gaps
            if gap['language_gaps']:
                lang = gap['language_gaps']
                print(f"\nProgramming Languages:")
                print(f"  Matched: {', '.join(lang['matched']) if lang['matched'] else 'None'}")
                print(f"  Missing: {', '.join(lang['missing']) if lang['missing'] else 'None'}")
            
            # Recommendations
            if gap['recommendations']:
                print(f"\nAI Recommendations:")
                for i, rec_text in enumerate(gap['recommendations'], 1):
                    print(f"  {i}. {rec_text}")
            
            break
    
    assert response.status_code == 200
    print("\n✅ Skill Gap Analyzer test passed!")


def run_all_tests():
    """Run all API tests"""
    print("\n" + "█"*70)
    print("  SkillZen AI - Comprehensive API Testing Suite")
    print("█"*70)
    
    try:
        test_health_check()
        test_get_stats()
        test_get_all_skills()
        test_admin_login()
        test_recommendations_high_performer()
        test_recommendations_average_student()
        test_recommendations_low_cgpa()
        test_skill_gap_analyzer()
        
        print("\n" + "█"*70)
        print("  ✅ ALL TESTS PASSED!")
        print("█"*70 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server!")
        print("   Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    run_all_tests()
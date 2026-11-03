"""
SkillZen AI - AI Recommendation Engine
FIXED VERSION - No JSON serialization errors
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SkillZenAI:
    """AI Engine for matching students with companies"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
    
    def recommend_companies(self, student_data, companies):
        """
        Generate personalized company recommendations
        
        Args:
            student_data (dict): Student profile data
            companies (list): List of Company model objects
            
        Returns:
            list: Sorted recommendations with scores
        """
        recommendations = []
        
        for company in companies:
            # Check eligibility
            eligible = self._check_eligibility(student_data, company)
            
            # Calculate match scores
            scores = self._calculate_match_scores(student_data, company)
            
            # Generate gap analysis
            gap_analysis = self._analyze_skill_gap(student_data, company, scores)
            
            recommendation = {
                'company': {
                    'id': company.id,
                    'name': company.name,
                    'description': company.description,
                    'location': company.location,
                    'email': company.email,
                    'phone': company.phone,
                    'website': company.website,
                    'min_cgpa': float(company.min_cgpa),
                    'min_sgpa': float(company.min_sgpa),
                    'duration': company.internship_duration,
                    'stipend_range': company.stipend_range,
                    'is_active': bool(company.is_active),
                    'vtu_approved': bool(company.vtu_approved)
                },
                'eligible': bool(eligible),
                'scores': scores,
                'gap_analysis': gap_analysis
            }
            
            recommendations.append(recommendation)
        
        # Sort by total score (descending)
        recommendations.sort(key=lambda x: x['scores']['total_score'], reverse=True)
        
        return recommendations
    
    def _check_eligibility(self, student_data, company):
        """Check if student meets minimum requirements"""
        cgpa_ok = student_data['cgpa'] >= company.min_cgpa
        sgpa_ok = student_data.get('sgpa', student_data['cgpa']) >= company.min_sgpa
        return bool(cgpa_ok and sgpa_ok)
    
    def _calculate_match_scores(self, student_data, company):
        """Calculate detailed matching scores"""
        
        # Get company requirements
        company_tech_skills = company.get_technical_skills()
        company_non_tech_skills = company.get_non_technical_skills()
        company_languages = company.get_programming_languages()
        
        # Get student skills
        student_tech_skills = student_data.get('technical_skills', [])
        student_non_tech_skills = student_data.get('non_technical_skills', [])
        student_languages = student_data.get('programming_languages', [])
        
        # Calculate technical skills match
        tech_matched = list(set(student_tech_skills) & set(company_tech_skills))
        tech_missing = list(set(company_tech_skills) - set(student_tech_skills))
        tech_score = (len(tech_matched) / len(company_tech_skills) * 100) if company_tech_skills else 0.0
        
        # Calculate programming languages match
        lang_matched = list(set(student_languages) & set(company_languages))
        lang_missing = list(set(company_languages) - set(student_languages))
        lang_score = (len(lang_matched) / len(company_languages) * 100) if company_languages else 0.0
        
        # Calculate non-technical skills match
        if company_non_tech_skills:
            non_tech_matched = list(set(student_non_tech_skills) & set(company_non_tech_skills))
            non_tech_missing = list(set(company_non_tech_skills) - set(student_non_tech_skills))
            non_tech_score = (len(non_tech_matched) / len(company_non_tech_skills) * 100)
        else:
            non_tech_matched = []
            non_tech_missing = []
            non_tech_score = 100.0
        
        # Calculate CGPA score (normalized to 100)
        cgpa_score = (student_data['cgpa'] / 10.0) * 100.0
        
        # Weighted total score
        # 30% CGPA, 40% Technical Skills, 20% Languages, 10% Non-Technical
        total_score = (
            cgpa_score * 0.30 +
            tech_score * 0.40 +
            lang_score * 0.20 +
            non_tech_score * 0.10
        )
        
        return {
            'total_score': float(round(total_score, 2)),
            'cgpa_score': float(round(cgpa_score, 2)),
            'technical_skills_score': float(round(tech_score, 2)),
            'programming_languages_score': float(round(lang_score, 2)),
            'non_technical_skills_score': float(round(non_tech_score, 2)),
            'tech_skills_matched': tech_matched,
            'tech_skills_missing': tech_missing,
            'lang_matched': lang_matched,
            'lang_missing': lang_missing,
            'non_tech_matched': non_tech_matched,
            'non_tech_missing': non_tech_missing
        }
    
    def _analyze_skill_gap(self, student_data, company, scores):
        """Generate actionable skill gap analysis"""
        
        missing_tech = scores['tech_skills_missing']
        missing_lang = scores['lang_missing']
        missing_non_tech = scores['non_tech_missing']
        
        priority_actions = []
        
        # High priority: Missing critical technical skills
        for skill in missing_tech[:3]:
            priority_actions.append({
                'priority': 'HIGH',
                'action': f'Learn {skill}',
                'impact': '+15% match score',
                'category': 'technical'
            })
        
        # Medium priority: Missing programming languages
        for lang in missing_lang[:2]:
            priority_actions.append({
                'priority': 'MEDIUM',
                'action': f'Learn {lang}',
                'impact': '+10% match score',
                'category': 'programming'
            })
        
        # Low priority: Missing non-technical skills
        for skill in missing_non_tech[:2]:
            priority_actions.append({
                'priority': 'LOW',
                'action': f'Improve {skill}',
                'impact': '+5% match score',
                'category': 'soft_skills'
            })
        
        # CGPA improvement if below company requirement
        if student_data['cgpa'] < company.min_cgpa:
            cgpa_gap = company.min_cgpa - student_data['cgpa']
            priority_actions.insert(0, {
                'priority': 'CRITICAL',
                'action': f'Improve CGPA by {cgpa_gap:.1f} points',
                'impact': 'Required for eligibility',
                'category': 'academic'
            })
        
        return {
            'overall_match': float(scores['total_score']),
            'priority_actions': priority_actions,
            'total_gaps': len(missing_tech) + len(missing_lang) + len(missing_non_tech),
            'recommendation': self._get_recommendation_text(scores['total_score'])
        }
    
    def _get_recommendation_text(self, score):
        """Get recommendation text based on score"""
        if score >= 90:
            return "Excellent match! Apply immediately."
        elif score >= 75:
            return "Great match! Strong candidate."
        elif score >= 60:
            return "Good match! Consider applying."
        elif score >= 50:
            return "Fair match. Improve key skills first."
        else:
            return "Low match. Significant skill gap exists."
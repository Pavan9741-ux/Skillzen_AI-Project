"""
SkillZen AI v2.0 - Advanced AI Engine
Deep Learning with Sentence Transformers & Skill Matching
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Try to import advanced ML libraries
try:
    from sentence_transformers import SentenceTransformer
    BERT_AVAILABLE = True
except ImportError:
    BERT_AVAILABLE = False
    print("⚠️  Sentence Transformers not installed. Using TF-IDF fallback.")


class AdvancedAI:
    """Advanced AI Engine with BERT/Sentence Transformers support"""
    
    def __init__(self, use_bert=False):
        self.use_bert = use_bert and BERT_AVAILABLE
        
        if self.use_bert:
            try:
                print("🤖 Loading BERT model...")
                self.bert_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("✅ BERT model loaded successfully!")
            except Exception as e:
                print(f"⚠️  BERT loading failed: {e}")
                print("🔄 Falling back to TF-IDF...")
                self.use_bert = False
                self.vectorizer = TfidfVectorizer()
        else:
            self.vectorizer = TfidfVectorizer()
        
        # Comprehensive skill synonyms mapping
        self.skill_synonyms = {
            # Frontend
            'react': ['reactjs', 'react.js', 'react js', 'react-js'],
            'vue': ['vuejs', 'vue.js', 'vue js', 'vue-js'],
            'angular': ['angularjs', 'angular.js', 'angular js'],
            'next': ['nextjs', 'next.js'],
            
            # Backend
            'node': ['nodejs', 'node.js', 'node js'],
            'express': ['expressjs', 'express.js'],
            'django': ['django framework'],
            'flask': ['flask framework'],
            'spring': ['spring boot', 'springboot'],
            
            # Mobile
            'react native': ['react-native', 'reactnative', 'rn'],
            'flutter': ['flutter framework'],
            
            # AI/ML
            'ai': ['artificial intelligence', 'machine learning', 'ml'],
            'dl': ['deep learning', 'neural networks', 'nn'],
            'nlp': ['natural language processing', 'text processing'],
            'cv': ['computer vision', 'image processing'],
            
            # Data
            'ds': ['data science', 'data analytics'],
            'bi': ['business intelligence', 'analytics'],
            
            # DevOps
            'docker': ['containerization', 'containers'],
            'k8s': ['kubernetes', 'container orchestration'],
            'ci/cd': ['cicd', 'continuous integration'],
            
            # Development
            'fullstack': ['full stack', 'full-stack'],
            'backend': ['back end', 'back-end', 'server-side'],
            'frontend': ['front end', 'front-end', 'client-side'],
            
            # Cloud
            'aws': ['amazon web services', 'amazon cloud'],
            'azure': ['microsoft azure', 'ms azure'],
            'gcp': ['google cloud', 'google cloud platform'],
        }
    
    def normalize_skill(self, skill):
        """Normalize skill name to handle synonyms"""
        if not skill:
            return ''
        
        skill_lower = skill.lower().strip()
        
        # Check if skill matches any synonym
        for canonical, synonyms in self.skill_synonyms.items():
            if skill_lower == canonical or skill_lower in synonyms:
                return canonical
        
        return skill_lower
    
    def get_skill_embeddings(self, skills_list):
        """Get embeddings for skills using BERT or TF-IDF"""
        if not skills_list:
            return np.zeros((1, 384)) if self.use_bert else np.zeros((1, 100))
        
        # Normalize skills
        normalized_skills = [self.normalize_skill(s) for s in skills_list if s]
        
        if not normalized_skills:
            return np.zeros((1, 384)) if self.use_bert else np.zeros((1, 100))
        
        skills_text = ' '.join(normalized_skills)
        
        if self.use_bert:
            return self.bert_model.encode([skills_text])
        else:
            try:
                return self.vectorizer.fit_transform([skills_text]).toarray()
            except:
                return np.zeros((1, 100))
    
    def calculate_semantic_similarity(self, student_skills, company_skills):
        """Calculate semantic similarity between skill sets"""
        if not student_skills or not company_skills:
            return 0.0
        
        try:
            student_embedding = self.get_skill_embeddings(student_skills)
            company_embedding = self.get_skill_embeddings(company_skills)
            
            similarity = cosine_similarity(student_embedding, company_embedding)[0][0]
            return float(max(0, min(100, similarity * 100)))
        except Exception as e:
            print(f"Similarity calculation error: {e}")
            return 0.0
    
    def recommend_with_advanced_ai(self, student_data, companies):
        """Advanced recommendations using deep learning or TF-IDF"""
        recommendations = []
        
        # Combine all student skills
        all_student_skills = []
        all_student_skills.extend(student_data.get('technical_skills', []))
        all_student_skills.extend(student_data.get('programming_languages', []))
        all_student_skills.extend(student_data.get('non_technical_skills', []))
        
        for company in companies:
            try:
                # Get company skills
                all_company_skills = []
                all_company_skills.extend(company.get_technical_skills())
                all_company_skills.extend(company.get_programming_languages())
                all_company_skills.extend(company.get_non_technical_skills())
                
                # Calculate semantic similarity
                semantic_score = self.calculate_semantic_similarity(
                    all_student_skills,
                    all_company_skills
                )
                
                # Check eligibility
                eligible = (
                    student_data.get('cgpa', 0) >= company.min_cgpa and
                    student_data.get('sgpa', student_data.get('cgpa', 0)) >= company.min_sgpa
                )
                
                # Calculate traditional scores
                traditional_scores = self._calculate_detailed_scores(student_data, company)
                
                # Hybrid score
                if self.use_bert:
                    # BERT: 70% semantic + 30% traditional
                    hybrid_score = (semantic_score * 0.70) + (traditional_scores['total_score'] * 0.30)
                else:
                    # TF-IDF: 50% semantic + 50% traditional
                    hybrid_score = (semantic_score * 0.50) + (traditional_scores['total_score'] * 0.50)
                
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
                        'view_count': company.view_count,
                        'application_count': company.application_count,
                    },
                    'eligible': bool(eligible),
                    'scores': {
                        'total_score': float(round(hybrid_score, 2)),
                        'semantic_similarity': float(round(semantic_score, 2)),
                        'traditional_score': float(round(traditional_scores['total_score'], 2)),
                        'cgpa_score': float(round(traditional_scores['cgpa_score'], 2)),
                        'technical_score': float(round(traditional_scores['technical_score'], 2)),
                        'language_score': float(round(traditional_scores['language_score'], 2)),
                        'soft_skills_score': float(round(traditional_scores['soft_skills_score'], 2)),
                        'tech_skills_matched': traditional_scores['tech_matched'],
                        'tech_skills_missing': traditional_scores['tech_missing'],
                        'lang_matched': traditional_scores['lang_matched'],
                        'lang_missing': traditional_scores['lang_missing'],
                    },
                    'gap_analysis': self._generate_advanced_gap_analysis(
                        student_data, 
                        company, 
                        hybrid_score,
                        traditional_scores
                    ),
                    'ai_engine': 'BERT' if self.use_bert else 'TF-IDF'
                }
                
                recommendations.append(recommendation)
                
            except Exception as e:
                print(f"Error processing company {company.name}: {e}")
                continue
        
        # Sort by total score
        recommendations.sort(key=lambda x: x['scores']['total_score'], reverse=True)
        
        return recommendations
    
    def _calculate_detailed_scores(self, student_data, company):
        """Calculate detailed matching scores"""
        # Get normalized skills
        company_tech = [self.normalize_skill(s) for s in company.get_technical_skills()]
        student_tech = [self.normalize_skill(s) for s in student_data.get('technical_skills', [])]
        
        company_lang = [self.normalize_skill(s) for s in company.get_programming_languages()]
        student_lang = [self.normalize_skill(s) for s in student_data.get('programming_languages', [])]
        
        company_soft = [self.normalize_skill(s) for s in company.get_non_technical_skills()]
        student_soft = [self.normalize_skill(s) for s in student_data.get('non_technical_skills', [])]
        
        # Technical skills matching
        tech_matched = list(set(student_tech) & set(company_tech))
        tech_missing = list(set(company_tech) - set(student_tech))
        tech_score = (len(tech_matched) / len(company_tech) * 100) if company_tech else 100.0
        
        # Programming languages matching
        lang_matched = list(set(student_lang) & set(company_lang))
        lang_missing = list(set(company_lang) - set(student_lang))
        lang_score = (len(lang_matched) / len(company_lang) * 100) if company_lang else 100.0
        
        # Soft skills matching
        soft_matched = list(set(student_soft) & set(company_soft))
        soft_missing = list(set(company_soft) - set(student_soft))
        soft_score = (len(soft_matched) / len(company_soft) * 100) if company_soft else 100.0
        
        # CGPA score
        cgpa = student_data.get('cgpa', 0)
        cgpa_score = (cgpa / 10.0) * 100.0
        
        # Weighted total: 30% CGPA, 40% Technical, 20% Languages, 10% Soft Skills
        total_score = (
            cgpa_score * 0.30 +
            tech_score * 0.40 +
            lang_score * 0.20 +
            soft_score * 0.10
        )
        
        return {
            'total_score': total_score,
            'cgpa_score': cgpa_score,
            'technical_score': tech_score,
            'language_score': lang_score,
            'soft_skills_score': soft_score,
            'tech_matched': tech_matched,
            'tech_missing': tech_missing,
            'lang_matched': lang_matched,
            'lang_missing': lang_missing,
            'soft_matched': soft_matched,
            'soft_missing': soft_missing,
        }
    
    def _generate_advanced_gap_analysis(self, student_data, company, final_score, detailed_scores):
        """Generate comprehensive gap analysis with actionable insights"""
        priority_actions = []
        
        # CRITICAL: CGPA below requirement
        if student_data.get('cgpa', 0) < company.min_cgpa:
            gap = company.min_cgpa - student_data.get('cgpa', 0)
            priority_actions.append({
                'priority': 'CRITICAL',
                'action': f'Improve CGPA by {gap:.1f} points to {company.min_cgpa}',
                'impact': 'Required for eligibility',
                'category': 'academic',
                'estimated_time': 'Next semester',
                'difficulty': 'high'
            })
        
        # HIGH: Missing critical technical skills
        critical_tech = ['Python', 'Java', 'JavaScript', 'C++', 'SQL']
        missing_critical = [s for s in detailed_scores['tech_missing'] 
                          if s in [self.normalize_skill(x) for x in critical_tech]]
        
        for skill in missing_critical[:3]:
            priority_actions.append({
                'priority': 'HIGH',
                'action': f'Learn {skill.title()}',
                'impact': '+15-20% match score',
                'category': 'technical',
                'estimated_time': '2-4 weeks',
                'difficulty': 'medium'
            })
        
        # MEDIUM: Missing programming languages
        for lang in detailed_scores['lang_missing'][:2]:
            priority_actions.append({
                'priority': 'MEDIUM',
                'action': f'Learn {lang.title()}',
                'impact': '+10-15% match score',
                'category': 'programming',
                'estimated_time': '3-6 weeks',
                'difficulty': 'medium'
            })
        
        # MEDIUM: Missing other technical skills
        for skill in detailed_scores['tech_missing'][:2]:
            if skill not in missing_critical:
                priority_actions.append({
                    'priority': 'MEDIUM',
                    'action': f'Learn {skill.title()}',
                    'impact': '+8-12% match score',
                    'category': 'technical',
                    'estimated_time': '1-3 weeks',
                    'difficulty': 'low-medium'
                })
        
        # LOW: Soft skills
        for skill in detailed_scores['soft_missing'][:2]:
            priority_actions.append({
                'priority': 'LOW',
                'action': f'Develop {skill.title()}',
                'impact': '+5% match score',
                'category': 'soft_skills',
                'estimated_time': '2-4 weeks',
                'difficulty': 'low'
            })
        
        return {
            'overall_match': float(round(final_score, 2)),
            'priority_actions': priority_actions[:8],  # Top 8 actions
            'total_gaps': len(detailed_scores['tech_missing']) + len(detailed_scores['lang_missing']),
            'strengths': {
                'matched_skills': len(detailed_scores['tech_matched']) + len(detailed_scores['lang_matched']),
                'cgpa_meets_requirement': student_data.get('cgpa', 0) >= company.min_cgpa,
            },
            'recommendation': self._get_recommendation_text(final_score),
            'estimated_improvement_time': self._estimate_improvement_time(priority_actions)
        }
    
    def _get_recommendation_text(self, score):
        """Get human-readable recommendation"""
        if score >= 90:
            return "🎯 Excellent match! Apply immediately - you're a perfect fit."
        elif score >= 80:
            return "✨ Great match! Strong candidate with high chances."
        elif score >= 70:
            return "👍 Good match! Solid profile, consider applying."
        elif score >= 60:
            return "📚 Fair match. Improve 2-3 key skills before applying."
        elif score >= 50:
            return "⚠️ Below average match. Significant skill gap - focus on learning."
        else:
            return "❌ Low match. Build foundational skills first."
    
    def _estimate_improvement_time(self, actions):
        """Estimate total time needed to close skill gaps"""
        if not actions:
            return "No improvements needed"
        
        high_priority = len([a for a in actions if a['priority'] in ['CRITICAL', 'HIGH']])
        
        if high_priority >= 3:
            return "2-3 months of focused learning"
        elif high_priority >= 1:
            return "1-2 months of learning"
        else:
            return "2-4 weeks of practice"
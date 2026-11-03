"""
SkillZen AI v2.0 - Analytics Engine
Real-time analytics and insights
"""

from app.models import (
    StudentProfileExtended, Company, Application, 
    SkillTrend, PlatformAnalytics
)
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func
import json


class AnalyticsEngine:
    """Analytics and insights engine"""
    
    @staticmethod
    def get_platform_stats():
        """Get overall platform statistics"""
        try:
            total_students = StudentProfileExtended.query.count()
            total_companies = Company.query.filter_by(is_active=True).count()
            total_applications = Application.query.count()
            successful_placements = Application.query.filter_by(status='accepted').count()
            
            # Calculate success rate
            success_rate = (successful_placements / total_applications * 100) if total_applications > 0 else 0
            
            # Average match score
            avg_match = db.session.query(func.avg(Application.match_score)).scalar() or 0
            
            # Profile completeness
            avg_completeness = db.session.query(
                func.avg(StudentProfileExtended.profile_completeness)
            ).scalar() or 0
            
            return {
                'total_students': total_students,
                'total_companies': total_companies,
                'total_applications': total_applications,
                'successful_placements': successful_placements,
                'success_rate': round(success_rate, 2),
                'avg_match_score': round(avg_match, 2),
                'avg_profile_completeness': round(avg_completeness, 2)
            }
        except Exception as e:
            print(f"Error getting platform stats: {e}")
            return {}
    
    @staticmethod
    def get_top_skills(limit=10):
        """Get most in-demand skills"""
        try:
            skills = SkillTrend.query.order_by(
                SkillTrend.demand_count.desc()
            ).limit(limit).all()
            
            return [{
                'name': skill.skill_name,
                'demand': skill.demand_count,
                'students': skill.student_count,
                'trend': skill.trend_status,
                'growth': skill.growth_rate,
                'category': skill.category
            } for skill in skills]
        except Exception as e:
            print(f"Error getting top skills: {e}")
            return []
    
    @staticmethod
    def get_trending_skills():
        """Get emerging and hot skills"""
        try:
            trending = SkillTrend.query.filter(
                SkillTrend.trend_status.in_(['emerging', 'hot'])
            ).order_by(SkillTrend.growth_rate.desc()).limit(15).all()
            
            return [{
                'name': skill.skill_name,
                'status': skill.trend_status,
                'growth_rate': skill.growth_rate,
                'demand': skill.demand_count,
                'category': skill.category,
                'difficulty': skill.difficulty_level,
                'salary_boost': skill.avg_salary_boost
            } for skill in trending]
        except Exception as e:
            print(f"Error getting trending skills: {e}")
            return []
    
    @staticmethod
    def get_student_analytics(student_id):
        """Get analytics for specific student"""
        try:
            student = StudentProfileExtended.query.filter_by(user_id=student_id).first()
            if not student:
                return None
            
            # Get application stats
            applications = Application.query.filter_by(student_id=student_id).all()
            
            status_breakdown = {
                'applied': 0,
                'viewed': 0,
                'shortlisted': 0,
                'interview': 0,
                'rejected': 0,
                'accepted': 0
            }
            
            for app in applications:
                status_breakdown[app.status] = status_breakdown.get(app.status, 0) + 1
            
            # Calculate conversion rate
            conversion_rate = (status_breakdown['accepted'] / len(applications) * 100) if applications else 0
            
            return {
                'profile_completeness': student.profile_completeness,
                'profile_views': student.profile_views,
                'applications_sent': len(applications),
                'applications_accepted': status_breakdown['accepted'],
                'conversion_rate': round(conversion_rate, 2),
                'status_breakdown': status_breakdown,
                'avg_match_score': round(
                    sum([a.match_score for a in applications if a.match_score]) / len(applications), 2
                ) if applications else 0
            }
        except Exception as e:
            print(f"Error getting student analytics: {e}")
            return None
    
    @staticmethod
    def get_company_analytics(company_id):
        """Get analytics for specific company"""
        try:
            company = Company.query.get(company_id)
            if not company:
                return None
            
            applications = Application.query.filter_by(company_id=company_id).all()
            
            return {
                'view_count': company.view_count,
                'application_count': len(applications),
                'avg_match_score': round(
                    sum([a.match_score for a in applications if a.match_score]) / len(applications), 2
                ) if applications else 0,
                'acceptance_rate': round(
                    len([a for a in applications if a.status == 'accepted']) / len(applications) * 100, 2
                ) if applications else 0
            }
        except Exception as e:
            print(f"Error getting company analytics: {e}")
            return None
    
    @staticmethod
    def get_timeline_data(days=30):
        """Get timeline data for charts"""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            analytics = PlatformAnalytics.query.filter(
                PlatformAnalytics.date >= start_date,
                PlatformAnalytics.date <= end_date
            ).order_by(PlatformAnalytics.date).all()
            
            return [{
                'date': a.date.isoformat(),
                'students': a.total_students,
                'companies': a.total_companies,
                'applications': a.total_applications,
                'placements': a.successful_placements
            } for a in analytics]
        except Exception as e:
            print(f"Error getting timeline data: {e}")
            return []
    
    @staticmethod
    def update_skill_trends():
        """Update skill trends based on company demands and student profiles"""
        try:
            # Get all companies
            companies = Company.query.filter_by(is_active=True).all()
            
            # Count skill demands
            skill_demands = {}
            
            for company in companies:
                all_skills = (
                    company.get_technical_skills() + 
                    company.get_programming_languages()
                )
                
                for skill in all_skills:
                    skill_lower = skill.lower().strip()
                    skill_demands[skill_lower] = skill_demands.get(skill_lower, 0) + 1
            
            # Update or create skill trends
            for skill_name, count in skill_demands.items():
                trend = SkillTrend.query.filter_by(skill_name=skill_name).first()
                
                if trend:
                    old_count = trend.demand_count
                    trend.demand_count = count
                    
                    # Calculate growth rate
                    if old_count > 0:
                        growth = ((count - old_count) / old_count) * 100
                        trend.growth_rate = round(growth, 2)
                        
                        # Update trend status
                        if growth > 50:
                            trend.trend_status = 'hot'
                        elif growth > 20:
                            trend.trend_status = 'emerging'
                        elif growth < -20:
                            trend.trend_status = 'declining'
                        else:
                            trend.trend_status = 'stable'
                else:
                    # Create new trend
                    trend = SkillTrend(
                        skill_name=skill_name,
                        demand_count=count,
                        category='technical',
                        trend_status='emerging' if count > 5 else 'stable'
                    )
                    db.session.add(trend)
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error updating skill trends: {e}")
            db.session.rollback()
            return False
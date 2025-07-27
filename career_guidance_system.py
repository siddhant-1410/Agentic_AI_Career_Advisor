import requests
import json
import os
from datetime import datetime
import time

class CareerGuidanceSystem:
    def __init__(self, mistral_api_key=None, serpapi_key=None):
        """Initialize the career guidance system with Mistral AI"""
        self.mistral_api_key = mistral_api_key
        self.serpapi_key = serpapi_key
        
        # Mistral API configuration
        self.mistral_base_url = "https://api.mistral.ai/v1/chat/completions"
        self.mistral_headers = {
            "Authorization": f"Bearer {mistral_api_key}",
            "Content-Type": "application/json"
        }
        
        self.career_data = {}
        self.search_cache = {}
        self.user_profile = {}
        
        self.fallback_career_options = {
            "Technology": [
                "Software Engineering",
                "Data Science", 
                "Cybersecurity",
                "AI/ML Engineering",
                "DevOps",
                "Cloud Architecture",
                "Mobile Development",
                "Full Stack Development",
                "Web Development",
                "Game Development"
            ],
            "Healthcare": [
                "Medicine",
                "Nursing",
                "Pharmacy",
                "Biomedical Engineering", 
                "Healthcare Administration",
                "Physical Therapy",
                "Medical Research",
                "Healthcare IT",
                "Clinical Psychology",
                "Dentistry"
            ],
            "Business": [
                "Finance",
                "Marketing",
                "Management",
                "Entrepreneurship",
                "Business Analysis",
                "Project Management",
                "Human Resources",
                "Sales",
                "Operations",
                "Consulting"
            ],
            "Creative": [
                "Graphic Design",
                "UX/UI Design",
                "Content Creation",
                "Digital Marketing",
                "Animation",
                "Film Production",
                "Photography",
                "Writing & Journalism",
                "Music Production",
                "Interior Design"
            ],
            "Engineering": [
                "Mechanical Engineering",
                "Electrical Engineering",
                "Civil Engineering",
                "Chemical Engineering",
                "Aerospace Engineering",
                "Environmental Engineering",
                "Industrial Engineering"
            ],
            "Education": [
                "Teaching",
                "Educational Administration",
                "Curriculum Development",
                "Educational Technology",
                "School Counseling",
                "Special Education"
            ]
        }
    
    def generate_mistral_response(self, prompt, max_tokens=3000, temperature=0.2):
        """Generate response using Mistral API"""
        if not self.mistral_api_key:
            return "Mistral API key is not available. Please provide a valid API key."
        
        payload = {
            "model": "mistral-large-latest",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                self.mistral_base_url,
                headers=self.mistral_headers,
                json=payload,
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            elif response.status_code == 429:
                # Rate limit hit, wait and retry once
                time.sleep(5)
                response = requests.post(
                    self.mistral_base_url,
                    headers=self.mistral_headers,
                    json=payload,
                    timeout=45
                )
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    return f"API Error after retry: {response.status_code} - {response.text[:200]}"
            else:
                return f"API Error: {response.status_code} - {response.text[:200]}"
                
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def search_with_cache(self, query, cache_key, ttl_hours=24, max_retries=3):
        """Perform a search with caching to avoid redundant API calls"""
        # Check cache first
        if cache_key in self.search_cache:
            timestamp = self.search_cache[cache_key]['timestamp']
            age_hours = (datetime.now() - timestamp).total_seconds() / 3600
            if age_hours < ttl_hours:
                return self.search_cache[cache_key]['data']
        
        # Use Mistral to generate comprehensive response
        retry_count = 0
        last_error = None
        
        while retry_count < max_retries:
            try:
                prompt = f"""
                Please provide comprehensive and detailed information on the following query: {query}
                
                Structure your response clearly with headings and bullet points.
                Make it detailed, informative, and professional.
                Include specific examples and actionable insights where possible.
                Focus on current industry standards and trends (2024-2025).
                Provide realistic and accurate information based on current market conditions.
                Use markdown formatting for better readability.
                """
                
                result = self.generate_mistral_response(prompt, max_tokens=3500)
                
                if not result.startswith("Error") and not result.startswith("API Error"):
                    # Cache successful result
                    self.search_cache[cache_key] = {
                        'data': result,
                        'timestamp': datetime.now()
                    }
                    time.sleep(1)  # Rate limiting
                    return result
                else:
                    last_error = result
                    retry_count += 1
                    time.sleep(2)
                    
            except Exception as e:
                last_error = str(e)
                retry_count += 1
                time.sleep(2)
        
        return f"Search failed after {max_retries} attempts. Last Error: {last_error}"
    
    def format_search_results(self, results, title):
        """Format search results into a well-structured markdown document"""
        formatted = f"# {title}\n\n"
        if isinstance(results, str) and not results.startswith("Error"):
            formatted += results
        else:
            formatted += "No results available or error occurred."
        return formatted
    
    def get_career_options(self):
        """Return all available career categories and options"""
        return self.fallback_career_options
    
    def comprehensive_career_analysis(self, career_name, user_profile=None):
        """Run comprehensive analysis of a career using Mistral AI"""
        try:
            if career_name in self.career_data:
                return self.career_data[career_name]
            
            # 1. Career Overview and Skills
            overview_query = (
                f"Create a detailed overview of the {career_name} career with the following structure:\n"
                f"1. **Role Overview**: What do {career_name} professionals do? Include main purpose and impact.\n"
                f"2. **Key Responsibilities**: List 8-10 main tasks and responsibilities with specific examples.\n"
                f"3. **Required Technical Skills**: List specific technical skills, tools, and software needed.\n"
                f"4. **Required Soft Skills**: List essential soft skills and interpersonal abilities.\n"
                f"5. **Educational Background**: What degrees, certifications, or qualifications are typically required?\n"
                f"6. **Career Entry Paths**: Describe 3-4 different ways someone can enter this field.\n"
                f"7. **Prerequisites**: What background knowledge or experience is helpful?\n\n"
                f"Provide specific, actionable information with real-world examples."
            )
            
            overview_result = self.search_with_cache(
                overview_query,
                f"{career_name}_overview"
            )
            research = self.format_search_results(overview_result, f"{career_name} Career Analysis")
            
            # 2. Market Analysis
            market_query = (
                f"Analyze the job market for {career_name} professionals with the following structure:\n"
                f"1. **Job Growth Projections**: How is job growth trending? Include specific percentages if available.\n"
                f"2. **Salary Ranges**: What are the salary ranges by experience level (entry: 0-2 years, mid: 3-7 years, senior: 8+ years)?\n"
                f"3. **Top Industries**: Which 5-7 industries hire {career_name} professionals most?\n"
                f"4. **Geographic Hotspots**: Which cities/regions have the most opportunities?\n"
                f"5. **Market Demand**: Is there high demand, competitive market, or oversaturation?\n"
                f"6. **Emerging Trends**: What new trends are affecting this field in 2024-2025?\n"
                f"7. **Job Market Outlook**: What's the 5-10 year outlook for this career?\n"
                f"8. **Competition Level**: How competitive is it to get hired?\n\n"
                f"Include specific data, statistics, and current market conditions where possible."
            )
            
            market_result = self.search_with_cache(
                market_query,
                f"{career_name}_market"
            )
            market_analysis = self.format_search_results(market_result, f"{career_name} Market Analysis")
            
            # 3. Learning Roadmap
            experience_level = "beginner"
            if user_profile:
                exp_years = user_profile.get("experience_years", 0)
                if exp_years >= 10:
                    experience_level = "advanced"
                elif exp_years >= 3:
                    experience_level = "intermediate"
            
            roadmap_query = (
                f"Create a comprehensive learning roadmap for becoming a {career_name} professional at the {experience_level} level:\n"
                f"1. **Core Skills to Develop**: What specific technical and soft skills are essential? Prioritize by importance.\n"
                f"2. **Education Requirements**: Degrees, certificates, bootcamps, or alternative qualifications needed.\n"
                f"3. **Recommended Courses**: Specific online courses, platforms, and training programs with names.\n"
                f"4. **Learning Resources**: Books, websites, YouTube channels, podcasts, and communities.\n"
                f"5. **Practical Experience**: How to gain hands-on experience, internships, and build portfolio.\n"
                f"6. **Certifications**: Industry-recognized certifications to pursue, with difficulty levels.\n"
                f"7. **Timeline**: Realistic timeline for skill acquisition and career transition (months/years).\n"
                f"8. **Milestones**: Key milestones to track progress and validate learning.\n"
                f"9. **Common Pitfalls**: What mistakes to avoid during learning process.\n\n"
                f"Make it actionable with specific recommendations and realistic timeframes."
            )
            
            roadmap_result = self.search_with_cache(
                roadmap_query,
                f"{career_name}_roadmap_{experience_level}"
            )
            learning_roadmap = self.format_search_results(roadmap_result, f"{career_name} Learning Roadmap")
            
            # 4. Industry Insights
            insights_query = (
                f"Provide comprehensive industry insights for {career_name} professionals:\n"
                f"1. **Workplace Culture**: What is the typical work environment and company culture like?\n"
                f"2. **Day-to-Day Activities**: What does a typical workday include? Provide hour-by-hour breakdown.\n"
                f"3. **Career Progression**: What career advancement paths and promotion tracks exist?\n"
                f"4. **Work-Life Balance**: How is work-life balance? Include typical hours and flexibility.\n"
                f"5. **Remote Work**: Are remote work opportunities available? What percentage work remotely?\n"
                f"6. **Industry Trends**: Current and emerging technology trends affecting this role.\n"
                f"7. **Success Strategies**: What tips and strategies help professionals succeed?\n"
                f"8. **Common Challenges**: What obstacles and difficulties do professionals face?\n"
                f"9. **Networking**: How important is networking and professional relationships?\n"
                f"10. **Future Outlook**: How will AI, automation, and technology changes affect this role?\n"
                f"11. **Job Security**: How stable is this career path?\n"
                f"12. **Stress Levels**: What are typical stress levels and pressure points?\n\n"
                f"Provide practical insights and real-world perspectives from industry professionals."
            )
            
            insights_results = self.search_with_cache(
                insights_query,
                f"{career_name}_insights"
            )
            industry_insights = self.format_search_results(insights_results, f"{career_name} Industry Insights")
            
            results = {
                "career_name": career_name,
                "research": research,
                "market_analysis": market_analysis,
                "learning_roadmap": learning_roadmap,
                "industry_insights": industry_insights,
                "timestamp": datetime.now().isoformat()
            }
            
            self.career_data[career_name] = results
            return results
            
        except Exception as e:
            return {
                "career_name": career_name,
                "research": f"Error analyzing career: {str(e)}. Please check your Mistral API key.",
                "market_analysis": "Market analysis not available due to an error.",
                "learning_roadmap": "Learning roadmap not available due to an error.",
                "industry_insights": "Industry insights not available due to an error.",
                "timestamp": datetime.now().isoformat()
            }
    
    def chat_with_assistant(self, question, career_data=None):
        """Engage in conversation with a user about career questions using Mistral"""
        try:
            context = ""
            if career_data and isinstance(career_data, dict):
                career_name = career_data.get("career_name", "the selected career")
                context = f"The user has selected the {career_name} career path."
                
                # Add relevant context based on question type
                question_lower = question.lower()
                
                if any(kw in question_lower for kw in ["skill", "learn", "study", "education", "degree", "course"]):
                    context += f"\n\nCareer Information: {career_data.get('research', '')[:1500]}"
                    context += f"\n\nLearning Roadmap: {career_data.get('learning_roadmap', '')[:1500]}"
                
                if any(kw in question_lower for kw in ["market", "job", "salary", "pay", "demand", "trend", "growth"]):
                    context += f"\n\nMarket Analysis: {career_data.get('market_analysis', '')[:1500]}"
                
                if any(kw in question_lower for kw in ["work", "day", "culture", "balance", "advance", "environment"]):
                    context += f"\n\nIndustry Insights: {career_data.get('industry_insights', '')[:1500]}"
            
            prompt = f"""
            You are a knowledgeable career guidance assistant helping users with their career questions.
            
            Context about the user's selected career:
            {context}
            
            User question: {question}
            
            Instructions:
            - Provide a helpful, informative response that directly addresses the user's question
            - Use the context information provided to give specific, relevant advice
            - Be conversational but professional and concise
            - Format your response with clear headings and bullet points where appropriate
            - Include specific examples and actionable advice when possible
            - If you don't have specific information, provide general career guidance principles
            - Keep the response focused and well-structured
            - Use markdown formatting for better readability
            
            Response:
            """
            
            return self.generate_mistral_response(prompt, max_tokens=2000)
            
        except Exception as e:
            return f"I encountered an error while processing your question: {str(e)}"
    
    # Additional methods for compatibility
    def search_career_information(self, career):
        """Get basic information about a specific career"""
        return self.comprehensive_career_analysis(career).get('research', 'Career information not available')
    
    def analyze_market_trends(self, career):
        """Analyze market trends for a specific career"""
        return self.comprehensive_career_analysis(career).get('market_analysis', 'Market analysis not available')
    
    def get_career_insights(self, career):
        """Get industry insights for a specific career"""
        return self.comprehensive_career_analysis(career).get('industry_insights', 'Industry insights not available')

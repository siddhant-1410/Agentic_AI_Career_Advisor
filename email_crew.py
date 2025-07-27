import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import markdown
from datetime import datetime
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class EmailInput(BaseModel):
    """Input schema for email tool"""
    recipient_email: str = Field(..., description="Email address of the recipient")
    subject: str = Field(..., description="Email subject")
    content: str = Field(..., description="Email content in markdown format")
    sender_name: str = Field(default="AI Career Guidance System", description="Name of sender")

class EmailTool(BaseTool):
    name: str = "send_email"
    description: str = "Sends formatted career guidance reports via email"
    args_schema: Type[BaseModel] = EmailInput

    def _run(self, recipient_email: str, subject: str, content: str, sender_name: str = "AI Career Guidance System") -> str:
        try:
            # Email configuration (using Gmail SMTP as example)
            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            sender_email = os.getenv("SENDER_EMAIL")
            sender_password = os.getenv("SENDER_PASSWORD")  # Use App Password for Gmail
            
            if not sender_email or not sender_password:
                return "Error: Email credentials not configured. Please set SENDER_EMAIL and SENDER_PASSWORD environment variables."
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{sender_name} <{sender_email}>"
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Convert markdown to HTML
            html_content = markdown.markdown(content, extensions=['tables', 'fenced_code'])
            
            # Add some basic styling
            html_styled = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    h1, h2, h3 {{ color: #2c3e50; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 30px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🎯 AI Career Guidance Report</h1>
                    <p>Powered by Mistral AI & CrewAI</p>
                </div>
                <div class="content">
                    {html_content}
                </div>
                <div class="footer">
                    <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p>© 2025 AI Career Guidance System</p>
                </div>
            </body>
            </html>
            """
            
            # Attach HTML content
            html_part = MIMEText(html_styled, 'html')
            msg.attach(html_part)
            
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            return f"✅ Email successfully sent to {recipient_email}"
            
        except Exception as e:
            return f"❌ Failed to send email: {str(e)}"

class CareerEmailCrew:
    def __init__(self):
        """Initialize the email crew for career guidance system"""
        self.email_tool = EmailTool()
        
        # Email Composer Agent
        self.email_composer = Agent(
            role='Career Report Email Composer',
            goal='Create professional and engaging email content for career guidance reports',
            backstory="""You are an expert email writer specializing in career guidance communications. 
            You excel at transforming technical career analysis into clear, actionable, and professionally 
            formatted email content that helps recipients understand their career path.""",
            tools=[self.email_tool],
            verbose=True,
            allow_delegation=False
        )
        
        # Email Sender Agent
        self.email_sender = Agent(
            role='Email Delivery Specialist',
            goal='Ensure career reports are delivered successfully via email',
            backstory="""You are responsible for the technical delivery of career guidance emails. 
            You ensure proper formatting, deliverability, and successful transmission of career reports 
            to help users receive their personalized career insights.""",
            tools=[self.email_tool],
            verbose=True,
            allow_delegation=False
        )

    def create_and_send_career_email(self, career_data, recipient_email, recipient_name=""):
        """Create and send a career analysis email using CrewAI"""
        
        career_name = career_data.get('career_name', 'Selected Career')
        
        # Task 1: Compose the email content
        compose_task = Task(
            description=f"""
            Create a comprehensive and professional email containing career analysis for {career_name}.
            
            Career Data to Include:
            - Career Name: {career_name}
            - Career Overview: {career_data.get('research', '')[:1000]}...
            - Market Analysis: {career_data.get('market_analysis', '')[:1000]}...
            - Learning Roadmap: {career_data.get('learning_roadmap', '')[:1000]}...
            - Industry Insights: {career_data.get('industry_insights', '')[:1000]}...
            
            Requirements:
            - Create an engaging subject line
            - Structure the content with clear sections and headings
            - Use markdown formatting for better readability
            - Include key highlights and actionable insights
            - Keep it professional yet personable
            - Add a personalized greeting for {recipient_name if recipient_name else 'Career Explorer'}
            - Include next steps and recommendations
            
            Format the response as:
            SUBJECT: [Your suggested subject line]
            CONTENT: [Your email content in markdown format]
            """,
            agent=self.email_composer,
            expected_output="Professional email content with subject line and markdown-formatted body"
        )
        
        # Task 2: Send the email
        send_task = Task(
            description=f"""
            Send the composed career guidance email to {recipient_email}.
            
            Use the content created by the email composer and ensure:
            - Proper email formatting and delivery
            - Professional presentation
            - Successful transmission
            
            Recipient: {recipient_email}
            """,
            agent=self.email_sender,
            expected_output="Confirmation of successful email delivery",
            context=[compose_task]
        )
        
        # Create and execute the crew
        career_email_crew = Crew(
            agents=[self.email_composer, self.email_sender],
            tasks=[compose_task, send_task],
            verbose=True
        )
        
        try:
            result = career_email_crew.kickoff()
            return {"success": True, "message": str(result)}
        except Exception as e:
            return {"success": False, "message": f"CrewAI execution failed: {str(e)}"}

    def send_simple_career_summary(self, career_data, recipient_email, recipient_name=""):
        """Send a simplified career summary email"""
        career_name = career_data.get('career_name', 'Selected Career')
        
        # Create simplified content
        subject = f"🎯 Your {career_name} Career Analysis Report"
        
        content = f"""# Your Personalized Career Analysis Report

Hello {recipient_name if recipient_name else 'Career Explorer'}! 👋

Thank you for using our AI Career Guidance System. Here's your comprehensive analysis for the **{career_name}** career path.

## 📊 Career Overview
{career_data.get('research', 'Analysis not available')[:500]}...

## 💼 Market Analysis  
{career_data.get('market_analysis', 'Market data not available')[:500]}...

## 📚 Learning Roadmap
{career_data.get('learning_roadmap', 'Learning path not available')[:500]}...

## 🏢 Industry Insights
{career_data.get('industry_insights', 'Insights not available')[:500]}...

---

## 🚀 Next Steps

1. **Review the detailed analysis** above
2. **Start with the learning roadmap** recommendations
3. **Connect with professionals** in your target industry
4. **Build your skills** based on the identified requirements

Need more guidance? Feel free to return to our platform for additional insights and chat with our AI assistant!

Best regards,  
**AI Career Guidance Team** 🎯

*Powered by Mistral AI & CrewAI*
"""

        try:
            result = self.email_tool._run(
                recipient_email=recipient_email,
                subject=subject,
                content=content,
                sender_name="AI Career Guidance System"
            )
            return {"success": True, "message": result}
        except Exception as e:
            return {"success": False, "message": f"Email sending failed: {str(e)}"}

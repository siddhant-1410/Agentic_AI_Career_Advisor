## Demo Video (The Deployed link provied may not work due to being uploaded on Render's Free Tier so Check out the demo video instead ):




https://github.com/user-attachments/assets/715746a2-590c-4806-9ba8-955beced85e9


# AI Career Guidance System

A sophisticated multi-agent AI system that provides personalized career guidance, analysis, and professional email reporting. This project demonstrates the power of collaborative AI agents working together to deliver comprehensive career counseling services.

## Overview

The application combines the analytical power of Mistral AI with specialized CrewAI agents and RAG-enhanced chatbot capabilities to provide users with personalized career insights, interactive consultations, and professional email reports.

Think of it as having your own personal career counseling team - each specialist focused on what they do best, working together to give you the most comprehensive and up-to-date career guidance possible.

## Why Multi-Agent Architecture?

Traditional single-AI systems try to do everything, but they are like asking one person to be a researcher, writer, and technical specialist all at once. Our multi-agent approach assigns specialized roles:

- **Career Analysis Expert**: Deep research and market analysis
- **Professional Writer**: Crafting polished email reports  
- **Technical Delivery Specialist**: Handling email delivery and formatting
- **Smart Memory Assistant**: Providing current information through RAG

This specialization means each task gets expert-level attention, resulting in higher quality outputs and better user experience.

## Core Features

### Comprehensive Career Analysis
- Career path research and analysis
- Market trends and salary information
- Industry insights and growth projections
- Personalized learning roadmaps
- Dynamic data visualizations

### Interactive AI Chat Assistant
- Real-time career guidance conversations
- RAG-enhanced responses with current market data
- Context-aware conversations that remember your career journey
- Quick action buttons for common questions

### Professional Email Reports
- AI-composed professional career reports
- Two delivery options: Simple summary or detailed CrewAI analysis
- HTML-formatted emails with professional styling
- Personalized content based on recipient information

### Dynamic Visualizations
- Salary progression charts based on career analysis
- Skills importance radar charts
- Industry trend impact scores
- Job market distribution analysis

## Multi-Agent System Architecture

### Primary Intelligence Layer

**Mistral AI Core Agent**
- Role: Master Career Analyst and Chat Assistant
- Responsibilities: Career research, market analysis, conversational support
- Capabilities: Processes complex career queries, generates comprehensive analyses, maintains conversation context

### Specialized Task Layer (CrewAI Agents)

**Email Composer Agent**
- Role: Career Report Email Composer
- Expertise: Professional writing and content structuring
- Function: Transforms technical career analysis into engaging, personalized email content

**Email Delivery Specialist Agent**  
- Role: Email Delivery Specialist
- Expertise: Technical email delivery and formatting
- Function: Handles SMTP protocols, HTML formatting, and delivery confirmation

### Knowledge Enhancement Feature for better experience 

**RAG System Integration**
- Role: Smart Memory Assistant
- Function: Provides access to current career data and remembers user interactions
- Benefits: Always up-to-date information, personalized context, reduced AI hallucination

## Setup:
## Create a virtual environment first:
``` python -m venv ven ```
## Activate the venv 
``` ./venv/Scripts/activate```
## Install the dependicies
``` pip install -r requirements.txt```
## Setup you API Keys in the .env file
## Run the app.py
``` streamlit run app.py```

## Technical Stack

### AI Frameworks and Models
- **Mistral AI**: Large language model for career analysis and chat (`mistral-large-latest`)
- **CrewAI**: Multi-agent orchestration and task management
- **RAG System**: Retrieval-augmented generation for enhanced responses

### Supporting Technologies
- **Streamlit**: Web application framework and user interface
- **Plotly**: Dynamic data visualization and charts
- **Python**: Core programming language
- **SMTP/Email**: Professional email delivery system

### Key Dependencies
LangChain
CrewAI
Streamlit
Mistral Model

## Selection of Models (Why and How I reached these Models?)
Earlier I used OpenAI and Google Gemini models via API through their respective dashboard from thier websites but the problem was they exceeded their quota and hence I decided to go to Mistral Open Source models with a generous limit of 1 billion token on free tier while maintaining the performance characterstics.

## WorkFlow of the Project:
User Query → Mistral AI (Initial Analysis) → SerpAPI (Real-time Search) → 
RAG System (Knowledge Enhancement) → CrewAI (Professional Email) → User

## AI Models and APIs Used

### **Mistral AI (`mistral-large-latest`)**
**What it does:** Core career analysis engine and conversational AI assistant
- Processes complex career queries and generates comprehensive career analyses
- Powers the interactive chat interface with context-aware responses
- Provides market insights, learning roadmaps, and industry analysis
- Maintains conversation history and user context

**Why Mistral AI:**
- **Generous Free Tier:** 1 billion tokens per month with no strict usage quotas
- **High Performance:** Quality comparable to premium models like GPT-4
- **Reliable API:** Consistent performance with good documentation
- **Cost Effective:** Excellent for development and production deployment
- **Strong Reasoning:** Exceptional analytical capabilities for career guidance tasks

### **CrewAI Framework**
**What it does:** Multi-agent orchestration for specialized task execution
- **Email Composer Agent:** Creates professional, personalized career report emails
- **Email Delivery Agent:** Handles technical email formatting and SMTP delivery
- **Task Coordination:** Manages workflow between different AI agents

**Why CrewAI:**
- **Specialized Expertise:** Each agent focuses on what it does best
- **Scalable Architecture:** Easy to add new agents for additional functionality
- **Better Quality:** Task specialization results in higher quality outputs

### **SerpAPI**
**What it does:** Real-time search engine results for current market intelligence
- Provides live job market data and salary information
- Searches for current industry trends and company hiring practices

**Why SerpAPI:**
- **Legal & Compliant:** Official API access without ToS violations
- **Structured Data:** Clean JSON responses instead of messy HTML scraping
- **Multiple Search Engines:** Google, Bing, Yahoo support for comprehensive coverage

### **RAG System Integration**
**What it does:** Knowledge enhancement and retrieval system
- Maintains searchable database of career information and user interactions
- Enhances AI responses with relevant stored knowledge
- Reduces AI hallucination by providing factual context
- Personalizes responses based on user history and preferences

**Why RAG:**
- **Current Information:** Access to up-to-date career data beyond AI training cutoffs
- **Personalization:** Remembers user career journey and preferences
- **Context Awareness:** Provides relevant information for more targeted responses



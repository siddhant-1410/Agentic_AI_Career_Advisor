# AI Career Guidance System

A sophisticated multi-agent AI system that provides personalized career guidance, analysis, and professional email reporting. This project demonstrates the power of collaborative AI agents working together to deliver comprehensive career counseling services.

## Overview

What started as a simple career guidance tool has evolved into a comprehensive multi-agent AI system. The application combines the analytical power of Mistral AI with specialized CrewAI agents and RAG-enhanced chatbot capabilities to provide users with personalized career insights, interactive consultations, and professional email reports.

Think of it as having your own personal career counseling team - each specialist focused on what they do best, working together to give you the most comprehensive and up-to-date career guidance possible.

## Why Multi-Agent Architecture?

Traditional single-AI systems try to do everything, but they're like asking one person to be a researcher, writer, and technical specialist all at once. Our multi-agent approach assigns specialized roles:

- **Career Analysis Expert**: Deep research and market analysis
- **Professional Writer**: Crafting polished email reports  
- **Technical Delivery Specialist**: Handling email delivery and formatting
- **Smart Memory Assistant**: Providing current information through RAG

This specialization means each task gets expert-level attention, resulting in higher quality outputs and better user experience.

## Core Features

### Comprehensive Career Analysis
- In-depth career path research and analysis
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

### Knowledge Enhancement Layer

**RAG System Integration**
- Role: Smart Memory Assistant
- Function: Provides access to current career data and remembers user interactions
- Benefits: Always up-to-date information, personalized context, reduced AI hallucination

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

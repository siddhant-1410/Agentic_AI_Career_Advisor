import streamlit as st
import time
import requests
import json

class CareerChatAssistant:
    def __init__(self, career_system=None):
        """Initialize the career chat assistant with the career guidance system."""
        self.career_system = career_system
        self.mistral_api_key = career_system.mistral_api_key if career_system else None
        self.conversational_history = []
        self.chat_history = []
        
        # Mistral API configuration
        if self.mistral_api_key:
            self.mistral_base_url = "https://api.mistral.ai/v1/chat/completions"
            self.mistral_headers = {
                "Authorization": f"Bearer {self.mistral_api_key}",
                "Content-Type": "application/json"
            }

    def generate_mistral_response(self, prompt, max_tokens=1800):
        """Generate response using Mistral API"""
        if not self.mistral_api_key:
            return "Mistral API key is not available."
        
        payload = {
            "model": "mistral-large-latest",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3
        }
        
        try:
            response = requests.post(
                self.mistral_base_url,
                headers=self.mistral_headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            elif response.status_code == 429:
                time.sleep(3)
                # Retry once
                response = requests.post(
                    self.mistral_base_url,
                    headers=self.mistral_headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                return f"Error: {response.status_code} - {response.text[:200]}"
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def add_to_history(self, role, message):
        """Add a message to the conversational history"""
        self.conversational_history.append({"role": role, "message": message})
        # Keep only last 10 messages to manage context length
        if len(self.conversational_history) > 10:
            self.conversational_history = self.conversational_history[-10:]

    def get_formatted_history(self):
        """Get the conversational history for context"""
        formatted = ""
        for entry in self.conversational_history[-6:]:  # Last 6 messages for context
            formatted += f"{entry['role']}: {entry['message'][:200]}...\n"
        return formatted

    def process_question(self, question, career_data=None):
        """Process a user question about career data using Mistral"""
        self.add_to_history("User", question)
        
        try:
            # Build context from career data
            context = ""
            if career_data:
                career_name = career_data.get("career_name", "the selected career")
                context = f"Career context: {career_name}\n\n"
                
                # Add relevant career data based on question type
                question_lower = question.lower()
                
                if any(kw in question_lower for kw in ["overview", "what", "role", "responsibility", "do"]):
                    context += f"Career Overview:\n{career_data.get('research', '')[:1500]}\n\n"
                
                if any(kw in question_lower for kw in ["market", "salary", "pay", "job", "demand", "trend", "growth", "money"]):
                    context += f"Market Analysis:\n{career_data.get('market_analysis', '')[:1500]}\n\n"
                
                if any(kw in question_lower for kw in ["learn", "skill", "education", "study", "course", "training", "how"]):
                    context += f"Learning Roadmap:\n{career_data.get('learning_roadmap', '')[:1500]}\n\n"
                
                if any(kw in question_lower for kw in ["culture", "work", "day", "balance", "environment", "life", "stress"]):
                    context += f"Industry Insights:\n{career_data.get('industry_insights', '')[:1500]}\n\n"
            
            # Get conversation history for context
            history_context = self.get_formatted_history()
            
            prompt = f"""
You are an AI Career Chat Assistant providing personalized career guidance.

Career Information Context:
{context}

Recent Conversation History:
{history_context}

Current User Question: {question}

Instructions:
- Provide a helpful, structured response based on the career information provided
- Use bullet points and clear headings to organize information
- Be conversational but professional
- Reference specific information from the career data when relevant
- If the question is outside the provided context, give general career advice
- Keep responses concise but informative (aim for 200-400 words)
- Format the response for easy reading with markdown
- Include specific examples when possible
- If asked about numbers/data, provide realistic estimates based on the context

Response:
"""
            
            response = self.generate_mistral_response(prompt)
            self.add_to_history("Career Assistant", response)
            return response
            
        except Exception as e:
            error_response = f"I encountered an error while processing your question: {str(e)}"
            self.add_to_history("Career Assistant", error_response)
            return error_response

def display_chat_interface(career_data=None, career_system=None):
    """Display a chat interface in the Streamlit app"""
    st.markdown("### 💬 Chat with AI Career Assistant")
    
    # Initialize chat assistant
    if 'chat_assistant' not in st.session_state:
        st.session_state.chat_assistant = CareerChatAssistant(career_system)
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
   
    if not st.session_state.chat_messages:
        if career_data:
            career_name = career_data.get('career_name', 'your selected career')
            welcome_msg = f"""👋 Hello! I'm your AI Career Assistant powered by Mistral AI.

I'm here to help you with questions about **{career_name}** or career guidance in general!

**What I can help you with:**
- 🎯 Career requirements and skills
- 💰 Salary information and market trends
- 📚 Learning paths and resources
- 🏢 Industry insights and work culture
- 🚀 Career progression strategies

Feel free to ask me anything!"""
        else:
            welcome_msg = "Hello! I'm your AI Career Assistant powered by Mistral AI. How can I help you with your career questions today?"
        
        st.session_state.chat_messages.append({"role": "assistant", "content": welcome_msg})
    
  
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.chat_messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about your career...", key="career_chat_input"):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        
       
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = st.session_state.chat_assistant.process_question(prompt, career_data)
            
           
            response_placeholder = st.empty()
            response_placeholder.markdown(response)
        
       
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        
        if len(st.session_state.chat_messages) > 20:
            st.session_state.chat_messages = st.session_state.chat_messages[-20:]
    
   
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🗑️ Clear Chat", type="secondary", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.chat_assistant = CareerChatAssistant(career_system)
            st.rerun()
    
    with col2:
        if st.button("📊 View Analysis", type="secondary", use_container_width=True):
            if 'current_step' in st.session_state:
                st.session_state.current_step = 'analysis'
                st.rerun()
    
    with col3:
        if st.button("🎯 New Career", type="secondary", use_container_width=True):
            if 'current_step' in st.session_state:
                st.session_state.current_step = 'career_selection'
                st.rerun()
    
    with st.expander("💡 Chat Tips & Example Questions"):
        st.markdown("""
        **💬 How to get the best responses:**
        - Be specific in your questions
        - Ask one topic at a time for detailed answers
        - Use follow-up questions to dive deeper

        **🎯 Example questions you can ask:**

        **About Skills & Learning:**
        - "What programming languages should I learn for data science?"
        - "How long does it take to become proficient in UX design?"
        - "What certifications are most valuable for cybersecurity?"

        **About Career & Market:**
        - "What's the salary range for entry-level software engineers?"
        - "Which cities have the best job opportunities for my field?"
        - "How competitive is the job market for data scientists?"

        **About Work Life:**
        - "What does a typical day look like for a product manager?"
        - "How is the work-life balance in consulting?"
        - "What are the biggest challenges in this career?"

        **About Career Growth:**
        - "What are the career advancement opportunities?"
        - "How can I transition from marketing to data science?"
        - "What skills should I focus on for promotion?"
        """)
    
    # Display current career context
    if career_data:
        st.sidebar.markdown("### 🎯 Current Career Focus")
        st.sidebar.info(f"**{career_data.get('career_name', 'Unknown Career')}**")
        
        # Quick action buttons in sidebar
        st.sidebar.markdown("### ⚡ Quick Actions")
        
        if st.sidebar.button("💰 Ask about Salary", use_container_width=True):
            salary_question = f"What is the salary range for {career_data.get('career_name', 'this career')}?"
            st.session_state.chat_messages.append({"role": "user", "content": salary_question})
            response = st.session_state.chat_assistant.process_question(salary_question, career_data)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.sidebar.button("📚 Ask about Learning", use_container_width=True):
            learning_question = f"How can I learn the skills needed for {career_data.get('career_name', 'this career')}?"
            st.session_state.chat_messages.append({"role": "user", "content": learning_question})
            response = st.session_state.chat_assistant.process_question(learning_question, career_data)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.sidebar.button("🏢 Ask about Work Culture", use_container_width=True):
            culture_question = f"What is the work culture like for {career_data.get('career_name', 'this career')}?"
            st.session_state.chat_messages.append({"role": "user", "content": culture_question})
            response = st.session_state.chat_assistant.process_question(culture_question, career_data)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        # Email report button
        if st.sidebar.button("📧 Email Report", use_container_width=True):
            st.session_state.show_email_interface = True
            st.rerun()

    
    if hasattr(st.session_state, 'show_email_interface') and st.session_state.show_email_interface:
        st.markdown("---")
        from email_crew import CareerEmailCrew
        
       
        if 'email_crew' not in st.session_state:
            st.session_state.email_crew = CareerEmailCrew()
        
        
        st.markdown("### 📧 Email Career Report")
        
        with st.form("chat_email_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                recipient_email = st.text_input(
                    "📧 Recipient Email *",
                    placeholder="example@email.com"
                )
            
            with col2:
                recipient_name = st.text_input(
                    "👤 Recipient Name (Optional)",
                    placeholder="John Doe"
                )
            
            email_type = st.selectbox(
                "📄 Email Type",
                ["Simple Summary", "Detailed Analysis with CrewAI"]
            )
            
            send_email_btn = st.form_submit_button("🚀 Send Email Report", use_container_width=True)
            
            if send_email_btn:
                if not recipient_email:
                    st.error("❌ Please enter a recipient email address.")
                elif not recipient_email or '@' not in recipient_email:
                    st.error("❌ Please enter a valid email address.")
                else:
                    with st.spinner("📨 Sending your career report..."):
                        try:
                            if email_type == "Simple Summary":
                                result = st.session_state.email_crew.send_simple_career_summary(
                                    career_data, recipient_email, recipient_name
                                )
                            else:
                                result = st.session_state.email_crew.create_and_send_career_email(
                                    career_data, recipient_email, recipient_name
                                )
                            
                            if result["success"]:
                                st.success(f"✅ {result['message']}")
                                st.balloons()
                            else:
                                st.error(f"❌ {result['message']}")
                                
                        except Exception as e:
                            st.error(f"❌ Unexpected error: {str(e)}")
        
        if st.button("❌ Close Email Interface"):
            st.session_state.show_email_interface = False
            st.rerun()
    
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models import SessionLocal, ChatSession, Message, CandidateProfile
from groq import Groq
import uuid
import json
import os
import re
import random
from sqlalchemy.orm.attributes import flag_modified
from config import config, feature_flags

# High-level question bank for different roles and experience levels
QUESTION_BANK = {
    "AI/ML": {
        "junior": [
            "Can you explain the difference between supervised and unsupervised learning with real-world examples?",
            "How would you handle overfitting in a machine learning model?",
            "Describe a time when you had to choose between different algorithms for a project.",
        ],
        "mid": [
            "How would you design an end-to-end ML pipeline for a recommendation system?",
            "Explain how you would approach model deployment and monitoring in production.",
            "What strategies would you use to handle data drift in a live ML system?",
        ],
        "senior": [
            "How would you architect a scalable ML platform for a company with 100M+ users?",
            "Describe your approach to building responsible AI systems and handling bias.",
            "How would you lead a team through the transition from traditional analytics to ML-driven insights?",
        ]
    },
    "Software Development": {
        "junior": [
            "Explain the difference between SQL and NoSQL databases with examples of when to use each.",
            "How do you approach debugging a piece of code that's not working as expected?",
            "Describe a challenging bug you've encountered and how you resolved it.",
        ],
        "mid": [
            "How would you design a system to handle 1 million concurrent users?",
            "Explain your approach to code reviews and maintaining code quality.",
            "Describe how you would implement caching in a distributed system.",
        ],
        "senior": [
            "How would you migrate a monolithic application to microservices architecture?",
            "Describe your strategy for technical debt management across multiple teams.",
            "How do you balance technical excellence with business requirements in your decisions?",
        ]
    },
    "Data Science": {
        "junior": [
            "You mentioned working with employee performance prediction - can you walk me through your approach to handling missing data in such datasets?",
            "Tell me about a time when you had to explain a complex data finding to a non-technical stakeholder. How did you make it understandable?",
            "If you had a dataset with 80% accuracy on training but only 60% on validation, what would be your first three steps to investigate?",
            "Describe your process for exploring a new dataset you've never seen before. What are the first things you look for?",
        ],
        "mid": [
            "How would you approach building an employee performance prediction model if you suspected there was bias in the historical data?",
            "You have conflicting results from two different models for the same problem. How would you decide which one to trust and deploy?",
            "Walk me through how you would design an A/B test to measure the impact of a new recommendation algorithm.",
            "If stakeholders asked you to improve model accuracy from 85% to 95%, how would you approach this challenge?",
        ],
        "senior": [
            "How would you build a data science strategy for a company that's transitioning from intuition-based to data-driven decision making?",
            "You're tasked with building a real-time fraud detection system for millions of transactions. What's your architectural approach?",
            "How do you balance the trade-off between model interpretability and performance when stakeholders demand both?",
            "Describe how you would establish data governance and quality standards across multiple teams and departments.",
        ]
    },
    "Default": {
        "junior": [
            "Tell me about a challenging project you've worked on and how you overcame obstacles.",
            "How do you stay updated with the latest trends in your field?",
            "Describe a time when you had to learn a new technology quickly.",
        ],
        "mid": [
            "How do you approach mentoring junior team members?",
            "Describe a situation where you had to make a technical decision with incomplete information.",
            "How do you balance innovation with maintaining existing systems?",
        ],
        "senior": [
            "How do you align technical strategy with business objectives?",
            "Describe your approach to building and scaling high-performing teams.",
            "How do you handle technical disagreements within your team?",
        ]
    }
}

def extract_experience_years(text: str) -> float:
    """Extract numeric years from experience text using AI logic"""
    text = text.lower().strip()
    
    # Direct patterns
    import re
    
    # Pattern: "5 years", "2.5 years", "3"
    year_patterns = [
        r'(\d+\.?\d*)\s*(?:years?|yrs?)',
        r'^(\d+\.?\d*)$',  # Just a number
        r'(\d+\.?\d*)\s*(?:year|yr)\s*(?:of\s*)?(?:experience)?'
    ]
    
    for pattern in year_patterns:
        match = re.search(pattern, text)
        if match:
            return float(match.group(1))
    
    # Keyword mapping
    keyword_map = {
        'fresher': 0, 'fresh': 0, 'beginner': 0, 'entry': 0,
        'junior': 1, 'recent': 0.5,
        'experienced': 5, 'senior': 7, 'lead': 8, 'principal': 10
    }
    
    for keyword, years in keyword_map.items():
        if keyword in text:
            return years
    
    return 0

def determine_competency_level(experience_years: float) -> str:
    """Determine competency level based on experience"""
    if experience_years <= 2:
        return "junior"
    elif experience_years <= 5:
        return "mid" 
    else:
        return "senior"

def categorize_position(position: str) -> str:
    """Categorize position into question bank categories"""
    position = position.lower()
    
    ai_ml_keywords = ['ai', 'ml', 'machine learning', 'artificial intelligence', 'data scientist', 'aiml']
    dev_keywords = ['developer', 'engineer', 'programmer', 'backend', 'frontend', 'fullstack', 'software']
    data_keywords = ['data', 'analyst', 'analytics', 'bi', 'business intelligence']
    
    if any(keyword in position for keyword in ai_ml_keywords):
        return "AI/ML"
    elif any(keyword in position for keyword in dev_keywords):
        return "Software Development"
    elif any(keyword in position for keyword in data_keywords):
        return "Data Science"
    else:
        return "Default"

def get_intelligent_question(position: str, experience_years: float) -> str:
    """Get a high-level question based on position and experience"""
    category = categorize_position(position)
    level = determine_competency_level(experience_years)
    
    questions = QUESTION_BANK.get(category, QUESTION_BANK["Default"]).get(level, QUESTION_BANK["Default"]["junior"])
    return random.choice(questions)

def extract_skills_from_text(text: str) -> list:
    """Extract technical skills from text using AI logic"""
    # Common tech skills database
    tech_skills = [
        'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb', 'postgresql',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'docker', 'kubernetes',
        'aws', 'azure', 'gcp', 'git', 'linux', 'machine learning', 'deep learning',
        'data analysis', 'statistics', 'r', 'scala', 'spark', 'hadoop', 'tableau'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in tech_skills:
        if skill in text_lower:
            found_skills.append(skill)
    
    return found_skills

app = FastAPI(
    title="Priyam AI Hiring Assistant API",
    description="Backend API for the Priyam AI Hiring Assistant chatbot with advanced features",
    version="2.0.0",
    debug=config.DEBUG
)

# Enable CORS for local development and same-origin serving
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to TalentScout AI Hiring Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "/": "API Information (this page)",
            "/chat": "POST - Chat with the AI assistant. Requires: {session_id?: string, user_input: string}",
            "/sessions/{session_id}": "GET - Retrieve chat session history by session ID",
            "/docs": "GET - Interactive API documentation and testing interface",
            "/redoc": "API Documentation (ReDoc)"
        },
        "status": "running",
        "model": "TinyLlama-1.1B-Chat-v1.0-GGUF",
        "database": "PostgreSQL"
    }

@app.get("/docs", response_class=HTMLResponse)
def get_api_docs():
    """Serve the interactive API documentation"""
    try:
        with open("api_docs.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse("""
        <html>
        <head><title>API Docs Not Found</title></head>
        <body>
        <h1>API Documentation Not Available</h1>
        <p>The interactive API documentation file (api_docs.html) was not found.</p>
        <p>Please ensure the file exists in the same directory as the API server.</p>
        </body>
        </html>
        """, status_code=404)

@app.on_event("startup")
def startup_event():
    from models import engine, Base
    Base.metadata.create_all(bind=engine)

@app.get("/ui", response_class=HTMLResponse)
def serve_ui():
    """Serve the professional UI HTML to avoid CORS issues."""
    ui_path = os.path.join(os.getcwd(), "professional_ui.html")
    if os.path.exists(ui_path):
        return FileResponse(ui_path, media_type="text/html")
    return HTMLResponse("<h1>UI file not found</h1>", status_code=404)

# Initialize Groq client with API key from environment
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_natural_response(prompt: str, max_tokens: int = 100, fallback: str = None) -> str:
    """Generate natural conversational response using Groq LLM"""
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Fast, reliable, FREE (updated model)
            messages=[
                {
                    "role": "system",
                    "content": "You are TalentScout, a professional AI hiring assistant. Your job is to ASK questions, not answer them. Keep responses brief (1-2 sentences), natural, and engaging. Always ASK the candidate questions - never provide answers or solutions. Be warm and encouraging while gathering information."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=1,
            stream=False
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] Groq API failed: {e}")
        # Use provided fallback or generic message
        return fallback if fallback else "I'm here to help! Let's continue."

class ChatRequest(BaseModel):
    session_id: str | None = None
    user_input: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    user_details: dict | None = None

def extract_name(text: str) -> str:
    """Extract actual name from sentences like 'My name is Om Choksi' or 'I am Om Choksi'"""
    text = text.strip()
    text_lower = text.lower()

    # Common patterns to remove (case-insensitive)
    patterns = [
        "my name is ", "my name's ", "my name: ", "my name - ",
        "i am ", "i'm ", "im ", "i m ",
        "this is ", "it's ", "its ",
        "call me ", "you can call me ",
        "name is ", "name: ", "name - ",
        "i'm called ", "im called "
    ]

    for pattern in patterns:
        if text_lower.startswith(pattern):
            # Preserve original case by using the same offset
            text = text[len(pattern):].strip()
            break

    # Also check for patterns anywhere in the sentence
    for pattern in ["is my name", "my name"]:
        if pattern in text_lower:
            # Extract everything BEFORE "is my name" or after "my name is"
            idx = text_lower.find(pattern)
            if idx > 0:
                text = text[:idx].strip()
                break

    return text

# REMOVED: LLM-based response generation replaced with rule-based state machine below

def is_valid_name(text: str) -> bool:
    """Check if text looks like a real name (not greetings or single words)"""
    # First extract the actual name
    name = extract_name(text)
    name_lower = name.lower()
    
    greetings = ["hi", "hii", "hello", "hey", "hiii", "hiiii", "helo", "yo", "sup", "wassup", "helo"]
    confirmation_words = ["yes", "yess", "yesss", "yeah", "yep", "yepp", "nope", "no", "nah"]
    
    # If it's just a greeting or confirmation word, not a name
    if name_lower in greetings or name_lower in confirmation_words:
        return False
    
    # If it has at least 2 words (first name + last name), likely valid
    words = name.split()
    if len(words) >= 2:
        return True
    
    # Single word name validation
    if len(words) == 1:
        # If it's a longer name (6+ chars) and contains only letters, likely a valid single name
        if len(name) >= 6 and name.isalpha():
            return True  # Valid single name (like "Sanskruti", "Alexander", etc.)
        # Shorter single names need confirmation
        elif len(name) >= 3:
            return None  # Ambiguous - ask for confirmation
    
    return False

def is_valid_experience(text: str) -> bool:
    """Check if text contains years/numbers for experience"""
    text = text.lower().strip()
    
    # Empty or too long
    if not text or len(text) > 50:
        return False
    
    # Direct number patterns (like "5", "10", "2.5")
    if any(char.isdigit() for char in text):
        return True
    
    # Experience keywords
    experience_keywords = ["year", "yr", "month", "experience", "fresher", "fresh", "beginner", "entry"]
    if any(keyword in text for keyword in experience_keywords):
        return True
    
    return False

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    db = SessionLocal()
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Expire all cached objects to force fresh database read
        db.expire_all()
        
        # Get or create session  
        session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if not session:
            session = ChatSession(session_id=session_id, user_details={})
            db.add(session)
            db.commit()
        
        # Ensure we have the latest committed state from database
        db.refresh(session)
        
        # Get all messages for this session
        messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()
        
        # Determine conversation state
        user_details = session.user_details or {}
        message_count = len(messages)
        
        user_input = request.user_input.strip()
        
        # Debug logging (remove in production)
        print(f"[DEBUG] Session: {session_id}")
        print(f"[DEBUG] Input: '{user_input}'")
        print(f"[DEBUG] Current State: {user_details}")
        print(f"[DEBUG] Message count: {message_count}")
        print(f"[DEBUG] Has name: {bool(user_details.get('name'))}")
        print(f"[DEBUG] Has experience: {bool(user_details.get('experience'))}")
        print(f"[DEBUG] Has position: {bool(user_details.get('position'))}")
        print(f"[DEBUG] Has tech_stack: {bool(user_details.get('tech_stack'))}")
        
        # STATE MACHINE WITH VALIDATION
        if not user_details.get("name"):
            print(f"[DEBUG] STATE: Asking for name")
            # STATE: Asking for name
            # STATE: Asking for name
            if message_count == 0:
                # First interaction - greet and ask for name
                response = "Hello! 👋 I'm TalentScout, your AI hiring assistant. To get started, could you please tell me your full name?"
            else:
                # Validate the name
                name_valid = is_valid_name(user_input)
                extracted_name = extract_name(user_input)
                
                if name_valid == False:
                    # It's a greeting or invalid - use LLM for natural rejection
                    prompt = f"User said '{user_input}' when asked for their name, but that's not a valid name (it's a greeting or invalid). Politely tell them you need their actual full name to proceed."
                    fallback = f"Hi! I need your actual name to continue. Could you please tell me your full name?"
                    response = generate_natural_response(prompt, fallback=fallback)
                elif name_valid == None:
                    # Ambiguous single word - ask for confirmation
                    response = f"Is '{extracted_name}' your full name? If yes, please type 'yes'. Otherwise, please provide your full name (first and last name)."
                    user_details["temp_name"] = extracted_name  # Store extracted name
                else:
                    # Valid full name - store it and use LLM for natural greeting
                    user_details["name"] = extracted_name
                    prompt = f"User's name is {extracted_name}. Greet them warmly and ask how many years of professional experience they have."
                    fallback = f"Nice to meet you, {extracted_name}! 😊 How many years of professional experience do you have?"
                    response = generate_natural_response(prompt, fallback=fallback)
        
        elif not user_details.get("experience"):
            print(f"[DEBUG] STATE: Asking for experience")
            # STATE: Asking for experience OR confirming name
            user_input_clean = user_input.lower().strip()
            
            # Smart confirmation detection (handles typos like "yess", "yesss", "yepp")
            confirmation_keywords = ["yes", "yeah", "yep", "correct", "right", "sure", "ok", "okay"]
            is_confirming = any(
                user_input_clean == keyword or 
                user_input_clean.startswith(keyword) and len(user_input_clean) - len(keyword) <= 2
                for keyword in confirmation_keywords
            )
            
            if user_details.get("temp_name"):
                # We're waiting for name confirmation first
                if is_confirming:
                    # User confirmed the single-word name
                    user_details["name"] = user_details.pop("temp_name")
                    prompt = f"User confirmed their name is {user_details['name']}. Greet them and ask about their professional experience."
                    fallback = f"Great! Nice to meet you, {user_details['name']}! 😊 How many years of professional experience do you have?"
                    response = generate_natural_response(prompt, fallback=fallback)
                else:
                    # User provided a different full name
                    extracted_name = extract_name(user_input)
                    name_check = is_valid_name(extracted_name)
                    
                    if name_check == True or name_check == None:
                        # Accept it as the name
                        user_details["name"] = extracted_name
                        user_details.pop("temp_name")
                        prompt = f"User's name is {extracted_name}. Greet them warmly and ask about their years of experience."
                        fallback = f"Perfect! Nice to meet you, {extracted_name}! 😊 How many years of professional experience do you have?"
                        response = generate_natural_response(prompt, fallback=fallback)
                    else:
                        # Still unclear, ask again
                        response = f"Please type 'yes' to confirm '{user_details['temp_name']}' is your name, or provide your full name (first and last name)."
            elif is_valid_experience(user_input):
                print(f"[DEBUG] Valid experience detected: '{user_input}'")
                # Valid experience - store and move on with natural response
                user_details["experience"] = user_input
                print(f"[DEBUG] Experience saved: {user_details['experience']}")
                prompt = f"User has {user_input} of experience. Acknowledge this and ask what position/role they're interested in."
                fallback = f"Got it, {user_input} of experience! What position or role are you interested in?"
                response = generate_natural_response(prompt, fallback=fallback)
            else:
                print(f"[DEBUG] Invalid experience: '{user_input}', is_valid_experience returned: {is_valid_experience(user_input)}")
                # Invalid/unclear experience - ask again with natural response
                prompt = f"User said '{user_input}' when asked for experience, which isn't clear. Ask for their years of experience with examples like '3 years', '5 years', or 'fresher'."
                fallback = "I need to know your years of experience. For example: '3 years', '5 years', or 'fresher' if you're just starting. How many years of professional experience do you have?"
                response = generate_natural_response(prompt, fallback=fallback)
        
        elif not user_details.get("position"):
            print(f"[DEBUG] STATE: Asking for position")
            # STATE: Asking for position
            user_details["position"] = user_input
            prompt = f"User is interested in the {user_input} position/role. Acknowledge this enthusiastically and ask what technologies or programming languages they're proficient in."
            fallback = f"Excellent! {user_input} is a great choice! 🚀 What technologies or programming languages are you proficient in?"
            response = generate_natural_response(prompt, fallback=fallback)
        
        elif not user_details.get("tech_stack"):
            # STATE: Asking for tech stack
            user_details["tech_stack"] = user_input
            
            # Extract intelligent insights
            experience_years = extract_experience_years(user_details.get("experience", "0"))
            position = user_details.get("position", "")
            skills = extract_skills_from_text(user_input)
            
            # Get intelligent question based on role and experience
            intelligent_question = get_intelligent_question(position, experience_years)
            
            prompt = f"User provided tech stack: {user_input}. You are a hiring assistant interviewing a candidate. ASK them this question (do not provide any answers or explanations): {intelligent_question}"
            fallback = f"Great tech stack! 💻 Here's a question for you: {intelligent_question}"
            
            # Store extracted insights in user_details for later analysis
            user_details["extracted_skills"] = skills
            user_details["competency_level"] = determine_competency_level(experience_years)
            user_details["intelligent_question"] = intelligent_question
            
            response = generate_natural_response(prompt, max_tokens=150, fallback=fallback)
        
        elif not user_details.get("questions_asked"):
            # STATE: Technical question answered
            user_input_lower = user_input.lower().strip()
            
            # Check if candidate doesn't know the answer
            dont_know_phrases = [
                "i don't know", "don't know", "not sure", "no idea", "i'm not sure",
                "can you tell me", "what is", "i dont know", "dont know", "idk"
            ]
            
            is_dont_know = any(phrase in user_input_lower for phrase in dont_know_phrases)
            
            if is_dont_know:
                # Handle "I don't know" responses with encouragement and completion
                user_details["questions_asked"] = True
                user_details["technical_answer"] = user_input
                
                prompt = f"Candidate said '{user_input}' when asked a technical question. Be encouraging and supportive. Thank them for their honesty, mention that learning is a continuous process, and tell them the recruitment team will be in touch."
                fallback = f"Thank you for your honesty! 😊 Learning is a continuous journey, and your willingness to admit when you don't know something shows great character. Our recruitment team will be in touch to discuss next steps and potential learning opportunities."
                response = generate_natural_response(prompt, fallback=fallback)
            else:
                # Regular technical answer
                user_details["questions_asked"] = True
                user_details["technical_answer"] = user_input
                
                prompt = f"User answered the technical question with: '{user_input}'. Thank them warmly, compliment their knowledge, and tell them the recruitment team will be in touch soon."
                fallback = f"Thank you for sharing that! Your technical knowledge is impressive. 🌟 Our recruitment team will review your details and get in touch with you soon. Have a great day!"
                response = generate_natural_response(prompt, fallback=fallback)
            
            # Save complete candidate profile with AI analysis
            try:
                # Extract all intelligent insights
                experience_years = extract_experience_years(user_details.get("experience", "0"))
                skills = user_details.get("extracted_skills", [])
                
                # Create AI assessment
                ai_assessment = {
                    "experience_numeric": experience_years,
                    "competency_level": user_details.get("competency_level", "junior"),
                    "technical_skills": skills,
                    "position_category": categorize_position(user_details.get("position", "")),
                    "question_asked": user_details.get("intelligent_question", ""),
                    "response_quality": "pending_review"  # Could be enhanced with AI analysis
                }
                
                # Save to CandidateProfile table
                candidate_profile = CandidateProfile(
                    session_id=session_id,
                    name=user_details.get("name", ""),
                    experience_years=experience_years,
                    experience_raw=user_details.get("experience", ""),
                    position=user_details.get("position", ""),
                    tech_stack=user_details.get("tech_stack", "").split(",") if user_details.get("tech_stack") else [],
                    skills_extracted=skills,
                    competency_level=user_details.get("competency_level", "junior"),
                    technical_answer=user_input,
                    ai_assessment=ai_assessment
                )
                db.add(candidate_profile)
                print(f"[DEBUG] Candidate profile created and saved")
                
            except Exception as e:
                print(f"[ERROR] Failed to save candidate profile: {e}")
            
            prompt = f"User answered the technical question with: '{user_input}'. Thank them warmly, compliment their profile, and tell them the recruitment team will be in touch soon."
            fallback = f"Thank you for sharing that! Your profile looks impressive. 🌟 Our recruitment team will review your details and get in touch with you soon. Have a great day!"
            response = generate_natural_response(prompt, fallback=fallback)
        
        else:
            # STATE: Conversation complete
            prompt = "The interview is complete. Thank the user again and let them know we'll be in touch. Be warm and professional."
            fallback = "Thanks for your time today! We'll be in touch soon. Have a wonderful day! 😊"
            response = generate_natural_response(prompt, fallback=fallback)
        
        # Save messages with error handling
        try:
            user_msg = Message(session_id=session_id, role="user", content=request.user_input)
            ai_msg = Message(session_id=session_id, role="assistant", content=response)
            db.add(user_msg)
            db.add(ai_msg)
            print(f"[DEBUG] Messages added to database")
        except Exception as e:
            print(f"[ERROR] Failed to save messages: {e}")
        
        print(f"[DEBUG] Before DB save - user_details: {user_details}")
        # Fix for SQLAlchemy JSON field: Force change detection
        session.user_details = user_details
        flag_modified(session, "user_details")  # Tell SQLAlchemy the JSON field has changed
        
        try:
            db.commit()
            print(f"[DEBUG] Database commit successful")
        except Exception as e:
            print(f"[ERROR] Database commit failed: {e}")
            db.rollback()
        
        # Refresh to verify the save worked
        db.refresh(session)
        print(f"[DEBUG] After DB save - session.user_details: {session.user_details}")
        
        return ChatResponse(session_id=session_id, response=response, user_details=user_details)
    finally:
        db.close()

@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    db = SessionLocal()
    try:
        session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        messages = db.query(Message).filter(Message.session_id == session_id).all()
        return {"session": session, "messages": messages}
    finally:
        db.close()

@app.get("/candidates")
def get_all_candidates():
    """Get all candidate profiles with AI analysis"""
    db = SessionLocal()
    try:
        candidates = db.query(CandidateProfile).order_by(CandidateProfile.created_at.desc()).all()
        return {"candidates": candidates, "count": len(candidates)}
    finally:
        db.close()

@app.get("/candidates/{session_id}")
def get_candidate_profile(session_id: str):
    """Get specific candidate profile by session ID"""
    db = SessionLocal()
    try:
        candidate = db.query(CandidateProfile).filter(CandidateProfile.session_id == session_id).first()
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate profile not found")
        
        # Also get chat messages for context
        messages = db.query(Message).filter(Message.session_id == session_id).all()
        
        return {
            "candidate": candidate,
            "messages": messages,
            "ai_insights": {
                "competency_level": candidate.competency_level,
                "extracted_skills": candidate.skills_extracted,
                "ai_assessment": candidate.ai_assessment
            }
        }
    finally:
        db.close()
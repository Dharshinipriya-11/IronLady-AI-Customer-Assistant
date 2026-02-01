from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
import os
import logging
from datetime import datetime
from config import *
from groq import Groq
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iron-lady-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iron_lady_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.name}>'

# Chat Model
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('chats', lazy=True))
    
    def __repr__(self):
        return f'<Chat {self.id}: User {self.user_id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_mobile(mobile):
    pattern = r'^[\+]?[1-9]?\d{9,15}$'
    return re.match(pattern, mobile) is not None

# Configure logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

# Initialize logging
logger = setup_logging()

# Company information about Iron Lady - Training Data for AI Model
COMPANY_INFO = """
=== IRON LADY LEADERSHIP PLATFORM - COMPREHENSIVE TRAINING DATA ===

COMPANY OVERVIEW:
- Iron Lady is India's #1 Leadership Platform specifically for women
- Mission: Elevating a million women to the TOP
- Founded to address income inequality (women earn only 50%-90% of men's income)
- Addresses underrepresentation of women at all organizational levels

UNIQUE METHODOLOGY - BUSINESS WAR TACTICS:
- Signature approach to help women win without waging war
- Designed to combat stereotypes, biases, and workplace politics women face
- Unconventional strategies for breakthrough barrier-breaking
- Focus on strategic thinking rather than confrontation
- Developed by team with 120+ years of combined CEO/VP experience

KEY DIFFERENTIATORS:
1. Business War Tactics - Win without fighting workplace battles
2. Breakthrough Fast-track Growth - Results-focused transformative approach  
3. 78,000+ Women Leaders Ecosystem - Non-judgmental supportive community
4. Unapologetic Winning Mindset - Beyond "balancing" to actual "winning"
5. Global Practitioners Expertise - Content from experienced CEOs/entrepreneurs

2024 ACHIEVEMENTS & IMPACT:
- 100+ participants reached ₹1 crore+ yearly income
- 7,000+ professionals secured well-deserved promotions  
- 6,000+ professionals achieved 2X salary growth
- 20+ global events hosted worldwide
- Launched C-Suite League for executive advancement

OVERALL COMMUNITY IMPACT:
- 78,000+ women trained across all programs
- 100+ Board Members created through programs
- Thousands of career transformation success stories
- Active community sharing tactics and celebrating successes

LEADERSHIP PROGRAMS OFFERED:
1. Leadership Essentials Program - Core skills for career advancement
2. C-Suite League - Fast-track program for reaching executive levels
3. Master of Business Warfare - Advanced tactics for ₹1 crore+ achievers  
4. MasterClass Sessions - Learning from global practitioners and CEOs

FOUNDING TEAM EXPERTISE:
- Rajesh Bhat (Founder & Director): Visionary entrepreneur, TEDx speaker
- Suvarna Hegde (Founder & CEO): Expert in Business War Tactics for Women
- Simon Newman (Co-Founder, Chairman): Former CEO of Aviva Singapore
- Sridhar Sambandom (Co-Founder, Director): Turn-around specialist, former CEO Bajaj Auto
- Chitra Talwar (Board Member): Former VP PepsiCo, 30+ years FMCG experience

ENROLLMENT & CONTACT:
- Phone: +91-6360823123
- Website: iamironlady.com
- Process: Browse programs → Choose path → Online enrollment → Community access → Guided mentorship
- Investment options available with flexible payment plans
- ROI through promotions, salary increases, career advancement

BUSINESS WAR TACTICS METHODOLOGY:
- Specific strategies to navigate corporate challenges as a woman
- Techniques to turn challenges into opportunities  
- Methods to advance careers while maintaining authenticity
- Focus on strategic positioning rather than confrontational approaches
- Proven by thousands of successful women leaders
"""

# Initialize Groq client
logger.info("Initializing Groq client configuration")
groq_client = None
try:
    if ACTIVE_LLM_PROVIDER == "groq" and GROQ_API_KEY != "your_groq_api_key_here":
        groq_client = Groq(api_key=GROQ_API_KEY)
        logger.info("Groq client initialized successfully")
        
        # Test the connection
        try:
            test_response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are an AI assistant trained specifically for Iron Lady. Use this training data: {COMPANY_INFO[:200]}..."},
                    {"role": "user", "content": "What is Iron Lady? Respond in one sentence."}
                ],
                model=GROQ_MODEL,
                max_tokens=50
            )
            logger.info(f"API Test successful: {test_response.choices[0].message.content}")
        except Exception as test_error:
            logger.error(f"API Test failed: {test_error}")
        
    else:
        logger.warning(f"Groq not active - Provider: {ACTIVE_LLM_PROVIDER}")
except Exception as e:
    logger.error(f"Error initializing Groq client: {e}")
    groq_client = None

def call_groq_api(user_question):
    """Call Groq API for LLM response using official client"""
    logger.info(f"Starting Groq API call for: {user_question[:50]}...")
    try:
        if not groq_client:
            logger.error("Groq client not initialized")
            return None
            
        # Create system prompt with company training data
        system_prompt = f"""You are an AI assistant specifically trained for Iron Lady, India's leading Leadership Platform for women. 

TRAINING DATA - Iron Lady Company Information:
{COMPANY_INFO}

INSTRUCTIONS:
- You are an expert on Iron Lady's programs, methodology, community, and services
- Always respond based on the training data provided above
- Be conversational, helpful, and enthusiastic about Iron Lady's mission
- When users ask about programs, costs, enrollment, or services, provide specific details from the training data
- If asked about something not covered in the training data, acknowledge that and redirect to what Iron Lady can help with
- Always maintain a professional yet warm tone that reflects Iron Lady's mission of empowering women
- Use specific numbers, achievements, and program names from the training data when relevant
- End responses with a question or call-to-action when appropriate"""

        user_prompt = f"User Question: {user_question}\n\nProvide a helpful response based on your Iron Lady training:"
        
        logger.info("Sending request to Groq API...")
        
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=GROQ_MODEL,
            max_tokens=600,
            temperature=0.7
        )
        
        response_text = chat_completion.choices[0].message.content
        logger.info(f"Response received ({len(response_text)} chars)")
        return response_text
        
    except Exception as e:
        logger.error(f"Groq API error: {str(e)}")
        return None

def call_huggingface_api(user_question):
    """Call Hugging Face API for LLM response with Iron Lady context"""
    logger.info(f"Starting Hugging Face API call for: {user_question[:50]}...")
    try:
        headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
        
        # Enhanced prompt with Iron Lady training data
        prompt = f"""Iron Lady AI Assistant Training Data:
{COMPANY_INFO}

User Question: {user_question}

As Iron Lady's AI assistant, provide a helpful response based on the training data above. Focus on specific programs, achievements, and how Iron Lady can help advance the user's career:"""
        
        data = {"inputs": prompt, "parameters": {"max_new_tokens": 300, "temperature": 0.7, "return_full_text": False}}
        logger.info("Sending request to Hugging Face API...")
        
        response = requests.post("https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
                               headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and result:
                generated_text = result[0].get("generated_text", "").strip()
                logger.info(f"HuggingFace response received ({len(generated_text)} chars)")
                return generated_text if generated_text else None
        
        logger.error(f"HuggingFace API failed with status: {response.status_code}")
        return None
        
    except Exception as e:
        logger.error(f"HuggingFace API error: {e}")
        return None

def call_openrouter_api(user_question):
    """Call OpenRouter API for LLM response"""
    logger.info(f"Starting OpenRouter API call for: {user_question[:50]}...")
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""You are an AI assistant for Iron Lady, India's leading Leadership Platform for women.
Company Info: {COMPANY_INFO}
User Question: {user_question}
Provide a helpful response about Iron Lady."""

        data = {
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 400
        }
        
        logger.info("Sending request to OpenRouter API...")
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                               headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            response_text = result["choices"][0]["message"]["content"]
            logger.info(f"OpenRouter response received ({len(response_text)} chars)")
            return response_text
        
        logger.error(f"OpenRouter API failed with status: {response.status_code}")
        return None
        
    except Exception as e:
        logger.error(f"OpenRouter API error: {e}")
        return None

def call_together_api(user_question):
    """Call Together AI API for LLM response"""
    try:
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""You are an AI assistant for Iron Lady, India's leading Leadership Platform for women.
{COMPANY_INFO}
User: {user_question}
Assistant:"""

        data = {
            "model": TOGETHER_MODEL,
            "prompt": prompt,
            "max_tokens": 300,
            "temperature": 0.7
        }
        
        response = requests.post("https://api.together.xyz/inference",
                               headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("output", {}).get("choices", [{}])[0].get("text", "").strip()
        return None
        
    except Exception as e:
        logger.error(f"Together API error: {e}")
        return None

def get_llm_response(user_question):
    """
    Get response from configured LLM API with intelligent fallback
    """
    logger.info(f"🤖 Starting LLM response generation for question: {user_question[:50]}...")
    logger.info(f"🤖 Primary LLM Provider: {ACTIVE_LLM_PROVIDER}")
    
    # Try Groq first if it's the active provider
    if ACTIVE_LLM_PROVIDER == "groq" and GROQ_API_KEY != "your_groq_api_key_here":
        logger.info("🚀 Attempting Groq API call...")
        response = call_groq_api(user_question)
        if response:
            logger.info("✅ Successfully got Groq response!")
            return response
        else:
            logger.warning("❌ Groq API failed, trying Hugging Face fallback...")
            # Fallback to Hugging Face
            if HUGGING_FACE_API_KEY != "your_huggingface_api_key_here":
                logger.info("🤗 Attempting Hugging Face fallback...")
                hf_response = call_huggingface_api(user_question)
                if hf_response:
                    logger.info("✅ Successfully got Hugging Face fallback response!")
                    return hf_response
                else:
                    logger.error("❌ Hugging Face also failed, using enhanced fallback")
    
    elif ACTIVE_LLM_PROVIDER == "huggingface" and HUGGING_FACE_API_KEY != "your_huggingface_api_key_here":
        logger.info("🤗 Attempting Hugging Face API call...")
        response = call_huggingface_api(user_question)
        if response:
            logger.info("✅ Successfully got Hugging Face response!")
            return response
        else:
            logger.error("❌ Hugging Face failed, using enhanced fallback")
    
    elif ACTIVE_LLM_PROVIDER == "openrouter" and OPENROUTER_API_KEY != "your_openrouter_api_key_here":
        logger.info("🚀 Attempting OpenRouter API call...")
        response = call_openrouter_api(user_question)
        if response:
            logger.info("✅ Successfully got OpenRouter response!")
            return response
        else:
            logger.error("❌ OpenRouter failed, using enhanced fallback")
    
    elif ACTIVE_LLM_PROVIDER == "together" and TOGETHER_API_KEY != "your_together_api_key_here":
        logger.info("🚀 Attempting Together API call...")
        response = call_together_api(user_question)
        if response:
            logger.info("✅ Successfully got Together response!")
            return response
        else:
            logger.error("❌ Together failed, using enhanced fallback")
    
    # Final fallback to enhanced local responses
    logger.warning("🔄 Using enhanced local response system as final fallback")
    return generate_enhanced_response(user_question)

def generate_enhanced_response(user_input):
    """
    Enhanced response generation with comprehensive Iron Lady information
    """
    logger.info(f"🦾 Generating enhanced local response for: {user_input[:50]}...")
    user_lower = user_input.lower()
    logger.debug(f"🔍 Analyzing keywords in user input: {user_lower}")
    
    if any(word in user_lower for word in ['program', 'programs', 'course', 'training']):
        logger.info("🎯 Detected program-related query, providing program information")
        return """Iron Lady offers several high-impact leadership programs:
        
• **Leadership Essentials Program** - Core leadership skills for career advancement
• **C-Suite League** - Fast-track program for reaching executive levels  
• **Master of Business Warfare** - Advanced tactics for the ₹1 crore+ club
• **MasterClass Sessions** - Learning from global practitioners and CEOs

Our programs have helped 100+ participants reach ₹1 crore+ income, with 7,000+ securing promotions and 6,000+ achieving 2X salary growth in 2024 alone!

Would you like to know more about any specific program?"""
    
    elif any(word in user_lower for word in ['process', 'how', 'join', 'enroll', 'apply']):
        logger.info("📝 Detected enrollment-related query, providing enrollment process")
        return """Here's how you can join Iron Lady's ecosystem:
        
1. **Explore Programs** - Visit iamironlady.com to browse our offerings
2. **Choose Your Path** - Select from Leadership Essentials, C-Suite League, or MasterClass
3. **Online Enrollment** - Easy registration process with immediate access
4. **Community Access** - Join 78,000+ women leaders in our supportive ecosystem
5. **Guided Mentorship** - Receive personalized guidance from industry experts

Contact us at +91-6360823123 or visit our website to start your leadership journey!"""
    
    elif any(word in user_lower for word in ['team', 'founder', 'leadership', 'who']):
        logger.info("👥 Detected team-related query, providing founder information")
        return """Iron Lady was founded by an exceptional team of global leaders:
        
• **Rajesh Bhat** - Founder & Director, visionary entrepreneur and TEDx speaker
• **Suvarna Hegde** - Founder & CEO, expert in Business War Tactics for Women
• **Simon Newman** - Co-Founder & Chairman, former CEO of Aviva Singapore
• **Sridhar Sambandom** - Co-Founder & Director, turn-around specialist, former CEO of Bajaj Auto
• **Chitra Talwar** - Board Member, former VP at PepsiCo with 30+ years experience

Together, they bring 120+ years of combined global CEO/VP/entrepreneurial experience!"""
    
    elif any(word in user_lower for word in ['community', 'network', 'women', 'support']):
        logger.info("🌐 Detected community-related query, providing community information")
        return """Join Iron Lady's thriving community of 78,000+ women leaders!
        
**What makes our community special:**
• Non-judgmental environment where ambitions are celebrated
• Secret Business War tactics shared among members  
• Peer-to-peer learning and mentorship
• Success stories and breakthrough strategies
• Regular networking events and masterclasses

Our community has produced hundreds of successful leaders, board members, and entrepreneurs. It's where ambitious women come together to WIN without waging war!"""
    
    elif any(word in user_lower for word in ['cost', 'price', 'fee', 'investment']):
        return """Iron Lady offers various investment options for different programs:
        
• Programs are designed as an investment in your career growth
• We've helped participants achieve 2X salary growth and ₹1 crore+ incomes
• ROI is typically seen through promotions, salary increases, and career advancement
• Flexible payment options available

For specific program fees and payment plans, please contact us at +91-6360823123 or visit iamironlady.com. Our team can help you choose the right program for your career goals and budget."""
    
    elif any(word in user_lower for word in ['success', 'results', 'achievement', 'outcome']):
        return """Iron Lady has achieved remarkable results for women leaders:
        
**2024 Achievements:**
• 100 participants reached ₹1 crore+ yearly income
• 7,000+ professionals secured well-deserved promotions
• 6,000+ professionals achieved 2X salary growth
• 20+ global events hosted worldwide
• Launched C-Suite League for executive advancement

**Overall Impact:**
• 78,000+ women trained across various programs
• 100+ Board Members created through our programs
• Thousands of success stories of career transformation

Our unique Business War Tactics help women win without fighting!"""
    
    elif any(word in user_lower for word in ['business', 'war', 'tactics', 'strategy']):
        return """Iron Lady's signature **Business War Tactics** help women navigate corporate challenges:
        
**What are Business War Tactics?**
• Strategies to deal with stereotypes, biases, and workplace politics
• Techniques to WIN without waging war or fighting
• Unconventional approaches to breakthrough barriers
• Methods to turn challenges into opportunities

**Why They Work:**
• Developed by CEOs with 120+ years of combined experience
• Tested and proven by thousands of successful women leaders
• Adapted specifically for the unique challenges women face
• Focus on strategic thinking rather than confrontation

Our approach helps women advance their careers while maintaining their authenticity and values!"""
    
    else:
        return f"""Thank you for your question about Iron Lady! 
        
Iron Lady is India's leading Leadership Platform for women, dedicated to elevating a million women to the TOP. We offer:

• **High-impact leadership programs** with proven results
• **Business War Tactics** to help women win without fighting
• **Community of 78,000+ women leaders** for networking and support
• **Global expertise** from experienced CEOs and entrepreneurs

I can help you learn more about:
- Our programs and enrollment process
- Success stories and community
- Our founding team and methodology
- Business War Tactics and strategies
- How to get started on your leadership journey

What specific aspect of Iron Lady would you like to know more about?"""

@app.route("/", methods=["GET"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    logger.info("🏠 Home page GET request received")
    logger.debug(f"🌐 User accessing main page at {datetime.now()}")
    return render_template("auth/login.html")

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    """API endpoint for AJAX chat requests"""
    from flask import jsonify
    
    # Enhanced input extraction and validation
    raw_input = request.form.get("message", "")
    user_input = raw_input.strip() if raw_input else ""
    
    # Detailed logging for debugging
    print(f"📝 AJAX Chat Request from user {current_user.name} (ID: {current_user.id})")
    print(f"📝 Raw input: '{raw_input}'")
    print(f"📝 Cleaned input: '{user_input}'")
    print(f"📝 Input length: {len(user_input)} characters")
    
    if user_input:
        print("🔄 Processing user input via AJAX...")
        print(f"🎯 Question: {user_input}")
        
        # Get AI-powered response about Iron Lady
        response = get_llm_response(user_input)
        
        # Validate response
        if response:
            print(f"📤 Generated response length: {len(response)} characters")
            print(f"📤 Response preview: {response[:100]}...")
            
            # Save chat to database
            try:
                chat_record = Chat(
                    user_id=current_user.id,
                    user_message=user_input,
                    bot_response=response
                )
                db.session.add(chat_record)
                db.session.commit()
                print(f"💾 Chat saved to database with ID: {chat_record.id}")
            except Exception as e:
                print(f"❌ Error saving chat to database: {e}")
                db.session.rollback()
            
            return jsonify({
                'success': True,
                'response': response,
                'user_input': user_input
            })
        else:
            print("❌ No response generated, using fallback")
            fallback_response = "I apologize, but I'm having trouble generating a response right now. Please try asking about Iron Lady's leadership programs, community, or how we can help advance your career."
            
            # Save failed chat attempt to database
            try:
                chat_record = Chat(
                    user_id=current_user.id,
                    user_message=user_input,
                    bot_response=fallback_response
                )
                db.session.add(chat_record)
                db.session.commit()
            except Exception as e:
                print(f"❌ Error saving fallback chat to database: {e}")
                db.session.rollback()
            
            return jsonify({
                'success': False,
                'response': fallback_response,
                'error': 'No LLM response generated'
            })
    else:
        print("⚠️ Empty or whitespace-only input received via AJAX")
        return jsonify({
            'success': False,
            'response': "Please ask me anything about Iron Lady's programs, community, or how we can help advance your career!",
            'error': 'Empty input'
        })

@app.route("/", methods=["POST"])
def home_post():
    """Fallback for non-AJAX form submissions"""
    logger.info("💻 Regular POST request received (fallback mode)")
    response = ""
    user_input = ""
    
    # Enhanced input extraction and validation
    raw_input = request.form.get("message", "")
    user_input = raw_input.strip() if raw_input else ""
    
    # Detailed logging for debugging
    logger.debug(f"📝 Raw input: '{raw_input}'")
    logger.debug(f"📝 Cleaned input: '{user_input}'")
    logger.info(f"📝 Input length: {len(user_input)} characters")
    
    if user_input:
        logger.info("🔄 Processing user input in fallback mode...")
        logger.info(f"🎯 Question: {user_input}")
        
        # Get AI-powered response about Iron Lady
        response = get_llm_response(user_input)
        
        # Validate response
        if response:
            logger.info(f"📤 Generated response length: {len(response)} characters")
            logger.debug(f"📤 Response preview: {response[:100]}...")
        else:
            logger.error("❌ No response generated, using fallback")
            response = "I apologize, but I'm having trouble generating a response right now. Please try asking about Iron Lady's leadership programs, community, or how we can help advance your career."
    else:
        response = "Please ask me anything about Iron Lady's programs, community, or how we can help advance your career!"
        logger.warning("⚠️ Empty or whitespace-only input received")

    # Log the final state
    logger.info(f"🏁 Final state - Input: '{user_input}', Response length: {len(response)}")
    
    return render_template("index.html", response=response, user_input=user_input)

# Authentication Routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '').strip()
        
        if not identifier or not password:
            flash('Please enter both identifier and password.', 'error')
            return render_template('auth/login.html')
        
        # Try to find user by email or mobile
        user = None
        if validate_email(identifier):
            user = User.query.filter_by(email=identifier).first()
        elif validate_mobile(identifier):
            user = User.query.filter_by(mobile=identifier).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    
    return render_template('auth/login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        mobile = request.form.get('mobile', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validation
        if not all([name, email, mobile, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('auth/register.html')
        
        if not validate_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('auth/register.html')
        
        if not validate_mobile(mobile):
            flash('Please enter a valid mobile number.', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('auth/register.html')
        
        # Check if user already exists
        existing_email = User.query.filter_by(email=email).first()
        existing_mobile = User.query.filter_by(mobile=mobile).first()
        
        if existing_email:
            flash('An account with this email already exists.', 'error')
            return render_template('auth/register.html')
        
        if existing_mobile:
            flash('An account with this mobile number already exists.', 'error')
            return render_template('auth/register.html')
        
        # Create new user
        user = User(
            name=name,
            email=email,
            mobile=mobile
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            logger.error(f"Registration error: {e}")
    
    return render_template('auth/register.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Admin Routes
@app.route("/admin")
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route("/admin/user/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def admin_edit_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        mobile = request.form.get('mobile', '').strip()
        is_admin = request.form.get('is_admin') == 'on'
        
        if not all([name, email, mobile]):
            flash('Name, email, and mobile are required.', 'error')
            return render_template('admin/edit_user.html', user=user)
        
        if not validate_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('admin/edit_user.html', user=user)
        
        if not validate_mobile(mobile):
            flash('Please enter a valid mobile number.', 'error')
            return render_template('admin/edit_user.html', user=user)
        
        # Check for existing users with same email/mobile (excluding current user)
        existing_email = User.query.filter(User.email == email, User.id != user_id).first()
        existing_mobile = User.query.filter(User.mobile == mobile, User.id != user_id).first()
        
        if existing_email:
            flash('Another user with this email already exists.', 'error')
            return render_template('admin/edit_user.html', user=user)
        
        if existing_mobile:
            flash('Another user with this mobile number already exists.', 'error')
            return render_template('admin/edit_user.html', user=user)
        
        try:
            user.name = name
            user.email = email
            user.mobile = mobile
            user.is_admin = is_admin
            
            db.session.commit()
            flash(f'User {user.name} updated successfully.', 'success')
            return redirect(url_for('admin_panel'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update user. Please try again.', 'error')
            logger.error(f"User update error: {e}")
    
    return render_template('admin/edit_user.html', user=user)

@app.route("/admin/user/<int:user_id>/delete", methods=["POST"])
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin_panel'))
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.name} deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete user. Please try again.', 'error')
        logger.error(f"User delete error: {e}")
    
    return redirect(url_for('admin_panel'))

@app.route("/admin/create_admin", methods=["POST"])
@login_required
def create_admin():
    # This is a special route to create the first admin user
    if User.query.filter_by(is_admin=True).first():
        flash('Admin already exists.', 'error')
        return redirect(url_for('dashboard'))
    
    if current_user:
        current_user.is_admin = True
        db.session.commit()
        flash('You are now an admin!', 'success')
    
    return redirect(url_for('admin_panel'))

# Admin Chat Management Routes
@app.route("/admin/chats")
@login_required
def admin_chats():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Number of chats per page
    
    # Get all chats with pagination, ordered by most recent first
    chats_query = Chat.query.filter_by(is_deleted=False).order_by(Chat.created_at.desc())
    chats_pagination = chats_query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/chats.html', 
                         chats=chats_pagination.items,
                         pagination=chats_pagination)

@app.route("/admin/user/<int:user_id>/chats")
@login_required
def admin_user_chats(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Get chats for specific user with pagination
    chats_query = Chat.query.filter_by(user_id=user_id, is_deleted=False).order_by(Chat.created_at.desc())
    chats_pagination = chats_query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/user_chats.html', 
                         user=user,
                         chats=chats_pagination.items,
                         pagination=chats_pagination)

@app.route("/admin/chat/<int:chat_id>/edit", methods=["GET", "POST"])
@login_required
def admin_edit_chat(chat_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    chat = Chat.query.get_or_404(chat_id)
    
    if request.method == "POST":
        user_message = request.form.get('user_message', '').strip()
        bot_response = request.form.get('bot_response', '').strip()
        
        if not user_message or not bot_response:
            flash('Both user message and bot response are required.', 'error')
            return render_template('admin/edit_chat.html', chat=chat)
        
        try:
            chat.user_message = user_message
            chat.bot_response = bot_response
            
            db.session.commit()
            flash(f'Chat message updated successfully.', 'success')
            return redirect(url_for('admin_user_chats', user_id=chat.user_id))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update chat message. Please try again.', 'error')
            logger.error(f"Chat update error: {e}")
    
    return render_template('admin/edit_chat.html', chat=chat)

@app.route("/admin/chat/<int:chat_id>/delete", methods=["POST"])
@login_required
def admin_delete_chat(chat_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    chat = Chat.query.get_or_404(chat_id)
    user_id = chat.user_id  # Store user_id before deletion
    
    try:
        # Soft delete - mark as deleted instead of actual deletion
        chat.is_deleted = True
        db.session.commit()
        flash(f'Chat message deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete chat message. Please try again.', 'error')
        logger.error(f"Chat delete error: {e}")
    
    return redirect(url_for('admin_user_chats', user_id=user_id))

@app.route("/admin/chats/stats")
@login_required
def admin_chat_stats():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    # Calculate chat statistics
    total_chats = Chat.query.filter_by(is_deleted=False).count()
    total_users_with_chats = db.session.query(Chat.user_id).filter_by(is_deleted=False).distinct().count()
    
    # Most active users (top 10)
    most_active_users = db.session.query(
        User.name, User.email, db.func.count(Chat.id).label('chat_count')
    ).join(Chat).filter(Chat.is_deleted == False).group_by(User.id).order_by(
        db.func.count(Chat.id).desc()
    ).limit(10).all()
    
    # Recent activity (last 7 days)
    from datetime import timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_chats = Chat.query.filter(
        Chat.created_at >= week_ago, Chat.is_deleted == False
    ).count()
    
    stats = {
        'total_chats': total_chats,
        'total_users_with_chats': total_users_with_chats,
        'recent_chats': recent_chats,
        'most_active_users': most_active_users
    }
    
    return render_template('admin/chat_stats.html', stats=stats)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        # Create admin user if no admin exists
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            admin_user = User(
                name="Admin",
                email="admin@ironlady.com",
                mobile="9999999999",
                is_admin=True
            )
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()
            logger.info("🔑 Default admin user created: admin@ironlady.com / admin123")
    
    logger.info("🚀 Iron Lady AI Assistant starting...")
    logger.info(f"📊 Active LLM Provider: {ACTIVE_LLM_PROVIDER}")
    logger.info(f"🌐 Visit: http://127.0.0.1:5000")
    logger.info("👩‍💼 Ready to assist with Iron Lady inquiries!")
    
    # Log system information
    logger.debug(f"🕰️ Application started at: {datetime.now()}")
    logger.debug(f"📁 Working directory: {os.getcwd()}")
    
    app.run(debug=True)
from flask import Flask, render_template, request
import requests
import json
import os
import logging
from datetime import datetime
from config import *
from groq import Groq

app = Flask(__name__)

# Configure debug logging
def setup_logging():
    # Create debug_logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(__file__), 'debug_logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Generate log filename with timestamp
    log_filename = f"iron_lady_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_filepath = os.path.join(log_dir, log_filename)
    
    # Configure logging to both file and console
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_filepath, encoding='utf-8'),
            logging.StreamHandler()  # This prints to console
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"🚀 Iron Lady AI Customer Assistant - Debug logging initialized")
    logger.info(f"📁 Log file: {log_filepath}")
    return logger

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
logger.info("🔧 Initializing Groq client configuration")
groq_client = None
try:
    if ACTIVE_LLM_PROVIDER == "groq" and GROQ_API_KEY != "your_groq_api_key_here":
        logger.info(f"🔑 Initializing Groq client with API key: {GROQ_API_KEY[:10]}...***")
        groq_client = Groq(api_key=GROQ_API_KEY)
        logger.info("✅ Groq client initialized successfully")
        
        # Test the connection with Iron Lady context
        try:
            logger.debug("🧪 Testing Groq API connection with sample request")
            test_response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are an AI assistant trained specifically for Iron Lady. Use this training data: {COMPANY_INFO[:200]}..."},
                    {"role": "user", "content": "What is Iron Lady? Respond in one sentence."}
                ],
                model=GROQ_MODEL,
                max_tokens=50
            )
            logger.info(f"🧪 API Test Response: {test_response.choices[0].message.content}")
        except Exception as test_error:
            logger.error(f"❌ API Test Failed: {test_error}")
        
    else:
        logger.warning(f"⚠️  Groq not active - Provider: {ACTIVE_LLM_PROVIDER}, Key valid: {GROQ_API_KEY != 'your_groq_api_key_here'}")
except Exception as e:
    logger.error(f"❌ Error initializing Groq client: {e}")
    print(f"❌ Failed to initialize Groq client: {e}")
    groq_client = None

def call_groq_api(user_question):
    """Call Groq API for LLM response using official client"""
    logger.info(f"🚀 Starting Groq API call for user question: {user_question[:50]}...")
    try:
        if not groq_client:
            logger.error("❌ Groq client not initialized")
            return None
            
        logger.debug(f"🔑 Using Groq API Key: {GROQ_API_KEY[:10]}...***")
        logger.debug(f"🤖 Using Model: {GROQ_MODEL}")
        
        # Create a comprehensive system prompt with company training data
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
        
        logger.info("📤 Sending request to Groq API...")
        logger.debug(f"📝 System prompt length: {len(system_prompt)} characters")
        logger.debug(f"📝 User prompt: {user_prompt[:100]}...")
        
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
        logger.info(f"📥 Received response length: {len(response_text)} characters")
        logger.debug(f"📥 Response preview: {response_text[:100]}...")
        return response_text
        
    except Exception as e:
        logger.error(f"❌ Groq API error: {str(e)}")
        logger.error(f"❌ Error type: {type(e)}")
        import traceback
        logger.error(f"❌ Full traceback: {traceback.format_exc()}")
        return None

def call_huggingface_api(user_question):
    """Call Hugging Face API for LLM response with Iron Lady context"""
    logger.info(f"🤗 Starting Hugging Face API call for user question: {user_question[:50]}...")
    try:
        headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
        logger.debug(f"🔑 Using HF API Key: {HUGGING_FACE_API_KEY[:10]}...***")
        
        # Enhanced prompt with comprehensive Iron Lady training data
        prompt = f"""Iron Lady AI Assistant Training Data:
{COMPANY_INFO}

User Question: {user_question}

As Iron Lady's AI assistant, provide a helpful response based on the training data above. Focus on specific programs, achievements, and how Iron Lady can help advance the user's career:"""
        
        data = {"inputs": prompt, "parameters": {"max_new_tokens": 300, "temperature": 0.7, "return_full_text": False}}
        logger.debug(f"📝 Prompt length: {len(prompt)} characters")
        logger.info("📤 Sending request to Hugging Face API...")
        
        response = requests.post("https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
                               headers=headers, json=data, timeout=15)
        
        logger.debug(f"🌐 HF API Response Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.debug(f"📊 HF API Result type: {type(result)}")
            if isinstance(result, list) and result:
                generated_text = result[0].get("generated_text", "").strip()
                logger.info(f"📥 HuggingFace response length: {len(generated_text)} characters")
                logger.debug(f"📥 HuggingFace response preview: {generated_text[:100]}...")
                return generated_text if generated_text else None
        
        logger.error(f"❌ HuggingFace API failed with status: {response.status_code}")
        logger.error(f"❌ Response content: {response.text[:200]}...")
        return None
        
    except Exception as e:
        logger.error(f"❌ HuggingFace API error: {e}")
        import traceback
        logger.error(f"❌ HF Full traceback: {traceback.format_exc()}")
        return None

def call_openrouter_api(user_question):
    """Call OpenRouter API for LLM response"""
    logger.info(f"🚀 Starting OpenRouter API call for user question: {user_question[:50]}...")
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        logger.debug(f"🔑 Using OpenRouter API Key: {OPENROUTER_API_KEY[:10]}...***")
        
        prompt = f"""You are an AI assistant for Iron Lady, India's leading Leadership Platform for women.
Company Info: {COMPANY_INFO}
User Question: {user_question}
Provide a helpful response about Iron Lady."""

        data = {
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 400
        }
        
        logger.info("📤 Sending request to OpenRouter API...")
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                               headers=headers, json=data, timeout=10)
        
        logger.debug(f"🌐 OpenRouter API Response Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            response_text = result["choices"][0]["message"]["content"]
            logger.info(f"📥 OpenRouter response length: {len(response_text)} characters")
            return response_text
        
        logger.error(f"❌ OpenRouter API failed with status: {response.status_code}")
        return None
        
    except Exception as e:
        logger.error(f"❌ OpenRouter API error: {e}")
        import traceback
        logger.error(f"❌ OpenRouter Full traceback: {traceback.format_exc()}")
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
        print(f"Together API error: {e}")
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
    logger.info("🏠 Home page GET request received")
    logger.debug(f"🌐 User accessing main page at {datetime.now()}")
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """API endpoint for AJAX chat requests"""
    from flask import jsonify
    
    # Enhanced input extraction and validation
    raw_input = request.form.get("message", "")
    user_input = raw_input.strip() if raw_input else ""
    
    # Detailed logging for debugging
    print(f"📝 AJAX Chat Request")
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
            return jsonify({
                'success': True,
                'response': response,
                'user_input': user_input
            })
        else:
            print("❌ No response generated, using fallback")
            return jsonify({
                'success': False,
                'response': "I apologize, but I'm having trouble generating a response right now. Please try asking about Iron Lady's leadership programs, community, or how we can help advance your career.",
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

if __name__ == "__main__":
    logger.info("🚀 Iron Lady AI Assistant starting...")
    logger.info(f"📊 Active LLM Provider: {ACTIVE_LLM_PROVIDER}")
    logger.info(f"🌐 Visit: http://127.0.0.1:5000")
    logger.info("👩‍💼 Ready to assist with Iron Lady inquiries!")
    
    # Log system information
    logger.debug(f"🕰️ Application started at: {datetime.now()}")
    logger.debug(f"📁 Working directory: {os.getcwd()}")
    
    app.run(debug=True)
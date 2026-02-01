# Iron Lady AI Customer Assistant

A comprehensive web application for Iron Lady, India's leading Leadership Platform for women, featuring an intelligent AI assistant, user authentication, admin management, and modern responsive design.

## ✨ Features

### 🤖 **AI-Powered Chat System**
- **Multi-API Support**: Groq (primary), HuggingFace, OpenRouter, Together AI with intelligent fallback
- **Smart Responses**: Specialized knowledge about Iron Lady's programs, community, and services  
- **Rich Text Formatting**: Supports **bold text** and line breaks in AI responses
- **Real-time Chat**: AJAX-powered conversations without page reloads

### 🔐 **User Authentication System**
- **Secure Registration/Login**: Email and mobile number support with validation
- **User Dashboard**: Personalized chat interface for registered users
- **Session Management**: Secure login sessions with Flask-Login
- **Password Security**: Werkzeug password hashing

### 👨‍💼 **Admin Management Panel**
- **User Management**: View, edit, delete user accounts
- **Chat Monitoring**: View all user conversations and responses
- **Chat Statistics**: Analytics dashboard with user activity metrics
- **Admin Controls**: Soft delete chats, edit messages, manage users

### 🎨 **Modern User Interface**
- **Consistent Branding**: Iron Lady logo integration across all pages
- **Animated Backgrounds**: Dynamic gradients with floating particle effects
- **Responsive Design**: Perfect display on desktop, tablet, and mobile
- **Professional Styling**: Modern CSS with smooth transitions and hover effects

### 💾 **Database Integration**
- **SQLite Database**: User accounts and chat history storage
- **Data Models**: User profiles with admin roles, chat conversations
- **Relationship Management**: Proper foreign key relationships
- **Data Persistence**: All conversations saved for future reference

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- A Groq API key (get free at [console.groq.com](https://console.groq.com/))
- Additional API keys (optional): HuggingFace, OpenRouter, Together AI for fallback options

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/IronLady-AI-Customer-Assistant.git
   cd IronLady-AI-Customer-Assistant
   ```

2. **Set up virtual environment**:

   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**:

   Create/edit your `config.py` file:

   ```python
   # Primary AI Provider (Groq - Recommended)
   GROQ_API_KEY = "your_groq_api_key_here"
   GROQ_MODEL = "llama-3.1-8b-instant"
   ACTIVE_LLM_PROVIDER = "groq"
   
   # Fallback API Keys (Optional but recommended)
   HUGGING_FACE_API_KEY = "your_hf_token_here"
   OPENROUTER_API_KEY = "your_openrouter_key_here"
   TOGETHER_API_KEY = "your_together_key_here"
   
   # Model configurations
   HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
   OPENROUTER_MODEL = "meta-llama/llama-3.1-8b-instruct:free"
   TOGETHER_MODEL = "meta-llama/Llama-2-7b-chat-hf"
   ```

5. **Run the application**:

   ```bash
   python app.py
   ```

6. **Access the application**:
   - Open your browser and visit: `http://127.0.0.1:5000`
   - **Default admin account**: admin@ironlady.com / admin123
   - Register new users or use admin panel to manage accounts

## 🎨 User Interface Features

### 🏠 **Landing Page (index.html)**
- **Professional Branding**: Iron Lady logo prominently displayed
- **Animated Background**: Dynamic gradient with floating particle effects
- **Quick Chat Interface**: Immediate access to AI assistant without registration
- **Smooth Interactions**: Hover effects and CSS transitions throughout

### 🔑 **Authentication Pages**
- **Unified Login/Register**: Modern tabbed interface with validation
- **Logo Integration**: Consistent branding across auth pages
- **Responsive Forms**: Mobile-friendly input fields and buttons
- **Error Handling**: Real-time validation feedback

### 📊 **User Dashboard**
- **Personalized Welcome**: User-specific greeting and information
- **Chat History**: All previous conversations saved and accessible
- **Message Bubbles**: WhatsApp-style chat interface with user/bot differentiation
- **Real-time Updates**: Live typing indicators and message delivery

### ⚙️ **Admin Panel**
- **User Management**: Complete CRUD operations for user accounts
- **Chat Monitoring**: View all conversations across all users
- **Statistics Dashboard**: User activity metrics and engagement data
- **Bulk Operations**: Manage multiple records efficiently

## 🔧 Technical Architecture

### **Backend Technologies**
- **Flask 2.x**: Modern Python web framework with blueprints
- **SQLAlchemy**: ORM for database operations with relationships
- **Flask-Login**: Secure session management and user authentication
- **Werkzeug Security**: Password hashing and validation
- **SQLite**: Lightweight database for development (easily upgradeable to PostgreSQL/MySQL)

### **Frontend Technologies**
- **HTML5**: Semantic markup with accessibility considerations
- **CSS3**: Modern styling with animations, gradients, and responsive design
- **Vanilla JavaScript**: ES6+ features with async/await for API calls
- **AJAX**: XMLHttpRequest and Fetch API for seamless interactions

### **AI Integration**
- **Primary**: Groq API with Llama 3.1-8B Instant (fast, reliable)
- **Fallbacks**: HuggingFace Transformers, OpenRouter, Together AI
- **Smart Routing**: Automatic fallback system if primary API fails
- **Error Handling**: Graceful degradation with local responses

### **Key Implementation Details**

#### **Chat Formatting System**
```javascript
// Automatic text formatting in both chat interfaces
let formattedText = text
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>') // Bold text
    .replace(/\n/g, '<br>'); // Line breaks
bubbleDiv.innerHTML = formattedText;
```

#### **Authentication Flow**
```python
# Secure user session management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)
```

#### **Database Models**
```python
# User model with admin capabilities
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.String(20), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    chats = db.relationship('Chat', backref='user', lazy=True)

# Chat model for conversation storage
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
```

## 🤖 AI Configuration

The chatbot is powered by **Groq's Llama 3.1-8B Instant** model, providing:

- Fast response times (typically under 2 seconds)
- High-quality, contextual responses
- Specialized knowledge about Iron Lady's services
- Natural conversation flow

### API Setup

```python
# config.py
GROQ_API_KEY = "your_groq_api_key_here"
ACTIVE_LLM_PROVIDER = "groq"

# Fallback options
HUGGING_FACE_API_KEY = "optional_fallback_key"
```

## 📁 Project Structure

```
IronLady-AI-Customer-Assistant/
├── app.py                   # Main Flask application with all routes
├── config.py                # API keys and configuration (create this file)
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore (includes cache/debug exclusions)
├── static/
│   └── iron-lady-logo.png  # Official Iron Lady branding
├── templates/
│   ├── index.html          # Landing page with AI chat
│   ├── dashboard.html      # User dashboard with chat history
│   ├── auth/
│   │   ├── login.html      # Login/Register combined interface
│   │   └── register.html   # Registration form
│   └── admin/
│       ├── users.html      # User management panel
│       ├── chats.html      # All chats overview
│       ├── user_chats.html # Individual user's chats
│       ├── edit_user.html  # Edit user details
│       ├── edit_chat.html  # Edit chat messages
│       └── chat_stats.html # Analytics dashboard
├── instance/
│   └── iron_lady_users.db  # SQLite database (auto-created)
└── README.md               # This documentation
```

## 🔍 Application Routes

### **Public Routes**
- `/` - Landing page with guest chat functionality
- `/login` - User authentication (GET/POST)
- `/register` - User registration (GET/POST)
- `/logout` - User session termination

### **Protected User Routes**
- `/dashboard` - User dashboard with chat history
- `/chat` - AJAX endpoint for AI conversations (POST)

### **Admin Routes** (Admin access required)
- `/admin` - Admin panel overview with user list
- `/admin/user/<id>/edit` - Edit user account details
- `/admin/user/<id>/delete` - Delete user account
- `/admin/chats` - View all chat conversations
- `/admin/user/<id>/chats` - View specific user's chats
- `/admin/chat/<id>/edit` - Edit individual chat messages
- `/admin/chat/<id>/delete` - Soft delete chat messages
- `/admin/chats/stats` - Analytics and usage statistics

## 💡 Example Interactions

### **Iron Lady Program Inquiries**
```
User: "Tell me about Iron Lady's leadership programs"
AI: "Iron Lady offers several high-impact leadership programs:

• **Leadership Essentials Program** - Core leadership skills for career advancement
• **C-Suite League** - Fast-track program for reaching executive levels  
• **Master of Business Warfare** - Advanced tactics for the ₹1 crore+ club
• **MasterClass Sessions** - Learning from global practitioners and CEOs

Our programs have helped 100+ participants reach ₹1 crore+ income, with 7,000+ securing promotions and 6,000+ achieving 2X salary growth in 2024 alone!

Would you like to know more about any specific program?"
```

### **Community and Success Stories**
```
User: "What results have you achieved?"
AI: "Iron Lady has achieved remarkable results for women leaders:

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

Our unique **Business War Tactics** help women win without fighting!"
```

### **Enrollment and Contact Information**
```
User: "How can I join Iron Lady?"
AI: "Here's how you can join Iron Lady's ecosystem:

1. **Explore Programs** - Visit iamironlady.com to browse our offerings
2. **Choose Your Path** - Select from Leadership Essentials, C-Suite League, or MasterClass
3. **Online Enrollment** - Easy registration process with immediate access
4. **Community Access** - Join 78,000+ women leaders in our supportive ecosystem
5. **Guided Mentorship** - Receive personalized guidance from industry experts

Contact us at **+91-6360823123** or visit our website to start your leadership journey!"
```

## 🚀 Deployment Options

### **Local Development**

```bash
# Clone and setup
git clone <repository-url>
cd IronLady-AI-Customer-Assistant
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Configure API keys in config.py
# Run the application
python app.py

# Access at http://127.0.0.1:5000
# Default admin: admin@ironlady.com / admin123
```

### **Production Deployment**

#### **Environment Variables**
```bash
# Required
GROQ_API_KEY=your_groq_api_key_here
FLASK_ENV=production
SECRET_KEY=your_secret_key_here

# Optional fallback APIs
HUGGING_FACE_API_KEY=your_hf_token
OPENROUTER_API_KEY=your_openrouter_key
TOGETHER_API_KEY=your_together_key
```

#### **Platform-Specific Deployment**

**Heroku:**
```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create iron-lady-ai-assistant
heroku config:set GROQ_API_KEY=your_key_here
git push heroku main
```

**Railway:**
- Connect GitHub repository
- Set environment variables in dashboard
- Auto-deploy on git push

**Render:**
- Connect repo with auto-build
- Set environment variables
- Use start command: `python app.py`

**DigitalOcean App Platform:**
- Upload as app spec or connect GitHub
- Configure environment variables
- Set run command: `python app.py`

#### **Production Checklist**
- ✅ Set `FLASK_ENV=production`
- ✅ Use strong `SECRET_KEY`
- ✅ Configure all API keys
- ✅ Set up database (SQLite → PostgreSQL for production)
- ✅ Enable HTTPS
- ✅ Set up monitoring and logging

## 🛠️ Development & Maintenance

### **Code Quality Features**
- **Clean Architecture**: Modular Flask app with clear separation of concerns
- **Error Handling**: Comprehensive try-catch blocks and user feedback
- **Security**: Password hashing, CSRF protection, input validation
- **Database**: Proper relationships and foreign keys
- **Logging**: Structured logging system (cleaned debug verbosity)
- **Performance**: AJAX prevents page reloads, optimized queries

### **Recent Improvements**
- ✅ **Logo Integration**: Iron Lady branding across all pages
- ✅ **Chat Formatting**: Bold text and line breaks in AI responses  
- ✅ **Code Cleanup**: Removed debug logs, console statements, cache files
- ✅ **User Authentication**: Complete registration and login system
- ✅ **Admin Panel**: Full user and chat management capabilities
- ✅ **Database Integration**: SQLite with proper models and relationships
- ✅ **Multi-API Support**: Intelligent fallback system for AI providers

### **Maintenance Tasks**
```bash
# Database management
# Backup database
cp instance/iron_lady_users.db backups/backup_$(date +%Y%m%d).db

# Clear cache files (if any)
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete

# Update dependencies
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt

# Test API connections
python -c "from app import *; test_groq_connection()"
```

### **Monitoring & Analytics**
- **User Metrics**: Registration trends, active users
- **Chat Analytics**: Conversation volume, response times
- **Error Tracking**: Failed API calls, user issues
- **Performance**: Page load times, database query performance

## 🎯 About Iron Lady

**Iron Lady** is India's leading Leadership Platform for women, empowering professionals to achieve extraordinary success.

### 📊 Proven Results

- **78,000+ women leaders** in the community
- **100+ participants** reached ₹1 crore+ yearly income in 2024
- **7,000+ professionals** secured promotions
- **6,000+ professionals** achieved 2X salary growth
- **Unique Business War Tactics** methodology

### 🏆 Leadership Programs

- **Leadership Essentials Program**: Foundation leadership skills
- **C-Suite League**: Executive leadership development
- **Master of Business Warfare**: Advanced strategic thinking
- **MasterClass Sessions**: Specialized skill workshops

### 👥 Founding Team

- **Rajesh Bhat**: Founder & Director, TEDx speaker
- **Suvarna Hegde**: Founder & CEO, Business War Tactics expert
- **Simon Newman**: Co-Founder & Chairman, former CEO of Aviva Singapore
- **Sridhar Sambandom**: Co-Founder & Director, former CEO of Bajaj Auto
- **Chitra Talwar**: Board Member, former VP at PepsiCo

## 🛠️ Development Notes

### Code Quality

- Clean, modular Flask architecture
- Comprehensive error handling and logging
- Responsive design principles
- Security best practices implemented

### Performance Optimizations

- AJAX prevents unnecessary page reloads
- Efficient API calls with proper error handling
- Optimized CSS animations for smooth performance
- Minimal dependencies for fast loading

## 📞 Contact & Support

### **For Iron Lady Programs & Services**
- 🌐 **Website**: [iamironlady.com](https://iamironlady.com)
- 📱 **Phone**: +91-6360823123
- 💬 **Direct Inquiry**: Use the AI assistant on this platform

### **For Technical Support**
- 🐛 **Issues**: Create an issue in the GitHub repository
- 🔧 **Debugging**: Check browser console for error details
- 📖 **Documentation**: Refer to code comments and this README
- 💡 **Feature Requests**: Submit via GitHub issues with enhancement label

### **Admin Access**
- **Default Admin**: admin@ironlady.com / admin123
- **Admin Panel**: Available at `/admin` after login
- **User Management**: Create, edit, delete user accounts
- **Chat Monitoring**: View and manage all conversations

---

## 🔒 Security & Privacy

### **Data Protection**
- **Password Security**: Werkzeug hashing with salt
- **Session Management**: Secure Flask-Login implementation
- **Input Validation**: Server-side validation for all forms
- **SQL Injection Prevention**: SQLAlchemy ORM prevents raw SQL
- **XSS Protection**: Proper input sanitization and output encoding

### **API Security**
- **Environment Variables**: API keys stored securely
- **Rate Limiting**: Consider implementing for production
- **Error Handling**: No sensitive data leaked in error messages
- **HTTPS**: Enable for production deployment

## 📊 Analytics & Insights

The admin panel provides comprehensive analytics:

### **User Metrics**
- Total registered users
- New registrations over time  
- User activity levels
- Admin vs regular user ratios

### **Chat Analytics**
- Total conversations conducted
- Most active users
- Common queries and topics
- AI response success rates
- Average conversation length

### **Technical Metrics**
- API response times
- Error rates and types
- Database query performance
- System uptime and reliability

## 🔮 Future Enhancements

### **Planned Features**
- 📧 **Email Integration**: Automated email responses and newsletters
- 📱 **Mobile App**: React Native companion app
- 🔔 **Push Notifications**: Real-time alerts and updates
- 🌍 **Multi-language**: Hindi and other regional language support
- 💳 **Payment Integration**: Direct program enrollment and payment
- 📈 **Advanced Analytics**: Detailed conversation insights and trends
- 🤖 **Enhanced AI**: Custom fine-tuned models for Iron Lady
- 🎥 **Video Integration**: Embedded program previews and testimonials

### **Technical Roadmap**
- 🐘 **PostgreSQL Migration**: Production-grade database
- 🚀 **Redis Caching**: Improved performance for frequent queries
- 📊 **Elasticsearch**: Advanced search capabilities
- 🔄 **CI/CD Pipeline**: Automated testing and deployment
- 🐳 **Docker Container**: Simplified deployment and scaling
- ☁️ **Cloud Migration**: AWS/GCP deployment with load balancing

---

## 📝 License & Credits

### **License**
This project is created specifically for Iron Lady's customer service and business needs. All rights reserved to Iron Lady organization.

### **Credits & Acknowledgments**
- **Iron Lady Team**: For vision, content, and business requirements
- **AI Providers**: Groq, HuggingFace, OpenRouter, Together AI for LLM services
- **Open Source**: Flask, SQLAlchemy, and other Python libraries
- **Design Inspiration**: Modern web design principles and UX best practices

### **API Usage Terms**
- Follow terms of service for Groq and other LLM providers
- Respect API rate limits and usage guidelines
- Implement proper error handling and fallback mechanisms
- Monitor API usage and costs for production deployments

**Built with ❤️ for empowering women leaders across India and beyond**

---

*Last Updated: February 2026*  
*Version: 2.0 - Complete Web Application with Authentication & Admin Panel*

# Iron Lady AI Customer Assistant

An intelligent chatbot for Iron Lady, India's leading Leadership Platform for women, powered by advanced LLM APIs with a modern, user friendly interface.

## ✨ Features

- 🤖 **AI-Powered Responses**: Dynamic conversations using Groq's Llama 3.1 model
- 🎨 **Modern Animated UI**: Beautiful gradient backgrounds with floating particle animations
- ⚡ **AJAX-Powered**: Seamless chat experience without page reloads
- 🎯 **Specialized Knowledge**: Deep expertise in Iron Lady's programs and services
- 📱 **Responsive Design**: Works perfectly on desktop and mobile devices
- 🔒 **Secure**: Environment-based configuration for API keys
- 💬 **Rich Text Formatting**: Supports bold text with **markdown** syntax
- 🚀 **Fast Performance**: Optimized for quick response times

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- A Groq API key (free at [console.groq.com](https://console.groq.com/))

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
4. **Configure API key**:

   - Create your `config.py` file with your Groq API key:

   ```python
   # Groq API Configuration
   GROQ_API_KEY = "your_groq_api_key_here"
   ACTIVE_LLM_PROVIDER = "groq"
   ```
5. **Run the application**:

   ```bash
   python app_with_llm.py
   ```
6. **Open your browser** and visit: `http://127.0.0.1:5000`

## 🎨 User Interface Features

- **Animated Background**: Dynamic gradient with floating particle effects
- **Iron Lady Branding**: Professional logo and color scheme
- **Smooth Interactions**: Hover effects and transitions throughout
- **Real-time Chat**: AJAX-powered messaging without page refreshes
- **Loading Indicators**: Visual feedback during AI processing
- **Responsive Layout**: Adapts to different screen sizes

## 🔧 Technical Architecture

### Core Technologies

- **Backend**: Flask web framework with Python
- **Frontend**: HTML5, CSS3 with animations, vanilla JavaScript
- **AI Integration**: Groq API with Llama 3.1-8B Instant model
- **Communication**: AJAX for seamless user interactions
- **Styling**: Modern CSS with gradients, animations, and responsive design

### Key Features Implementation

- **Real-time Chat**: JavaScript fetch API with form handling
- **Text Formatting**: Automatic **bold** text conversion from markdown
- **Error Handling**: Comprehensive try-catch blocks with user feedback
- **Loading States**: Visual indicators during API requests
- **Input Validation**: Client and server-side validation

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
├── app.py      # Main Flask application with AI integration
├── config.py            # API configuration (create this file)
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
├── templates/
│   └── index.html      # Frontend with animations and AJAX
├── static/             # Static assets (if any)
└── README.md           # This documentation
```

## 💡 Example Interactions

Try these sample questions to see the AI assistant in action:

- "Tell me about Iron Lady's leadership programs"
- "How can I join the Iron Lady community?"
- "What are Business War Tactics and how do they work?"
- "Who are the founders and leadership team?"
- "What success stories and results have you achieved?"
- "How do I enroll in the Leadership Essentials program?"
- "What makes Iron Lady different from other platforms?"
- "Can you explain the C-Suite League program?"

## 🚀 Deployment Options

### Local Development

```bash
# Debug mode (recommended for development)
python app_with_llm.py
```

### Production Deployment

The application is ready for deployment on various platforms:

- **Heroku**: Include `Procfile` with `web: python app_with_llm.py`
- **Railway**: Connect GitHub repository directly
- **Render**: Deploy from GitHub with auto-builds
- **DigitalOcean App Platform**: One-click deployment
- **AWS Elastic Beanstalk**: Upload as zip file

### Environment Variables for Production

```bash
GROQ_API_KEY=your_groq_api_key_here
FLASK_ENV=production
```

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

For questions about Iron Lady programs:

- **Website**: [iamironlady.com](https://iamironlady.com)
- **Phone**: +91-6360823123

For technical support with this chatbot:

- Create an issue in the GitHub repository
- Check the browser console for debugging information

---

## 📝 License

This project is created for Iron Lady's customer service needs. Please ensure you have appropriate API keys and follow the terms of service for Groq and other LLM providers.

**Built with ❤️ for empowering women leaders across India**

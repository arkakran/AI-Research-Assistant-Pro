# 🔬 AI Research Assistant Pro

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.0+-green.svg)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2.0+-purple.svg)](https://langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Professional multi-agent research system that generates comprehensive reports using LLaMA-3.3-70B and Tavily AI Search**

An intelligent research platform built with Flask, LangChain, and advanced AI models that transforms any research query into a professionally formatted report through a sophisticated four-agent pipeline.

## 🌟 Features

### 🤖 **Advanced AI Pipeline**
- **Multi-Agent System**: Research → Summarize → Critique → Write
- **LLaMA-3.3-70B Integration**: State-of-the-art language model via Groq
- **Tavily AI Search**: Advanced web search with domain filtering
- **Real-time Progress Tracking**: Live updates during research process

### 📊 **Professional Reports**
- **Comprehensive Analysis**: Executive summaries, market data, investment insights
- **Multiple Export Formats**: PDF, Markdown, and JSON downloads
- **Proper Formatting**: Clean typography with headings, bullet points, and links
- **Source Citations**: Clickable references with publication dates

### 🎨 **Modern Interface**
- **Responsive Design**: Bootstrap 5 with custom styling
- **Real-time Updates**: Progress bars and status messages
- **Interactive Elements**: Copy-to-clipboard, example queries
- **Professional Styling**: Gradient themes and smooth animations

## 🚀 Quick Start

### Prerequisites
# 🔬 AI Research Assistant Pro

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.0+-green.svg)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2.0+-purple.svg)](https://langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Professional multi-agent research system that generates comprehensive reports using LLaMA-3.3-70B and Tavily AI Search**

An intelligent research platform built with Flask, LangChain, and advanced AI models that transforms any research query into a professionally formatted report through a sophisticated four-agent pipeline.

## 🌟 Features

### 🤖 **Advanced AI Pipeline**
- **Multi-Agent System**: Research → Summarize → Critique → Write
- **LLaMA-3.3-70B Integration**: State-of-the-art language model via Groq
- **Tavily AI Search**: Advanced web search with domain filtering
- **Real-time Progress Tracking**: Live updates during research process

### 📊 **Professional Reports**
- **Comprehensive Analysis**: Executive summaries, market data, investment insights
- **Multiple Export Formats**: PDF, Markdown, and JSON downloads
- **Proper Formatting**: Clean typography with headings, bullet points, and links
- **Source Citations**: Clickable references with publication dates

### 🎨 **Modern Interface**
- **Responsive Design**: Bootstrap 5 with custom styling
- **Real-time Updates**: Progress bars and status messages
- **Interactive Elements**: Copy-to-clipboard, example queries
- **Professional Styling**: Gradient themes and smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git

### 1. Clone the Repository
git clone https://github.com/yourusername/ai-research-assistant.git

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Set Up Environment Variables
create .env file 
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
SECRET_KEY=your_flask_secret_key_here

### 4. Get API Keys

#### **Groq API (LLaMA-3.3-70B)**
1. Visit [console.groq.com](https://console.groq.com)
2. Create a free account
3. Generate your API key

#### **Tavily API (Advanced Search)**
1. Visit [tavily.com](https://tavily.com)
2. Sign up for free account
3. Get your API key (1000 free searches/month)

#### **Flask Secret Key**
Generate a secure secret key:
python -c "import secrets; print(secrets.token_hex())"

### 5. Run the Application
python app.py


## 📁 Project Structure

ai-research-assistant/
├── app.py # Main Flask application
├── .env # Environment variables (API keys)
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── static/
│ ├── css/
│ │ └── styles.css # Custom styling
│ └── js/
│ └── main.js # JavaScript functionality
├── templates/
│ ├── base.html # Base template
│ ├── index.html # Home page
│ └── research.html # Results page
└── utils/
├── init.py # Package initializer
├── config.py # Configuration settings
├── agents.py # AI research agents
├── search.py # Tavily search integration
└── report_generator.py # PDF/Markdown generation

## 🔧 Architecture

### Multi-Agent Research Pipeline
graph LR
A[User Query] --> B[Tavily Search]
B --> C[Research Agent]
C --> D[Summarizer Agent]
D --> E[Critic Agent]
E --> F[Writer Agent]
F --> G[Professional Report]


### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Flask | Web framework and API |
| **AI Model** | LLaMA-3.3-70B (Groq) | Language understanding and generation |
| **Search Engine** | Tavily AI | Advanced web search and data retrieval |
| **AI Framework** | LangChain | Agent orchestration and prompt management |
| **Frontend** | Bootstrap 5 + Custom CSS | Responsive user interface |
| **Report Generation** | ReportLab | Professional PDF creation |
| **Background Processing** | Threading | Concurrent research handling |


### Sample Report Structure
Executive Summary
Brief overview and key insights

Top Companies/Trends
Detailed analysis with:

Founded/established dates

Focus areas and technologies

Funding and financial data

Recent developments

Market Analysis
Market size and projections

Growth trends and statistics

Key technologies and applications

Challenges and opportunities

Investment Landscape
Funding trends and patterns

Key investors and sources

Success stories and achievements

Future Outlook
Emerging trends and technologies

Market predictions and forecasts

Development opportunities

References and Sources
Credible sources with clickable links


## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with research form |
| `/start_research` | POST | Initiate research process |
| `/research_progress/<id>` | GET | Get research progress status |
| `/research_result/<id>` | GET | Display completed research report |
| `/download/<format>/<id>` | GET | Download report (pdf/markdown/json) |
| `/health` | GET | API health check |
| `/test` | POST | Test endpoint for debugging |

## 🚀 Deployment

### Render (Recommended)

1. **Push to GitHub**


2. **Deploy on Render**
- Visit [render.com](https://render.com)
- Connect your GitHub repository
- Choose "Web Service" → "Free tier"
- Set environment variables in Render dashboard
- Deploy!

### Environment Variables for Deployment
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
SECRET_KEY=your_secret_key
PYTHON_VERSION=3.11.0

### Build Commands
Build Command
pip install -r requirements.txt

Start Command
python app.py


## 📊 Performance & Limits

### Free Tier Limits
- **Groq**: 30 requests/minute, 6,000 tokens/minute
- **Tavily**: 1,000 searches/month
- **Processing Time**: 2-5 minutes per research query

### Optimization Tips
- Use specific, focused research queries
- Leverage the 4-agent pipeline for thorough analysis
- Export reports for offline viewing
- Monitor API usage in respective dashboards

## 🔧 Configuration

### Custom Search Domains

Edit `utils/search.py` to modify search domains:

include_domains=[
"yourstory.com",
"economictimes.indiatimes.com",
"techcrunch.com",
"inc42.com",
# Add your preferred domains
]


### Agent Customization

Modify agent prompts in `utils/agents.py` for different research styles:



### Agent Customization

Modify agent prompts in `utils/agents.py` for different research styles:

research_prompt = PromptTemplate(
input_variables=["query", "search_results"],
template="""Your custom research prompt here..."""
)


## 🐛 Troubleshooting

### Common Issues

**🔥 API Keys Not Working**

Check your .env file format
GROQ_API_KEY=gsk_your_key_without_quotes
TAVILY_API_KEY=tvly-your_key_without_quotes


**🔥 Research Stuck on "Searching"**
- Check internet connection
- Verify Tavily API key validity
- Check Tavily quota limits

**🔥 Report Formatting Issues**
- Clear browser cache
- Check browser console for JavaScript errors
- Ensure all static files are loading

**🔥 Deployment Issues**
- Verify all environment variables are set
- Check build logs for missing dependencies
- Ensure Python version compatibility

### Debug Mode

Enable debug logging:
In app.py
app.run(debug=True, host='0.0.0.0', port=5000)



## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request




## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Groq](https://groq.com)** - Ultra-fast LLaMA-3.3-70B inference
- **[Tavily](https://tavily.com)** - AI-optimized search engine
- **[LangChain](https://langchain.com)** - AI application framework
- **[Bootstrap](https://getbootstrap.com)** - Responsive UI components
- **[ReportLab](https://reportlab.com)** - Professional PDF generation

## 📈 Roadmap

- [ ] **User Authentication** - Save and manage research history
- [ ] **Research Templates** - Pre-built templates for different industries
- [ ] **Collaborative Features** - Share and collaborate on research
- [ ] **Advanced Analytics** - Research insights and trending topics
- [ ] **API Access** - RESTful API for developers
- [ ] **Mobile App** - React Native mobile application

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yourusername/ai-research-assistant/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-research-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-research-assistant/discussions)

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

[Live Demo](your-deployment-url) 
• [Report Bug](https://github.com/yourusername/ai-research-assistant/issues) 
• [Request Feature](https://github.com/yourusername/ai-research-assistant/issues)

</div>



### 1. Clone the Repository


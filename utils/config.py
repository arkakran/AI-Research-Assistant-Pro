import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_MODEL = "llama-3.3-70b-versatile"
    TAVILY_MAX_RESULTS = 15
    TAVILY_SEARCH_DEPTH = "advanced"
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")

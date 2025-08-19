import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tavily import TavilyClient
from .config import Config

class ModernResearchAgents:
    def __init__(self):
        self.groq_api_key = Config.GROQ_API_KEY
        self.tavily_api_key = Config.TAVILY_API_KEY
        
        if not self.groq_api_key or not self.tavily_api_key:
            raise ValueError("API keys not found in environment variables")
        
        self.llm = ChatGroq(
            api_key=self.groq_api_key,
            model_name=Config.GROQ_MODEL,
            temperature=0.1,
            max_tokens=4000
        )
        
        self.tavily = TavilyClient(api_key=self.tavily_api_key)
        
    def setup_research_agent(self):
        research_prompt = PromptTemplate(
            input_variables=["query", "search_results"],
            template="""You are an Expert Research Agent. Analyze this search data about: {query}

SEARCH RESULTS:
{search_results}

Extract:
1. Specific company names, funding amounts, recent developments
2. Key market players and leaders
3. Concrete statistics and growth data
4. Expert quotes and industry insights
5. Recent news and technological breakthroughs

Focus on factual, recent information. Prioritize Indian companies and current developments."""
        )
        
        chain = research_prompt | self.llm | StrOutputParser()
        return chain
    
    def setup_summarizer_agent(self):
        summarizer_prompt = PromptTemplate(
            input_variables=["research_content"],
            template="""Process this research content: {research_content}

Create structured summary:

## Company Profiles
- Company name, founding year, headquarters
- Core AI technology and healthcare focus
- Key products/services and recent funding

## Market Intelligence
- Market size, growth statistics
- Investment trends, key partnerships
- Technology applications and innovations

## Recent Developments
- Latest news, product launches
- Awards, recognitions, expansions

Include specific numbers, dates, and company names."""
        )
        
        chain = summarizer_prompt | self.llm | StrOutputParser()
        return chain
    
    def setup_critic_agent(self):
        critic_prompt = PromptTemplate(
            input_variables=["summary_content"],
            template="""Evaluate this content for accuracy: {summary_content}

Analyze:
- Information consistency and conflicts
- Data completeness and currency
- Source credibility and reliability
- Missing critical information

Provide reliability score (1-10) and improvement recommendations."""
        )
        
        chain = critic_prompt | self.llm | StrOutputParser()
        return chain
    
    def setup_writer_agent(self):
        writer_prompt = PromptTemplate(
            input_variables=["research_data", "summary", "critique"],
            template="""Create a comprehensive research report using:

RESEARCH: {research_data}
SUMMARY: {summary}
CRITIQUE: {critique}

Structure:

# Executive Summary
Brief overview of Indian AI healthcare startup ecosystem, key insights, and top performers.

# Top AI Healthcare Startups in India

For each company:
## [Company Name]
- **Founded:** Year, Location
- **Focus Area:** Healthcare AI application
- **Technology:** Core AI technologies
- **Funding:** Latest rounds, total raised, valuation
- **Products:** Main offerings
- **Recent News:** Latest developments

# Market Analysis
- **Market Size:** Current and projected figures
- **Growth Trends:** Investment patterns and statistics
- **Key Technologies:** Popular AI applications
- **Challenges:** Market obstacles and opportunities

# Investment Landscape
- **Funding Trends:** Recent investment patterns
- **Key Investors:** Major VCs and sources
- **Success Stories:** Notable achievements

# Future Outlook
- **Emerging Trends:** Next-gen technologies
- **Predictions:** Market forecasts
- **Opportunities:** Development areas

# References and Sources
List sources with clickable URLs and publication dates.

Use professional tone with specific data, figures, and company details."""
        )
        
        chain = writer_prompt | self.llm | StrOutputParser()
        return chain

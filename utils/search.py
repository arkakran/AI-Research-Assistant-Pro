from tavily import TavilyClient
from .config import Config

class TavilyRetrievalSystem:
    def __init__(self, tavily_api_key: str):
        self.tavily = TavilyClient(api_key=tavily_api_key)
        
    def advanced_search(self, query: str) -> str:
        try:
            # Comprehensive search with Indian business domains
            primary_response = self.tavily.search(
                query=query,
                search_depth=Config.TAVILY_SEARCH_DEPTH,
                max_results=Config.TAVILY_MAX_RESULTS,
                include_answer=True,
                include_raw_content=True,
                include_domains=[
                    "yourstory.com",
                    "economictimes.indiatimes.com", 
                    "techcrunch.com",
                    "inc42.com",
                    "entrackr.com",
                    "business-standard.com",
                    "livemint.com",
                    "startupnews.fyi",
                    "forbesindia.com",
                    "moneycontrol.com"
                ]
            )
            
            # Targeted searches
            targeted_searches = [
                f"{query} funding investment 2024 2025",
                f"{query} latest news recent developments",
                f"Indian AI healthcare market statistics"
            ]
            
            all_results = [self._format_response(primary_response)]
            
            for targeted_query in targeted_searches:
                try:
                    response = self.tavily.search(
                        query=targeted_query,
                        search_depth="basic",
                        max_results=5,
                        include_answer=True
                    )
                    all_results.append(self._format_response(response))
                except:
                    continue
            
            return "\n\n" + "="*50 + "\n\n".join(all_results)
            
        except Exception as e:
            raise Exception(f"Search failed: {str(e)}")
    
    def _format_response(self, response: dict) -> str:
        formatted = []
        
        if response.get('answer'):
            formatted.append(f"**INSIGHT:** {response['answer']}\n")
        
        if response.get('results'):
            for i, result in enumerate(response['results'], 1):
                formatted.append(f"**SOURCE {i}:** {result.get('title', 'No title')}")
                formatted.append(f"**URL:** {result.get('url', 'No URL')}")
                formatted.append(f"**CONTENT:** {result.get('content', 'No content')}")
                formatted.append("-" * 30)
        
        return "\n".join(formatted)

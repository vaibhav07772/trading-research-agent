"""
News & Sentiment Analysis Tools
"""
import os
from datetime import datetime
from typing import Dict, Any, List
from tavily import TavilyClient


def get_news(query: str, num_results: int = 5) -> Dict[str, Any]:
    """
    Get recent news articles using Tavily API
    
    Args:
        query: Search query (e.g., stock ticker or company name)
        num_results: Number of news articles to fetch
    
    Returns:
        Dictionary with news articles
    """
    try:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key:
            return {"error": "TAVILY_API_KEY not found in environment"}
        
        client = TavilyClient(api_key=tavily_api_key)
        
        # Search for news
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=num_results,
            include_domains=["reuters.com", "bloomberg.com", "cnbc.com", "marketwatch.com", 
                           "yahoo.com", "investing.com", "seekingalpha.com", "fool.com"]
        )
        
        articles = []
        for result in response.get("results", []):
            articles.append({
                "title": result.get("title", "N/A"),
                "url": result.get("url", "N/A"),
                "content": result.get("content", "N/A"),
                "score": result.get("score", 0),
                "published_date": result.get("published_date", "N/A")
            })
        
        return {
            "query": query,
            "num_articles": len(articles),
            "articles": articles,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "query": query,
            "timestamp": datetime.now().isoformat()
        }


def get_company_news(ticker: str, company_name: str = None) -> Dict[str, Any]:
    """
    Get company-specific news
    
    Args:
        ticker: Stock ticker symbol
        company_name: Optional company name for better search
    
    Returns:
        Dictionary with company news
    """
    try:
        query = f"{company_name or ticker} stock news earnings"
        return get_news(query, num_results=10)
    except Exception as e:
        return {
            "error": str(e),
            "ticker": ticker,
            "timestamp": datetime.now().isoformat()
        }


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Simple sentiment analysis (can be enhanced with ML models)
    
    Args:
        text: Text to analyze
    
    Returns:
        Dictionary with sentiment score
    """
    try:
        # Simple keyword-based sentiment (can be replaced with proper NLP model)
        positive_words = [
            "growth", "profit", "beat", "exceed", "surge", "rally", "bullish", 
            "upgrade", "outperform", "buy", "strong", "positive", "gain", "rise"
        ]
        negative_words = [
            "loss", "decline", "fall", "drop", "bearish", "downgrade", 
            "underperform", "sell", "weak", "negative", "crash", "plunge"
        ]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            sentiment_score = 0
            sentiment_label = "NEUTRAL"
        else:
            sentiment_score = (positive_count - negative_count) / total
            if sentiment_score > 0.2:
                sentiment_label = "POSITIVE"
            elif sentiment_score < -0.2:
                sentiment_label = "NEGATIVE"
            else:
                sentiment_label = "NEUTRAL"
        
        return {
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label,
            "positive_mentions": positive_count,
            "negative_mentions": negative_count,
            "text_length": len(text),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
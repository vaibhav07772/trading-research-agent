"""
Macro Economic Indicators Tools
"""
import os
from datetime import datetime
from typing import Dict, Any
from tavily import TavilyClient


def search_macro_indicators(indicator: str = "all") -> Dict[str, Any]:
    """
    Search for macroeconomic indicators and economic data
    
    Args:
        indicator: Specific indicator (e.g., 'inflation', 'gdp', 'interest rates') or 'all'
    
    Returns:
        Dictionary with macroeconomic data
    """
    try:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key:
            return {"error": "TAVILY_API_KEY not found in environment"}
        
        client = TavilyClient(api_key=tavily_api_key)
        
        # Build search query
        if indicator == "all":
            query = "US macroeconomic indicators 2026 inflation GDP interest rates unemployment"
        else:
            query = f"US {indicator} rate 2026 current value"
        
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_domains=["tradingeconomics.com", "investing.com", "forexfactory.com",
                           "fred.stlouisfed.org", "bls.gov", "bea.gov", "federalreserve.gov"]
        )
        
        # Extract key macro data
        macro_data = {
            "query": query,
            "indicators": [],
            "timestamp": datetime.now().isoformat()
        }
        
        for result in response.get("results", []):
            macro_data["indicators"].append({
                "title": result.get("title", "N/A"),
                "content": result.get("content", "N/A"),
                "url": result.get("url", "N/A"),
                "source": result.get("url", "").split("//")[-1].split("/")[0] if result.get("url") else "N/A"
            })
        
        return macro_data
    
    except Exception as e:
        return {
            "error": str(e),
            "indicator": indicator,
            "timestamp": datetime.now().isoformat()
        }


def get_fed_interest_rate() -> Dict[str, Any]:
    """
    Get current Federal Reserve interest rate
    
    Returns:
        Dictionary with interest rate data
    """
    try:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        client = TavilyClient(api_key=tavily_api_key)
        
        response = client.search(
            query="Federal Reserve interest rate 2026 current federal funds rate",
            search_depth="advanced",
            max_results=3,
            include_domains=["federalreserve.gov", "tradingeconomics.com", "investing.com"]
        )
        
        return {
            "indicator": "Federal Funds Rate",
            "data": response.get("results", []),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "indicator": "Federal Funds Rate",
            "timestamp": datetime.now().isoformat()
        }


def get_inflation_rate() -> Dict[str, Any]:
    """
    Get current US inflation rate (CPI)
    
    Returns:
        Dictionary with inflation data
    """
    try:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        client = TavilyClient(api_key=tavily_api_key)
        
        response = client.search(
            query="US inflation rate CPI 2026 current year over year",
            search_depth="advanced",
            max_results=3,
            include_domains=["bls.gov", "tradingeconomics.com", "investing.com"]
        )
        
        return {
            "indicator": "CPI Inflation Rate",
            "data": response.get("results", []),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "indicator": "CPI Inflation Rate",
            "timestamp": datetime.now().isoformat()
        }


def get_gdp_growth() -> Dict[str, Any]:
    """
    Get current US GDP growth rate
    
    Returns:
        Dictionary with GDP data
    """
    try:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        client = TavilyClient(api_key=tavily_api_key)
        
        response = client.search(
            query="US GDP growth rate 2026 quarterly annual",
            search_depth="advanced",
            max_results=3,
            include_domains=["bea.gov", "tradingeconomics.com", "investing.com"]
        )
        
        return {
            "indicator": "GDP Growth Rate",
            "data": response.get("results", []),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "indicator": "GDP Growth Rate",
            "timestamp": datetime.now().isoformat()
        }


def get_unemployment_rate() -> Dict[str, Any]:
    """
    Get current US unemployment rate
    
    Returns:
        Dictionary with unemployment data
    """
    try:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        client = TavilyClient(api_key=tavily_api_key)
        
        response = client.search(
            query="US unemployment rate 2026 current nonfarm payrolls",
            search_depth="advanced",
            max_results=3,
            include_domains=["bls.gov", "tradingeconomics.com", "investing.com"]
        )
        
        return {
            "indicator": "Unemployment Rate",
            "data": response.get("results", []),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "indicator": "Unemployment Rate",
            "timestamp": datetime.now().isoformat()
        }
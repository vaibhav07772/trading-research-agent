"""
Helper Utilities
"""
import os
from datetime import datetime
from typing import Dict, Any, Optional


def format_currency(value: float, currency: str = "USD") -> str:
    """
    Format number as currency
    
    Args:
        value: Numeric value
        currency: Currency symbol
    
    Returns:
        Formatted string
    """
    if value >= 1e12:
        return f"{currency}{value/1e12:.2f}T"
    elif value >= 1e9:
        return f"{currency}{value/1e9:.2f}B"
    elif value >= 1e6:
        return f"{currency}{value/1e6:.2f}M"
    elif value >= 1e3:
        return f"{currency}{value/1e3:.2f}K"
    else:
        return f"{currency}{value:.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format number as percentage
    
    Args:
        value: Decimal value (e.g., 0.05 for 5%)
        decimals: Number of decimal places
    
    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def parse_ticker(ticker: str) -> str:
    """
    Clean and validate ticker symbol
    
    Args:
        ticker: Raw ticker input
    
    Returns:
        Cleaned ticker symbol
    """
    if not ticker:
        return ""
    
    # Remove spaces and convert to uppercase
    ticker = ticker.strip().upper()
    
    # Remove special characters except hyphen
    ticker = ''.join(c for c in ticker if c.isalnum() or c == '-')
    
    return ticker


def get_timestamp() -> str:
    """
    Get current timestamp in ISO format
    
    Returns:
        ISO formatted timestamp
    """
    return datetime.now().isoformat()


def get_formatted_timestamp() -> str:
    """
    Get human-readable timestamp
    
    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def validate_api_keys() -> Dict[str, bool]:
    """
    Check if all required API keys are configured
    
    Returns:
        Dictionary with API key status
    """
    return {
        "google_api": bool(os.getenv("GOOGLE_API_KEY")),
        "groq_api": bool(os.getenv("GROQ_API_KEY")),
        "tavily_api": bool(os.getenv("TAVILY_API_KEY"))
    }


def calculate_risk_score(
    volatility: float,
    beta: float,
    debt_to_equity: float,
    pe_ratio: float
) -> Dict[str, Any]:
    """
    Calculate overall risk score based on multiple factors
    
    Args:
        volatility: Annualized volatility
        beta: Stock beta
        debt_to_equity: Debt to equity ratio
        pe_ratio: P/E ratio
    
    Returns:
        Dictionary with risk metrics
    """
    # Normalize factors (simplified scoring)
    volatility_score = min(volatility * 10, 10)  # Cap at 10
    beta_score = min(abs(beta - 1) * 10, 10)
    debt_score = min(debt_to_equity / 50, 10)
    pe_score = min(pe_ratio / 30, 10)
    
    # Weighted average
    overall_risk = (
        volatility_score * 0.3 +
        beta_score * 0.25 +
        debt_score * 0.25 +
        pe_score * 0.2
    )
    
    # Risk level
    if overall_risk < 3:
        risk_level = "LOW"
    elif overall_risk < 6:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
    
    return {
        "overall_risk_score": round(overall_risk, 2),
        "risk_level": risk_level,
        "volatility_score": round(volatility_score, 2),
        "beta_score": round(beta_score, 2),
        "debt_score": round(debt_score, 2),
        "valuation_score": round(pe_score, 2),
        "timestamp": get_timestamp()
    }


def determine_recommendation(
    fundamental_score: float,
    technical_score: float,
    sentiment_score: float,
    macro_score: float
) -> Dict[str, Any]:
    """
    Determine investment recommendation based on multiple scores
    
    Args:
        fundamental_score: -10 to 10
        technical_score: -10 to 10
        sentiment_score: -10 to 10
        macro_score: -10 to 10
    
    Returns:
        Dictionary with recommendation
    """
    # Weighted average
    overall_score = (
        fundamental_score * 0.35 +
        technical_score * 0.25 +
        sentiment_score * 0.2 +
        macro_score * 0.2
    )
    
    # Determine recommendation
    if overall_score >= 6:
        recommendation = "STRONG BUY"
        confidence = "HIGH"
    elif overall_score >= 3:
        recommendation = "BUY"
        confidence = "MEDIUM-HIGH"
    elif overall_score >= 0:
        recommendation = "HOLD"
        confidence = "MEDIUM"
    elif overall_score >= -3:
        recommendation = "SELL"
        confidence = "MEDIUM"
    else:
        recommendation = "STRONG SELL"
        confidence = "HIGH"
    
    return {
        "recommendation": recommendation,
        "overall_score": round(overall_score, 2),
        "confidence": confidence,
        "fundamental_score": round(fundamental_score, 2),
        "technical_score": round(technical_score, 2),
        "sentiment_score": round(sentiment_score, 2),
        "macro_score": round(macro_score, 2),
        "timestamp": get_timestamp()
    }
"""
Stock Data Tools - Get stock info, history, and fundamentals
"""
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


def get_stock_info(ticker: str) -> Dict[str, Any]:
    """
    Get fundamental stock information
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
    
    Returns:
        Dictionary with stock fundamental data
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            "ticker": ticker,
            "company_name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", 0),
            "current_price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
            "pe_ratio": info.get("trailingPE", 0),
            "forward_pe": info.get("forwardPE", 0),
            "peg_ratio": info.get("pegRatio", 0),
            "price_to_book": info.get("priceToBook", 0),
            "debt_to_equity": info.get("debtToEquity", 0),
            "roe": info.get("returnOnEquity", 0),
            "revenue_growth": info.get("revenueGrowth", 0),
            "earnings_growth": info.get("earningsGrowth", 0),
            "profit_margin": info.get("profitMargins", 0),
            "dividend_yield": info.get("dividendYield", 0),
            "beta": info.get("beta", 0),
            "52_week_high": info.get("fiftyTwoWeekHigh", 0),
            "52_week_low": info.get("fiftyTwoWeekLow", 0),
            "average_volume": info.get("averageVolume", 0),
            "recommendation": info.get("recommendationKey", "N/A"),
            "target_price": info.get("targetHighPrice", 0),
            "analyst_rating": info.get("recommendationMean", 0),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": str(e),
            "ticker": ticker,
            "timestamp": datetime.now().isoformat()
        }


def get_stock_history(ticker: str, period: str = "3mo") -> Dict[str, Any]:
    """
    Get historical stock price data and technical indicators
    
    Args:
        ticker: Stock ticker symbol
        period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
    
    Returns:
        Dictionary with historical data and technical summary
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return {"error": "No historical data available", "ticker": ticker}
        
        # Calculate technical indicators
        current_price = hist['Close'].iloc[-1]
        price_change = current_price - hist['Close'].iloc[0]
        price_change_pct = (price_change / hist['Close'].iloc[0]) * 100
        
        # Moving averages
        ma_20 = hist['Close'].rolling(window=20).mean().iloc[-1] if len(hist) >= 20 else current_price
        ma_50 = hist['Close'].rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else current_price
        ma_200 = hist['Close'].rolling(window=200).mean().iloc[-1] if len(hist) >= 200 else current_price
        
        # RSI (simplified)
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_value = rsi.iloc[-1] if not rsi.empty else 50
        
        # Volatility
        volatility = hist['Close'].pct_change().std() * (252 ** 0.5)
        
        return {
            "ticker": ticker,
            "period": period,
            "current_price": current_price,
            "period_start_price": hist['Close'].iloc[0],
            "period_high": hist['High'].max(),
            "period_low": hist['Low'].min(),
            "price_change": price_change,
            "price_change_percent": price_change_pct,
            "average_volume": hist['Volume'].mean(),
            "ma_20": ma_20,
            "ma_50": ma_50,
            "ma_200": ma_200,
            "rsi": rsi_value,
            "volatility": volatility,
            "trend": "BULLISH" if current_price > ma_50 else "BEARISH",
            "data_points": len(hist),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": str(e),
            "ticker": ticker,
            "timestamp": datetime.now().isoformat()
        }


def get_stock_key_statistics(ticker: str) -> Dict[str, Any]:
    """
    Get key statistics for a stock
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        Dictionary with key statistics
    """
    try:
        stock = yf.Ticker(ticker)
        
        return {
            "ticker": ticker,
            "enterprise_value": stock.info.get("enterpriseValue", 0),
            "trailing_pe": stock.info.get("trailingPE", 0),
            "forward_pe": stock.info.get("forwardPE", 0),
            "peg_ratio": stock.info.get("pegRatio", 0),
            "price_to_sales": stock.info.get("priceToSalesTrailing12Months", 0),
            "price_to_book": stock.info.get("priceToBook", 0),
            "enterprise_to_revenue": stock.info.get("enterpriseToRevenue", 0),
            "enterprise_to_ebitda": stock.info.get("enterpriseToEbitda", 0),
            "beta": stock.info.get("beta", 0),
            "52_week_change": stock.info.get("52WeekChange", 0),
            "shares_outstanding": stock.info.get("sharesOutstanding", 0),
            "float_shares": stock.info.get("floatShares", 0),
            "shares_short": stock.info.get("sharesShort", 0),
            "short_ratio": stock.info.get("shortRatio", 0),
            "short_percent_of_float": stock.info.get("shortPercentOfFloat", 0),
            "held_by_insiders": stock.info.get("heldPercentInsiders", 0),
            "held_by_institutions": stock.info.get("heldPercentInstitutions", 0),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": str(e),
            "ticker": ticker,
            "timestamp": datetime.now().isoformat()
        }
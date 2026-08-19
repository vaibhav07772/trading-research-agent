"""
Multi-Agent Trading Research System
FastAPI Backend
"""

import os
import traceback

from datetime import datetime
from typing import Any, Dict, Optional
from contextlib import asynccontextmanager

from dotenv import load_dotenv

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# FASTAPI IMPORTS
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


# ============================================================
# LANGCHAIN / LANGGRAPH IMPORTS
# ============================================================

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from google.api_core.exceptions import ResourceExhausted


# ============================================================
# CUSTOM TOOLS
# ============================================================

from tools import (
    get_stock_info,
    get_stock_history,
    get_news,
    search_macro_indicators,
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ResearchRequest(BaseModel):
    query: str
    ticker: Optional[str] = None
    model: str = "groq"


# ============================================================
# RESPONSE MODEL
# ============================================================

class ResearchResponse(BaseModel):
    success: bool
    response: str
    ticker: Optional[str] = None
    timestamp: str
    error: Optional[str] = None


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an expert Investment Research Analyst.

You analyze stocks using:
- Fundamental analysis
- Technical analysis
- News sentiment
- Macroeconomic conditions

You have access to the following tools:

1. get_stock_info
   Use this for company fundamentals, financial metrics,
   valuation information, and company data.

2. get_stock_history
   Use this for historical stock prices and technical analysis.

3. get_news
   Use this for recent company news and market sentiment.

4. search_macro_indicators
   Use this for macroeconomic information and economic context.

For stock-related requests, use the appropriate tools before
giving your final answer.

Return a clear and data-driven report with these sections:

## Executive Summary

## Fundamental Analysis

## Technical Analysis

## Sentiment & News

## Macro Environment

## Risk Assessment

## Final Recommendation

For the Final Recommendation provide:

- BUY / HOLD / SELL
- Reasons for the recommendation
- Target price only when supported by available data
- Suggested time horizon

Important Rules:

- Never invent financial data.
- Never invent stock prices.
- Never invent company metrics.
- Clearly say when information is unavailable.
- Base conclusions on tool results.
- Mention important risks.
- This system is for educational research only.
- Do not provide personalized financial advice.
"""


# ============================================================
# GET LLM
# ============================================================

def get_llm(provider: str):

    provider = provider.lower().strip()

    # --------------------------------------------------------
    # GROQ
    # --------------------------------------------------------

    if provider == "groq":

        key = os.getenv("GROQ_API_KEY")

        if not key:
            raise RuntimeError(
                "GROQ_API_KEY is missing in the .env file"
            )

        return ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            api_key=key,
        )

    # --------------------------------------------------------
    # GOOGLE GEMINI
    # --------------------------------------------------------

    if provider == "gemini":

        key = os.getenv("GOOGLE_API_KEY")

        if not key:
            raise RuntimeError(
                "GOOGLE_API_KEY is missing in the .env file"
            )

        return ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            temperature=0.2,
            google_api_key=key,
        )

    # --------------------------------------------------------
    # INVALID PROVIDER
    # --------------------------------------------------------

    raise ValueError(
        "model must be either 'groq' or 'gemini'"
    )


# ============================================================
# CREATE RESEARCH AGENT
# ============================================================

def create_research_agent(provider: str):

    llm = get_llm(provider)

    agent_tools = [
        get_stock_info,
        get_stock_history,
        get_news,
        search_macro_indicators,
    ]

    # For your installed LangGraph version
    agent = create_react_agent(
        model=llm,
        tools=agent_tools,
        state_modifier=SYSTEM_PROMPT,
        checkpointer=MemorySaver(),
    )

    return agent


# ============================================================
# CONVERT MESSAGE CONTENT TO TEXT
# ============================================================

def content_to_text(content: Any) -> str:

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, dict):

                if "text" in item:
                    parts.append(str(item["text"]))

                elif "content" in item:
                    parts.append(str(item["content"]))

                else:
                    parts.append(str(item))

            else:
                parts.append(str(item))

        return "\n".join(parts)

    return str(content)


# ============================================================
# RUN RESEARCH
# ============================================================

def run_research(
    query: str,
    ticker: Optional[str] = None,
    provider: str = "groq",
) -> Dict[str, Any]:

    if ticker:
        full_query = (
            f"{query}\n\n"
            f"Stock Ticker: {ticker}"
        )
    else:
        full_query = query

    thread_id = f"research_{ticker or 'general'}"

    try:

        agent = create_research_agent(provider)

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": full_query,
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            },
        )

        messages = result.get("messages", [])

        if messages:
            final_message = messages[-1]
            final_text = content_to_text(
                final_message.content
            )
        else:
            final_text = "No response was generated by the AI agent."

        return {
            "success": True,
            "response": final_text,
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "error": None,
        }

    except ResourceExhausted as exc:

        return {
            "success": False,
            "response": (
                "API quota or rate limit exceeded. "
                "Please wait and try again, or select "
                "the other LLM provider."
            ),
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "error": str(exc),
        }

    except Exception as exc:

        return {
            "success": False,
            "response": f"Error: {str(exc)}",
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "error": traceback.format_exc(),
        }


# ============================================================
# FASTAPI LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print()
    print("=" * 60)
    print("MULTI-AGENT TRADING RESEARCH SYSTEM")
    print("=" * 60)
    print("API Server Started Successfully")
    print("API URL:  http://127.0.0.1:8000")
    print("Docs URL: http://127.0.0.1:8000/docs")
    print("Health:   http://127.0.0.1:8000/health")
    print("=" * 60)
    print()

    yield

    print()
    print("=" * 60)
    print("Trading Research API stopped")
    print("=" * 60)


# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="Multi-Agent Trading Research System",
    description=(
        "Fundamental + Technical + Sentiment + "
        "Macro Analysis using AI Agents"
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "status": "online",
        "service": "trading-research",
        "timestamp": datetime.now().isoformat(),
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "apis": {
            "groq": bool(os.getenv("GROQ_API_KEY")),
            "google": bool(os.getenv("GOOGLE_API_KEY")),
            "tavily": bool(os.getenv("TAVILY_API_KEY")),
        },
        "timestamp": datetime.now().isoformat(),
    }


# ============================================================
# RESEARCH API ENDPOINT
# ============================================================

@app.post(
    "/research",
    response_model=ResearchResponse,
)
def research(request: ResearchRequest):

    result = run_research(
        query=request.query,
        ticker=request.ticker,
        provider=request.model,
    )

    if not result["success"]:

        error_message = result.get(
            "error",
            ""
        ).lower()

        if (
            "quota" in error_message
            or "resource exhausted" in error_message
            or "rate limit" in error_message
        ):
            status_code = 429
        else:
            status_code = 500

        raise HTTPException(
            status_code=status_code,
            detail=result.get(
                "error",
                result["response"],
            ),
        )

    return ResearchResponse(**result)


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
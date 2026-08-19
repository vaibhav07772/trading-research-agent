"""
Multi-Agent Trading Research System - Streamlit Frontend
Beautiful UI for investment research
"""
import os
import requests
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🤖 Multi-Agent Trading Research",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .report-box {
        background-color: #f8f9fa;
        border-left: 5px solid #1f77b4;
        padding: 1.5rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border: none;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


# ==================== Sidebar ====================

with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
    st.markdown("### ⚙️ Configuration")
    
    # API Status
    st.markdown("#### 🔑 API Status")
    google_status = "✅" if os.getenv("GOOGLE_API_KEY") else "❌"
    groq_status = "✅" if os.getenv("GROQ_API_KEY") else "❌"
    tavily_status = "✅" if os.getenv("TAVILY_API_KEY") else "❌"
    
    st.write(f"{google_status} Google Gemini API")
    st.write(f"{groq_status} Groq API")
    st.write(f"{tavily_status} Tavily API")
    
    st.divider()
    
    # Model selection
    model_provider = st.selectbox(
        "🤖 Select LLM Provider",
        options=["gemini", "groq"],
        format_func=lambda x: "Google Gemini 2.0 Flash" if x == "gemini" else "Groq Llama 3.3 70B"
    )
    
    st.divider()
    
    # Info
    st.markdown("""
    ### 📊 Agent Team
    
    - 👤 **Coordinator** - Orchestrates analysis
    - 📊 **Fundamental Analyst** - Company metrics
    - 📈 **Technical Analyst** - Price trends
    - 📰 **Sentiment Analyst** - News & mood
    - 🌍 **Macro Economist** - Economic context
    """)
    
    st.divider()
    
    # Links
    st.markdown("""
    ### 🔗 Resources
    
    - [API Documentation](http://localhost:8000/docs)
    - [Health Check](http://localhost:8000/health)
    """)


# ==================== Main Content ====================

# Header
st.markdown('<p class="main-header">🤖 Multi-Agent Trading Research System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Fundamental + Technical + Sentiment + Macro Analysis — All in One</p>', unsafe_allow_html=True)

st.divider()

# Agent cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="agent-card">
        <h3 style="margin:0; font-size:1.5rem;">📊</h3>
        <p style="margin:0.5rem 0 0 0; font-size:0.9rem;">Fundamental<br>Analyst</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card">
        <h3 style="margin:0; font-size:1.5rem;">📈</h3>
        <p style="margin:0.5rem 0 0 0; font-size:0.9rem;">Technical<br>Analyst</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="agent-card">
        <h3 style="margin:0; font-size:1.5rem;">📰</h3>
        <p style="margin:0.5rem 0 0 0; font-size:0.9rem;">Sentiment<br>Analyst</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="agent-card">
        <h3 style="margin:0; font-size:1.5rem;">🌍</h3>
        <p style="margin:0.5rem 0 0 0; font-size:0.9rem;">Macro<br>Economist</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==================== Input Form ====================

st.markdown("### 🔍 Research Query")

with st.form("research_form"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Research Question",
            placeholder="e.g., Analyze this stock for long-term investment",
            label_visibility="collapsed"
        )
    
    with col2:
        ticker = st.text_input(
            "Ticker (optional)",
            placeholder="e.g., AAPL",
            label_visibility="collapsed"
        )
    
    submitted = st.form_submit_button("🚀 Run Research", use_container_width=True)

# ==================== Process Research ====================

if submitted:
    if not query:
        st.error("❌ Please enter a research question")
    else:
        with st.spinner("🔍 AI agents are analyzing... This may take 30-60 seconds."):
            try:
                # Call FastAPI backend
                backend_url = "http://localhost:8000/research"
                
                payload = {
                    "query": query,
                    "ticker": ticker if ticker else None,
                    "model": model_provider
                }
                
                response = requests.post(backend_url, json=payload, timeout=120)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display success
                    st.success("✅ Research complete!")
                    
                    # Display report
                    st.markdown("### 📄 Research Report")
                    
                    st.markdown("""
                    <div class="report-box">
                    """, unsafe_allow_html=True)
                    
                    # Parse and display the report
                    report_text = result["response"]
                    st.markdown(report_text)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Metadata
                    with st.expander("📊 Report Metadata"):
                        st.json({
                            "ticker": result.get("ticker"),
                            "timestamp": result.get("timestamp"),
                            "model_used": model_provider,
                            "query": query
                        })
                    
                    # Download button
                    st.download_button(
                        label="💾 Download Report",
                        data=report_text,
                        file_name=f"research_report_{ticker or 'general'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                    
                else:
                    # Handle error
                    error_detail = response.json().get("detail", "Unknown error")
                    st.error(f"❌ Error: {error_detail}")
                    
                    if "Rate limit" in error_detail:
                        st.info("💡 Tip: You've hit the API rate limit. Wait 1-2 minutes and try again, or switch to Groq LLM in the sidebar.")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend server. Make sure FastAPI is running on http://localhost:8000")
                st.info("💡 Run: `python main.py` in a separate terminal")
            
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. The analysis is taking longer than expected.")
                st.info("💡 Try again or use a simpler query")
            
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

# ==================== Footer ====================

st.divider()

st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Built with LangChain • LangGraph • DeepAgents • FastAPI • Streamlit</p>
    <p style="font-size: 0.8rem;">⚠️ This is for educational purposes only. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)
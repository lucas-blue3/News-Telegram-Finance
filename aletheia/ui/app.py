"""
Main Streamlit application for the Aletheia dashboard.
"""

import os
import json
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from pyvis.network import Network

from aletheia.agents.strategist import StrategistAgent
from aletheia.memory.relational_store import RelationalMemory


# Set page configuration
st.set_page_config(
    page_title="Aletheia - Market Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "strategist_agent" not in st.session_state:
    st.session_state.strategist_agent = StrategistAgent()

if "db" not in st.session_state:
    # Use SQLite for local development
    st.session_state.db = RelationalMemory(db_url="sqlite:///data/aletheia.db")
    # Create tables if they don't exist
    st.session_state.db.create_tables()


# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #424242;
        margin-bottom: 0.5rem;
    }
    
    .card {
        background-color: #f9f9f9;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1E88E5;
    }
    
    .risk-card {
        background-color: #fff3f3;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #E53935;
    }
    
    .narrative-card {
        background-color: #f3f8ff;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #7986CB;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
    }
    
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    
    .bot-message {
        background-color: #F5F5F5;
        border-left: 4px solid #9E9E9E;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown('<div class="main-header">Aletheia</div>', unsafe_allow_html=True)
    st.markdown("### Market Intelligence Platform")
    
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["Dashboard", "Market Analysis", "Risk Assessment", "Chat with Aletheia"]
    )
    
    st.markdown("---")
    
    # Quick filters
    st.markdown("### Quick Filters")
    
    asset_filter = st.selectbox(
        "Asset",
        ["All", "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "BTC-USD", "ETH-USD"]
    )
    
    time_range = st.selectbox(
        "Time Range",
        ["1D", "1W", "1M", "3M", "6M", "1Y", "YTD"]
    )
    
    st.markdown("---")
    
    # About
    st.markdown("### About")
    st.markdown(
        "Aletheia is an AI-powered cognitive ecosystem for market intelligence and alpha generation."
    )
    st.markdown(
        "Built with LangChain, LangGraph, and DeepSeek."
    )


# Main content
if page == "Dashboard":
    st.markdown('<div class="main-header">Market Intelligence Dashboard</div>', unsafe_allow_html=True)
    
    # Top row - Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric(
            label="S&P 500",
            value="5,123.45",
            delta="0.75%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric(
            label="NASDAQ",
            value="16,234.56",
            delta="1.2%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric(
            label="10Y Treasury",
            value="3.85%",
            delta="-0.05%",
            delta_color="inverse"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric(
            label="VIX",
            value="18.75",
            delta="-2.3%",
            delta_color="inverse"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Middle row - Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="sub-header">Market Performance</div>', unsafe_allow_html=True)
        
        # Sample data for the chart
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        sp500 = pd.DataFrame({
            'Date': dates,
            'S&P 500': [4800 + i * 10 + (i % 5) * 20 for i in range(len(dates))],
            'NASDAQ': [15000 + i * 30 + (i % 7) * 50 for i in range(len(dates))],
            'DJIA': [37000 + i * 20 + (i % 6) * 30 for i in range(len(dates))]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sp500['Date'], y=sp500['S&P 500'], mode='lines', name='S&P 500'))
        fig.add_trace(go.Scatter(x=sp500['Date'], y=sp500['NASDAQ'], mode='lines', name='NASDAQ'))
        fig.add_trace(go.Scatter(x=sp500['Date'], y=sp500['DJIA'], mode='lines', name='DJIA'))
        
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="Date",
            yaxis_title="Index Value",
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="sub-header">Sector Performance (1M)</div>', unsafe_allow_html=True)
        
        # Sample data for the chart
        sectors = ['Technology', 'Healthcare', 'Financials', 'Consumer Discretionary', 
                   'Communication Services', 'Industrials', 'Consumer Staples', 
                   'Energy', 'Utilities', 'Materials', 'Real Estate']
        performance = [8.5, 3.2, -1.5, 5.7, 4.2, 2.1, -0.8, -3.5, 1.2, 0.5, -2.3]
        
        sector_df = pd.DataFrame({
            'Sector': sectors,
            'Performance (%)': performance
        })
        
        fig = px.bar(
            sector_df,
            x='Performance (%)',
            y='Sector',
            orientation='h',
            color='Performance (%)',
            color_continuous_scale=['#EF5350', '#FFEE58', '#66BB6A'],
            range_color=[-5, 10]
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="Performance (%)",
            yaxis_title="",
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Bottom row - Narratives and Risks
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="sub-header">Dominant Market Narratives</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="narrative-card">
            <h4>Fed Policy Pivot Expectations</h4>
            <p>Markets are increasingly pricing in multiple rate cuts for 2025 as inflation continues to moderate and economic growth shows signs of slowing.</p>
            <p><strong>Confidence:</strong> High</p>
        </div>
        
        <div class="narrative-card">
            <h4>AI Investment Supercycle</h4>
            <p>The ongoing investment in AI infrastructure and applications continues to drive tech sector outperformance, with expectations of significant productivity gains.</p>
            <p><strong>Confidence:</strong> Medium</p>
        </div>
        
        <div class="narrative-card">
            <h4>Geopolitical Tensions Impact on Supply Chains</h4>
            <p>Escalating conflicts and trade restrictions are forcing companies to reconsider global supply chains, with implications for inflation and margins.</p>
            <p><strong>Confidence:</strong> Medium</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="sub-header">Key Risk Factors</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="risk-card">
            <h4>Persistent Inflation</h4>
            <p>Despite recent moderation, structural factors including deglobalization and labor market tightness could keep inflation above target.</p>
            <p><strong>Probability:</strong> Medium | <strong>Impact:</strong> High</p>
        </div>
        
        <div class="risk-card">
            <h4>Tech Valuation Correction</h4>
            <p>Current valuations in the technology sector, particularly AI-related companies, may be pricing in unrealistic growth expectations.</p>
            <p><strong>Probability:</strong> Medium | <strong>Impact:</strong> High</p>
        </div>
        
        <div class="risk-card">
            <h4>Escalation in Middle East Conflict</h4>
            <p>Widening of the conflict could disrupt oil supplies and global shipping routes, leading to energy price spikes and supply chain disruptions.</p>
            <p><strong>Probability:</strong> Low | <strong>Impact:</strong> Very High</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "Market Analysis":
    st.markdown('<div class="main-header">Market Analysis</div>', unsafe_allow_html=True)
    
    # Asset selector
    selected_asset = st.selectbox(
        "Select Asset",
        ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "BTC-USD", "ETH-USD", "SPY", "QQQ"]
    )
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["Price Analysis", "Sentiment Analysis", "Narratives", "Causal Relationships"])
    
    with tab1:
        st.markdown("### Price Analysis")
        
        # Sample price data
        dates = pd.date_range(start=datetime.now() - timedelta(days=180), end=datetime.now(), freq='D')
        price_data = pd.DataFrame({
            'Date': dates,
            'Close': [150 + i * 0.1 + (i % 20) * 0.5 - (i % 50) * 0.3 for i in range(len(dates))],
            'Volume': [10000000 + (i % 10) * 1000000 for i in range(len(dates))]
        })
        
        # Price chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=price_data['Date'], y=price_data['Close'], mode='lines', name='Price'))
        
        # Add moving averages
        price_data['MA50'] = price_data['Close'].rolling(window=50).mean()
        price_data['MA200'] = price_data['Close'].rolling(window=200).mean()
        
        fig.add_trace(go.Scatter(x=price_data['Date'], y=price_data['MA50'], mode='lines', name='50-Day MA', line=dict(dash='dash')))
        fig.add_trace(go.Scatter(x=price_data['Date'], y=price_data['MA200'], mode='lines', name='200-Day MA', line=dict(dash='dash')))
        
        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Technical indicators
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Technical Indicators")
            st.markdown("""
            - **RSI (14):** 58.3 (Neutral)
            - **MACD:** Bullish Crossover
            - **Bollinger Bands:** Within Bands
            - **Stochastic Oscillator:** 75.2 (Approaching Overbought)
            """)
        
        with col2:
            st.markdown("#### Key Support/Resistance")
            st.markdown("""
            - **Strong Resistance:** $175.50
            - **Resistance:** $168.20
            - **Support:** $160.80
            - **Strong Support:** $155.30
            """)
        
        with col3:
            st.markdown("#### Volume Analysis")
            st.markdown("""
            - **Avg. Daily Volume (10D):** 12.5M
            - **Avg. Daily Volume (3M):** 15.2M
            - **Volume Trend:** Decreasing
            - **Unusual Volume Days:** 2 in last 30 days
            """)
    
    with tab2:
        st.markdown("### Sentiment Analysis")
        
        # Sample sentiment data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        sentiment_data = pd.DataFrame({
            'Date': dates,
            'News Sentiment': [0.2 + (i % 10) * 0.05 - (i % 7) * 0.07 for i in range(len(dates))],
            'Social Media Sentiment': [0.1 + (i % 8) * 0.06 - (i % 5) * 0.08 for i in range(len(dates))],
            'Overall Sentiment': [0.15 + (i % 9) * 0.055 - (i % 6) * 0.075 for i in range(len(dates))]
        })
        
        # Sentiment chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sentiment_data['Date'], y=sentiment_data['News Sentiment'], mode='lines', name='News Sentiment'))
        fig.add_trace(go.Scatter(x=sentiment_data['Date'], y=sentiment_data['Social Media Sentiment'], mode='lines', name='Social Media Sentiment'))
        fig.add_trace(go.Scatter(x=sentiment_data['Date'], y=sentiment_data['Overall Sentiment'], mode='lines', name='Overall Sentiment', line=dict(width=3)))
        
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="Date",
            yaxis_title="Sentiment Score",
            yaxis=dict(range=[-0.5, 0.5]),
            template="plotly_white"
        )
        
        # Add a horizontal line at y=0
        fig.add_shape(
            type="line",
            x0=sentiment_data['Date'].min(),
            y0=0,
            x1=sentiment_data['Date'].max(),
            y1=0,
            line=dict(color="gray", width=1, dash="dash")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Sentiment dimensions
        st.markdown("#### Sentiment Dimensions")
        
        sentiment_dimensions = pd.DataFrame({
            'Dimension': ['Optimism/Pessimism', 'Confidence/Uncertainty', 'Fear/Greed', 'Excitement/Boredom', 'Surprise/Expectation'],
            'Score': [2.5, -1.2, 0.8, 1.5, -0.5]
        })
        
        fig = px.bar(
            sentiment_dimensions,
            x='Score',
            y='Dimension',
            orientation='h',
            color='Score',
            color_continuous_scale=['#EF5350', '#FFEE58', '#66BB6A'],
            range_color=[-5, 5]
        )
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="Score (-5 to +5)",
            yaxis_title="",
            template="plotly_white"
        )
        
        # Add a vertical line at x=0
        fig.add_shape(
            type="line",
            x0=0,
            y0=-0.5,
            x1=0,
            y1=4.5,
            line=dict(color="gray", width=1, dash="dash")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key phrases
        st.markdown("#### Key Sentiment Phrases")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Positive Sentiment:**")
            st.markdown("""
            - "Strong product pipeline"
            - "Exceeding analyst expectations"
            - "Market share gains"
            - "Robust cash flow"
            - "Strategic acquisitions"
            """)
        
        with col2:
            st.markdown("**Negative Sentiment:**")
            st.markdown("""
            - "Regulatory challenges"
            - "Margin pressure"
            - "Increasing competition"
            - "Supply chain constraints"
            - "Valuation concerns"
            """)
    
    with tab3:
        st.markdown("### Market Narratives")
        
        # Dominant narrative
        st.markdown('<div class="narrative-card">', unsafe_allow_html=True)
        st.markdown("#### Dominant Narrative: AI Integration Driving Growth")
        st.markdown("""
        The company's aggressive integration of AI across its product lineup is seen as a key differentiator and growth driver. Recent product announcements have highlighted AI features that analysts believe will drive upgrade cycles and expand market share.
        
        **Supporting Evidence:**
        - Recent product launches featuring advanced AI capabilities
        - Positive analyst reports highlighting AI strategy
        - Management's increased R&D allocation to AI initiatives
        - Partnerships with leading AI research institutions
        
        **Market Implications:**
        - Potential for margin expansion through premium pricing
        - Accelerated replacement cycles
        - Competitive advantage in key market segments
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Competing narratives
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="narrative-card">', unsafe_allow_html=True)
            st.markdown("#### Competing Narrative: Valuation Concerns")
            st.markdown("""
            Despite strong fundamentals, the current valuation may be pricing in unrealistic growth expectations. The stock's premium multiple relative to historical averages and peers suggests limited upside potential.
            
            **Supporting Evidence:**
            - P/E ratio 35% above 5-year average
            - Recent insider selling
            - Slowing growth in key markets
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="narrative-card">', unsafe_allow_html=True)
            st.markdown("#### Emerging Narrative: Regulatory Headwinds")
            st.markdown("""
            Increasing regulatory scrutiny across global markets could impact growth strategies and increase compliance costs. Recent antitrust investigations and data privacy concerns represent growing risks.
            
            **Supporting Evidence:**
            - Recent regulatory filings in EU and US
            - Increased mentions of regulatory risks in earnings calls
            - Similar companies facing significant fines
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Narrative shifts
        st.markdown("#### Narrative Shifts Over Time")
        
        # Sample data for narrative shifts
        narrative_shifts = pd.DataFrame({
            'Date': pd.date_range(start=datetime.now() - timedelta(days=180), end=datetime.now(), freq='MS'),
            'Growth Story': [0.6, 0.65, 0.7, 0.65, 0.55, 0.5, 0.45],
            'AI Integration': [0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7],
            'Valuation Concerns': [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4],
            'Regulatory Risks': [0.05, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
        })
        
        fig = go.Figure()
        for column in narrative_shifts.columns[1:]:
            fig.add_trace(go.Scatter(x=narrative_shifts['Date'], y=narrative_shifts[column], mode='lines+markers', name=column))
        
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="Date",
            yaxis_title="Narrative Strength",
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Causal Relationships")
        
        # Create a network graph of causal relationships
        st.markdown("#### Causal Relationship Network")
        
        # Create a network graph
        net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="#000000")
        
        # Add nodes
        net.add_node(1, label="AI Investment", title="Increased R&D in AI technologies", color="#7986CB")
        net.add_node(2, label="Product Innovation", title="New product features and capabilities", color="#7986CB")
        net.add_node(3, label="Customer Satisfaction", title="Improved customer experience and loyalty", color="#7986CB")
        net.add_node(4, label="Market Share", title="Percentage of total market captured", color="#7986CB")
        net.add_node(5, label="Revenue Growth", title="Year-over-year revenue increase", color="#66BB6A")
        net.add_node(6, label="Margin Expansion", title="Improved profit margins", color="#66BB6A")
        net.add_node(7, label="Stock Performance", title="Share price appreciation", color="#66BB6A")
        net.add_node(8, label="Regulatory Scrutiny", title="Increased attention from regulators", color="#EF5350")
        net.add_node(9, label="Competitive Response", title="Actions taken by competitors", color="#EF5350")
        net.add_node(10, label="Market Valuation", title="P/E and other valuation metrics", color="#FFEE58")
        
        # Add edges (connections)
        net.add_edge(1, 2, value=5, title="Strong: AI drives product innovation")
        net.add_edge(2, 3, value=4, title="Strong: Better products improve satisfaction")
        net.add_edge(3, 4, value=3, title="Moderate: Satisfied customers increase market share")
        net.add_edge(4, 5, value=5, title="Strong: Market share drives revenue")
        net.add_edge(2, 6, value=3, title="Moderate: Innovation enables premium pricing")
        net.add_edge(5, 7, value=4, title="Strong: Revenue growth drives stock performance")
        net.add_edge(6, 7, value=4, title="Strong: Margin expansion drives stock performance")
        net.add_edge(1, 8, value=2, title="Weak: AI investment attracts regulatory attention")
        net.add_edge(2, 9, value=3, title="Moderate: Innovation triggers competitive response")
        net.add_edge(9, 4, value=2, title="Weak: Competition impacts market share", color="#EF5350")
        net.add_edge(7, 10, value=5, title="Strong: Performance affects valuation")
        net.add_edge(8, 10, value=2, title="Weak: Regulation impacts valuation", color="#EF5350")
        
        # Generate the graph
        net.repulsion(node_distance=100, spring_length=200)
        path = "aletheia/ui/components/causal_network.html"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        net.save_graph(path)
        
        # Display the graph
        with open(path, "r") as f:
            html = f.read()
            st.components.v1.html(html, height=550)
        
        # Key causal relationships
        st.markdown("#### Key Causal Relationships")
        
        causal_data = [
            {"cause": "AI Investment", "effect": "Product Innovation", "strength": "Strong", "confidence": "High"},
            {"cause": "Product Innovation", "effect": "Customer Satisfaction", "strength": "Strong", "confidence": "High"},
            {"cause": "Market Share Gains", "effect": "Revenue Growth", "strength": "Strong", "confidence": "High"},
            {"cause": "Innovation", "effect": "Competitive Response", "strength": "Moderate", "confidence": "Medium"},
            {"cause": "Regulatory Scrutiny", "effect": "Valuation Multiple", "strength": "Weak", "confidence": "Medium"}
        ]
        
        causal_df = pd.DataFrame(causal_data)
        
        st.dataframe(causal_df, use_container_width=True)

elif page == "Risk Assessment":
    st.markdown('<div class="main-header">Risk Assessment</div>', unsafe_allow_html=True)
    
    # Risk overview
    st.markdown("### Risk Overview")
    
    # Risk heatmap
    st.markdown("#### Risk Heatmap")
    
    # Sample data for risk heatmap
    risks = [
        {"Risk": "Regulatory Changes", "Probability": 3, "Impact": 4, "Category": "Regulatory"},
        {"Risk": "Competitive Disruption", "Probability": 2, "Impact": 5, "Category": "Market"},
        {"Risk": "Supply Chain Disruption", "Probability": 3, "Impact": 3, "Category": "Operational"},
        {"Risk": "Cybersecurity Breach", "Probability": 2, "Impact": 5, "Category": "Technology"},
        {"Risk": "Talent Retention", "Probability": 4, "Impact": 3, "Category": "Organizational"},
        {"Risk": "Product Failure", "Probability": 1, "Impact": 5, "Category": "Product"},
        {"Risk": "Currency Fluctuation", "Probability": 4, "Impact": 2, "Category": "Financial"},
        {"Risk": "Geopolitical Tension", "Probability": 3, "Impact": 4, "Category": "Geopolitical"},
        {"Risk": "Inflation Persistence", "Probability": 3, "Impact": 3, "Category": "Economic"},
        {"Risk": "Interest Rate Hikes", "Probability": 2, "Impact": 4, "Category": "Economic"}
    ]
    
    risk_df = pd.DataFrame(risks)
    
    # Create a bubble chart for the risk heatmap
    fig = px.scatter(
        risk_df,
        x="Probability",
        y="Impact",
        size=[4] * len(risk_df),  # Constant size for all bubbles
        color="Category",
        hover_name="Risk",
        text="Risk",
        size_max=60,
        range_x=[0, 5],
        range_y=[0, 5]
    )
    
    # Update layout
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Probability",
        yaxis_title="Impact",
        template="plotly_white"
    )
    
    # Add grid lines to create the risk matrix
    fig.add_shape(type="line", x0=0, y0=3, x1=5, y1=3, line=dict(color="gray", width=1, dash="dash"))
    fig.add_shape(type="line", x0=3, y0=0, x1=3, y1=5, line=dict(color="gray", width=1, dash="dash"))
    
    # Add risk zones
    fig.add_shape(type="rect", x0=0, y0=0, x1=3, y1=3, fillcolor="green", opacity=0.1, line_width=0)
    fig.add_shape(type="rect", x0=3, y0=0, x1=5, y1=3, fillcolor="yellow", opacity=0.1, line_width=0)
    fig.add_shape(type="rect", x0=0, y0=3, x1=3, y1=5, fillcolor="yellow", opacity=0.1, line_width=0)
    fig.add_shape(type="rect", x0=3, y0=3, x1=5, y1=5, fillcolor="red", opacity=0.1, line_width=0)
    
    # Add annotations for risk zones
    fig.add_annotation(x=1.5, y=1.5, text="Low Risk", showarrow=False, font=dict(color="darkgreen"))
    fig.add_annotation(x=4, y=1.5, text="Medium Risk", showarrow=False, font=dict(color="darkorange"))
    fig.add_annotation(x=1.5, y=4, text="Medium Risk", showarrow=False, font=dict(color="darkorange"))
    fig.add_annotation(x=4, y=4, text="High Risk", showarrow=False, font=dict(color="darkred"))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk details
    st.markdown("### Key Risk Factors")
    
    tab1, tab2, tab3 = st.tabs(["High Impact Risks", "Emerging Risks", "Black Swan Scenarios"])
    
    with tab1:
        st.markdown("#### High Impact Risks")
        
        st.markdown("""
        <div class="risk-card">
            <h4>Competitive Disruption</h4>
            <p><strong>Description:</strong> Emergence of disruptive competitors with superior technology or business models that could erode market share.</p>
            <p><strong>Probability:</strong> Medium (2/5) | <strong>Impact:</strong> Very High (5/5)</p>
            <p><strong>Early Warning Indicators:</strong></p>
            <ul>
                <li>Increasing customer acquisition costs</li>
                <li>Loss of key customers to competitors</li>
                <li>Emergence of startups with significant funding in the space</li>
            </ul>
            <p><strong>Mitigation Strategies:</strong></p>
            <ul>
                <li>Accelerate R&D in key technology areas</li>
                <li>Strategic acquisitions of emerging competitors</li>
                <li>Enhance customer loyalty programs</li>
            </ul>
        </div>
        
        <div class="risk-card">
            <h4>Cybersecurity Breach</h4>
            <p><strong>Description:</strong> Major data breach or system compromise affecting customer data or intellectual property.</p>
            <p><strong>Probability:</strong> Medium (2/5) | <strong>Impact:</strong> Very High (5/5)</p>
            <p><strong>Early Warning Indicators:</strong></p>
            <ul>
                <li>Increased attempted breaches detected by security systems</li>
                <li>Similar breaches at peer companies</li>
                <li>Emergence of new attack vectors in the wild</li>
            </ul>
            <p><strong>Mitigation Strategies:</strong></p>
            <ul>
                <li>Enhance security infrastructure and protocols</li>
                <li>Regular penetration testing and security audits</li>
                <li>Cyber insurance coverage</li>
                <li>Employee security awareness training</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("#### Emerging Risks")
        
        st.markdown("""
        <div class="risk-card">
            <h4>AI Regulation</h4>
            <p><strong>Description:</strong> Emerging regulatory frameworks specifically targeting AI technologies could impact product development and deployment.</p>
            <p><strong>Probability:</strong> High (4/5) | <strong>Impact:</strong> Medium (3/5)</p>
            <p><strong>Trend:</strong> Increasing</p>
            <p><strong>Key Developments:</strong></p>
            <ul>
                <li>EU AI Act implementation timeline accelerating</li>
                <li>US federal agencies developing AI regulatory frameworks</li>
                <li>Industry self-regulation initiatives gaining traction</li>
            </ul>
        </div>
        
        <div class="risk-card">
            <h4>Talent War Escalation</h4>
            <p><strong>Description:</strong> Intensifying competition for specialized talent, particularly in AI, cybersecurity, and advanced engineering.</p>
            <p><strong>Probability:</strong> High (4/5) | <strong>Impact:</strong> Medium (3/5)</p>
            <p><strong>Trend:</strong> Increasing</p>
            <p><strong>Key Developments:</strong></p>
            <ul>
                <li>Compensation packages for specialized roles increasing 20%+ YoY</li>
                <li>Employee turnover in key departments above industry average</li>
                <li>Competitors establishing research centers in new geographic locations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("#### Black Swan Scenarios")
        
        st.markdown("""
        <div class="risk-card">
            <h4>Taiwan Semiconductor Disruption</h4>
            <p><strong>Description:</strong> Major disruption to semiconductor production in Taiwan due to geopolitical conflict or natural disaster.</p>
            <p><strong>Probability:</strong> Very Low (1/5) | <strong>Impact:</strong> Catastrophic (5/5)</p>
            <p><strong>Potential Consequences:</strong></p>
            <ul>
                <li>Severe global chip shortage lasting 12-24 months</li>
                <li>Inability to manufacture key products</li>
                <li>Massive price increases for available components</li>
                <li>Accelerated reshoring of semiconductor manufacturing</li>
            </ul>
        </div>
        
        <div class="risk-card">
            <h4>Quantum Computing Breakthrough</h4>
            <p><strong>Description:</strong> Unexpected breakthrough in quantum computing that renders current encryption methods vulnerable.</p>
            <p><strong>Probability:</strong> Very Low (1/5) | <strong>Impact:</strong> Very High (5/5)</p>
            <p><strong>Potential Consequences:</strong></p>
            <ul>
                <li>Immediate vulnerability of secure communications and data</li>
                <li>Need for rapid transition to quantum-resistant encryption</li>
                <li>Potential compromise of intellectual property</li>
                <li>Regulatory mandates for quantum-safe security</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Geopolitical risk assessment
    st.markdown("### Geopolitical Risk Assessment")
    
    # World map of geopolitical risks
    st.markdown("#### Global Risk Map")
    
    # Sample data for geopolitical risks
    geo_risks = pd.DataFrame({
        'country': ['United States', 'China', 'Russia', 'Germany', 'Japan', 'India', 'Brazil', 'United Kingdom', 'France', 'Italy', 'Canada', 'South Korea', 'Australia', 'Mexico', 'Indonesia', 'Turkey', 'Saudi Arabia', 'Switzerland', 'Taiwan', 'Netherlands'],
        'risk_score': [3.2, 4.5, 4.8, 2.8, 3.0, 3.7, 3.5, 3.1, 3.2, 3.4, 2.5, 3.6, 2.7, 3.8, 3.9, 4.2, 4.0, 2.0, 4.7, 2.6]
    })
    
    fig = px.choropleth(
        geo_risks,
        locations="country",
        locationmode="country names",
        color="risk_score",
        hover_name="country",
        color_continuous_scale="Reds",
        range_color=[1, 5],
        title="Geopolitical Risk Score (1-5)"
    )
    
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        coloraxis_colorbar=dict(title="Risk Score"),
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Regional risk factors
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### High-Risk Regions")
        
        st.markdown("""
        <div class="risk-card">
            <h4>East Asia</h4>
            <p><strong>Risk Score:</strong> 4.2/5</p>
            <p><strong>Key Factors:</strong></p>
            <ul>
                <li>Taiwan Strait tensions</li>
                <li>North Korea nuclear program</li>
                <li>Technology export controls</li>
                <li>Supply chain dependencies</li>
            </ul>
        </div>
        
        <div class="risk-card">
            <h4>Eastern Europe</h4>
            <p><strong>Risk Score:</strong> 4.5/5</p>
            <p><strong>Key Factors:</strong></p>
            <ul>
                <li>Ongoing Russia-Ukraine conflict</li>
                <li>Energy security concerns</li>
                <li>Cyber warfare escalation</li>
                <li>NATO expansion tensions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Emerging Risk Regions")
        
        st.markdown("""
        <div class="risk-card">
            <h4>Middle East</h4>
            <p><strong>Risk Score:</strong> 4.0/5</p>
            <p><strong>Key Factors:</strong></p>
            <ul>
                <li>Regional conflict expansion</li>
                <li>Oil supply disruption potential</li>
                <li>Shipping route vulnerabilities</li>
                <li>Political instability</li>
            </ul>
        </div>
        
        <div class="risk-card">
            <h4>South Asia</h4>
            <p><strong>Risk Score:</strong> 3.7/5</p>
            <p><strong>Key Factors:</strong></p>
            <ul>
                <li>India-China border tensions</li>
                <li>Pakistan political instability</li>
                <li>Climate change impacts</li>
                <li>Supply chain diversification</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif page == "Chat with Aletheia":
    st.markdown('<div class="main-header">Chat with Aletheia</div>', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_area("Ask Aletheia about market intelligence:", height=100)
    
    if st.button("Send"):
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get response from the Strategist Agent
            try:
                response = st.session_state.strategist_agent.run(user_input)
                
                # Extract the response content
                if isinstance(response, dict) and "output" in response:
                    bot_response = response["output"]
                else:
                    bot_response = str(response)
                
                # Add bot message to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                
                # Rerun to update the display
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    # This code will only run when the script is executed directly
    pass
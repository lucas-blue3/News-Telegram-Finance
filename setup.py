"""
Setup script for the Aletheia project.
"""

from setuptools import setup, find_packages

setup(
    name="aletheia",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community>=0.0.10",
        "langchain-core>=0.1.0",
        "langgraph>=0.0.20",
        "chromadb>=0.4.18",
        "faiss-cpu>=1.7.4",
        "openai>=1.3.0",
        "streamlit>=1.28.0",
        "plotly>=5.18.0",
        "pyvis>=0.3.2",
        "pandas>=2.1.1",
        "numpy>=1.26.0",
        "sqlalchemy>=2.0.23",
        "psycopg2-binary>=2.9.9",
        "yfinance>=0.2.31",
        "fredapi>=0.5.1",
        "sec-edgar-downloader>=5.0.1",
        "praw>=7.7.1",
        "tweepy>=4.14.0",
        "newsapi-python>=0.2.7",
        "arxiv>=1.4.8",
        "apscheduler>=3.10.4",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.10",
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-powered cognitive ecosystem for market intelligence and alpha generation",
    keywords="ai, finance, market intelligence, langchain, langgraph",
    url="https://github.com/yourusername/aletheia",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
)
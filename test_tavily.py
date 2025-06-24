"""
Test script for the Tavily API.
"""

import os
from dotenv import load_dotenv
from aletheia.api.tavily import TavilyClient

# Load environment variables
load_dotenv()

def main():
    """Test the Tavily API."""
    # Initialize the Tavily client
    tavily_client = TavilyClient()
    
    # Test search_news
    print("Testing search_news...")
    news = tavily_client.search_news(
        query="PETR4 Petrobras",
        max_results=5,
        days_back=7
    )
    
    # Print the results
    print(f"Found {len(news)} news articles:")
    for i, article in enumerate(news):
        print(f"\n--- Article {i+1} ---")
        print(f"Title: {article.get('title')}")
        print(f"URL: {article.get('url')}")
        print(f"Source: {article.get('source')}")
        print(f"Published: {article.get('published_date')}")
        
    # Test search_web
    print("\n\nTesting search_web...")
    web_results = tavily_client.search_web(
        query="Petrobras financial results 2025",
        max_results=3
    )
    
    # Print the results
    print(f"Found {len(web_results)} web pages:")
    for i, result in enumerate(web_results):
        print(f"\n--- Result {i+1} ---")
        print(f"Title: {result.get('title')}")
        print(f"URL: {result.get('url')}")
        print(f"Source: {result.get('source')}")
        
    # Test crawl_website
    print("\n\nTesting crawl_website...")
    crawl_results = tavily_client.crawl_website(
        url="https://www.petrobras.com.br/en/",
        max_results=10,
        max_depth=1,
        instructions="Extract information about financial results and investments"
    )
    
    # Print the results
    print(f"Crawled {len(crawl_results.get('results', []))} pages:")
    for i, result in enumerate(crawl_results.get('results', [])[:3]):  # Show only first 3 results
        print(f"\n--- Page {i+1} ---")
        print(f"Title: {result.get('title')}")
        print(f"URL: {result.get('url')}")
        
    print("\nTest completed successfully!")

if __name__ == "__main__":
    main()
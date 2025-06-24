"""
Tavily API client for news and web search.
"""

import os
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta

from tavily import TavilyClient as BaseTavilyClient
from dotenv import load_dotenv

load_dotenv()


class TavilyClient:
    """
    Client for the Tavily API to search for news and web content.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Tavily API client.

        Args:
            api_key: The Tavily API key (defaults to TAVILY_API_KEY environment variable)
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("Tavily API key is required")
        
        self.client = BaseTavilyClient(api_key=self.api_key)
    
    def search_news(
        self,
        query: str,
        max_results: int = 10,
        days_back: int = 3,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for news articles related to the query.

        Args:
            query: The search query
            max_results: Maximum number of results to return
            days_back: Number of days back to search
            include_domains: List of domains to include in the search
            exclude_domains: List of domains to exclude from the search

        Returns:
            List of news articles with title, url, content, and published_date
        """
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            topic="news",
            days=days_back,
            include_domains=include_domains or [],
            exclude_domains=exclude_domains or [],
        )
        
        # Process the results to extract relevant information
        articles = []
        for result in response.get("results", []):
            article = {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "source": result.get("source", ""),
                "published_date": result.get("published_date", ""),
            }
            articles.append(article)
        
        return articles
    
    def search_web(
        self,
        query: str,
        max_results: int = 10,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search the web for content related to the query.

        Args:
            query: The search query
            max_results: Maximum number of results to return
            include_domains: List of domains to include in the search
            exclude_domains: List of domains to exclude from the search

        Returns:
            List of web pages with title, url, and content
        """
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            topic="general",
            include_domains=include_domains or [],
            exclude_domains=exclude_domains or [],
        )
        
        # Process the results to extract relevant information
        results = []
        for result in response.get("results", []):
            page = {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "source": result.get("source", ""),
            }
            results.append(page)
        
        return results
    
    def crawl_website(
        self,
        url: str,
        max_results: int = 50,
        max_depth: int = 2,
        instructions: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Crawl a website to extract structured information.

        Args:
            url: The URL to crawl
            max_results: Maximum number of pages to crawl
            max_depth: Maximum depth of the crawl
            instructions: Natural language instructions for the crawler

        Returns:
            Dictionary with crawl results and extracted information
        """
        response = self.client.crawl(
            url=url,
            limit=max_results,
            max_depth=max_depth,
            instructions=instructions or "",
        )
        
        return response
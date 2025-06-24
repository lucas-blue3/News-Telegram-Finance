"""
Narrative Hunter Agent - Collects qualitative data from various sources.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union

import tweepy
from langchain_core.tools import BaseTool, tool
import arxiv
from sec_edgar_downloader import Downloader

from aletheia.api.tavily import TavilyClient

class NarrativeHunterAgent:
    """
    Agent responsible for collecting qualitative data from various sources:
    - Twitter/X
    - Tavily (for news and web search)
    - SEC Filings
    - Research papers (arXiv)
    """
    
    def __init__(self):
        """Initialize the Narrative Hunter Agent with API clients."""
        # Initialize Twitter API client
        self._init_twitter_client()
        
        # Initialize Tavily API client
        self._init_tavily_client()
        
        # Initialize SEC Edgar downloader
        self._init_sec_edgar()
        
        # Initialize arXiv client
        # No initialization needed for arXiv
    
    def _init_twitter_client(self):
        """Initialize the Twitter API client."""
        try:
            api_key = os.getenv("TWITTER_API_KEY")
            api_secret = os.getenv("TWITTER_API_SECRET")
            access_token = os.getenv("TWITTER_ACCESS_TOKEN")
            access_secret = os.getenv("TWITTER_ACCESS_SECRET")
            
            if all([api_key, api_secret, access_token, access_secret]):
                auth = tweepy.OAuth1UserHandler(
                    api_key, api_secret, access_token, access_secret
                )
                self.twitter_client = tweepy.API(auth)
            else:
                self.twitter_client = None
                print("Twitter API credentials not found. Twitter functionality will be disabled.")
        except Exception as e:
            self.twitter_client = None
            print(f"Error initializing Twitter client: {e}")
    
    def _init_tavily_client(self):
        """Initialize the Tavily API client."""
        try:
            tavily_api_key = os.getenv("TAVILY_API_KEY")
            
            if tavily_api_key:
                self.tavily_client = TavilyClient(api_key=tavily_api_key)
            else:
                self.tavily_client = None
                print("Tavily API key not found. Tavily functionality will be disabled.")
        except Exception as e:
            self.tavily_client = None
            print(f"Error initializing Tavily client: {e}")
    
    def _init_sec_edgar(self):
        """Initialize the SEC EDGAR downloader."""
        try:
            self.edgar_downloader = Downloader()
        except Exception as e:
            self.edgar_downloader = None
            print(f"Error initializing SEC EDGAR downloader: {e}")
    
    @tool
    def search_twitter(self, query: str, days_back: int = 7, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Search Twitter for tweets matching the query.
        
        Args:
            query: The search query
            days_back: Number of days to look back
            max_results: Maximum number of results to return
            
        Returns:
            List of tweets with metadata
        """
        if not self.twitter_client:
            return [{"error": "Twitter API client not initialized"}]
        
        try:
            # Calculate the start date
            start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            
            # Search tweets
            tweets = tweepy.Cursor(
                self.twitter_client.search_tweets,
                q=query,
                lang="en",
                since=start_date,
                tweet_mode="extended"
            ).items(max_results)
            
            # Format the results
            results = []
            for tweet in tweets:
                results.append({
                    "id": tweet.id_str,
                    "created_at": tweet.created_at.isoformat(),
                    "text": tweet.full_text,
                    "user": {
                        "id": tweet.user.id_str,
                        "name": tweet.user.name,
                        "screen_name": tweet.user.screen_name,
                        "followers_count": tweet.user.followers_count
                    },
                    "retweet_count": tweet.retweet_count,
                    "favorite_count": tweet.favorite_count,
                    "source": "twitter"
                })
            
            return results
        except Exception as e:
            return [{"error": f"Error searching Twitter: {str(e)}"}]
    
    @tool
    def get_twitter_list_tweets(self, list_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Get tweets from a Twitter list.
        
        Args:
            list_id: The ID of the Twitter list
            max_results: Maximum number of results to return
            
        Returns:
            List of tweets from the list
        """
        if not self.twitter_client:
            return [{"error": "Twitter API client not initialized"}]
        
        try:
            # Get tweets from the list
            tweets = tweepy.Cursor(
                self.twitter_client.list_timeline,
                list_id=list_id,
                tweet_mode="extended"
            ).items(max_results)
            
            # Format the results
            results = []
            for tweet in tweets:
                results.append({
                    "id": tweet.id_str,
                    "created_at": tweet.created_at.isoformat(),
                    "text": tweet.full_text,
                    "user": {
                        "id": tweet.user.id_str,
                        "name": tweet.user.name,
                        "screen_name": tweet.user.screen_name,
                        "followers_count": tweet.user.followers_count
                    },
                    "retweet_count": tweet.retweet_count,
                    "favorite_count": tweet.favorite_count,
                    "source": "twitter_list"
                })
            
            return results
        except Exception as e:
            return [{"error": f"Error getting tweets from list: {str(e)}"}]
    
    @tool
    def search_news(self, query: str, days_back: int = 7, max_results: int = 20, include_domains: Optional[List[str]] = None, exclude_domains: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search for news articles matching the query using Tavily.
        
        Args:
            query: The search query
            days_back: Number of days to look back
            max_results: Maximum number of results to return
            include_domains: List of domains to include in the search
            exclude_domains: List of domains to exclude from the search
            
        Returns:
            List of news articles with metadata
        """
        if not self.tavily_client:
            return [{"error": "Tavily API client not initialized"}]
        
        try:
            # Search for articles
            articles = self.tavily_client.search_news(
                query=query,
                max_results=max_results,
                days_back=days_back,
                include_domains=include_domains,
                exclude_domains=exclude_domains
            )
            
            # Add source information
            for article in articles:
                article["source_type"] = "tavily_news"
            
            return articles
        except Exception as e:
            return [{"error": f"Error searching news: {str(e)}"}]
    
    @tool
    def search_web(self, query: str, max_results: int = 20, include_domains: Optional[List[str]] = None, exclude_domains: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search the web for content related to the query using Tavily.
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            include_domains: List of domains to include in the search
            exclude_domains: List of domains to exclude from the search
            
        Returns:
            List of web pages with metadata
        """
        if not self.tavily_client:
            return [{"error": "Tavily API client not initialized"}]
        
        try:
            # Search the web
            results = self.tavily_client.search_web(
                query=query,
                max_results=max_results,
                include_domains=include_domains,
                exclude_domains=exclude_domains
            )
            
            # Add source information
            for result in results:
                result["source_type"] = "tavily_web"
            
            return results
        except Exception as e:
            return [{"error": f"Error searching web: {str(e)}"}]
    
    @tool
    def search_arxiv(self, query: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Search for research papers on arXiv.
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            
        Returns:
            List of arXiv papers with metadata
        """
        try:
            # Search arXiv
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            # Format the results
            results = []
            for paper in search.results():
                results.append({
                    "id": paper.entry_id,
                    "title": paper.title,
                    "summary": paper.summary,
                    "published": paper.published.isoformat() if paper.published else None,
                    "updated": paper.updated.isoformat() if paper.updated else None,
                    "authors": [author.name for author in paper.authors],
                    "pdf_url": paper.pdf_url,
                    "categories": paper.categories,
                    "source": "arxiv"
                })
            
            return results
        except Exception as e:
            return [{"error": f"Error searching arXiv: {str(e)}"}]
    
    @tool
    def get_sec_filings(self, ticker: str, filing_type: str = "10-K", amount: int = 5) -> List[Dict[str, Any]]:
        """
        Download SEC filings for a company.
        
        Args:
            ticker: The company's ticker symbol
            filing_type: The type of filing to download (10-K, 10-Q, 8-K, etc.)
            amount: Number of filings to download
            
        Returns:
            List of downloaded filings with metadata
        """
        if not self.edgar_downloader:
            return [{"error": "SEC EDGAR downloader not initialized"}]
        
        try:
            # Download the filings
            dl_dir = os.path.join(os.getcwd(), "data", "sec_filings")
            os.makedirs(dl_dir, exist_ok=True)
            
            self.edgar_downloader.set_download_folder(dl_dir)
            self.edgar_downloader.get(filing_type, ticker, amount=amount)
            
            # Get the downloaded files
            company_dir = os.path.join(dl_dir, ticker)
            filing_dir = os.path.join(company_dir, filing_type)
            
            if not os.path.exists(filing_dir):
                return [{"error": f"No {filing_type} filings found for {ticker}"}]
            
            # Format the results
            results = []
            for filename in os.listdir(filing_dir):
                file_path = os.path.join(filing_dir, filename)
                
                # Get file metadata
                file_stat = os.stat(file_path)
                
                results.append({
                    "ticker": ticker,
                    "filing_type": filing_type,
                    "filename": filename,
                    "path": file_path,
                    "size_bytes": file_stat.st_size,
                    "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                    "source": "sec_edgar"
                })
            
            return results
        except Exception as e:
            return [{"error": f"Error downloading SEC filings: {str(e)}"}]
    
    @tool
    def crawl_website(self, url: str, max_results: int = 50, max_depth: int = 2, instructions: Optional[str] = None) -> Dict[str, Any]:
        """
        Crawl a website to extract structured information using Tavily.
        
        Args:
            url: The URL to crawl
            max_results: Maximum number of pages to crawl
            max_depth: Maximum depth of the crawl
            instructions: Natural language instructions for the crawler
            
        Returns:
            Dictionary with crawl results and extracted information
        """
        if not self.tavily_client:
            return {"error": "Tavily API client not initialized"}
        
        try:
            # Crawl the website
            results = self.tavily_client.crawl_website(
                url=url,
                max_results=max_results,
                max_depth=max_depth,
                instructions=instructions
            )
            
            # Add source information
            results["source_type"] = "tavily_crawl"
            
            return results
        except Exception as e:
            return {"error": f"Error crawling website: {str(e)}"}
    
    def get_tools(self) -> List[BaseTool]:
        """
        Get all the tools provided by this agent.
        
        Returns:
            List of tools
        """
        return [
            self.search_twitter,
            self.get_twitter_list_tweets,
            self.search_news,
            self.search_web,
            self.crawl_website,
            self.search_arxiv,
            self.get_sec_filings
        ]
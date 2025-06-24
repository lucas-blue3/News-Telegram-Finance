"""
Quantitative Analyst Agent - Collects and analyzes quantitative financial data.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple

import numpy as np
import pandas as pd
import yfinance as yf
from fredapi import Fred
from langchain_core.tools import BaseTool, tool

class QuantAnalystAgent:
    """
    Agent responsible for collecting and analyzing quantitative financial data:
    - Stock prices and volumes
    - Financial statements
    - Economic indicators
    - Technical indicators
    """
    
    def __init__(self):
        """Initialize the Quantitative Analyst Agent."""
        # Initialize FRED API client
        self._init_fred_client()
    
    def _init_fred_client(self):
        """Initialize the FRED API client."""
        try:
            fred_api_key = os.getenv("FRED_API_KEY")
            
            if fred_api_key:
                self.fred_client = Fred(api_key=fred_api_key)
            else:
                self.fred_client = None
                print("FRED API key not found. FRED functionality will be disabled.")
        except Exception as e:
            self.fred_client = None
            print(f"Error initializing FRED client: {e}")
    
    @tool
    def get_stock_data(
        self, 
        ticker: str, 
        period: str = "1y", 
        interval: str = "1d"
    ) -> Dict[str, Any]:
        """
        Get historical stock data.
        
        Args:
            ticker: The stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            
        Returns:
            Dictionary with stock data and metadata
        """
        try:
            # Get the stock data
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period, interval=interval)
            
            # Reset index to make date a column
            hist = hist.reset_index()
            
            # Convert to dictionary
            data_dict = hist.to_dict(orient="records")
            
            # Get basic info
            info = stock.info
            
            # Calculate some basic statistics
            if not hist.empty and "Close" in hist.columns:
                latest_price = hist["Close"].iloc[-1]
                price_change = hist["Close"].iloc[-1] - hist["Close"].iloc[0]
                price_change_pct = (price_change / hist["Close"].iloc[0]) * 100
                
                # Calculate volatility (standard deviation of returns)
                returns = hist["Close"].pct_change().dropna()
                volatility = returns.std() * 100  # Convert to percentage
                
                # Calculate moving averages
                ma_50 = hist["Close"].rolling(window=min(50, len(hist))).mean().iloc[-1] if len(hist) >= 5 else None
                ma_200 = hist["Close"].rolling(window=min(200, len(hist))).mean().iloc[-1] if len(hist) >= 20 else None
            else:
                latest_price = None
                price_change = None
                price_change_pct = None
                volatility = None
                ma_50 = None
                ma_200 = None
            
            return {
                "ticker": ticker,
                "period": period,
                "interval": interval,
                "data": data_dict,
                "latest_price": latest_price,
                "price_change": price_change,
                "price_change_pct": price_change_pct,
                "volatility": volatility,
                "ma_50": ma_50,
                "ma_200": ma_200,
                "company_name": info.get("shortName", ticker),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": info.get("dividendYield"),
                "source": "yfinance"
            }
        except Exception as e:
            return {"error": f"Error getting stock data for {ticker}: {str(e)}"}
    
    @tool
    def get_financial_statements(
        self, 
        ticker: str, 
        statement_type: str = "income", 
        period: str = "annual"
    ) -> Dict[str, Any]:
        """
        Get financial statements for a company.
        
        Args:
            ticker: The stock ticker symbol
            statement_type: Type of statement (income, balance, cash)
            period: Period (annual, quarterly)
            
        Returns:
            Dictionary with financial statement data
        """
        try:
            # Get the stock data
            stock = yf.Ticker(ticker)
            
            # Get the requested financial statement
            if statement_type.lower() == "income":
                if period.lower() == "annual":
                    financials = stock.income_stmt
                else:
                    financials = stock.quarterly_income_stmt
            elif statement_type.lower() == "balance":
                if period.lower() == "annual":
                    financials = stock.balance_sheet
                else:
                    financials = stock.quarterly_balance_sheet
            elif statement_type.lower() == "cash":
                if period.lower() == "annual":
                    financials = stock.cashflow
                else:
                    financials = stock.quarterly_cashflow
            else:
                return {"error": f"Invalid statement type: {statement_type}. Use 'income', 'balance', or 'cash'."}
            
            # Convert to dictionary
            if financials is not None and not financials.empty:
                # Reset index to make the statement items a column
                financials = financials.reset_index()
                
                # Convert to dictionary
                data_dict = financials.to_dict(orient="records")
                
                return {
                    "ticker": ticker,
                    "statement_type": statement_type,
                    "period": period,
                    "data": data_dict,
                    "source": "yfinance"
                }
            else:
                return {"error": f"No {statement_type} statement data available for {ticker}"}
        except Exception as e:
            return {"error": f"Error getting financial statements for {ticker}: {str(e)}"}
    
    @tool
    def get_economic_indicator(
        self, 
        indicator_id: str, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get economic indicator data from FRED.
        
        Args:
            indicator_id: FRED series ID (e.g., 'GDP', 'UNRATE', 'CPIAUCSL')
            start_date: Start date in YYYY-MM-DD format (default: 1 year ago)
            end_date: End date in YYYY-MM-DD format (default: today)
            
        Returns:
            Dictionary with economic indicator data
        """
        if not self.fred_client:
            return {"error": "FRED API client not initialized"}
        
        try:
            # Set default dates if not provided
            if not end_date:
                end_date = datetime.now().strftime("%Y-%m-%d")
            
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            
            # Get the indicator data
            series = self.fred_client.get_series(
                indicator_id, 
                start_date=start_date, 
                end_date=end_date
            )
            
            # Convert to DataFrame and reset index
            df = pd.DataFrame(series).reset_index()
            df.columns = ["date", "value"]
            
            # Convert to dictionary
            data_dict = df.to_dict(orient="records")
            
            # Get series information
            series_info = self.fred_client.get_series_info(indicator_id)
            
            return {
                "indicator_id": indicator_id,
                "title": series_info.get("title", indicator_id),
                "units": series_info.get("units", ""),
                "frequency": series_info.get("frequency", ""),
                "start_date": start_date,
                "end_date": end_date,
                "data": data_dict,
                "latest_value": series.iloc[-1] if not series.empty else None,
                "source": "fred"
            }
        except Exception as e:
            return {"error": f"Error getting economic indicator {indicator_id}: {str(e)}"}
    
    @tool
    def calculate_technical_indicators(
        self, 
        ticker: str, 
        period: str = "1y", 
        indicators: List[str] = ["sma", "ema", "rsi", "macd", "bollinger"]
    ) -> Dict[str, Any]:
        """
        Calculate technical indicators for a stock.
        
        Args:
            ticker: The stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            indicators: List of indicators to calculate (sma, ema, rsi, macd, bollinger)
            
        Returns:
            Dictionary with technical indicators
        """
        try:
            # Get the stock data
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                return {"error": f"No historical data available for {ticker}"}
            
            result = {
                "ticker": ticker,
                "period": period,
                "indicators": {}
            }
            
            # Calculate Simple Moving Averages
            if "sma" in indicators:
                sma_periods = [20, 50, 200]
                sma_data = {}
                
                for period in sma_periods:
                    if len(hist) >= period:
                        sma = hist["Close"].rolling(window=period).mean()
                        sma_data[f"SMA_{period}"] = sma.iloc[-1]
                
                result["indicators"]["sma"] = sma_data
            
            # Calculate Exponential Moving Averages
            if "ema" in indicators:
                ema_periods = [12, 26, 50]
                ema_data = {}
                
                for period in ema_periods:
                    if len(hist) >= period:
                        ema = hist["Close"].ewm(span=period, adjust=False).mean()
                        ema_data[f"EMA_{period}"] = ema.iloc[-1]
                
                result["indicators"]["ema"] = ema_data
            
            # Calculate Relative Strength Index (RSI)
            if "rsi" in indicators and len(hist) >= 14:
                delta = hist["Close"].diff()
                gain = delta.where(delta > 0, 0).rolling(window=14).mean()
                loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
                
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                
                result["indicators"]["rsi"] = {
                    "RSI_14": rsi.iloc[-1],
                    "is_overbought": rsi.iloc[-1] > 70,
                    "is_oversold": rsi.iloc[-1] < 30
                }
            
            # Calculate MACD
            if "macd" in indicators and len(hist) >= 26:
                ema_12 = hist["Close"].ewm(span=12, adjust=False).mean()
                ema_26 = hist["Close"].ewm(span=26, adjust=False).mean()
                
                macd_line = ema_12 - ema_26
                signal_line = macd_line.ewm(span=9, adjust=False).mean()
                macd_histogram = macd_line - signal_line
                
                result["indicators"]["macd"] = {
                    "MACD_Line": macd_line.iloc[-1],
                    "Signal_Line": signal_line.iloc[-1],
                    "Histogram": macd_histogram.iloc[-1],
                    "is_bullish": macd_line.iloc[-1] > signal_line.iloc[-1]
                }
            
            # Calculate Bollinger Bands
            if "bollinger" in indicators and len(hist) >= 20:
                sma_20 = hist["Close"].rolling(window=20).mean()
                std_20 = hist["Close"].rolling(window=20).std()
                
                upper_band = sma_20 + (std_20 * 2)
                lower_band = sma_20 - (std_20 * 2)
                
                current_price = hist["Close"].iloc[-1]
                
                result["indicators"]["bollinger"] = {
                    "SMA_20": sma_20.iloc[-1],
                    "Upper_Band": upper_band.iloc[-1],
                    "Lower_Band": lower_band.iloc[-1],
                    "is_above_upper": current_price > upper_band.iloc[-1],
                    "is_below_lower": current_price < lower_band.iloc[-1],
                    "bandwidth": (upper_band.iloc[-1] - lower_band.iloc[-1]) / sma_20.iloc[-1]
                }
            
            result["source"] = "calculated"
            return result
        except Exception as e:
            return {"error": f"Error calculating technical indicators for {ticker}: {str(e)}"}
    
    @tool
    def get_market_calendar(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get economic calendar events.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (default: today)
            end_date: End date in YYYY-MM-DD format (default: 7 days from today)
            
        Returns:
            Dictionary with economic calendar events
        """
        try:
            # Set default dates if not provided
            if not start_date:
                start_date = datetime.now().strftime("%Y-%m-%d")
            
            if not end_date:
                end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            
            # This is a placeholder - in a real implementation, you would use a proper
            # economic calendar API or web scraping to get this data
            # For now, we'll return some sample data
            
            # Convert dates to datetime objects for comparison
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            # Sample economic events
            sample_events = [
                {
                    "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                    "time": "08:30",
                    "event": "Non-Farm Payrolls",
                    "country": "US",
                    "importance": "High",
                    "previous": "194K",
                    "forecast": "200K"
                },
                {
                    "date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                    "time": "14:00",
                    "event": "Fed Interest Rate Decision",
                    "country": "US",
                    "importance": "High",
                    "previous": "5.50%",
                    "forecast": "5.50%"
                },
                {
                    "date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                    "time": "08:30",
                    "event": "Initial Jobless Claims",
                    "country": "US",
                    "importance": "Medium",
                    "previous": "215K",
                    "forecast": "220K"
                }
            ]
            
            # Filter events by date range
            filtered_events = []
            for event in sample_events:
                event_dt = datetime.strptime(event["date"], "%Y-%m-%d")
                if start_dt <= event_dt <= end_dt:
                    filtered_events.append(event)
            
            return {
                "start_date": start_date,
                "end_date": end_date,
                "events": filtered_events,
                "source": "simulated"  # In a real implementation, this would be the actual source
            }
        except Exception as e:
            return {"error": f"Error getting market calendar: {str(e)}"}
    
    def get_tools(self) -> List[BaseTool]:
        """
        Get all the tools provided by this agent.
        
        Returns:
            List of tools
        """
        return [
            self.get_stock_data,
            self.get_financial_statements,
            self.get_economic_indicator,
            self.calculate_technical_indicators,
            self.get_market_calendar
        ]
"""
Relational database implementation for structured data storage.
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, 
    Text, ForeignKey, Boolean, JSON, Table, MetaData
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session


# Create the base class for declarative models
Base = declarative_base()


# Define the models
class Asset(Base):
    """Asset model for stocks, commodities, currencies, etc."""
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    asset_type = Column(String(20), nullable=False)  # stock, commodity, currency, etc.
    sector = Column(String(50))
    industry = Column(String(50))
    country = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prices = relationship("AssetPrice", back_populates="asset", cascade="all, delete-orphan")
    news = relationship("News", secondary="asset_news", back_populates="assets")
    narratives = relationship("Narrative", secondary="asset_narratives", back_populates="assets")


class AssetPrice(Base):
    """Asset price model for storing historical prices."""
    __tablename__ = "asset_prices"
    
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    asset = relationship("Asset", back_populates="prices")
    
    # Composite unique constraint
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )


class News(Base):
    """News model for storing news articles."""
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    url = Column(String(255), unique=True)
    source = Column(String(100))
    published_at = Column(DateTime)
    sentiment_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    assets = relationship("Asset", secondary="asset_news", back_populates="news")
    narratives = relationship("Narrative", secondary="news_narratives", back_populates="news")


# Association table for Asset-News many-to-many relationship
asset_news = Table(
    "asset_news",
    Base.metadata,
    Column("asset_id", Integer, ForeignKey("assets.id"), primary_key=True),
    Column("news_id", Integer, ForeignKey("news.id"), primary_key=True)
)


class Narrative(Base):
    """Narrative model for storing market narratives."""
    __tablename__ = "narratives"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    narrative_type = Column(String(50))  # dominant, competing, emerging
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assets = relationship("Asset", secondary="asset_narratives", back_populates="narratives")
    news = relationship("News", secondary="news_narratives", back_populates="narratives")
    causal_relationships = relationship("CausalRelationship", back_populates="narrative")


# Association table for Asset-Narrative many-to-many relationship
asset_narratives = Table(
    "asset_narratives",
    Base.metadata,
    Column("asset_id", Integer, ForeignKey("assets.id"), primary_key=True),
    Column("narrative_id", Integer, ForeignKey("narratives.id"), primary_key=True)
)


# Association table for News-Narrative many-to-many relationship
news_narratives = Table(
    "news_narratives",
    Base.metadata,
    Column("news_id", Integer, ForeignKey("news.id"), primary_key=True),
    Column("narrative_id", Integer, ForeignKey("narratives.id"), primary_key=True)
)


class CausalRelationship(Base):
    """Causal relationship model for storing cause-effect relationships."""
    __tablename__ = "causal_relationships"
    
    id = Column(Integer, primary_key=True)
    narrative_id = Column(Integer, ForeignKey("narratives.id"))
    cause = Column(Text, nullable=False)
    effect = Column(Text, nullable=False)
    strength = Column(String(20))  # strong, moderate, weak
    confidence = Column(String(20))  # high, medium, low
    conditions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    narrative = relationship("Narrative", back_populates="causal_relationships")


class Risk(Base):
    """Risk model for storing identified risks."""
    __tablename__ = "risks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    risk_type = Column(String(50))  # market, geopolitical, regulatory, etc.
    probability = Column(String(20))  # high, medium, low
    impact = Column(String(20))  # high, medium, low
    time_horizon = Column(String(20))  # short-term, medium-term, long-term
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional fields for black swan risks
    is_black_swan = Column(Boolean, default=False)
    early_warning_indicators = Column(JSON)
    historical_parallels = Column(Text)


class EconomicIndicator(Base):
    """Economic indicator model for storing economic data."""
    __tablename__ = "economic_indicators"
    
    id = Column(Integer, primary_key=True)
    indicator_id = Column(String(50), nullable=False)  # e.g., GDP, UNRATE, CPIAUCSL
    title = Column(String(255))
    date = Column(DateTime, nullable=False)
    value = Column(Float)
    units = Column(String(50))
    frequency = Column(String(20))  # daily, weekly, monthly, quarterly, annual
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Composite unique constraint
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )


class Report(Base):
    """Report model for storing generated reports."""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    report_type = Column(String(50))  # market_analysis, risk_assessment, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    assets = relationship("Asset", secondary="report_assets")


# Association table for Report-Asset many-to-many relationship
report_assets = Table(
    "report_assets",
    Base.metadata,
    Column("report_id", Integer, ForeignKey("reports.id"), primary_key=True),
    Column("asset_id", Integer, ForeignKey("assets.id"), primary_key=True)
)


class RelationalMemory:
    """
    Relational database implementation for structured data storage.
    """
    
    def __init__(self, db_url: Optional[str] = None):
        """
        Initialize the relational memory.
        
        Args:
            db_url: SQLAlchemy database URL
        """
        # Set default database URL if not provided
        if db_url is None:
            postgres_user = os.getenv("POSTGRES_USER", "postgres")
            postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")
            postgres_db = os.getenv("POSTGRES_DB", "aletheia")
            postgres_host = os.getenv("POSTGRES_HOST", "localhost")
            postgres_port = os.getenv("POSTGRES_PORT", "5432")
            
            db_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
        
        # Create the engine
        self.engine = create_engine(db_url)
        
        # Create the session factory
        self.Session = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """Create all tables in the database."""
        Base.metadata.create_all(self.engine)
    
    def drop_tables(self):
        """Drop all tables from the database."""
        Base.metadata.drop_all(self.engine)
    
    def get_session(self) -> Session:
        """
        Get a new session.
        
        Returns:
            SQLAlchemy session
        """
        return self.Session()
    
    def add_asset(self, asset_data: Dict[str, Any]) -> Asset:
        """
        Add an asset to the database.
        
        Args:
            asset_data: Asset data
            
        Returns:
            The created Asset object
        """
        with self.get_session() as session:
            asset = Asset(**asset_data)
            session.add(asset)
            session.commit()
            session.refresh(asset)
            return asset
    
    def add_asset_price(self, price_data: Dict[str, Any]) -> AssetPrice:
        """
        Add an asset price to the database.
        
        Args:
            price_data: Asset price data
            
        Returns:
            The created AssetPrice object
        """
        with self.get_session() as session:
            price = AssetPrice(**price_data)
            session.add(price)
            session.commit()
            session.refresh(price)
            return price
    
    def add_news(self, news_data: Dict[str, Any], asset_ids: Optional[List[int]] = None) -> News:
        """
        Add a news article to the database.
        
        Args:
            news_data: News data
            asset_ids: List of asset IDs to associate with the news
            
        Returns:
            The created News object
        """
        with self.get_session() as session:
            news = News(**news_data)
            
            if asset_ids:
                assets = session.query(Asset).filter(Asset.id.in_(asset_ids)).all()
                news.assets = assets
            
            session.add(news)
            session.commit()
            session.refresh(news)
            return news
    
    def add_narrative(
        self,
        narrative_data: Dict[str, Any],
        asset_ids: Optional[List[int]] = None,
        news_ids: Optional[List[int]] = None,
        causal_relationships: Optional[List[Dict[str, Any]]] = None
    ) -> Narrative:
        """
        Add a market narrative to the database.
        
        Args:
            narrative_data: Narrative data
            asset_ids: List of asset IDs to associate with the narrative
            news_ids: List of news IDs to associate with the narrative
            causal_relationships: List of causal relationships to add
            
        Returns:
            The created Narrative object
        """
        with self.get_session() as session:
            narrative = Narrative(**narrative_data)
            
            if asset_ids:
                assets = session.query(Asset).filter(Asset.id.in_(asset_ids)).all()
                narrative.assets = assets
            
            if news_ids:
                news_items = session.query(News).filter(News.id.in_(news_ids)).all()
                narrative.news = news_items
            
            session.add(narrative)
            session.flush()  # Flush to get the narrative ID
            
            if causal_relationships:
                for rel_data in causal_relationships:
                    rel_data["narrative_id"] = narrative.id
                    causal_rel = CausalRelationship(**rel_data)
                    session.add(causal_rel)
            
            session.commit()
            session.refresh(narrative)
            return narrative
    
    def add_risk(self, risk_data: Dict[str, Any]) -> Risk:
        """
        Add a risk to the database.
        
        Args:
            risk_data: Risk data
            
        Returns:
            The created Risk object
        """
        with self.get_session() as session:
            risk = Risk(**risk_data)
            session.add(risk)
            session.commit()
            session.refresh(risk)
            return risk
    
    def add_economic_indicator(self, indicator_data: Dict[str, Any]) -> EconomicIndicator:
        """
        Add an economic indicator to the database.
        
        Args:
            indicator_data: Economic indicator data
            
        Returns:
            The created EconomicIndicator object
        """
        with self.get_session() as session:
            indicator = EconomicIndicator(**indicator_data)
            session.add(indicator)
            session.commit()
            session.refresh(indicator)
            return indicator
    
    def add_report(self, report_data: Dict[str, Any], asset_ids: Optional[List[int]] = None) -> Report:
        """
        Add a report to the database.
        
        Args:
            report_data: Report data
            asset_ids: List of asset IDs to associate with the report
            
        Returns:
            The created Report object
        """
        with self.get_session() as session:
            report = Report(**report_data)
            
            if asset_ids:
                assets = session.query(Asset).filter(Asset.id.in_(asset_ids)).all()
                report.assets = assets
            
            session.add(report)
            session.commit()
            session.refresh(report)
            return report
    
    def get_asset_by_symbol(self, symbol: str) -> Optional[Asset]:
        """
        Get an asset by its symbol.
        
        Args:
            symbol: Asset symbol
            
        Returns:
            Asset object or None if not found
        """
        with self.get_session() as session:
            return session.query(Asset).filter(Asset.symbol == symbol).first()
    
    def get_latest_price(self, asset_id: int) -> Optional[AssetPrice]:
        """
        Get the latest price for an asset.
        
        Args:
            asset_id: Asset ID
            
        Returns:
            AssetPrice object or None if not found
        """
        with self.get_session() as session:
            return session.query(AssetPrice).filter(
                AssetPrice.asset_id == asset_id
            ).order_by(AssetPrice.date.desc()).first()
    
    def get_recent_news(self, limit: int = 10) -> List[News]:
        """
        Get recent news articles.
        
        Args:
            limit: Maximum number of news articles to return
            
        Returns:
            List of News objects
        """
        with self.get_session() as session:
            return session.query(News).order_by(News.published_at.desc()).limit(limit).all()
    
    def get_narratives_by_asset(self, asset_id: int) -> List[Narrative]:
        """
        Get narratives for an asset.
        
        Args:
            asset_id: Asset ID
            
        Returns:
            List of Narrative objects
        """
        with self.get_session() as session:
            asset = session.query(Asset).filter(Asset.id == asset_id).first()
            if asset:
                return asset.narratives
            return []
    
    def get_risks_by_type(self, risk_type: str) -> List[Risk]:
        """
        Get risks by type.
        
        Args:
            risk_type: Risk type
            
        Returns:
            List of Risk objects
        """
        with self.get_session() as session:
            return session.query(Risk).filter(Risk.risk_type == risk_type).all()
    
    def get_black_swan_risks(self) -> List[Risk]:
        """
        Get black swan risks.
        
        Returns:
            List of Risk objects
        """
        with self.get_session() as session:
            return session.query(Risk).filter(Risk.is_black_swan == True).all()
    
    def get_economic_indicator_history(self, indicator_id: str, limit: int = 100) -> List[EconomicIndicator]:
        """
        Get historical data for an economic indicator.
        
        Args:
            indicator_id: Economic indicator ID
            limit: Maximum number of data points to return
            
        Returns:
            List of EconomicIndicator objects
        """
        with self.get_session() as session:
            return session.query(EconomicIndicator).filter(
                EconomicIndicator.indicator_id == indicator_id
            ).order_by(EconomicIndicator.date.desc()).limit(limit).all()
    
    def get_recent_reports(self, report_type: Optional[str] = None, limit: int = 10) -> List[Report]:
        """
        Get recent reports.
        
        Args:
            report_type: Report type filter
            limit: Maximum number of reports to return
            
        Returns:
            List of Report objects
        """
        with self.get_session() as session:
            query = session.query(Report)
            
            if report_type:
                query = query.filter(Report.report_type == report_type)
            
            return query.order_by(Report.created_at.desc()).limit(limit).all()
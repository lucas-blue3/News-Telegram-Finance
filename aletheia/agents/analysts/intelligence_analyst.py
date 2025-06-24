"""
Intelligence Analyst Agent - Analyzes qualitative data to extract insights.
"""

from typing import Dict, List, Optional, Any, Union

from langchain_core.tools import BaseTool, tool
from langchain_openai import ChatOpenAI


class IntelligenceAnalystAgent:
    """
    Agent responsible for analyzing qualitative data to extract insights:
    - Advanced sentiment analysis
    - Causal relationship extraction
    - Market narrative identification
    - Persona-specific summarization
    """
    
    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """
        Initialize the Intelligence Analyst Agent.
        
        Args:
            llm: The language model to use
        """
        self.llm = llm or ChatOpenAI(
            model="deepseek-chat",
            temperature=0.1,
            base_url="https://api.deepseek.com/v1",  # Replace with actual DeepSeek API URL
        )
    
    @tool
    def analyze_advanced_sentiment(self, texts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform advanced sentiment analysis on a list of texts.
        
        Args:
            texts: List of text items with metadata
            
        Returns:
            Dictionary with sentiment analysis results
        """
        try:
            # Extract the text content from each item
            text_contents = []
            for item in texts:
                if "text" in item:
                    text_contents.append(item["text"])
                elif "content" in item:
                    text_contents.append(item["content"])
                elif "selftext" in item:
                    text_contents.append(item["selftext"])
                elif "title" in item:
                    text_contents.append(item["title"])
                elif "summary" in item:
                    text_contents.append(item["summary"])
            
            # Combine texts for analysis (limit to avoid token limits)
            combined_text = "\n\n".join(text_contents[:50])
            
            # Use the LLM to analyze sentiment
            prompt = f"""
            Analyze the sentiment in the following texts. Go beyond simple positive/negative classification.
            Identify nuanced emotional states such as:
            - Optimism/Pessimism
            - Confidence/Uncertainty
            - Fear/Greed
            - Excitement/Boredom
            - Surprise/Expectation
            
            For each emotional dimension, provide:
            1. A score from -5 to +5
            2. Key phrases that support this assessment
            3. Overall sentiment trend
            
            Texts to analyze:
            {combined_text}
            
            Respond in JSON format with the following structure:
            {{
                "overall_sentiment": "string",
                "sentiment_score": float,
                "dimensions": {{
                    "optimism_pessimism": {{
                        "score": float,
                        "key_phrases": [strings]
                    }},
                    "confidence_uncertainty": {{
                        "score": float,
                        "key_phrases": [strings]
                    }},
                    "fear_greed": {{
                        "score": float,
                        "key_phrases": [strings]
                    }},
                    "excitement_boredom": {{
                        "score": float,
                        "key_phrases": [strings]
                    }},
                    "surprise_expectation": {{
                        "score": float,
                        "key_phrases": [strings]
                    }}
                }},
                "trend": "string",
                "notable_outliers": [strings]
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            # Parse the response to extract the sentiment analysis
            # In a real implementation, you would use a more robust parsing method
            import json
            try:
                sentiment_analysis = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback to a simple extraction if JSON parsing fails
                sentiment_analysis = {
                    "overall_sentiment": "mixed",
                    "sentiment_score": 0.0,
                    "dimensions": {
                        "optimism_pessimism": {
                            "score": 0.0,
                            "key_phrases": ["parsing error"]
                        },
                        "confidence_uncertainty": {
                            "score": 0.0,
                            "key_phrases": ["parsing error"]
                        },
                        "fear_greed": {
                            "score": 0.0,
                            "key_phrases": ["parsing error"]
                        },
                        "excitement_boredom": {
                            "score": 0.0,
                            "key_phrases": ["parsing error"]
                        },
                        "surprise_expectation": {
                            "score": 0.0,
                            "key_phrases": ["parsing error"]
                        }
                    },
                    "trend": "unknown",
                    "notable_outliers": ["parsing error"],
                    "raw_response": response.content
                }
            
            return sentiment_analysis
        except Exception as e:
            return {"error": f"Error analyzing sentiment: {str(e)}"}
    
    @tool
    def extract_causal_relationships(self, texts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract causal relationships from a list of texts.
        
        Args:
            texts: List of text items with metadata
            
        Returns:
            Dictionary with extracted causal relationships
        """
        try:
            # Extract the text content from each item
            text_contents = []
            for item in texts:
                if "text" in item:
                    text_contents.append(item["text"])
                elif "content" in item:
                    text_contents.append(item["content"])
                elif "selftext" in item:
                    text_contents.append(item["selftext"])
                elif "title" in item:
                    text_contents.append(item["title"])
                elif "summary" in item:
                    text_contents.append(item["summary"])
            
            # Combine texts for analysis (limit to avoid token limits)
            combined_text = "\n\n".join(text_contents[:30])
            
            # Use the LLM to extract causal relationships
            prompt = f"""
            Extract causal relationships from the following texts. Focus on identifying clear cause-and-effect relationships
            related to financial markets, economics, or business.
            
            For each causal relationship, identify:
            1. The cause
            2. The effect
            3. The strength of the relationship (strong, moderate, weak)
            4. The confidence in this assessment (high, medium, low)
            5. Any conditions or context that modify this relationship
            
            Texts to analyze:
            {combined_text}
            
            Respond in JSON format with the following structure:
            {{
                "causal_relationships": [
                    {{
                        "cause": "string",
                        "effect": "string",
                        "strength": "string",
                        "confidence": "string",
                        "conditions": "string"
                    }}
                ],
                "key_factors": [strings],
                "common_effects": [strings],
                "feedback_loops": [
                    {{
                        "description": "string",
                        "cycle": [strings]
                    }}
                ]
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            # Parse the response to extract the causal relationships
            import json
            try:
                causal_relationships = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback to a simple extraction if JSON parsing fails
                causal_relationships = {
                    "causal_relationships": [
                        {
                            "cause": "parsing error",
                            "effect": "parsing error",
                            "strength": "unknown",
                            "confidence": "low",
                            "conditions": "parsing error"
                        }
                    ],
                    "key_factors": ["parsing error"],
                    "common_effects": ["parsing error"],
                    "feedback_loops": [],
                    "raw_response": response.content
                }
            
            return causal_relationships
        except Exception as e:
            return {"error": f"Error extracting causal relationships: {str(e)}"}
    
    @tool
    def identify_market_narratives(self, texts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify market narratives from a list of texts.
        
        Args:
            texts: List of text items with metadata
            
        Returns:
            Dictionary with identified market narratives
        """
        try:
            # Extract the text content from each item
            text_contents = []
            for item in texts:
                if "text" in item:
                    text_contents.append(item["text"])
                elif "content" in item:
                    text_contents.append(item["content"])
                elif "selftext" in item:
                    text_contents.append(item["selftext"])
                elif "title" in item:
                    text_contents.append(item["title"])
                elif "summary" in item:
                    text_contents.append(item["summary"])
            
            # Combine texts for analysis (limit to avoid token limits)
            combined_text = "\n\n".join(text_contents[:40])
            
            # Use the LLM to identify market narratives
            prompt = f"""
            Identify the dominant market narratives in the following texts. A market narrative is a story or explanation
            that market participants use to make sense of market events and justify price movements.
            
            For each narrative, identify:
            1. A concise title for the narrative
            2. A detailed description of the narrative
            3. Key supporting evidence from the texts
            4. Potential counter-evidence or challenges to this narrative
            5. The likely market implications if this narrative becomes dominant
            
            Texts to analyze:
            {combined_text}
            
            Respond in JSON format with the following structure:
            {{
                "dominant_narratives": [
                    {{
                        "title": "string",
                        "description": "string",
                        "supporting_evidence": [strings],
                        "counter_evidence": [strings],
                        "market_implications": "string"
                    }}
                ],
                "competing_narratives": [
                    {{
                        "title": "string",
                        "description": "string",
                        "supporting_evidence": [strings],
                        "counter_evidence": [strings],
                        "market_implications": "string"
                    }}
                ],
                "emerging_narratives": [
                    {{
                        "title": "string",
                        "description": "string",
                        "supporting_evidence": [strings],
                        "market_implications": "string"
                    }}
                ],
                "narrative_shifts": [
                    {{
                        "from": "string",
                        "to": "string",
                        "catalyst": "string"
                    }}
                ]
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            # Parse the response to extract the market narratives
            import json
            try:
                market_narratives = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback to a simple extraction if JSON parsing fails
                market_narratives = {
                    "dominant_narratives": [
                        {
                            "title": "parsing error",
                            "description": "parsing error",
                            "supporting_evidence": ["parsing error"],
                            "counter_evidence": ["parsing error"],
                            "market_implications": "parsing error"
                        }
                    ],
                    "competing_narratives": [],
                    "emerging_narratives": [],
                    "narrative_shifts": [],
                    "raw_response": response.content
                }
            
            return market_narratives
        except Exception as e:
            return {"error": f"Error identifying market narratives: {str(e)}"}
    
    @tool
    def summarize_for_different_personas(
        self, 
        texts: List[Dict[str, Any]], 
        personas: List[str] = ["trader", "portfolio_manager", "retail_investor", "executive"]
    ) -> Dict[str, Any]:
        """
        Create persona-specific summaries from a list of texts.
        
        Args:
            texts: List of text items with metadata
            personas: List of personas to create summaries for
            
        Returns:
            Dictionary with persona-specific summaries
        """
        try:
            # Extract the text content from each item
            text_contents = []
            for item in texts:
                if "text" in item:
                    text_contents.append(item["text"])
                elif "content" in item:
                    text_contents.append(item["content"])
                elif "selftext" in item:
                    text_contents.append(item["selftext"])
                elif "title" in item:
                    text_contents.append(item["title"])
                elif "summary" in item:
                    text_contents.append(item["summary"])
            
            # Combine texts for analysis (limit to avoid token limits)
            combined_text = "\n\n".join(text_contents[:30])
            
            # Use the LLM to create persona-specific summaries
            prompt = f"""
            Create summaries of the following texts tailored to different personas in the financial industry.
            Each summary should focus on the aspects most relevant to that persona and use appropriate language and level of detail.
            
            Personas:
            - Trader: Focus on short-term price movements, volatility, and trading opportunities
            - Portfolio Manager: Focus on long-term trends, risk management, and portfolio implications
            - Retail Investor: Focus on clear explanations, avoiding jargon, and practical investment advice
            - Executive: Focus on strategic implications, competitive landscape, and high-level insights
            
            Texts to summarize:
            {combined_text}
            
            Respond in JSON format with the following structure:
            {{
                "summaries": {{
                    "trader": {{
                        "summary": "string",
                        "key_points": [strings],
                        "actionable_insights": [strings]
                    }},
                    "portfolio_manager": {{
                        "summary": "string",
                        "key_points": [strings],
                        "actionable_insights": [strings]
                    }},
                    "retail_investor": {{
                        "summary": "string",
                        "key_points": [strings],
                        "actionable_insights": [strings]
                    }},
                    "executive": {{
                        "summary": "string",
                        "key_points": [strings],
                        "actionable_insights": [strings]
                    }}
                }}
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            # Parse the response to extract the persona-specific summaries
            import json
            try:
                persona_summaries = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback to a simple extraction if JSON parsing fails
                persona_summaries = {
                    "summaries": {
                        "trader": {
                            "summary": "parsing error",
                            "key_points": ["parsing error"],
                            "actionable_insights": ["parsing error"]
                        },
                        "portfolio_manager": {
                            "summary": "parsing error",
                            "key_points": ["parsing error"],
                            "actionable_insights": ["parsing error"]
                        },
                        "retail_investor": {
                            "summary": "parsing error",
                            "key_points": ["parsing error"],
                            "actionable_insights": ["parsing error"]
                        },
                        "executive": {
                            "summary": "parsing error",
                            "key_points": ["parsing error"],
                            "actionable_insights": ["parsing error"]
                        }
                    },
                    "raw_response": response.content
                }
            
            return persona_summaries
        except Exception as e:
            return {"error": f"Error creating persona-specific summaries: {str(e)}"}
    
    def get_tools(self) -> List[BaseTool]:
        """
        Get all the tools provided by this agent.
        
        Returns:
            List of tools
        """
        return [
            self.analyze_advanced_sentiment,
            self.extract_causal_relationships,
            self.identify_market_narratives,
            self.summarize_for_different_personas
        ]
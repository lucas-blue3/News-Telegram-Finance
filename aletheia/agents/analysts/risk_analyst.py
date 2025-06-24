"""
Risk Analyst Agent - Challenges the main narrative and identifies potential risks.
"""

from typing import Dict, List, Optional, Any, Union

from langchain_core.tools import BaseTool, tool
from langchain_openai import ChatOpenAI


class RiskAnalystAgent:
    """
    Agent responsible for challenging the main narrative and identifying potential risks:
    - Finding contradictory evidence
    - Identifying black swan signals
    - Assessing geopolitical risk factors
    """
    
    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """
        Initialize the Risk Analyst Agent.
        
        Args:
            llm: The language model to use
        """
        self.llm = llm or ChatOpenAI(
            model="deepseek-chat",
            temperature=0.1,
            base_url="https://api.deepseek.com/v1",  # Replace with actual DeepSeek API URL
        )
    
    @tool
    def find_contradictory_evidence(
        self, 
        main_narrative: Dict[str, Any], 
        all_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Find evidence that contradicts the main narrative.
        
        Args:
            main_narrative: The main narrative to challenge
            all_data: All collected data
            
        Returns:
            Dictionary with contradictory evidence
        """
        try:
            # Extract the narrative description
            narrative_description = ""
            if isinstance(main_narrative, dict):
                if "description" in main_narrative:
                    narrative_description = main_narrative["description"]
                elif "dominant_narratives" in main_narrative and len(main_narrative["dominant_narratives"]) > 0:
                    narrative_description = main_narrative["dominant_narratives"][0]["description"]
                elif "title" in main_narrative:
                    narrative_description = main_narrative["title"]
            elif isinstance(main_narrative, str):
                narrative_description = main_narrative
            
            # Extract text data from all_data
            text_data = []
            
            # Extract from news data
            if "news" in all_data:
                for item in all_data["news"]:
                    if "content" in item:
                        text_data.append(item["content"])
                    elif "description" in item:
                        text_data.append(item["description"])
                    elif "title" in item:
                        text_data.append(item["title"])
            
            # Extract from social media data
            if "social_media" in all_data:
                for item in all_data["social_media"]:
                    if "text" in item:
                        text_data.append(item["text"])
                    elif "content" in item:
                        text_data.append(item["content"])
                    elif "title" in item:
                        text_data.append(item["title"])
            
            # Extract from research data
            if "research" in all_data:
                for item in all_data["research"]:
                    if "summary" in item:
                        text_data.append(item["summary"])
                    elif "abstract" in item:
                        text_data.append(item["abstract"])
                    elif "title" in item:
                        text_data.append(item["title"])
            
            # Combine text data (limit to avoid token limits)
            combined_text = "\n\n".join(text_data[:30])
            
            # Use the LLM to find contradictory evidence
            prompt = f"""
            You are a contrarian risk analyst. Your job is to find evidence that contradicts or challenges the main market narrative.
            
            Main Narrative:
            {narrative_description}
            
            Data to analyze for contradictory evidence:
            {combined_text}
            
            Find and analyze evidence that contradicts or challenges the main narrative. Focus on:
            1. Direct contradictions to key claims
            2. Alternative explanations for the same phenomena
            3. Historical precedents where similar narratives were wrong
            4. Logical fallacies or weaknesses in the narrative
            5. Data points that don't fit the narrative
            
            Respond in JSON format with the following structure:
            {{
                "contradictory_evidence": [
                    {{
                        "evidence": "string",
                        "contradiction_type": "string",
                        "strength": "string",
                        "source": "string",
                        "implications": "string"
                    }}
                ],
                "alternative_narratives": [
                    {{
                        "narrative": "string",
                        "supporting_evidence": [strings],
                        "probability": "string"
                    }}
                ],
                "logical_weaknesses": [
                    {{
                        "weakness": "string",
                        "explanation": "string"
                    }}
                ],
                "overall_assessment": "string"
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            # Parse the response to extract the contradictory evidence
            import json
            try:
                contradictory_evidence = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback to a simple extraction if JSON parsing fails
                contradictory_evidence = {
                    "contradictory_evidence": [
                        {
                            "evidence": "parsing error",
                            "contradiction_type": "parsing error",
                            "strength": "unknown",
                            "source": "parsing error",
                            "implications": "parsing error"
                        }
                    ],
                    "alternative_narratives": [],
                    "logical_weaknesses": [],
                    "overall_assessment": "parsing error",
                    "raw_response": response.content
                }
            
            return contradictory_evidence
        except Exception as e:
            return {"error": f"Error finding contradictory evidence: {str(e)}"}
    
    @tool
    def identify_black_swan_signals(self, all_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify potential black swan signals from the data.
        
        Args:
            all_data: All collected data
            
        Returns:
            Dictionary with identified black swan signals
        """
        try:
            # Extract text data from all_data
            text_data = []
            
            # Extract from news data
            if "news" in all_data:
                for item in all_data["news"]:
                    if "content" in item:
                        text_data.append(item["content"])
                    elif "description" in item:
                        text_data.append(item["description"])
                    elif "title" in item:
                        text_data.append(item["title"])
            
            # Extract from social media data
            if "social_media" in all_data:
                for item in all_data["social_media"]:
                    if "text" in item:
                        text_data.append(item["text"])
                    elif "content" in item:
                        text_data.append(item["content"])
                    elif "title" in item:
                        text_data.append(item["title"])
            
            # Extract from research data
            if "research" in all_data:
                for item in all_data["research"]:
                    if "summary" in item:
                        text_data.append(item["summary"])
                    elif "abstract" in item:
                        text_data.append(item["abstract"])
                    elif "title" in item:
                        text_data.append(item["title"])
            
            # Combine text data (limit to avoid token limits)
            combined_text = "\n\n".join(text_data[:30])
            
            # Use the LLM to identify black swan signals
            prompt = f"""
            You are a risk analyst specializing in identifying potential "black swan" events - rare, high-impact, and hard-to-predict events
            that could significantly disrupt markets.
            
            Data to analyze for black swan signals:
            {combined_text}
            
            Identify potential black swan signals in this data. Focus on:
            1. Low-probability but high-impact events mentioned in marginal sources
            2. Unusual patterns or anomalies that don't fit conventional models
            3. Emerging risks that are being underestimated by the market
            4. Historical parallels to previous black swan events
            5. Potential cascade effects or non-linear consequences
            
            Respond in JSON format with the following structure:
            {{
                "black_swan_signals": [
                    {{
                        "signal": "string",
                        "source": "string",
                        "probability": "string",
                        "potential_impact": "string",
                        "early_warning_indicators": [strings],
                        "historical_parallels": "string"
                    }}
                ],
                "risk_clusters": [
                    {{
                        "cluster_name": "string",
                        "related_signals": [strings],
                        "systemic_implications": "string"
                    }}
                ],
                "blind_spots": [
                    {{
                        "area": "string",
                        "explanation": "string"
                    }}
                ],
                "overall_assessment": "string"
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            # Parse the response to extract the black swan signals
            import json
            try:
                black_swan_signals = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback to a simple extraction if JSON parsing fails
                black_swan_signals = {
                    "black_swan_signals": [
                        {
                            "signal": "parsing error",
                            "source": "parsing error",
                            "probability": "unknown",
                            "potential_impact": "parsing error",
                            "early_warning_indicators": ["parsing error"],
                            "historical_parallels": "parsing error"
                        }
                    ],
                    "risk_clusters": [],
                    "blind_spots": [],
                    "overall_assessment": "parsing error",
                    "raw_response": response.content
                }
            
            return black_swan_signals
        except Exception as e:
            return {"error": f"Error identifying black swan signals: {str(e)}"}
    
    @tool
    def assess_geopolitical_risk_factor(
        self, 
        region_or_country: str, 
        sector: str, 
        all_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess geopolitical risk factors for a specific region/country and sector.
        
        Args:
            region_or_country: The region or country to assess
            sector: The sector to assess
            all_data: All collected data
            
        Returns:
            Dictionary with geopolitical risk assessment
        """
        try:
            # Extract text data from all_data
            text_data = []
            
            # Extract from news data
            if "news" in all_data:
                for item in all_data["news"]:
                    if "content" in item:
                        text_data.append(item["content"])
                    elif "description" in item:
                        text_data.append(item["description"])
                    elif "title" in item:
                        text_data.append(item["title"])
            
            # Extract from social media data
            if "social_media" in all_data:
                for item in all_data["social_media"]:
                    if "text" in item:
                        text_data.append(item["text"])
                    elif "content" in item:
                        text_data.append(item["content"])
                    elif "title" in item:
                        text_data.append(item["title"])
            
            # Extract from research data
            if "research" in all_data:
                for item in all_data["research"]:
                    if "summary" in item:
                        text_data.append(item["summary"])
                    elif "abstract" in item:
                        text_data.append(item["abstract"])
                    elif "title" in item:
                        text_data.append(item["title"])
            
            # Combine text data (limit to avoid token limits)
            combined_text = "\n\n".join(text_data[:30])
            
            # Use the LLM to assess geopolitical risk factors
            prompt = f"""
            You are a geopolitical risk analyst. Your job is to assess the geopolitical risks affecting a specific region/country and sector.
            
            Region/Country: {region_or_country}
            Sector: {sector}
            
            Data to analyze for geopolitical risks:
            {combined_text}
            
            Assess the geopolitical risk factors for this region/country and sector. Focus on:
            1. Political stability and governance risks
            2. Regulatory and policy risks
            3. International relations and trade tensions
            4. Social and demographic factors
            5. Resource security and environmental risks
            
            For each risk factor, provide:
            - A description of the risk
            - Current status and trends
            - Potential triggers for escalation
            - Likely impact on the specified sector
            - Mitigation strategies
            
            Respond in JSON format with the following structure:
            {{
                "overall_risk_score": {{
                    "score": float,  # 0-10 scale
                    "assessment": "string"
                }},
                "risk_factors": [
                    {{
                        "factor": "string",
                        "description": "string",
                        "current_status": "string",
                        "potential_triggers": [strings],
                        "sector_impact": "string",
                        "mitigation_strategies": [strings],
                        "risk_score": float  # 0-10 scale
                    }}
                ],
                "key_monitoring_indicators": [strings],
                "scenario_analysis": [
                    {{
                        "scenario": "string",
                        "probability": "string",
                        "impact": "string"
                    }}
                ],
                "historical_precedents": [strings]
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            # Parse the response to extract the geopolitical risk assessment
            import json
            try:
                geopolitical_risk = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback to a simple extraction if JSON parsing fails
                geopolitical_risk = {
                    "overall_risk_score": {
                        "score": 5.0,
                        "assessment": "parsing error"
                    },
                    "risk_factors": [
                        {
                            "factor": "parsing error",
                            "description": "parsing error",
                            "current_status": "parsing error",
                            "potential_triggers": ["parsing error"],
                            "sector_impact": "parsing error",
                            "mitigation_strategies": ["parsing error"],
                            "risk_score": 5.0
                        }
                    ],
                    "key_monitoring_indicators": ["parsing error"],
                    "scenario_analysis": [],
                    "historical_precedents": [],
                    "raw_response": response.content
                }
            
            return geopolitical_risk
        except Exception as e:
            return {"error": f"Error assessing geopolitical risk factors: {str(e)}"}
    
    def get_tools(self) -> List[BaseTool]:
        """
        Get all the tools provided by this agent.
        
        Returns:
            List of tools
        """
        return [
            self.find_contradictory_evidence,
            self.identify_black_swan_signals,
            self.assess_geopolitical_risk_factor
        ]
"""
Tests for the agent components.
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from aletheia.agents.hunters.narrative_hunter import NarrativeHunterAgent
from aletheia.agents.hunters.quant_analyst import QuantAnalystAgent
from aletheia.agents.analysts.intelligence_analyst import IntelligenceAnalystAgent
from aletheia.agents.analysts.risk_analyst import RiskAnalystAgent


class TestNarrativeHunterAgent(unittest.TestCase):
    """Tests for the NarrativeHunterAgent."""
    
    def setUp(self):
        """Set up the test environment."""
        self.agent = NarrativeHunterAgent()
    
    def test_get_tools(self):
        """Test that the agent returns a list of tools."""
        tools = self.agent.get_tools()
        self.assertIsInstance(tools, list)
        self.assertTrue(len(tools) > 0)


class TestQuantAnalystAgent(unittest.TestCase):
    """Tests for the QuantAnalystAgent."""
    
    def setUp(self):
        """Set up the test environment."""
        self.agent = QuantAnalystAgent()
    
    def test_get_tools(self):
        """Test that the agent returns a list of tools."""
        tools = self.agent.get_tools()
        self.assertIsInstance(tools, list)
        self.assertTrue(len(tools) > 0)


class TestIntelligenceAnalystAgent(unittest.TestCase):
    """Tests for the IntelligenceAnalystAgent."""
    
    def setUp(self):
        """Set up the test environment."""
        # Mock the LLM to avoid API calls during testing
        with patch('langchain_openai.ChatOpenAI') as mock_llm:
            mock_llm_instance = MagicMock()
            mock_llm.return_value = mock_llm_instance
            self.agent = IntelligenceAnalystAgent(llm=mock_llm_instance)
    
    def test_get_tools(self):
        """Test that the agent returns a list of tools."""
        tools = self.agent.get_tools()
        self.assertIsInstance(tools, list)
        self.assertTrue(len(tools) > 0)


class TestRiskAnalystAgent(unittest.TestCase):
    """Tests for the RiskAnalystAgent."""
    
    def setUp(self):
        """Set up the test environment."""
        # Mock the LLM to avoid API calls during testing
        with patch('langchain_openai.ChatOpenAI') as mock_llm:
            mock_llm_instance = MagicMock()
            mock_llm.return_value = mock_llm_instance
            self.agent = RiskAnalystAgent(llm=mock_llm_instance)
    
    def test_get_tools(self):
        """Test that the agent returns a list of tools."""
        tools = self.agent.get_tools()
        self.assertIsInstance(tools, list)
        self.assertTrue(len(tools) > 0)


if __name__ == '__main__':
    unittest.main()
"""
Strategist Agent (CIO) - The main entry point for user interactions.
"""

from typing import Dict, List, Optional, Any

from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from aletheia.agents.orchestrator import create_orchestration_graph


class StrategistAgent:
    """
    The Chief Investment Officer (CIO) agent that serves as the main interface
    for user interactions. It decomposes high-level directives into strategic plans
    and delegates subtasks to the orchestrator.
    """

    def __init__(
        self,
        llm: Optional[ChatOpenAI] = None,
        tools: Optional[List[BaseTool]] = None,
        memory_k: int = 10,
    ):
        """
        Initialize the Strategist Agent.

        Args:
            llm: The language model to use (defaults to DeepSeek)
            tools: List of tools available to the agent
            memory_k: Number of conversation turns to keep in memory
        """
        self.llm = llm or ChatOpenAI(
            model="deepseek-chat",
            temperature=0.1,
            base_url="https://api.deepseek.com/v1",  # Replace with actual DeepSeek API URL
        )
        
        # Create orchestration graph as a tool
        orchestration_graph = create_orchestration_graph(llm=self.llm)
        
        # Default tools include the orchestration graph
        self.tools = tools or []
        self.tools.append(
            orchestration_graph.as_tool(
                name="run_market_analysis",
                description="Run a comprehensive market analysis workflow based on the given directive",
            )
        )
        
        # Set up memory
        self.memory = ConversationBufferWindowMemory(
            k=memory_k,
            memory_key="chat_history",
            return_messages=True,
        )
        
        # Create the agent prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Aletheia's Chief Investment Officer (CIO), an expert in financial markets and investment strategy.
            Your role is to understand high-level directives from users and decompose them into strategic plans.
            You have access to a team of specialized agents that can perform detailed market analysis.
            
            When given a directive:
            1. Acknowledge and clarify the request if needed
            2. Decompose the directive into a structured plan
            3. Delegate the execution to your team using the appropriate tools
            4. Synthesize the results into clear, actionable insights
            
            Always maintain a professional, analytical tone and focus on providing value through deep market intelligence."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent executor
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.llm.bind_tools(self.tools).as_agent(self.prompt),
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
        )
    
    def run(self, directive: str) -> Dict[str, Any]:
        """
        Process a user directive and return the results.
        
        Args:
            directive: The user's high-level directive
            
        Returns:
            The agent's response and any additional metadata
        """
        return self.agent_executor.invoke({"input": directive})
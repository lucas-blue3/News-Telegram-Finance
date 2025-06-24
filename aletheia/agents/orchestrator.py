"""
Orchestrator Agent - Manages the flow of data collection and processing.
"""

from typing import Dict, List, Optional, Any, TypedDict, Annotated, Literal

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode


class OrchestrationState(TypedDict):
    """Type for the state of the orchestration graph."""
    directive: str
    task_list: List[Dict[str, Any]]
    current_task: Optional[Dict[str, Any]]
    collected_data: Dict[str, Any]
    analysis_results: Dict[str, Any]
    risk_assessment: Optional[Dict[str, Any]]
    final_report: Optional[str]
    messages: List[BaseMessage]
    next: Optional[str]


def create_orchestration_graph(llm: Optional[ChatOpenAI] = None):
    """
    Create the orchestration graph that manages the flow of data collection and processing.
    
    Args:
        llm: The language model to use
        
    Returns:
        The orchestration graph
    """
    # Initialize the LLM if not provided
    if llm is None:
        llm = ChatOpenAI(
            model="deepseek-chat",
            temperature=0.1,
            base_url="https://api.deepseek.com/v1",  # Replace with actual DeepSeek API URL
        )
    
    # Define the nodes in the graph
    
    # 1. Task Planning Node
    def plan_tasks(state: OrchestrationState) -> OrchestrationState:
        """Plan the tasks needed to fulfill the directive."""
        directive = state["directive"]
        
        # Use the LLM to decompose the directive into tasks
        planning_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial research operations manager. 
            Your job is to break down high-level market analysis directives into specific, actionable tasks.
            For each task, specify:
            1. task_id: A unique identifier
            2. task_type: One of [data_collection, analysis, risk_assessment, synthesis]
            3. description: What needs to be done
            4. required_data: What data is needed (for analysis tasks)
            5. priority: High, Medium, or Low
            
            Return a JSON-formatted list of tasks that will comprehensively address the directive."""),
            ("human", f"Directive: {directive}\n\nBreak this down into specific tasks:"),
        ])
        
        response = llm.invoke(planning_prompt)
        
        # Parse the response to extract the task list
        # In a real implementation, you would use a more robust parsing method
        import json
        try:
            task_list = json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback to a simple task list if parsing fails
            task_list = [
                {
                    "task_id": "collect_market_data",
                    "task_type": "data_collection",
                    "description": "Collect relevant market data",
                    "priority": "High"
                },
                {
                    "task_id": "analyze_sentiment",
                    "task_type": "analysis",
                    "description": "Analyze market sentiment",
                    "required_data": ["market_news"],
                    "priority": "Medium"
                },
                {
                    "task_id": "assess_risks",
                    "task_type": "risk_assessment",
                    "description": "Identify potential risks",
                    "required_data": ["market_data", "sentiment_analysis"],
                    "priority": "Medium"
                },
                {
                    "task_id": "generate_report",
                    "task_type": "synthesis",
                    "description": "Generate final report",
                    "required_data": ["market_data", "sentiment_analysis", "risk_assessment"],
                    "priority": "High"
                }
            ]
        
        # Update the state with the task list
        state["task_list"] = task_list
        state["collected_data"] = {}
        state["analysis_results"] = {}
        state["messages"].append(HumanMessage(content=f"Planned {len(task_list)} tasks for directive: {directive}"))
        state["next"] = "select_next_task"
        
        return state
    
    # 2. Task Selection Node
    def select_next_task(state: OrchestrationState) -> OrchestrationState:
        """Select the next task to execute based on dependencies and priorities."""
        task_list = state["task_list"]
        collected_data = state["collected_data"]
        analysis_results = state["analysis_results"]
        
        # Filter out completed tasks
        incomplete_tasks = [
            task for task in task_list 
            if (task["task_type"] == "data_collection" and task["task_id"] not in collected_data) or
               (task["task_type"] == "analysis" and task["task_id"] not in analysis_results) or
               (task["task_type"] == "risk_assessment" and state["risk_assessment"] is None) or
               (task["task_type"] == "synthesis" and state["final_report"] is None)
        ]
        
        if not incomplete_tasks:
            # All tasks are complete
            state["next"] = END
            return state
        
        # Sort tasks by priority and dependencies
        def can_execute(task):
            if task["task_type"] in ["analysis", "risk_assessment", "synthesis"]:
                if "required_data" in task:
                    return all(data_id in collected_data for data_id in task["required_data"])
            return True
        
        executable_tasks = [task for task in incomplete_tasks if can_execute(task)]
        
        if not executable_tasks:
            # No tasks can be executed yet, need more data
            # In a real implementation, you would handle this case better
            data_collection_tasks = [task for task in incomplete_tasks if task["task_type"] == "data_collection"]
            if data_collection_tasks:
                state["current_task"] = data_collection_tasks[0]
                state["next"] = "execute_task"
                return state
            else:
                # This is an error state - we have tasks but can't execute any of them
                state["next"] = END
                return state
        
        # Sort by priority (High > Medium > Low)
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        executable_tasks.sort(key=lambda t: priority_order.get(t["priority"], 3))
        
        # Select the highest priority task
        state["current_task"] = executable_tasks[0]
        state["next"] = "execute_task"
        
        return state
    
    # 3. Task Execution Router
    def route_task(state: OrchestrationState) -> Literal["collect_data", "analyze_data", "assess_risks", "synthesize_report"]:
        """Route the task to the appropriate execution node based on its type."""
        task = state["current_task"]
        task_type = task["task_type"]
        
        if task_type == "data_collection":
            return "collect_data"
        elif task_type == "analysis":
            return "analyze_data"
        elif task_type == "risk_assessment":
            return "assess_risks"
        elif task_type == "synthesis":
            return "synthesize_report"
        else:
            # Default fallback
            return "collect_data"
    
    # 4. Data Collection Node (placeholder - would connect to actual data collection agents)
    def collect_data(state: OrchestrationState) -> OrchestrationState:
        """Collect data according to the current task."""
        task = state["current_task"]
        task_id = task["task_id"]
        
        # In a real implementation, this would call the appropriate data collection agent
        # For now, we'll just simulate collecting some data
        collected_data = {
            "timestamp": "2025-06-24T12:00:00Z",
            "source": "simulated",
            "data": f"Sample data for {task_id}"
        }
        
        # Store the collected data
        state["collected_data"][task_id] = collected_data
        state["messages"].append(HumanMessage(content=f"Collected data for task: {task_id}"))
        state["next"] = "select_next_task"
        
        return state
    
    # 5. Data Analysis Node (placeholder - would connect to actual analysis agents)
    def analyze_data(state: OrchestrationState) -> OrchestrationState:
        """Analyze data according to the current task."""
        task = state["current_task"]
        task_id = task["task_id"]
        
        # In a real implementation, this would call the appropriate analysis agent
        # For now, we'll just simulate analyzing some data
        analysis_result = {
            "timestamp": "2025-06-24T12:05:00Z",
            "source": "simulated",
            "result": f"Sample analysis for {task_id}"
        }
        
        # Store the analysis result
        state["analysis_results"][task_id] = analysis_result
        state["messages"].append(HumanMessage(content=f"Analyzed data for task: {task_id}"))
        state["next"] = "select_next_task"
        
        return state
    
    # 6. Risk Assessment Node (placeholder - would connect to the risk analyst agent)
    def assess_risks(state: OrchestrationState) -> OrchestrationState:
        """Assess risks based on the collected data and analysis results."""
        task = state["current_task"]
        
        # In a real implementation, this would call the risk analyst agent
        # For now, we'll just simulate a risk assessment
        risk_assessment = {
            "timestamp": "2025-06-24T12:10:00Z",
            "source": "simulated",
            "risks": [
                {"risk_type": "market_volatility", "probability": "medium", "impact": "high"},
                {"risk_type": "regulatory_change", "probability": "low", "impact": "high"}
            ]
        }
        
        # Store the risk assessment
        state["risk_assessment"] = risk_assessment
        state["messages"].append(HumanMessage(content="Completed risk assessment"))
        state["next"] = "select_next_task"
        
        return state
    
    # 7. Report Synthesis Node
    def synthesize_report(state: OrchestrationState) -> OrchestrationState:
        """Synthesize the final report based on all collected data and analyses."""
        directive = state["directive"]
        collected_data = state["collected_data"]
        analysis_results = state["analysis_results"]
        risk_assessment = state["risk_assessment"]
        
        # Use the LLM to generate the final report
        synthesis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial analyst responsible for synthesizing market intelligence into clear, actionable reports.
            Based on the collected data, analysis results, and risk assessment, create a comprehensive report that addresses the original directive.
            
            Your report should include:
            1. Executive Summary
            2. Key Findings
            3. Market Analysis
            4. Risk Assessment
            5. Actionable Recommendations
            
            Use a professional, analytical tone and focus on providing valuable insights."""),
            ("human", f"""
            Directive: {directive}
            
            Collected Data: {collected_data}
            
            Analysis Results: {analysis_results}
            
            Risk Assessment: {risk_assessment}
            
            Please synthesize this information into a comprehensive report:
            """),
        ])
        
        response = llm.invoke(synthesis_prompt)
        
        # Store the final report
        state["final_report"] = response.content
        state["messages"].append(HumanMessage(content="Generated final report"))
        state["next"] = END
        
        return state
    
    # Create the graph
    workflow = StateGraph(OrchestrationState)
    
    # Add nodes
    workflow.add_node("plan_tasks", plan_tasks)
    workflow.add_node("select_next_task", select_next_task)
    workflow.add_node("collect_data", collect_data)
    workflow.add_node("analyze_data", analyze_data)
    workflow.add_node("assess_risks", assess_risks)
    workflow.add_node("synthesize_report", synthesize_report)
    
    # Add edges
    workflow.add_edge("plan_tasks", "select_next_task")
    workflow.add_conditional_edges(
        "select_next_task",
        lambda state: state["next"],
        {
            "execute_task": "route_task",
            END: END
        }
    )
    workflow.add_conditional_edges(
        "route_task",
        route_task,
        {
            "collect_data": "collect_data",
            "analyze_data": "analyze_data",
            "assess_risks": "assess_risks",
            "synthesize_report": "synthesize_report"
        }
    )
    workflow.add_edge("collect_data", "select_next_task")
    workflow.add_edge("analyze_data", "select_next_task")
    workflow.add_edge("assess_risks", "select_next_task")
    workflow.add_edge("synthesize_report", "select_next_task")
    
    # Set the entry point
    workflow.set_entry_point("plan_tasks")
    
    # Compile the graph
    return workflow.compile()


def run_orchestration(directive: str, llm: Optional[ChatOpenAI] = None) -> Dict[str, Any]:
    """
    Run the orchestration graph with a given directive.
    
    Args:
        directive: The high-level directive to process
        llm: The language model to use
        
    Returns:
        The final state of the orchestration graph
    """
    graph = create_orchestration_graph(llm)
    
    # Initialize the state
    initial_state: OrchestrationState = {
        "directive": directive,
        "task_list": [],
        "current_task": None,
        "collected_data": {},
        "analysis_results": {},
        "risk_assessment": None,
        "final_report": None,
        "messages": [],
        "next": None
    }
    
    # Run the graph
    result = graph.invoke(initial_state)
    
    return result
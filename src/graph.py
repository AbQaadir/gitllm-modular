import re
from .state import State
from langgraph.graph import END, StateGraph, START
from .prompt_template import planner_prompt_template
from .llm import planner_llm, analyzer_llm
from .helper import create_tuples_from_plans, format_plans
from .tools import get_file_content
from .prompt import solver_prompt
from .repo_config import get_repo_url



def get_plan(state: State):
    task = state["task"]
    planner = planner_prompt_template | planner_llm
    result = planner.invoke({"task": task})
    matches = create_tuples_from_plans(result.plans)
    return {"steps": matches, "plan_string": format_plans(result.plans)}


def _get_current_task(state: State):
    if "results" not in state or state["results"] is None:
        return 1
    if len(state["results"]) == len(state["steps"]):
        return None
    else:
        return len(state["results"]) + 1



def tool_execution(state: State):
    """Worker node that executes the tools of a given plan."""
    # Retrieve the current step's details
    _step = _get_current_task(state)
    _, step_name, tool, tool_input = state["steps"][_step - 1]
    
    # Initialize or retrieve previous results
    _results = state.get("results", {})
    
    # Replace placeholders in tool_input with actual values from _results
    for k, v in _results.items():
        tool_input = tool_input.replace(k, v) if tool_input else tool_input
    
    # Execute the appropriate tool based on the tool name
    if tool == "ContentExtractorTool":
        # apply regex to get the file path (e.g., file_path="src/Main.java")
        file_path = re.search(r'file_path="(.+?)"', tool_input).group(1)
        
        result = get_file_content.invoke({
            "github_repo_url": get_repo_url(),
            "file_path": file_path})
    elif tool == "LLM":
        result = analyzer_llm.invoke(tool_input)
    else:
        raise ValueError(f"Unsupported tool: {tool}")
    
    # Update results with the current step's result
    _results[step_name] = str(result)
    return {"results": _results}


def solve(state: State):
    plan = ""
    
    # Loop through each step to build the plan string
    for _plan, step_name, tool, tool_input in state["steps"]:
        _results = state.get("results", {})
        
        # Replace any placeholders in tool_input and step_name
        for k, v in _results.items():
            tool_input = tool_input.replace(k, v)
            step_name = step_name.replace(k, v)
        
        # Append each step plan to the overall plan string with better formatting
        plan += f"Plan: {_plan}\n{step_name} = {tool}[{tool_input}]\n\n"
    
    # Format the prompt with the completed plan and task
    prompt = solver_prompt.format(plan=plan.strip(), task=state["task"])
    
    # Invoke the LLM and get the result
    result = analyzer_llm.invoke(prompt)
    return {"result": result.content}


def _route(state: State):
    _step = _get_current_task(state)
    if _step is None:
        # We have executed all tasks
        return "solve"
    else:
        # We are still executing tasks, loop back to the "tool" node
        return "tool"
    

graph = StateGraph(State)
graph.add_node("plan", get_plan)
graph.add_node("tool", tool_execution)
graph.add_node("solve", solve)
graph.add_edge("plan", "tool")
graph.add_edge("solve", END)
graph.add_conditional_edges("tool", _route)
graph.add_edge(START, "plan")

app = graph.compile()
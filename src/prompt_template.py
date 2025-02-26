import re
from .prompt import planner_prompt
from langchain_core.prompts import ChatPromptTemplate

planner_prompt_template = ChatPromptTemplate.from_messages([("user", planner_prompt)])
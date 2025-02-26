from .output_structure import PlanList
from langchain_openai import ChatOpenAI
from .config import get_openai_api_key


planner_llm = ChatOpenAI(
    model ="o3-mini",
    api_key = get_openai_api_key(),
).with_structured_output(PlanList)



analyzer_llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=get_openai_api_key(),
)


if __name__ == "__main__":
    print(planner_llm.invoke("Generate a list of plans for the task"))
    print(analyzer_llm.invoke("Analyze the text and extract the entities"))
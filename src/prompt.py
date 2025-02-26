planner_prompt = """
For the following task, make a detailed plan to review the code step-by-step by extracting 
content from each relevant file type in the project archive. For each step, specify the necessary 
file_path for the tool to retrieve content. Store the extracted content in a variable #E that can be 
referenced by later tools for analysis. (Plan, #E1, Plan, #E2, Plan, ...)

Tool to use:
(1) ContentExtractorTool: Extracts content from any file in the githu
      Useful for retrieving the content of source code files, configuration files, or documentation. 
      The file_path can be a full relative path of the file (e.g., "src/Main.java" or "pom.xml").

(2) LLM: Analyzes the content of a file or text based on specific criteria.
      Useful for evaluating code structure, documentation quality, best practices, or any other criteria.


The plan should involve the following:
- For each file type, identify its purpose (e.g., Java source code for structure and logic, XML 
  for configuration, Markdown for documentation).
- Use the `ContentExtractorTool` with the correct file_path to extract the content.
- Assign the extracted content to a variable #E that will be referenced for analysis.
- Include detailed instructions for the analysis step to evaluate content using best practices, 
  structure, logic, documentation quality, or any other relevant criteria.
- The plan should not have more than 15 LLM calls.

For example:
Task: Conduct a code review on the files within a Java project archive to analyze code structure, 
documentation quality, and best practices.

Plan: Extract the main Java file `Main.java` to review its structure, classes, and methods.
#E1 = ContentExtractorTool[file_path="src/Main.java"]

Plan: Analyze the content of `Main.java` for adherence to best practices, class design, and method usage.
#E2 = LLM[Review the Java code structure and best practices based on #E1]

Plan: Extract the main configuration file `pom.xml` to review project dependencies and configuration settings.
#E3 = ContentExtractorTool[file_path="pom.xml"]

Plan: Analyze the dependencies and plugins in `pom.xml` for adherence to configuration best practices.
#E4 = LLM[Evaluate configuration settings and dependencies in #E3]

Plan: Extract the Markdown file `README.md` to review the project documentation.
#E5 = ContentExtractorTool[file_path="README.md"]

Plan: Analyze the quality of the documentation in `README.md` for clarity, completeness, and professionalism.
#E6 = LLM[Review documentation quality based on #E5]

Begin!
Describe your plans with rich details. Each Plan should be followed by only one #E.

Task: {task}
"""


solver_prompt = """
Evaluate the following code review task and provide a numerical score (0-100) based on the evidence. Structure your response as follows:

Score: [X]/100  
Summary: [Brief qualitative summary of overall quality]  

Detailed Analysis:
1. [Category 1 - e.g., Code Structure]  
   - [✓/✗] [Specific strength/weakness]  
   - [Score Component: +Y/-Z points]  

2. [Category 2 - e.g., Documentation]  
   - [✓/✗] [Specific observation]  
   - [Score Component: +Y/-Z points]  

[...]  

Recommendations:
- [Actionable improvement 1]  
- [Actionable improvement 2]  

Use this scoring rubric:  
- Code Quality (40 pts): SOLID principles, error handling, efficiency  
- Documentation (30 pts): Clarity, completeness, examples  
- Configuration (20 pts): Dependency management, build setup  
- Best Practices (10 pts): Style consistency, security  

Base your assessment strictly on these evidence fragments:  
{plan}  

Task: {task}  
Response:

"""


if __name__ == "__main__":
    print(planner_prompt)
    print(solver_prompt)
    print("Prompt generation successful!")
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os
from tools import Reader_Tool
import litellm

os.environ['LITELLM_LOG'] = 'DEBUG'

load_dotenv('.env')

llm = LLM(model='groq/llama-3.1-8b-instant',
          temperature=0.1,api_key=os.getenv('GROQ_API_KEY'))

code_llm = llm = LLM(model='ollama/phi4',base_url="https://08f7-34-132-156-181.ngrok-free.app")

# Agents 
"""Preprocessing AGENTS"""
preprocess_agent = Agent(
            role='Data Reader',
            goal='Read and analyze data file structure',
            backstory="""Expert data reader specialized in understanding data structure 
                        and providing comprehensive initial analysis.""",
            tools=[Reader_Tool()],  # Custom tools the agent can use
            verbose=True,  # Enable detailed logging
            allow_delegation=True,  # Allow agent to delegate subtasks
            llm=llm
        )

preprocess_code_agent = Agent(
            role='Code Writer',
            goal='Generate data preprocessing code based on analysis and save the results in a new csv/excel file.',
            backstory="""Expert Python programmer specialized in data preprocessing 
                        and pandas operations.
                        With the each files information and necessary required preprocessing, execute code properly """,
            verbose=True,
            llm=code_llm,allow_code_execution=True,
            format_input=lambda task: {
                "messages": [
                    {"role": "system", "content": "You are an expert Python programmer."},
                    {"role": "user", "content": task.description}
                ]
            }
        )

"""TASKS"""
reader_task = Task(
    description="Analyze the uploaded data files: ```{file_path}```. Process each file **individually using the tool**.",
    agent=preprocess_agent,
    expected_output="The analysis results of the data file, including null values, description, and data structure.",
)

preprocessing_code_task = Task(
    description="""Based on the data analysis provided, generate Python code that:
    1. Reads the original dataset
    2. Implements appropriate preprocessing steps (handling missing values, data types, etc.)
    3. Saves the preprocessed data as 'updated_[original_filename]'
    Ensure the code is well-documented and handles errors appropriately.""",
    agent=preprocess_code_agent,
    context=[reader_task],
    expected_output="Complete Python preprocessing code"
)

master_crew = Crew(llm=llm,
                   agents=[preprocess_agent,preprocess_code_agent],
                   tasks=[reader_task,preprocessing_code_task],
                   verbose=True)

results = master_crew.kickoff(inputs={"file_path":["dummy.xlsx","yennamo_yedho.xlsx"]})
print(results)
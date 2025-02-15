from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os
from tools import Reader_Tool, Code_Runner, code_executor
import litellm

# import logging
# logging.basicConfig(level=logging.DEBUG)

os.environ['LITELLM_LOG'] = 'DEBUG'

load_dotenv('.env',override=True)

# llm = LLM(model='groq/llama-3.1-8b-instant',
#           temperature=0.0,api_key=os.getenv('GROQ_API_KEY'))
# print(os.getenv('AZURE_API_BASE'),os.getenv('AZURE_API_VERSION'),os.getenv('AZURE_API_KEY'))
# llm = LLM(model='azure_ai/Phi-4',api_key=os.getenv('AZURE_API_KEY'),base_url=os.getenv('AZURE_API_BASE'),api_version=os.getenv('AZURE_API_VERSION'))

llm = LLM(model='gemini/gemini-2.0-flash',api_key=os.getenv('GEMINI_API_KEY'))
code_llm = llm 
# = LLM(model='ollama/phi4',base_url="https://08f7-34-132-156-181.ngrok-free.app")


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
            role='Code Writer & Executor',
            goal="Generate python code and execute the generated code using the tool.",
            backstory="""Expert Python programmer specialized in Machine Learning, data preprocessing, 
                        and pandas operations. 
                        Guideline for different datatypes:
                        Datatype: Numeric
                            - To handle null values: Take mean
                            - To handle outlier: Perform IQR
                            - Perform binning if numeric data is continuous

                        Datatype: Categorical 
                            To handle null values: Take mode[0]
                        """,
            verbose=True,
            llm=code_llm
        )

"""Plot suggestor - Insight Agent"""
plot_suggestor = Agent(
    role='Read the updated dataset - analyse the data and then provide plot suggestions,possible relationship between datas or columns.',
    goal="To provide meaningful insights about the dataset, relationship between different columns, what type of plots can be generated to understand the underlying information of the data.",
    backstory="""As the greatest Data Analyst cum Scientist in the history of mankind, you are tasked with a simple problem:
                - Read the preprocessed dataset.
                - Analyze the dataset and find patterns across the columns.
                - Understand the relationships between the columns.
                - Generate insights and suggest what types of plots (e.g., scatter plots, histograms, box plots etc) can best visualize the data.
                - You must also provide the exact column name that should be used in the axis for the plot.
                """,
    verbose=True,
    llm=code_llm,
    tools=[Reader_Tool()]
)

"""Plot generator/ Dashboard generator Agent"""
plot_generator = Agent(
    role='Plot Generator / Dashboard Creator',
    goal="Generate Python code that creates visualizations (charts/dashboards) based on insights and human-specified suggestions, and save all charts locally.",
    backstory="""You are an expert Python developer with a deep knowledge of data visualization using matplotlib and Plotly.
                Your job is to:
                - Read the insights provided by the Plot Suggestor Agent.
                - Generate Python code to create the required visualizations (scatter plots, histograms, box plots, or interactive dashboards).
                - Ensure the code saves all the generated charts or dashboards locally (as image files for matplotlib or HTML files for Plotly).
                - Include error handling and clear inline comments for clarity.
                """,
    verbose=True,
    llm=code_llm,
    tools=[Reader_Tool()]
)

"""TASKS"""
reader_task = Task(
    name="Data Reader",
    description="Analyze the uploaded data files: ```{file_path}```. Process each file **individually using the tool**.",
    agent=preprocess_agent,
    expected_output="The analysis results of the data file, including null values, description, and data structure.",
)

preprocessing_code_task = Task(
    name="Preprocessing code writter",
    description="""Based on the data analysis provided, generate Python code that:
    1. Reads the original dataset path ```{file_path}```.
    2. Implements appropriate preprocessing steps (handling missing values, data types, etc.)
    3. Saves the preprocessed data as 'updated_[original_filename]'
    
    **Guidelines:**
        - If a column is only of numerical values then fill the null values using the mean of different groups using group by function.
        - With the each files information and necessary required preprocessing gsenerate the code.
        - Make sure you give the actual file path of the data to generate the clcode.
        - Ensure the code is well-documented and handles errors appropriately.
        - your code will be executed directly so don't provide any further comments without commenting them.""",
    agent=preprocess_code_agent,
    context=[reader_task],
    callback=code_executor,
    expected_output="A well structured and a fully working Python preprocessing code"
)

plot_suggestor_task = Task(
     name="Plot Suggestion Task",
    description="Read the updated dataset ```updated_{file_path}```, analyze the data to identify relationships between columns, and suggest appropriate plot types (e.g., scatter, histogram, box) for visualization.",
    agent=plot_suggestor,
    # human_input=True,
    expected_output="A detailed insights of the dataset. -[S.NO] [Plotname]: [columns to be used with proper axis(x,y,z... based on the plot)]-[Why and what might be understand from this plot etc]"
)

plot_generator_task = Task(
    name="Plot Generator Task",
    description="""Using the preprocessed dataset ```updated_{file_path}``` and insights from the Plot Suggestor Task (which may include human input on required charts), generate Python code that:
    1. Creates the suggested visualizations using libraries such as matplotlib or Plotly.
    2. Saves all generated charts locally (e.g., image files for matplotlib plots, HTML files for Plotly dashboards).
    3. Includes appropriate error handling and documentation within the code.
    
    **Note:** If specific human input is provided for chart types or design, integrate those instructions into the visualization code.
    """,
    agent=plot_generator,
    context=[plot_suggestor_task],
    callback=code_executor,
    expected_output="Well-documented Python code that generates and saves the required visualizations based on the provided insights."
)

master_crew = Crew(
    llm=llm,
    agents=[preprocess_agent, preprocess_code_agent,plot_suggestor,plot_generator],
    tasks=[reader_task, preprocessing_code_task,plot_suggestor_task,plot_generator_task],
    verbose=True,
    output_log_file="logs.txt"
)

results = master_crew.kickoff(inputs={"file_path": ["titanic.csv"]})
print(results)

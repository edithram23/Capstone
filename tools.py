from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import pandas as pd
import io
import subprocess
import time


class Reader_Tool(BaseTool):
    def Input_param():
        class MyToolInput(BaseModel):
            """Input scheme - file_path"""
            file_path: str = Field(...,description='single file_path of the excel/csv file')
        return MyToolInput

    name:str = "DatasetReader"
    description:str = "Reads an excel/csv file [can process one file at one time, if multiple files then call individually] from the given file_path and returns information about the dataset -> null-values, description, first 5-10 rows, info, column types etc. "
    args_schema: Type[BaseModel] = Input_param()
    def _run(self, file_path:str) -> str :
        def get_describe(file_path:str,dataframe:pd.DataFrame):
            return f"Description of the Dataframe - {file_path} :- ```{dataframe.describe()}```\n"
        
        def get_info(file_path: str, dataframe: pd.DataFrame):
            buffer = io.StringIO()
            dataframe.info(buf=buffer)
            info_str = buffer.getvalue()
            buffer.close()
            return f"Information of the Dataframe - {file_path} :- ```{info_str}```\n"

        def get_null(file_path: str, dataframe: pd.DataFrame):
            total_missing = dataframe.isnull().sum().sum()
            missing_by_column = dataframe.isnull().sum().to_dict()
            missing_percentage = (dataframe.isnull().sum() / len(dataframe) * 100).to_dict()

            return (
                f"Null values of the Dataframe - ```{file_path} :-\n"
                f"Total Missing: {total_missing}\n"
                f"Missing by Column: {missing_by_column}\n"
                f"Missing Percentage: {missing_percentage}```\n"
            )

        def get_head(file_path:str,dataframe:pd.DataFrame):
            return f"Head of the Dataframe - {file_path} :- ```{dataframe.head(5)}```\n" 
        
        # file_path = file_path[0]
        print(file_path)
        try:
                
            try:    
                df = pd.read_excel(file_path)
                return f"""After reading the file {file_path}:\n \
                    {get_describe(file_path=file_path,dataframe=df)} \
                    {get_info(file_path=file_path,dataframe=df)} \
                    {get_null(file_path=file_path,dataframe=df)}\
                    {get_head(file_path=file_path,dataframe=df)}
                    """
            except Exception as e:
                df = pd.read_csv(file_path)
                return f"""After reading the file {file_path}:\n \
                    {get_describe(file_path=file_path,dataframe=df)} \
                    {get_info(file_path=file_path,dataframe=df)} \
                    {get_null(file_path=file_path,dataframe=df)}\
                    {get_head(file_path=file_path,dataframe=df)}
                    """
        except Exception as e:
            return f"""Error: Could not read the dataframe {str(e)}"""
    
    
class Code_Runner(BaseTool):
    def Input_param():
        class MyToolInput(BaseModel):
            """Input scheme - code"""
            code: str = Field(...,description='Provide the code that needs to be executed as a string')
            # code_description: str = Field(...,description='Description of the task for which code that needs to be executed [max 2 words : format separated by "_" underscores ]')
        return MyToolInput

    name:str = "Code_Executor"
    description:str = "Accepts the code as a string in the key 'code', executes the code and provides the output. If encountered an error - returns error."
    args_schema: Type[BaseModel] = Input_param()
    def _run(self, code:str) -> str :
        try:
            file_name = 'preprocessing.py'
            print(file_name)
            print(code)
            with open(file_name, "w") as script_file:
                    script_file.write(str(code))
            result = subprocess.run(
                ["python", file_name],
                capture_output=True,
                text=True,
                check=True  # Raises an exception if the script returns a non-zero exit code
            )
            time.sleep(10)
            return f"Execution Result {result.stdout}"
        except subprocess.CalledProcessError as e:
            return f"Error while executing the script {e.stderr}"
        except Exception as e:
            return f"Error : {str(e)}"
        
def code_executor(code):
        # print("called")
        try:
            code = str(code)
            file_name = 'preprocessing.py'
            code_file = code.split('```python')[1].split('```')[0]
            # print(code_file)
            with open(file_name, "wb") as script_file:
                    script_file.write(str(code_file).encode('utf-8'))
            result = subprocess.run(
                ["python", file_name],
                capture_output=True,
                text=True,
                check=True  # Raises an exception if the script returns a non-zero exit code
            )
            time.sleep(10)
            return f"Execution Result {result.stdout}"
        except subprocess.CalledProcessError as e:
                print("Subprocess error:", e.stderr)
                return f"Error while executing the script: {e.stderr}"
        except Exception as e:
            print(e)
            return f"Error : {str(e)}"